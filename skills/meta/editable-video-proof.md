# Editable Video Proof — Six Small Jobs, One Accepted Video

Use this production overlay **inside the existing OpenMontage pipeline**, not as a new scheduler, renderer, or replacement for pipeline manifests. Best for reference-driven shorts, data-driven explainers, product films and bounded cinematic proofs. The objective is a watchable, **editable** output: changing pacing or one title must not regenerate unrelated assets.

## Six bounded jobs, mapped to canonical artifacts

| Job | Concrete output | Existing OpenMontage checkpoint |
|---|---|---|
| 1. Understand reference | `reference_spec.md` with source URL, first motion, shot lengths, rhythm, what to transform (not imitate) | `video_analysis_brief` / `research_brief` |
| 2. Ground factual claims | `data.json` containing claim, source URL, observed date and uncertainty for **each** factual number; use `[]` for fiction | `research_brief` |
| 3. Lock story | `story.md`: one point, dominant visual idea, three beats, hook, ending, 2–3 genuine creative alternatives before selecting | `proposal_packet`, `script`, `scene_plan` |
| 4. Build shots | source footage and/or bespoke project-local `Scene.tsx` for Remotion atelier; an asset manifest tracks provenance/rights | `asset_manifest`, `scene_plan` |
| 5. Edit without re-rolling | `timing.ts` or project-local timing constants *for atelier only*; canonical `edit_decisions.json` for all runtimes | `edit_decisions` |
| 6. Render + verify | `final.mp4`, `render_report`, sampled contact sheet, audio inspection, explicit pass/fail against the original delivery promise | `render_report`, `final_review` |

Do not fabricate user-supplied reference analysis when exact video frames/audio were not acquired. Clearly mark estimates. No external video/voice/music generation without the provider/credit permissions available to this project. Do not copy copyrighted footage from a reference merely to imitate its style.

## Editing and time semantics — hard contract

- In `edit_decisions.cuts[]`, `in_seconds`/`out_seconds` are **source trim coordinates**, not final-timeline positions; playback duration is `(out_seconds - in_seconds) / speed`.
- The canonical cut list is ordered; primary cuts concatenate. `layer=overlay` does not add timeline duration. Effects/transitions may alter exact export length: **ffprobe the final MP4**.
- For an atelier scene, title entrance, hold, exit and beat position belong to explicit local constants. A note like *"title a beat late"* changes those constants or edit decisions, not original footage, sourced numbers, story or previously accepted performances.
- Never edit generated or source media merely to correct a text or cut-timing error. Re-render affected composition and compare against previous output.
- Keep project-owned source media and assets stable, keyed by content hash or immutable filename. Change a source only when the editorial feedback specifically requests it.
- Do not silently switch from actual movement/performance to slide animations for a motion-led promise.

## Gate: accepted output, not file existence

1. Preflight assets, source permissions, audio lengths and edit schema. Run `composition_validator` where its supported cut representation applies. If it fails, stop the render; don't ignore it.
2. Render a **short playable excerpt first** using the selected runtime, no new spend or release. Inspect first motion, mid-beat, title timing and the ending with sound.
3. Validate MP4 via ffprobe, sampled frames, readability, narration/music presence and levels, factual citations, asset licence and actual motion where promised. Store exact artifact and results; identify unchanged shots on revisions.
4. Human/editorial approval is requested for genuinely disputed creative taste and final public release, not for each reversible zero-cost intermediate edit already covered by the founder's brief.
5. Preserve a direct playable/exportable review file. Repository commits and screenshots are NOT accepted video.

This overlay adds no background services, paid provider default, Github-hosted Actions or separate control plane. Preserve the current Project Agent's execution authority and the existing project-level allocation gates.
