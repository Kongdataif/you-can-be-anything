# You Can Be Anything: Technical Specification

## Runtime

- Verified with Ren'Py 8.5.3; Ren'Py Lint completed with no errors or warnings on July 21, 2026.
- English submission UI with a complete API-free offline path.
- Optional live AI requests use a separately started local proxy; credentials are never embedded in the game.

## Narrative engine

`StorySession` stores the protagonist profile, genre, opening sentence, act index, generated choices, selected scenes, soundtrack state, finale data, illustration state, and archive location. Five acts cover origin, growth, crisis, climax, and resolution. Genre metadata supplies settings, actions, twists, emotional beats, colors, and imagery.

The live protocol uses six GPT-5.6 Luna requests per completed cycle. `/choices` first creates three concise choices from the profile, genre, and opening sentence. Every selection then calls `/advance` with the selected choice, last scene, accumulated facts, and previous selected history. That response contains exactly two paragraphs and 1-3 facts for the chosen action only, plus three choices for the next act. The fifth advance returns an epilogue and no further choices. If Luna is unavailable, the game presents **Retry GPT-5.6 Luna**, **Continue Offline**, and **Main Menu**; the deterministic generator is never selected silently.

## Finale and persistence

At playthrough start, `StorySession` creates one immutable `session_id`. After five acts, `compose_finale()` builds display data without performing file I/O. The complete story uses Origin, Growth, Crisis, Climax, Resolution, and Epilogue headings instead of inserting synthetic `Because ...` transitions between already connected AI scenes. A separate `ensure_story_archive()` operation creates or atomically updates the one session folder below Ren'Py's save directory:

```text
story_archive/<session>/story.txt
story_archive/<session>/session.json
story_archive/<session>/illustration.png  # after successful generation only
```

The version 3 JSON record includes the fixed session ID, archive status, creation/update timestamps, player profile, opening line, selected choices, accumulated story facts, finale, full story, and illustration metadata. Re-entering the finale updates the same files rather than creating another directory. The background illustration task captures the session's archive and manifest paths when it starts; completion copies the PNG beside that story and atomically updates that exact manifest.

## Illustration pipeline

The finale offers an explicit, cost-labelled generation button. It never generates automatically. After confirmation, the proxy requests exactly one low-quality `gpt-image-1-mini` image in a background task. SHA-256 request hashing enables cache reuse; in-flight duplicate requests are rejected; failures are not cached or automatically retried. API-free mocks cover creation, caching, failure cleanup, duplicate rejection, and the `/illustration` route.

## Audio

A registered `bgm` channel supports the overlay toggle. Soundtrack metadata is included, but licensed audio files are not bundled; missing tracks are reported without interrupting gameplay.

## Known limitations

- Live AI requires an authorized Sogang University Gateway credential and a local proxy process.
- The downloadable judge build is intended to be tested through its complete offline flow.
- Earlier decisions contribute to context and the finale but do not yet unlock separate branching act graphs.
- A player-facing archive browser and bundled licensed soundtrack are future work.
