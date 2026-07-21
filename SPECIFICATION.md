# You Can Be Anything: Technical Specification

## Runtime

- Verified with Ren'Py 8.5.3; Ren'Py Lint completed with no errors or warnings on July 21, 2026.
- English submission UI with a complete API-free offline path.
- Optional live AI requests use a separately started local proxy; credentials are never embedded in the game.

## Narrative engine

`StorySession` stores the protagonist profile, genre, opening sentence, act index, generated choices, selected scenes, soundtrack state, finale data, illustration state, and archive location. Five acts cover origin, growth, crisis, climax, and resolution. Genre metadata supplies settings, actions, twists, emotional beats, colors, and imagery.

For each act, the game requests three choices from GPT-5.6 Luna when the proxy is available. Responses are validated before use. A deterministic procedural generator supplies three choices whenever the proxy, network, credential, or model is unavailable.

## Finale and persistence

After five acts, the game composes the complete story, epilogue, soundtrack plan, and a structured illustration prompt. Every completed cycle is immediately archived below Ren'Py's save directory in a unique session folder:

```text
story_archive/<session>/story.txt
story_archive/<session>/session.json
story_archive/<session>/illustration.png  # after successful generation only
```

The JSON record includes the player profile, opening line, choices, finale, full story, and illustration metadata. Illustration completion copies the PNG beside the story and atomically updates the manifest.

## Illustration pipeline

The finale offers an explicit, cost-labelled generation button. It never generates automatically. After confirmation, the proxy requests exactly one low-quality `gpt-image-1-mini` image in a background task. SHA-256 request hashing enables cache reuse; in-flight duplicate requests are rejected; failures are not cached or automatically retried. API-free mocks cover creation, caching, failure cleanup, duplicate rejection, and the `/illustration` route.

## Audio

A registered `bgm` channel supports the overlay toggle. Soundtrack metadata is included, but licensed audio files are not bundled; missing tracks are reported without interrupting gameplay.

## Known limitations

- Live AI requires an authorized Sogang University Gateway credential and a local proxy process.
- The downloadable judge build is intended to be tested through its complete offline flow.
- Earlier decisions contribute to context and the finale but do not yet unlock separate branching act graphs.
- A player-facing archive browser and bundled licensed soundtrack are future work.
