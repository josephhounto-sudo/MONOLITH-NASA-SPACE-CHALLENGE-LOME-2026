# AI usage declaration

| Tool | Used for | Human review |
|---|---|---|
| Claude (Anthropic) | Planning documents before the event (no code); from 14/11/2026 04:15 (after the organizers confirmed work could start; the confirmation was given orally and heard by all participants, no written trace): data analysis, synthetic generator, rules engine, tests, documentation drafts | Every change is reviewed by a team member before merge (checklist V10) |
| ChatGPT (OpenAI), Gemini (Google) | Research notes and review of drafts. The project idea and the solution concept came from the team. | Facts re-checked against the cited sources |
| Cursor (models selected by hand: Claude, GPT or Gemini; one agent session on 14/11/2026 ran on Grok 4.7 (xAI) and is declared here) | Code assistance during the event: tests, UI checks, consistency checks | Pull-request review; nothing is merged without it |

Rules we followed: no personal data, names or phone numbers in any prompt; no model of Chinese origin (local organizer rule); no AI-generated code or data was reused from before the event.
One exception, declared here: **the team logo is an AI-generated image** (OpenAI image model, created on 22/10/2026, before the event, with the model's provenance metadata still inside the file). It is used as-is, **without a visible watermark** (M1 decision, 15/11/2026: the logo is a brand mark, not project content). To our knowledge, the other images in the slides are captures of the running software and charts or simple diagrams produced by the project's own scripts (to be re-checked by M1 before submission).
Pre-event work was limited to design documents (planning was allowed; building was not).
