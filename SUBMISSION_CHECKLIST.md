# Devpost submission handoff

Items marked `[USER]` require access to your Codex, YouTube, GitHub, or Devpost account and cannot be completed from the local source folder.

## Demo video

- [ ] `[USER]` Record using `DEMO_SCRIPT.md` and keep the final cut below 3:00.
- [ ] `[USER]` Upload to YouTube with Public visibility.
- [ ] `[USER]` Verify the URL in a private/incognito browser window.
- [ ] `[USER]` Paste the verified URL into **Video demo link**.
- [ ] `[USER]` Confirm the narration covers what was built, how Codex was used, and how GPT-5.6 was used.

Suggested YouTube title:

```text
You Can Be Anything — GPT-5.6 Codex Build Week Demo
```

Suggested description:

```text
You Can Be Anything is a hybrid Ren'Py interactive story that transforms a player's profile, genre, opening line, and five choices into a personalized finale. GPT-5.6 through Codex was used to inspect, debug, improve, document, and implement the codebase. GPT-5.6 Terra generates live choices through a local key-holding proxy, with an automatic offline procedural fallback.
```

## Codex feedback Session ID

- [ ] `[USER]` In the Codex session where most of the work was performed, run `/feedback`.
- [ ] `[USER]` Complete or dismiss the feedback prompts as appropriate and copy the Session ID shown by Codex.
- [ ] `[USER]` Paste only that letters-and-numbers ID into the Devpost **/feedback Session ID** field.
- [ ] `[USER]` Recheck for missing characters or accidental spaces.

Use the ID from this project-hardening session if this is the session in which the majority of the submitted work was completed. A repository UUID, Git commit hash, conversation URL, or Devpost project ID is not a substitute.

## Repository

- [x] Portable `README.md` with setup, architecture, limitations, judge path, and Codex/GPT-5.6 disclosure is included.
- [x] Machine-specific absolute setup path has been removed from the primary documentation.
- [x] Local repository metadata has been initialized.
- [ ] `[USER]` Create an empty private GitHub repository without auto-generating a README or `.gitignore`.
- [ ] `[USER]` Add that repository as `origin` and push the local branch.
- [ ] `[USER]` Invite `testing@devpost.com` and `build-week-event@openai.com` using the access method specified by the event.
- [ ] `[USER]` Open the repository URL in the invited account or verify both invitations/access entries.
- [ ] `[USER]` Paste the repository URL into the required Devpost field.

Example commands after replacing the placeholder URL:

```powershell
git add .
git commit -m "Prepare You Can Be Anything submission"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

Do not paste credentials, personal access tokens, or judge-only secrets into the repository or Devpost public story.

## Judge test instructions

Paste or adapt this into the private judge instructions field:

```text
Install Ren'Py 8.4.1 or a compatible newer 8.x SDK. Clone the repository and follow README.md. To test live AI choices, start `scripts/story_api_server.py` with an authorized external credential file or the `SOGANG_API_KEY` environment variable; never place the key in the repository. Without the proxy, the game automatically uses its offline procedural generator. Referenced audio is not bundled, so unassigned soundtrack entries are expected.
```

## Final verification

- [ ] `[USER]` Add all team members and confirm they accepted.
- [ ] `[USER]` Select the best matching category shown by Devpost.
- [ ] `[USER]` Confirm project name and elevator pitch.
- [ ] `[USER]` Preview Markdown formatting and media.
- [ ] `[USER]` Confirm the submission is submitted and not saved as a draft.
