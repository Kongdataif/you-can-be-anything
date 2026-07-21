# Demo Video Script and Upload Guide

For the current recording audit and the revised shot-by-shot edit plan, see `VIDEO_EDIT_PLAN.md`. The July 21 VS Code capture is 3:57.774, contains a silent audio track, and remains on the editor instead of showing the game, so it should only contribute a short code shot rather than serve as the final demo.

Target runtime: **2 minutes 45 seconds**. Hard limit: **under 3 minutes**.

Record a horizontal 1080p screencast with clear English narration. Hide notifications, credentials, terminals containing secrets, and personal browser tabs. Rehearse once, then remove launcher loading, typing, generation waits, mistakes, and silence.

This recording intentionally demonstrates one new live illustration request. Budget for a single request, confirm it only once, and do not retry automatically if it fails. Never display the Sogang credential.

## Recording preparation

1. Open the game at its English main menu.
2. Prepare this opening line so it can be pasted quickly:

   ```text
   When I opened my eyes, the city had forgotten my name.
   ```

3. Choose a new profile, genre, opening line, or decision path so the finale differs from the earlier image test and does not resolve to the old cache entry.
4. Start the local proxy with the authorized external credential before recording. Keep its terminal completely outside the capture area.
5. Confirm that the proxy is ready, but do not press the illustration button during preparation.
6. Set the game to a readable window size and close unrelated applications.
7. On Windows, press `Win+G`, open **Capture**, enable the microphone, and start recording. `Win+Alt+R` is the usual recording shortcut.
8. If Game Bar does not capture File Explorer or the code editor, record those shots separately or use another screen recorder, then edit the clips together.

## Shot list and English voiceover

### 0:00-0:15 - Hook

**Show:** Main menu, then select **Start**.

**Say:**

> You Can Be Anything turns a player's identity, opening line, and five decisions into a personalized interactive story, while remaining fully playable offline.

### 0:15-0:35 - Personalization

**Show:** Enter `Mina`, `INFP`, `Cinematic`, and `Curious`; choose **Cyberpunk**; paste the prepared opening line.

**Say:**

> I begin with a name, MBTI, preferred style, mood, genre, and an original opening sentence. These fields become structured narrative context, not just profile decoration.

### 0:35-1:05 - Five-act choices

**Show:** Display one choice screen clearly and show both resulting narrative paragraphs. Then use short cuts to show selections across the remaining acts so the final video stays under three minutes.

**Say:**

> The story follows origin, growth, crisis, climax, and resolution. GPT-5.6 Luna is the default story engine. One initial request creates the first choices, and every click triggers one advance request that writes two paragraphs for only my selected action while generating the next choices. The selected scene and its facts continue into the next act and final story. A full live cycle uses six text requests, while offline mode remains available only through an explicit player choice.

### 1:05-1:30 - Finale and archive

**Show:** Scroll through the complete finale and its Origin, Growth, Crisis, Climax, Resolution, and Epilogue headings. Briefly show the single session archive folder with `story.txt` and `session.json`.

**Say:**

> After the fifth act, the game assembles my selected scenes under six readable story headings. Each playthrough receives one session ID, so revisiting the finale updates the same archive instead of creating duplicates. The archive includes the profile, opening line, choices, finale, and illustration metadata.

### 1:30-1:55 - Cost-controlled illustration

**Show:** Select **Generate Protagonist Illustration**, pause on the cost confirmation, approve it once, show the locked generating state briefly, then cut the waiting time. Reveal the newly generated image inside the same session archive folder beside `story.txt` and `session.json`.

**Say:**

> Illustration generation is never automatic. I am explicitly approving one new low-quality GPT Image 1 Mini request with a stated maximum cost of eight credits. It runs in the background, locks the button against duplicate requests, and keeps the originating session path even if the interface refreshes. Identical endings can later reuse the SHA-256 cache at no additional image cost, while failures are never retried automatically.

### 1:55-2:15 - Replay and offline reliability

**Show:** Return to the game and select **Try Another Path**. Briefly show the offline status indicator or a new first-act choice.

**Say:**

> A replay starts a fresh session, so the player can change their profile, genre, opening line, or decisions. Judges can complete this entire path without credentials or network access.

### 2:15-2:38 - Codex and GPT-5.6

**Show:** Briefly show `game/script.rpy`, `scripts/story_api_server.py`, the passing mock-test output, and the README. Do not show any credential file.

**Say:**

> I used GPT-5.6 through Codex as a hands-on coding collaborator. Codex inspected and modified the Ren'Py code, fixed the BGM channel, and implemented the Luna proxy integration, background illustration workflow, caching, duplicate prevention, complete story archives, mock tests, and submission documentation. Ren'Py 8.5.3 Lint passes successfully.

### 2:38-2:45 - Close

**Show:** Finale illustration or title screen.

**Say:**

> You Can Be Anything makes each small story feel personal, replayable, and safe to demonstrate offline.

## Editing checklist

- Final duration is between 2:35 and 2:55, never 3:00 or longer.
- The first 15 seconds explain what the project does.
- The video shows working software, not only slides or source code.
- The narration explicitly explains the project, Codex, and GPT-5.6 Luna.
- No API key, credential file, personal notification, or private account detail is visible.
- Generation waiting time, launcher loading, typing, and silence are removed.
- Voice is understandable at normal playback speed; use 1.1x or 1.25x only if still clear.
- Exactly one intentional live illustration request is approved and shown.
- The newly generated `illustration.png` is shown beside the same cycle's `story.txt` and `session.json`.
- If generation fails, the failure state is recorded; do not press Retry during the recording without separately deciding to spend more credits.

## Upload to YouTube

1. Sign in to [YouTube Studio](https://studio.youtube.com/).
2. Select **Create** in the upper-right corner, then **Upload videos**.
3. Select the final video file.
4. Use this title:

   ```text
   You Can Be Anything - GPT-5.6 Codex Build Week Demo
   ```

5. Use this description, editing it in your own voice if desired:

   ```text
   You Can Be Anything is a hybrid Ren'Py interactive story that transforms a player's profile, genre, opening line, and five decisions into a personalized finale.

   GPT-5.6 through Codex was used as a hands-on coding collaborator to inspect, debug, implement, test, and document the project. GPT-5.6 Luna generates optional live story choices through a local credential-holding proxy, while the full game remains playable offline. GPT Image 1 Mini creates an optional, explicitly confirmed finale illustration.

   Source: https://github.com/Kongdataif/you-can-be-anything
   ```

6. Choose the correct audience setting. This project demo is normally **No, it is not made for kids**.
7. Complete YouTube's **Checks** step and resolve any copyright warning. Do not add unlicensed music during editing.
8. Under **Visibility**, select **Public**. Do not leave it Private, and do not use Unlisted when the event requires public visibility.
9. Select **Publish** or **Save** and wait until HD processing has completed.
10. Copy the normal shareable YouTube URL, such as `https://youtu.be/<video-id>` or `https://www.youtube.com/watch?v=<video-id>`.

YouTube notes that closing the upload flow before choosing visibility can leave the video Private. Confirm the setting after publishing.

## Verify before entering the Devpost URL

1. Sign out of YouTube or open a private/incognito browser window.
2. Paste the copied URL and confirm that it plays without requesting access or sign-in.
3. Confirm the duration is under 3:00, audio works, and HD playback is available.
4. Confirm the title, description, and source link are correct.
5. Paste that exact YouTube URL into Devpost's **Video demo link** field.
6. Save the Devpost page, preview it, and confirm that the embedded player loads.
7. If Devpost reports `Must be a valid YouTube, Vimeo, or Youku url`, paste the standard share/watch URL rather than a Studio editing URL, channel URL, local file path, or cloud-drive link.

Official references: [YouTube upload instructions](https://support.google.com/youtube/answer/57407?co=GENIE.Platform%3DDesktop&hl=en) and [Devpost video-making best practices](https://help.devpost.com/article/84-video-making-best-practices).
