# You Can Be Anything

An offline, replayable Ren'Py story experience that turns a player's profile, mood, chosen genre, opening line, and five decisions into a personalized narrative.

The submission build uses English for profile prompts, procedural fallback text, AI-generated choices, standard Ren'Py menus, finale controls, errors, and illustration status messages.

## What it does

The player enters a protagonist name, MBTI, preferred style, current mood, and an original opening sentence. They then choose one of four genres:

- Mystery
- Cyberpunk
- Science fiction
- Romance fantasy

The story progresses through origin, growth, crisis, climax, and resolution. Every act offers three contextual choices. The selected scenes are preserved and assembled into a finale with an act-by-act soundtrack plan. At the player's explicit request, the finale can also generate and display one protagonist illustration.

## Current implementation

The game now supports a cost-aware hybrid narrative mode. When the local story proxy is running, GPT-5.6 Luna generates three personalized choices for each act through Sogang University's OpenAI-compatible API Gateway. If the proxy, network, or model is unavailable, the existing procedural engine takes over automatically, so the core game remains playable offline.

After the fifth act, the player may approve a single `gpt-image-1-mini` illustration at `low` quality. The UI states the maximum cost before the request. Identical endings reuse a SHA-256-addressed local PNG cache for zero additional credits, active duplicate requests are rejected, and failed responses are never cached or automatically retried.

Every completed playthrough is archived immediately, even when the player skips image generation or the API is offline. The archive contains the full story and a structured session record. When an illustration completes, its PNG is copied into the same playthrough directory and the manifest is updated atomically.

The repository contains soundtrack metadata and checks whether each referenced file is available. Audio files are not currently bundled, so missing tracks are shown as unassigned without stopping the story.

## Built with

- Ren'Py 8.4.1
- Python embedded in Ren'Py
- Ren'Py Screen Language
- GPT-5.6 through Codex for development assistance
- GPT-5.6 Luna through the Sogang University API Gateway for runtime choices
- GPT Image 1 Mini for an optional finale illustration

## How Codex and GPT-5.6 were used

GPT-5.6 through Codex was used as a hands-on development collaborator during the submission hardening process. Codex inspected the full Ren'Py codebase, traced the profile-to-finale state flow, compared the implementation with its specification, and identified a concrete audio runtime risk: the game played music through a custom `bgm` channel that had never been registered.

Codex then modified `game/script.rpy` to register the dedicated BGM channel, preserving the existing in-game BGM toggle while preventing an unknown-channel failure when audio is added. It also replaced the machine-specific quick-start document with this portable README, documented an exact judge testing path, and prepared a truthful demo narration and submission checklist.

Codex also implemented the later hybrid runtime integration: a local key-holding proxy calls GPT-5.6 Luna through Sogang University's API Gateway, validates three generated choices, and lets Ren'Py fall back to the procedural generator whenever that service is unavailable. It then implemented the optional finale illustration pipeline, including structured ending context, explicit cost confirmation, background generation, strict one-image guards, SHA-256 caching, duplicate suppression, failure handling, saved PNG display, mock tests, and a live one-image verification. This keeps the credential outside the game and repository while making GPT-5.6 part of the playable experience.

## Requirements

- Windows, macOS, or Linux supported by Ren'Py 8.4.1
- Ren'Py SDK 8.4.1 or a compatible newer 8.x release
- No credential is required for the offline fallback
- An authorized Sogang Gateway key and internet connection are required for live choices and illustration generation

## Setup and run

### Install the Ren'Py SDK on Windows

Ren'Py is not installed through `pip`, and `renpy.exe` is not part of this repository. It is included in the extracted Ren'Py SDK. This project was developed for Ren'Py 8.4.1, so use that version for the first validation even if a newer release exists.

1. Open the official [Ren'Py 8.4.1 release page](https://www.renpy.org/release/8.4.1).
2. Under the main downloads, select **Download SDK 7z.exe** for Windows. The ZIP SDK also works, but the self-extracting `7z.exe` is simpler.
3. After the download completes, open the downloaded file. Its name will resemble:

   ```text
   renpy-8.4.1-sdk.7z.exe
   ```

4. When asked where to extract it, use a short writable path such as:

   ```text
   C:\Tools\RenPy
   ```

   Avoid extracting it into `Program Files`, the game repository, or a deeply nested OneDrive folder.
5. After extraction, open the created SDK directory. Depending on the archive name, the path will resemble one of these:

   ```text
   C:\Tools\RenPy\renpy-8.4.1-sdk\renpy.exe
   C:\Tools\RenPy\renpy-8.4.1\renpy.exe
   ```

6. Double-click `renpy.exe`. This opens the Ren'Py Launcher; it does not directly open this game yet.
7. Optional: right-click `renpy.exe` and select **Pin to Start** or **Send to → Desktop (create shortcut)**.

If Windows hides file extensions, the executable may appear simply as `renpy` with an application icon. In File Explorer, enable **View → Show → File name extensions** to see `.exe`.

To locate an already extracted copy, search File Explorer for:

```text
renpy.exe
```

or run this in PowerShell after replacing the search root with the directory where you usually install tools:

```powershell
Get-ChildItem C:\Tools -Filter renpy.exe -File -Recurse -ErrorAction SilentlyContinue
```

Do not download the Ren'Py source-code archive for this task. The source archive does not provide the ready-to-run Windows Launcher expected by this guide.

### Windows quick start: offline and no API cost

Use this path first. It makes no external model or image request.

1. Complete the SDK installation above.
2. Run `renpy.exe` from the extracted SDK folder, for example `C:\Tools\RenPy\renpy-8.4.1-sdk\renpy.exe`.
3. In the Ren'Py Launcher, open **Preferences**.
4. Set **Projects Directory** to the directory that contains this repository, not to the `game` subdirectory. For the current workspace that parent directory is:

   ```text
   C:\Users\datan\Downloads\renpy-choose-game-main
   ```

5. Return to the launcher. Select **You Can Be Anything** or the project folder name shown by Ren'Py.
6. Select **Lint** first. Fix any error reported by the Ren'Py Launcher before recording or building.
7. Select **Launch Project**.
8. Do not start `story_api_server.py`. The game will show `Choices: offline generator` and complete the full cycle without API cost.
9. Finish all five acts and confirm that the finale reports a playthrough archive path.

The directory selected in Ren'Py must have this shape:

```text
renpy-choose-game-main/
  renpy-choose-game-main/    <- project selected by the launcher
    game/
      script.rpy
      screens.rpy
      options.rpy
```

Do not select `game/` itself as the projects directory.

### Optional live AI mode

Only use this path when you intentionally want model requests. In a separate PowerShell window, change to the repository root and start the local proxy with an external credential file:

   ```powershell
   cd C:\Users\datan\Downloads\renpy-choose-game-main\renpy-choose-game-main
   python scripts/story_api_server.py --key-file "C:\path\outside\the\repository\credential.txt"
   ```

Alternatively set `SOGANG_API_KEY` and omit `--key-file`. Never copy a key into this repository. Keep the proxy terminal open, then launch the game. The overlay reports whether choices came from GPT-5.6 Luna or the offline generator.

Finale illustration generation is never automatic. It requires a separate confirmation that states the maximum expected credit cost. For an initial gameplay check, select **Cancel** in that confirmation.

Do not point Ren'Py at a path copied from another computer. The repository is portable and can be placed anywhere inside your own Ren'Py projects directory.

### If VS Code shows `9+` errors on `script.rpy`

`script.rpy` is not a normal Python file. It combines Ren'Py Script Language, Screen Language, and embedded Python. A Python language server therefore marks valid statements such as `screen`, `frame`, `textbutton`, and `action` as Python syntax errors.

- The `9+` badge is the editor's diagnostic count, not a Ren'Py runtime result.
- The `U` badge means the file is untracked by Git.
- Install a Ren'Py language extension and change the file language mode from **Python** to **Ren'Py**.
- If no Ren'Py extension is available, use **Plain Text** to avoid false Python diagnostics.
- Treat Ren'Py Launcher's **Lint** and an actual `traceback.txt` as the authoritative error sources.

### Where completed cycles are saved on Windows

Open `%APPDATA%\RenPy\Choose-1758378693\story_archive` in File Explorer. Each completed cycle has its own directory containing `story.txt` and `session.json`; `illustration.png` is added after successful image generation.

## Judge testing path

The core flow takes approximately two minutes:

1. Launch the game and select **Start**.
2. Enter the following sample profile:
   - Name: `Mina`
   - MBTI: `INFP`
   - Style: `Cinematic`
   - Mood: `Curious`
3. Choose **Cyberpunk**.
4. Use this opening sentence: `When I opened my eyes, the city had forgotten my name.`
5. Select one of the three choices in each of the five acts.
6. On the finale screen, review the completed story and soundtrack plan.
7. Select **Generate protagonist illustration — up to 8 credits**, review the confirmation, and approve one image.
8. Wait for the background task to finish and verify the PNG, model, and charged-or-cached status.
9. Select **Try another path** and make at least one different choice to verify replay behavior.
10. Use the BGM toggle to verify that the dedicated audio control remains responsive. No sound is expected until licensed `.ogg` tracks are added under `game/audio/`.

## Cost and cache behavior

- Text choice model: `gpt-5.6-luna`
- Illustration model: `gpt-image-1-mini`
- Illustration quality: `low`
- Images per request: exactly `1`
- Nominal image cost reported by the university guide: `8 credits`
- Automatic image generation: disabled
- Automatic image retry: disabled
- Identical ending cache hit: `0` additional credits
- Default generated image directory: `%LOCALAPPDATA%\YouCanBeAnything\generated` on Windows

The proxy only allows image models listed in its internal cost table. The current list intentionally contains only `gpt-image-1-mini`.

## Saved playthroughs

Completed cycles are stored below Ren'Py's platform-specific save directory:

```text
story_archive/
  YYYYMMDD-HHMMSS-session/
    story.txt
    session.json
    illustration.png  # present only after successful image generation
```

`story.txt` contains the complete prose, illustration prompt, and soundtrack summary. `session.json` contains the profile, genre, opening sentence, five selected choices, epilogue, complete story, and illustration metadata. Manifest updates use a temporary file and atomic replacement to reduce corruption risk.

## Tests

Run the API-free mock suite:

```powershell
python -m unittest tests.test_story_api_server -v
```

Run an API-free mock image smoke test:

```powershell
python scripts/story_api_server.py --image-smoke-test --mock-images
```

The suite verifies mock file creation, cache reuse, zero cached cost, failed-request cleanup, in-flight duplicate rejection, and the `/illustration` HTTP route. Do not run a live image smoke test casually: deleting or changing the cached sample context can cause a new 8-credit request.

## Build a judge-ready game package

1. Run the game offline once and complete a full cycle.
2. Run **Lint** in the Ren'Py Launcher and resolve every actual error.
3. In the launcher, select **Build Distributions**.
4. Build the Windows package, or the combined PC package if the judges may use macOS/Linux.
5. Extract the produced archive into a temporary directory and launch that copy once.
6. Confirm that the packaged game reaches the finale without the proxy.
7. Keep the source repository as the primary judge path. The packaged game may be attached to Devpost only if it fits the upload limit.

The local proxy is a separate developer process and is not automatically bundled into the Ren'Py executable. Judges can always test the offline fallback. To judge the live AI path, they need an authorized key and must start the proxy using the command above.

## Git and submission workflow

The `U` shown beside files in VS Code means **untracked**. After the offline cycle, Lint, and tests pass, create the first commit:

```powershell
git add .
git status
git commit -m "Prepare You Can Be Anything submission"
git branch -M main
```

Create an empty GitHub repository and connect it:

```powershell
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

For a private repository, grant the event-required Devpost and OpenAI judge accounts access before submitting. Do not add the university credential file, `.env`, generated images, save data, or API keys to Git.

Recommended submission order:

1. Choose the best matching Devpost category.
2. Push the final source and README to GitHub.
3. Verify private-repository judge access, if applicable.
4. Record a public YouTube demo under three minutes using `DEMO_SCRIPT.md`.
5. Open the video URL in an incognito window to verify public playback.
6. Run `/feedback` in the Codex session where most work was completed and copy the Session ID.
7. Add the repository URL, YouTube URL, judge instructions, built-with tags, gallery images, and Session ID to Devpost.
8. Add all team members and confirm their invitations.
9. Preview the submission and verify that it is submitted rather than saved as a draft.

Suggested private judge instructions:

```text
Install Ren'Py 8.4.1 or a compatible 8.x SDK. Set the launcher projects directory to the folder containing this repository, select the project, run Lint, and launch it. No credential is required for the complete offline path. The game automatically archives each completed cycle under the Ren'Py save directory. Live GPT-5.6 Luna choices and GPT Image 1 Mini illustration generation require an authorized Sogang Gateway key and the separately started local proxy documented in README.md.
```

## Project structure

```text
game/
  script.rpy       Narrative data, session state, five-act flow, and custom screens
  screens.rpy      Standard Ren'Py menus and interface screens
  options.rpy      Project metadata and build configuration
  gui.rpy          Visual style configuration
  images/          Main menu artwork
SPECIFICATION.md   Detailed architecture and known extension points
DEMO_SCRIPT.md     Sub-three-minute recording and narration guide
SUBMISSION_CHECKLIST.md  Final Devpost handoff checklist
```

## Known limitations

- AI choice generation requires the separately started local proxy and an authorized Sogang API credential.
- Earlier choices affect accumulated context, but do not yet unlock entirely different act graphs.
- Referenced BGM files are not bundled.
- Automated Ren'Py launcher tests are not included; the judge path above is the current smoke test.

## Next steps

- Add distinct state-driven ending types and deeper consequences for earlier decisions.
- Bundle properly licensed audio and document attribution.
- Add export or copy controls for completed stories.
- Improve input validation and accessibility.
- Add a user-facing cache gallery and optional deletion controls.

## License and assets

The bundled interface assets and font should be reviewed for redistribution terms before a public production release. Any future music must include its license and attribution in this repository.
