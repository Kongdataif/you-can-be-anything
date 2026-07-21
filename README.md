# You Can Be Anything

An interactive Ren'Py story in which a protagonist profile, an opening sentence, and five decisions shape a complete personalized narrative.

![You Can Be Anything title screen](game/images/main.png)

## Features

- Five-act structure: Origin, Growth, Crisis, Climax, and Resolution
- Three contextual choices per act
- Two story paragraphs generated for each selected path
- GPT-5.6 Luna as the optional live story engine
- Complete offline mode with no credential or network requirement
- Optional GPT Image 1 Mini finale illustration with explicit cost confirmation
- Hash-based response caching and duplicate-request protection
- One persistent archive per playthrough, containing the story, decision history, and optional illustration

## Requirements

For the game:

- [Ren'Py 8.5.3](https://www.renpy.org/latest.html) or a compatible Ren'Py 8.x SDK
- Windows, macOS, or Linux supported by Ren'Py

For the optional live AI mode:

- Python 3.10 or newer
- Either an authorized Sogang gateway credential or an OpenAI API key with billing enabled

The offline game does not require Python, an API key, or internet access beyond what is included with the Ren'Py SDK.

## Download the source

```bash
git clone https://github.com/Kongdataif/you-can-be-anything.git
cd you-can-be-anything
```

You can also download the repository as a ZIP and extract it.

## Run the game

The complete offline path is available to every user and does not require an API key.

### Offline mode

1. Download and extract the Ren'Py SDK.
2. Start the Ren'Py Launcher.
3. Open **Preferences** and set **Projects Directory** to the directory that contains this repository, not to the repository itself.
4. Return to the launcher and select **You Can Be Anything**.
5. Select **Check Script (Lint)**.
6. Select **Launch Project**.
7. Start a new game and enter the protagonist profile and opening sentence.
8. When the live-engine screen appears, select **Continue Offline**.

The complete five-act story, finale, and archive work in offline mode.

The project directory recognized by Ren'Py should contain:

```text
you-can-be-anything/
├── game/
│   ├── script.rpy
│   ├── screens.rpy
│   └── options.rpy
├── scripts/
├── tests/
└── README.md
```

## Optional live AI mode

The game never stores an API credential. Live requests go through a localhost proxy. You must explicitly choose either the Sogang gateway or the official OpenAI API; credentials are never shared between providers.

### Sogang University gateway

This configuration is available only to users with an authorized Sogang University gateway credential. The credential is not included in this repository and must not be shared.

PowerShell:

```powershell
$env:SOGANG_API_KEY = "your-authorized-key"
python scripts\story_api_server.py --provider sogang
```

macOS or Linux:

```bash
export SOGANG_API_KEY="your-authorized-key"
python3 scripts/story_api_server.py --provider sogang
```

<details>
<summary>Use an external Sogang credential file</summary>

Keep the credential file outside the repository:

```text
key: your-authorized-key
```

Start the proxy with the provider selected explicitly:

```bash
python scripts/story_api_server.py --provider sogang --key-file /path/to/external-key-file.txt
```

Do not place the credential file inside the repository or distribute it with the game.

</details>

### Official OpenAI API

General users may use their own OpenAI API account. API usage is billed to that account. Select the provider explicitly so the key is sent only to `api.openai.com`.

PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
python scripts\story_api_server.py --provider openai
```

macOS or Linux:

```bash
export OPENAI_API_KEY="your-openai-api-key"
python3 scripts/story_api_server.py --provider openai
```

The proxy does not fall back between providers. `SOGANG_API_KEY` is read only in `sogang` mode, and `OPENAI_API_KEY` is read only in `openai` mode.

### Verify the proxy

Open the following address in a browser:

```text
http://127.0.0.1:8765/health
```

A healthy response reports the selected provider, `gpt-5.6-luna`, and the current story schema.

### Launch the game with the proxy

Launch the project from Ren'Py and start a new playthrough. The overlay displays:

```text
Choices: AI | gpt-5.6-luna
```

A complete live cycle uses six text requests:

1. One `/choices` request creates the first three choices.
2. Each of the five selections sends one `/advance` request.
3. Every advance returns the selected scene, established facts, and the next choices.
4. The final advance returns an epilogue instead of more choices.

Successful text responses are cached locally per provider. Repeating an identical request with the same provider reuses the cached result.

## Optional finale illustration

After the final act, the player may approve one low-quality `gpt-image-1-mini` illustration.

- Generation never starts automatically.
- The confirmation screen shows the maximum cost before the request.
- Identical image requests reuse a SHA-256-addressed cache.
- Simultaneous duplicate requests are rejected.
- Failed image requests are not retried automatically.
- The completed PNG is attached to the archive for the originating playthrough.

No image request is necessary to complete the game.

## Saved stories

Each playthrough receives one session ID. Re-entering the finale updates the same archive instead of creating another folder.

On Windows, archives are stored under:

```text
%APPDATA%\RenPy\Choose-1758378693\story_archive
```

On macOS and Linux, use the normal Ren'Py save-data location for the platform and open the `story_archive` directory.

Each completed session contains:

```text
story_archive/<session-id>/
├── story.txt
├── session.json
└── illustration.png   # only after successful image generation
```

`story.txt` is divided into Origin, Growth, Crisis, Climax, Resolution, and Epilogue. `session.json` stores the profile, opening sentence, selected choices, established facts, archive status, and illustration metadata.

## Tests

The automated tests do not call the live text or image APIs.

```bash
python -m unittest tests.test_story_api_server -v
```

The suite covers:

- Initial choice generation
- Selection-driven story advancement
- The complete six-request story protocol
- Finale response validation
- HTTP endpoint contracts
- Mock image generation
- Cache reuse
- Failed-request cleanup
- In-flight duplicate rejection

Run Ren'Py's parser check from the launcher with **Check Script (Lint)** before building a release.

## Build a distributable version

1. Open the project in the Ren'Py Launcher.
2. Run **Check Script (Lint)**.
3. Select **Build Distributions**.
4. Choose the Windows or desktop package appropriate for your users.
5. Extract the generated archive and test the packaged executable.

The packaged game supports the complete offline path. The localhost proxy and credentials are intentionally not bundled.

## Architecture

```text
Ren'Py client
    |
    +-- offline story path (no proxy or credential)
    |
    `-- optional live requests
            |
Local Python proxy
    |-- /choices
    |-- /advance
    |-- /illustration
    |-- response validation
    |-- provider-specific caches
    |
    +-- provider=sogang
    |       `-- SOGANG_API_KEY -> Mindlogic gateway
    |
    `-- provider=openai
            `-- OPENAI_API_KEY -> api.openai.com
```

The credential remains in the proxy process and is never returned to Ren'Py. Provider selection is explicit: the proxy never sends an OpenAI key to the Sogang gateway or a Sogang key to OpenAI.

## Built with Codex and GPT-5.6

GPT-5.6 through Codex was used as a hands-on coding collaborator to inspect, debug, implement, and test the project. Codex helped build the live Luna request flow, response validation, Ren'Py state handling, offline fallback, cost-aware image pipeline, background generation, response caching, idempotent session archives, and automated tests.

GPT-5.6 Luna is also the optional runtime story engine. It receives structured context containing the player profile, genre, opening sentence, selected history, previous scene, and established story facts. Credentials are kept outside the game and repository.

## Security and privacy

- Never commit API keys, environment files, or external credential files.
- Do not embed credentials in Ren'Py scripts or packaged builds.
- Review generated text and images before sharing them publicly.
- Story archives and generated images are local user data and are excluded from Git.

## Known limitations

- Live AI requires the separately running proxy and either an authorized Sogang credential or a billed OpenAI API account.
- The distributed game is intended to remain fully usable through offline mode.
- Soundtrack metadata is present, but audio files and adaptive BGM generation are not yet included.
- A player-facing archive gallery is not yet implemented; saved sessions can be opened from the filesystem.

## Project structure

```text
game/                       Ren'Py scripts and assets
scripts/story_api_server.py Local AI proxy
tests/                      API-free proxy tests
SPECIFICATION.md            Technical design notes
```
