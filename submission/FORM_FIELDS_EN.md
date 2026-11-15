# Submission form — final texts to paste (English) · 15/11/2026
Source of truth for the 8 official fields (read on https://www.spaceappschallenge.org/resources/project-submission-guide/). The guide gives no word limit. Paste each block as is.

## 1. Project name
C-Sync

## 2. High-Level Summary
C-Sync (Care Sync) is an offline-first assistant for a deep-space crew that is minutes or days away from help. It compares each astronaut with their own baseline, flags drifts in body, attention and morale, shows what it does not know as UNKNOWN (never as normal), guides the crew step by step in a medical emergency, and queues the report for the ground. A resume gate refuses to restart work when the supporting measurement is stale, and the final decision always stays with a human. It runs on synthetic crew data labelled as such and on real NASA ISS cabin telemetry for habitat context.

## 3. Project Demo (link)
https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026/blob/main/pitch/deck/C-Sync_pitch_7_slides.pdf
(7 slides, English. Open without login. To be tested by someone other than M1 in a private window.)

## 4. Final Project Link
https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026

## 5. Project Details
C-Sync (Care Sync) works on the crew's side, where a message to Earth can take up to about 22 minutes each way and links can drop for days. It does three things.

1. Notice. Each astronaut is compared with their own baseline (first five days), not a universal norm. An indicator is flagged when it drifts by at least 1.5 standard deviations for two consecutive days; one flag gives WATCH, two or more give DEGRADED, and two dimensions away from baseline open a fatigue procedure. Body, Attention and Morale are evaluated; Mission and Habitat are context. Missing data is shown as UNKNOWN, never as normal.
2. Guide. On an emergency event (in our story, chest pain) it opens a fixed procedure, guides the measurements one by one (how to take each, with a NASA source), records each value with its time and origin, and queues the report for the ground; the queue delivers it once, without duplicates. It proposes no treatment and no drug; a fixed sentence points to the onboard medical checklist and the crew medical officer.
3. Protect the decision. A resume gate refuses to resume work when the last measurement is older than 10 minutes and explains why in plain words. A commander override is logged but never sufficient on its own.

The app also has a Commander board (the same rule on six synthetic crew members, sorted by urgency, deciding nothing), a body map with eight zones, trend charts, a habitat panel with real NASA data, and a reader for a text format of device measurements (format check only; no real device is connected).

Evidence: on synthetic crews, with the rule never retuned on them, 0 of 300 healthy crews triggered a procedure (2.0 % on a second set of 200, so 0 to 2 % depending on the simulated crews), 139 of 150 gradual drifts (92.7 %) and 86 of 150 abrupt shifts (57.3 %) were detected; the abrupt case is the known weak point. Crew data is synthetic (generator csync-synth-0.1, labelled with version and seed). Nothing is clinically validated. Stack: Python, NumPy, pandas, Streamlit, jsonschema, pytest (211 tests). Next steps: expert review of the rules, then a trial on analog-isolation data, then real sensors.

## 6. Use of Artificial Intelligence
Claude (Anthropic): planning documents before the event (no code); after the organizers confirmed work could start, data analysis, synthetic generator, rules engine, tests, interface, pitch scripts and documentation drafts. ChatGPT (OpenAI) and Gemini (Google): research notes and review of drafts; the project idea and the solution concept came from the team. Cursor with models chosen by hand (one review session on Grok 4.7, xAI, read-only). Images: the team logo is an AI-generated image (OpenAI image model, created 22/10/2026, before the event); the C-Sync mark and logo animation were drawn by Claude as code-generated vector geometry on 15/11/2026; slide 1 carries a visible line naming them. Other images are captures of the running software. No personal data was put in any prompt. Human review is partial: code is covered by automated tests and the team lead reads the final state. Full declaration: AI_USAGE.md.

## 7. NASA data and resources used
NASA OSDR Environmental Data App (ISS cabin CO2, temperature, humidity, radiation; 759,525 points, 20 missions; used for habitat context and data-quality checks only, not scored). NASA Human Research Program risk and hazard pages, paraphrased in our own words for the help cards and countermeasures panel. NASA ASCEND report on Mars communication delays (NTRS 20220013418). Methodological inspiration from the Artemis II Data Methodology Challenge winners. Crew physiology in the demo is synthetic, not NASA data. Full list with links: SOURCES.md.

## 8. References
SOURCES.md in the repository (NASA sources, PhysioNet Wearable Device Dataset v1.0.1 for the sensor-noise model, Basner et al. 2011 on the PVT-B, software list).

## Two boxes on the platform page (M1 only)
- Terms and conditions accepted.
- The work is original and was produced during the event.
