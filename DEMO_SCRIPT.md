# Demo Video Script and Upload Guide

Target runtime: **2 minutes 45 seconds**. Hard limit: **under 3 minutes**.

Record a horizontal 1080p screencast with clear English narration. Hide notifications, credentials, terminals containing secrets, and personal browser tabs. Rehearse once, then remove launcher loading, typing, generation waits, mistakes, and silence.

Do not spend credits while recording. Use the already generated illustration or previously captured footage of the successful result. Never display the Sogang credential.

## Recording preparation

1. Open the game at its English main menu.
2. Prepare this opening line so it can be pasted quickly:

   ```text
   When I opened my eyes, the city had forgotten my name.
   ```

3. Prepare the existing finale illustration and one completed archive folder containing `story.txt`, `session.json`, and `illustration.png`.
4. Set the game to a readable window size and close unrelated applications.
5. On Windows, press `Win+G`, open **Capture**, enable the microphone, and start recording. `Win+Alt+R` is the usual recording shortcut.
6. If Game Bar does not capture File Explorer or the code editor, record those shots separately or use another screen recorder, then edit the clips together.

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

**Show:** Display one choice screen clearly, then use short cuts to show selections across all five acts.

**Say:**

> The story follows origin, growth, crisis, climax, and resolution. Each act offers three contextual choices. The selected scene is stored and carried into the next act and the final story. GPT-5.6 Luna can generate these choices through a secure local proxy, while a procedural fallback keeps the complete experience available offline.

### 1:05-1:30 - Finale and archive

**Show:** Scroll through the complete finale and soundtrack plan. Briefly show the archive folder with `story.txt` and `session.json`.

**Say:**

> After the fifth act, the game assembles the scenes I selected into one complete ending. Every finished cycle is immediately archived as readable story text and structured session data, including the profile, opening line, choices, finale, and illustration metadata.

### 1:30-1:55 - Cost-controlled illustration

**Show:** Open the illustration confirmation, but select **Cancel** to avoid a new request. Cut to the already generated illustration and its archived `illustration.png`.

**Say:**

> Illustration generation is never automatic. The player must confirm one low-quality GPT Image 1 Mini request with a stated maximum cost. For this recording I cancel the request and show the previously generated result. Identical endings reuse a SHA-256 cache, duplicate requests are blocked, and failures are not automatically retried.

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
- The existing image result is shown without making another paid request.

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
