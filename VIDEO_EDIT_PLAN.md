# Demo Video Edit Plan

Target: **2:35-2:45**, with a hard maximum of **2:59**.

## Audit of the July 21 12:58 gameplay capture

- Duration: 3:02.953
- Video: H.264, 1920x992, 60 fps
- Audio: AAC stereo track, but silent for the entire recording
- Content: complete main-menu-to-finale gameplay, all five acts, cost confirmation, and illustration result

This capture is suitable as the main demo after shortening. Apply a uniform 1.04x speed change to produce an approximately 2:56 source, then record narration against that edited timeline. Import `VIDEO_SUBTITLES_EN.srt` after the speed change. Trim any remaining black or static tail so the final export remains safely below 2:59.

The gameplay capture does not visibly show the source code or test output. The final subtitle explicitly credits GPT-5.6 through Codex, but a stronger submission should replace 4-6 seconds of the long finale scroll with the reusable VS Code shot and passing test output while keeping the same final narration line.

## Audit of the July 21 capture

- Duration: 3:57.774
- Video: H.264, 1920x1020, 60 fps
- Audio: AAC stereo track, but the entire recording is silent
- Visual content: the capture remains on the VS Code `DEMO_SCRIPT.md` window for almost the entire file

This recording is not suitable as the main demo because it does not show the running game and has no voiceover. Keep at most 4-6 seconds as the code/documentation shot. Record the gameplay, archive, illustration, and test output as separate clips.

## Recording strategy

Record short clips instead of one uninterrupted take:

1. Main menu and profile setup.
2. First choice, followed by both generated story paragraphs.
3. One short clip from each remaining act.
4. Finale headings and the session archive.
5. Image cost confirmation and an already completed image result. Do not make another image request only for editing.
6. Code, tests, and README.
7. Replay or explicit offline option.

When using Game Bar, click the Ren'Py game window before pressing `Win+Alt+R`. Game Bar generally records the active application, so switching from VS Code to Ren'Py during one capture can leave the recording stuck on the wrong window. Use separate recordings for the game and VS Code, or use a display-capture recorder.

Record narration separately in a quiet room. This makes it possible to cut loading and generation waits without breaking the voiceover.

## Final timeline and English narration

### 0:00-0:12 — Hook

**Video:** Title screen, then Start.

**Voiceover:**

> You Can Be Anything is an AI-assisted Ren'Py story where a player's profile, opening sentence, and five decisions shape a complete personalized ending.

### 0:12-0:30 — Personalization

**Video:** Fast cuts of the protagonist name, MBTI, style, mood, genre, and opening sentence. Remove typing pauses.

**Voiceover:**

> I provide a protagonist, personality, visual style, mood, genre, and an original first line. These values become structured story context rather than decorative profile fields.

### 0:30-1:08 — Live interactive story

**Video:** Hold the first choice screen for 3 seconds, show the selection, then show both result paragraphs. Use 2-3 second cuts for Growth, Crisis, Climax, and Resolution. Keep the `Choices: AI | gpt-5.6-luna` indicator visible at least once.

**Voiceover:**

> GPT-5.6 Luna is the default story engine. One request creates the opening choices. Each selection then makes one advance request that continues only the chosen path with two new paragraphs, established facts, and three context-aware next choices. The selected result becomes the previous scene for the following act. A complete live cycle uses one initial request and five advances.

### 1:08-1:30 — Finale and persistence

**Video:** Scroll through Origin, Growth, Crisis, Climax, Resolution, and Epilogue. Cut to the one session folder showing `story.txt` and `session.json`.

**Voiceover:**

> The finale preserves the five selected scenes under clear act headings. Every playthrough receives one session ID, so revisiting the finale updates the same archive instead of creating duplicates. The readable story and structured decision history are saved together.

### 1:30-1:52 — Cost-controlled illustration

**Video:** Show the image button and eight-credit confirmation. Do not approve a new request unless a new paid generation was intentionally budgeted. Cut to the existing completed illustration and show `illustration.png` beside the same story files.

**Voiceover:**

> Finale illustration is optional and never automatic. The player sees the maximum cost before one low-quality GPT Image 1 Mini request. A content hash reuses identical results, duplicate requests are blocked, and the background task keeps the originating session path so the image stays with its story.

### 1:52-2:18 — Codex and engineering

**Video:** Reuse 4-6 seconds from the existing VS Code capture, then show `script.rpy`, `story_api_server.py`, the passing 10-test output, and the Ren'Py Lint result. Crop away unrelated panels.

**Voiceover:**

> I used GPT-5.6 through Codex as a hands-on coding collaborator. Codex inspected and modified the Ren'Py project, implemented the Luna proxy and validation flow, fixed story continuity and Ren'Py collection handling, added cost-aware caching, made archives idempotent, and updated the tests and submission documentation. Ren'Py 8.5.3 Lint and ten API-free tests pass.

### 2:18-2:32 — Offline judge path

**Video:** Show the explicit Luna error decision screen or the `Continue Offline` button, followed by the offline status indicator.

**Voiceover:**

> Credentials are never bundled with the game. Judges can deliberately choose the complete offline path, while the public demo and source show the live AI integration.

### 2:32-2:40 — Close

**Video:** Generated illustration, title screen, and project name.

**Voiceover:**

> You Can Be Anything makes each playthrough personal, traceable, replayable, and safe to demonstrate.

## Editing instructions

1. Create a 1920x1080, 30 fps timeline. The 60 fps source can be conformed to 30 fps without visible loss for this UI demo.
2. Place the narration first and edit visuals to the voice. Keep the final duration below 2:50 to leave upload margin.
3. Delete all loading, typing, mouse hesitation, repeated clicks, and model waiting time.
4. Use straight cuts. Add a 4-6 frame crossfade only between unrelated locations such as the game and VS Code.
5. Speed up profile entry and long scrolling to 2x-4x. Keep choice text and generated paragraphs at normal speed long enough to read.
6. Add small section labels only when useful: `PERSONALIZE`, `LIVE LUNA`, `ONE SESSION ARCHIVE`, `OPTIONAL IMAGE`, and `BUILT WITH CODEX`.
7. Zoom or crop the game to keep text readable. Avoid showing the Windows taskbar, notifications, credential terminal, attachment paths, or personal account information.
8. Normalize narration to a consistent level and use light noise reduction. Do not add music unless its license is known and it remains well below the voice.
9. Use the existing generated illustration if needed. Do not imply that it was generated during this exact recording unless the approval and completion were actually captured.
10. Export H.264 MP4 at 1080p, 30 fps, with AAC audio. Watch the exported file from beginning to end before upload.

## Final checks

- Duration is under 3:00.
- Voiceover explicitly explains the project, Codex, and GPT-5.6 Luna.
- At least one choice and both resulting story paragraphs are visible.
- The finale headings and single session archive are visible.
- Image consent and the saved result are shown truthfully.
- No key, credential file, or private account information is visible.
- The YouTube video is Public and works in an incognito window.
