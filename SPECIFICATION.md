# Personalized 5-Act Story Simulation

## Overview
- Built on Ren'Py 8.4.1 (project folder: `renpy/Choose`).
- Implements a personalized narrative generator that asks the player for profile information, preferred genre, and a custom opening sentence, then synthesizes a five-act story.
- Provides dynamically generated act summaries, three context-aware choices per act, act-specific BGM lookups, and a replay loop that re-seeds generation for alternate endings.

## Narrative Engine (`StorySession`)
- Maintains session state: profile, genre, start sentence, random seeds, act index, player choices, and soundtrack selections.
- Five-act scaffold defined in `ACT_STRUCTURE` (origin, growth, crisis, climax, resolution). Each act stores intent and a guiding question used in choice copy.
- Genre metadata table (`GENRE_FLAVORS`) supplies setting backdrops, verb palettes, twists, beats, color keywords, and imagery prompts for Mystery, Cyberpunk, SF, and Romance Fantasy.
- Choice generation flow per act:
  1. Builds a context phrase from MBTI description, preferred style, mood, and previous headline.
  2. Samples genre-specific anchors, verbs, and twists with a deterministic RNG seeded by profile + session.
  3. Produces three variants containing headline, detail blurb, narrative paragraph, and thematic impact message.
- After the player commits to a choice, the selection is stored with act metadata and the story advances.

## Audio Handling
- `SOUNDTRACK_LIBRARY` maps genres and acts to preferred track metadata including source API hints (Pixabay or Freesound) and expected relative audio paths (`game/audio/...`).
- When an act begins, `_resolve_track` verifies whether the referenced file exists via `renpy.loader.loadable`; unavailable tracks are marked as placeholders so the final soundtrack summary can distinguish missing audio.
- Overlay UI exposes a BGM toggle that pauses or resumes the active channel while preserving the planned track list.

## Finale Assembly
- `compose_finale()` concatenates the custom opening sentence, each act’s narrative paragraph, and a generated epilogue that reinforces replayability.
- Output bundle includes:
  - `story`: wrapped prose suitable for display inside the finale viewport.
  - `illustration_prompt`: genre + trait driven prompt to hand off to an external image model (e.g., Nano Banana / Midjourney).
  - `soundtrack`: textual summary of act-by-act tracks with availability flags plus an optional ending theme entry.

## Screens & Flow
1. `profile_setup` label collects protagonist name, MBTI, style, mood, genre choice (menu), and opening sentence.
2. `start` label narrates the profile recap, displays `story_overlay`, and loops through five acts:
   - Calls `begin_act()` to log/activate BGM.
   - Shows `act_choice_screen` with act intro text and scrollable choice list.
   - Defaults to the first choice if player cancels.
3. After five acts, stops music, composes the finale, and launches `finale_screen` which contains scrollable panes for story text, illustration prompt, and soundtrack summary.
4. Finale buttons allow replay (restarts from `start`) or returning to main menu.

## UI Highlights
- `story_overlay` screen shows profile summary (MBTI/style/mood), selected genre label, act counter bar, current track title/API, and an inline BGM toggle button.
- `act_choice_screen` uses a modal frame with vertical scrollbar; each choice has a headline button and descriptive detail text.
- `finale_screen` consolidates all deliverables and exposes replay messaging.

## Extensibility Hooks
- `StorySession.prepare_session` accepts arbitrary profile fields—future NPC/relationship traits can extend the dictionary without breaking existing logic.
- `_build_illustration_prompt` and `_soundtrack_summary` centralize text generation for downstream multimodal calls.
- `reset_story_session()` helper allows other labels to clear progress before starting a fresh simulation.

## Known Gaps & Follow-Up Work
- Placeholder Korean strings currently render with mojibake when viewed under non-Unicode console encodings; ensure files are opened with UTF-8 in Ren'Py to avoid garbling.
- Audio files referenced in `SOUNDTRACK_LIBRARY` are not bundled; add CC0-compatible tracks or adjust the mapping to available assets before release.
- LLM/BGM/image integrations are stubbed conceptually—connect to Gemini 2.5 Flash, LLaMA 3.1, Nano Banana, Pixabay, or Freesound APIs via custom Python modules for a fully automated pipeline.
- No persistence yet for analytics (decision timing, multiple playthrough archives). Future phases can store metadata in save slots or external logs.
