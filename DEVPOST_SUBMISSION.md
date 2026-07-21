# Devpost Submission Copy

Edit the personal motivation and learning details so they remain true to your own experience before submitting.

## Project name

```text
You Can Be Anything
```

## Elevator pitch

```text
A hybrid Ren'Py experience that turns your personality, opening line, and five decisions into a personalized story and optional finale illustration.
```

## About the project

```markdown
## Inspiration

Most interactive stories ask players to step into a character that has already been written. I wanted to explore a different idea: what if a story began with who the player is, how they feel today, and the first sentence they personally want to write?

That question became **You Can Be Anything**, a replayable five-act narrative experience where a lightweight personality profile and a sequence of meaningful choices shape both the journey and its final image.

## What it does

The player enters a protagonist name, MBTI, preferred style, current mood, and an original opening sentence. They then select one of four genres: Mystery, Cyberpunk, Science Fiction, or Romance Fantasy.

The story progresses through five acts—Origin, Growth, Crisis, Climax, and Resolution. Each act presents three choices generated from the player's profile, genre, opening sentence, and previous decisions. After the final choice, the game assembles the selected scenes into a complete story.

Every completed playthrough is automatically archived with its profile, opening sentence, five selected decisions, finale, illustration prompt, and soundtrack plan. The player can also explicitly approve one low-cost protagonist illustration. If an identical ending has already been illustrated, the game reuses its cached image without making another image request.

The game includes a complete offline path, but GPT-5.6 Luna is the default story engine. If Luna is unavailable, the game asks the player to retry, continue offline, or return to the menu; it never changes engines silently.

## How I built it

I built the game with Ren'Py 8.5.3, Ren'Py Screen Language, and embedded Python.

The narrative architecture separates a reusable five-act structure from genre-specific settings, actions, twists, emotional beats, colors, and imagery. A `StorySession` object tracks the player profile, current act, generated choices, selected scenes, soundtrack state, finale data, illustration state, and playthrough archive.

For the live story, the Ren'Py client sends structured context to a local Python proxy. The proxy keeps the credential outside the game and repository. An initial GPT-5.6 Luna request creates three choices; each of five selection-driven advance requests generates two paragraphs for only the chosen action, canonical facts, and the next choices. This six-request pipeline makes every click visibly change the generated story without spending long-form output on unselected branches.

For finale art, the proxy uses GPT Image 1 Mini with one image and low quality enforced by code. Image generation is never automatic: the player sees a maximum-cost confirmation first. Requests are addressed by a SHA-256 hash, identical endings reuse a local cache, simultaneous duplicates are rejected, failures are not cached, and failed requests are not automatically retried.

The downloadable game remains fully playable without the proxy through its offline procedural fallback.

## How I used Codex and GPT-5.6

I used GPT-5.6 through Codex as a hands-on coding collaborator rather than only as a writing assistant. Codex inspected the existing Ren'Py project, traced its state and replay flow, identified an unregistered custom BGM channel, and modified the game code to correct it.

Codex then helped convert the interface and narrative flow to English, implement the GPT-5.6 Luna choice pipeline, keep credentials outside the client, validate model output, and preserve an offline fallback. It also implemented structured finale context, explicit image-cost confirmation, background image generation, SHA-256 caching, duplicate suppression, failure handling, and automatic playthrough archives that keep the complete story and generated illustration together.

Codex also created API-free mock tests for cache reuse, failed-request cleanup, duplicate rejection, and the illustration HTTP endpoint. I used those tests alongside Ren'Py 8.5.3 Lint and manual gameplay testing.

GPT-5.6 Luna is the default runtime story engine. When the local proxy is available, it generates the three choices and two-paragraph branch outcomes shown in each act. When it is unavailable, the game presents an explicit retry or offline choice instead of silently changing engines.

## Challenges I ran into

One challenge was making AI generation optional rather than allowing the entire game to depend on a network request. I solved this by preserving a procedural generator behind the same choice interface. The player can complete the same five-act cycle whether the model is online or offline.

Another challenge was protecting a university API credential in a downloadable desktop game. Embedding the key in Ren'Py would expose it, so I separated model access into a localhost proxy that reads an external credential or environment variable. The key is never returned to the game or committed to the repository.

Image generation introduced a different problem: a double-click, retry, or repeated ending could create unnecessary cost. The final design requires explicit approval, allows only one low-quality image per request, blocks an identical in-flight request, reuses completed images by content hash, and never retries a failed image automatically.

I also had to distinguish real Ren'Py errors from editor diagnostics. A standard Python language server marks valid Screen Language statements as errors because `.rpy` is not ordinary Python. Ren'Py 8.5.3 Lint became the authoritative parser check, followed by a complete manual playthrough.

## Accomplishments that I'm proud of

- A complete profile-to-finale five-act gameplay loop
- Live GPT-5.6 Luna choices with strict response validation
- A credential-free offline fallback for judges and players
- Optional GPT Image 1 Mini finale artwork with visible cost consent
- Hash-based image caching and duplicate-request protection
- Automatic archives containing the complete story, structured decision history, and illustration
- English gameplay and standard Ren'Py interface
- API-free mock tests and a successful Ren'Py 8.5.3 Lint run

## What I learned

I learned that adding a model call is only one part of building a reliable AI product. The surrounding system—state, validation, fallback behavior, credential boundaries, cost controls, caching, persistence, and an understandable user experience—is just as important as the generated text.

I also learned how Ren'Py combines its own script and screen languages with Python, and how to move blocking model work away from the interaction thread while returning safe state updates to the UI.

## What's next

Next, I would deepen the consequences of earlier decisions so they unlock different act structures and ending types. I would also add a player-facing archive gallery, export and sharing controls, licensed soundtrack assets, broader accessibility testing, and a hosted authenticated backend for a public live-AI release.
```

## Built with

```text
Ren'Py
Python
OpenAI
GPT-5.6
GPT-5.6 Luna
GPT Image 1 Mini
Codex
Interactive Fiction
Procedural Generation
```

## Private judge instructions

```text
Download the Windows build from the GitHub Release, extract it, and run the included executable. No credential or internet connection is required for the complete offline path. Complete all five acts and verify that the finale reports a playthrough archive path.

For source testing, install Ren'Py 8.5.3, set the launcher projects directory to the folder containing the repository, select the project, run Check Script (Lint), and launch it.

Live GPT-5.6 Luna choices and GPT Image 1 Mini generation require an authorized Sogang University API Gateway credential and the separately started local proxy documented in README.md. Credentials are intentionally not included in the repository or downloadable build. The public demo video shows the live AI path; the repository includes the proxy implementation and API-free mock tests.
```

## Remaining submission values

```text
Repository URL: [ADD AFTER GITHUB PUSH]
Windows Release URL: [ADD AFTER RELEASE]
Public YouTube URL: [ADD AFTER UPLOAD]
Codex /feedback Session ID: [ADD AFTER RUNNING /feedback]
Submitter type: Individual
Country of residence: [SELECT YOUR COUNTRY]
Category: [SELECT THE BEST AVAILABLE CATEGORY]
```
