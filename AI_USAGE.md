# AI usage declaration

| Tool | Used for | Human review |
|---|---|---|
| Claude (Anthropic) | Planning documents before the event (no code); from 14/11/2026 04:15 (after the organizers confirmed work could start; the confirmation was given orally and heard by all participants, no written trace): data analysis, synthetic generator, rules engine, tests, documentation drafts | Review status: partial. Code is covered by automated tests; the team lead reads the final state before submission (checklist V10, tracked in docs/SOUMISSION_CRITERES.md) |
| ChatGPT (OpenAI), Gemini (Google) | Research notes and review of drafts. The project idea and the solution concept came from the team. | Facts re-checked against the cited sources |
| Cursor (models selected by hand: Claude, GPT or Gemini; one agent session on 14/11/2026 ran on Grok 4.7 (xAI) and is declared here) | Code assistance during the event: tests, UI checks, consistency checks | Automated tests before every merge; human read-through of the final state before submission |
| Grok 4.7 (xAI) via Cursor, read-only mode | Review of the engine code (audit) on branch m2-audit; only Grok was usable on the free Cursor plan | Output cross-checked line by line against the code and tests; the tool modified no file |

Rules we followed: no personal data, names or phone numbers in any prompt; no model of Chinese origin (local organizer rule); no AI-generated code or data was reused from before the event.
Visible marking (15/11/2026): slide 1 carries the line "AI-generated images: team logo, C-Sync mark". The team logo is an AI-generated image (OpenAI image model, created on 22/10/2026, before the event, with the model's provenance metadata still inside the file); it is used as-is and is the only pre-event AI asset. The C-Sync product mark and the short logo animation (folder `brand/`, used on slide 1 and in the 30-second video storyboard) were drawn by an AI assistant (Claude) as code-generated vector geometry on 15/11/2026, from mood images chosen by the team. The other images in the slides are captures of the running software, labelled synthetic where they show crew data, and one chart of real NASA ISS telemetry.
Pre-event work was limited to design documents (planning was allowed; building was not).
Also AI-assisted on 15/11/2026 (Claude): the deck design (dark theme, geometric shapes), the Commander board prototype (six synthetic crew members, decides nothing), the device-feed format reader (no real device) and the French/English pitch scripts; all synthetic or format-only, see `docs/PITCH_FIGE_ET_REPONSES.md`.
