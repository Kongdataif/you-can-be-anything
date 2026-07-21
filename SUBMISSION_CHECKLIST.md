# Devpost Submission Handoff

Items marked `[USER]` require access to your YouTube, Codex, GitHub, or Devpost account.

## Demo video

- [ ] `[USER]` Record with `DEMO_SCRIPT.md`; keep the final cut below 3:00.
- [ ] `[USER]` Confirm the narration explains the project, Codex, and GPT-5.6 Luna.
- [ ] `[USER]` Confirm no credential or personal information is visible.
- [ ] `[USER]` Upload to YouTube and set visibility to **Public**.
- [ ] `[USER]` Wait for HD processing and copyright checks.
- [ ] `[USER]` Verify playback in a private/incognito window without signing in.
- [ ] `[USER]` Paste the standard share URL into Devpost's **Video demo link** and preview the embed.

Suggested title:

```text
You Can Be Anything - GPT-5.6 Codex Build Week Demo
```

The prepared description and exact upload procedure are in `DEMO_SCRIPT.md`.

## Codex feedback Session ID

- [ ] `[USER]` Run `/feedback` in the Codex session where most project work occurred.
- [ ] `[USER]` Copy the Session ID shown by Codex.
- [ ] `[USER]` Paste only that ID into Devpost's **/feedback Session ID** field.

A Git commit, repository UUID, conversation URL, or Devpost project ID is not a substitute.

## Repository

- [x] Portable README, architecture, limitations, judge path, and Codex/GPT-5.6 disclosure included.
- [x] Machine-specific absolute paths removed from primary documentation.
- [x] Private GitHub repository created and configured as `origin`.
- [ ] `[USER]` Commit and push the latest documentation.
- [ ] `[USER]` Confirm the repository is accessible at `https://github.com/Kongdataif/you-can-be-anything`.
- [ ] `[USER]` For a private repository, provide access using the exact Devpost/OpenAI event instructions.
- [ ] `[USER]` Paste the repository URL into Devpost.

Latest-document push:

```powershell
git add README.md SPECIFICATION.md DEMO_SCRIPT.md SUBMISSION_CHECKLIST.md
git commit -m "Update submission and demo documentation"
git push
```

Never commit credentials, personal access tokens, generated save data, or secret files.

## Technical verification

- [x] Ren'Py 8.5.3 Lint passed with no errors or warnings.
- [x] Game launch confirmed.
- [x] API-free proxy mock tests passed.
- [ ] `[USER]` Complete one full offline five-act cycle.
- [ ] `[USER]` Confirm `story.txt` and `session.json` appear in the reported archive folder.
- [ ] `[USER]` Build a Windows distribution ZIP and launch the extracted copy.
- [ ] `[USER]` Upload the ZIP to a GitHub Release or another judge-accessible location.

Judge instructions:

```text
Download and extract the Windows build, then run the included executable. No credential or internet connection is required for the complete offline path. Complete all five acts and confirm that the finale reports a playthrough archive path. For source testing, use Ren'Py 8.5.3 and follow README.md. Live GPT-5.6 Luna choices and GPT Image 1 Mini generation require an authorized external Sogang Gateway credential and the separately started local proxy; credentials are intentionally not included.
```

## Devpost final verification

- [x] Individual submission; no team-member invitations are required.
- [ ] `[USER]` Enter project name and elevator pitch.
- [ ] `[USER]` Paste and personally edit the About the Project text from `DEVPOST_SUBMISSION.md`.
- [ ] `[USER]` Enter Built With tags.
- [ ] `[USER]` Add gallery images.
- [ ] `[USER]` Select the best matching category.
- [ ] `[USER]` Add the repository, build, video, and Session ID.
- [ ] `[USER]` Preview all Markdown and media.
- [ ] `[USER]` Confirm the entry is submitted, not saved as a draft.
