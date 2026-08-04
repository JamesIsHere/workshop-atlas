# plan.md -- casework

Agent-owned strategy; rewritten freely, judged by results. Phase
detail below is COARSE by design -- each phase's units are drafted
and red-penned at its supervised gate, not here.

## Phase roster (invariant order)

| Phase | Delivers                                | Gate output          |
| ----- | --------------------------------------- | -------------------- |
| 0     | Criterion map (spine-map.json, all 111  | Map + schema + test  |
|       | classed), schema for fact store / audit | harness ratified     |
|       | / soft delete, test harness skeleton,   |                      |
|       | synthetic seed generator                |                      |
| 1     | Data spine: contacts, matters, notes,   | Phase 1 criteria     |
|       | users/permissions, login, audit trail   | green; schema frozen |
|       | live on every mutation                  | for invariant tables |
| 2     | Forms engine: fact store -> schema-     | Phase 2 criteria     |
|       | driven form fill, starter set (G-28     | green; anchor        |
|       | first), intake loop, packet assembly    | workflow through     |
|       |                                         | G-28 works           |
| 3     | Deadline machinery: events, reminders   | Phase 3 criteria     |
|       | (email), expiry auto-calendaring, VMAX, | green                |
|       | priority-date tracking (replay adapter) |                      |
| 4     | Files/documents, template-automation,   | Phase 4 criteria     |
|       | CSV export, remaining firm-settings     | green                |
| 5     | Verifier 2 hardening, full spine run    | Both verifiers pass; |
|       | x2, self-audit, result.md               | wind-down            |

## Standing tactics

- Oracle-first: tests exist before their features (op rule 7).
- Paper-design before code inside each unit (trials 2-3 pattern).
- Cheapest-reversible choice + log where feedback is absent.
- Churn counters: producer-side rejections logged per unit.

## Phase 0 units (RATIFIED by James 2026-08-01, zero kills)

Order is dependency order: U0.1 feeds U0.3 (test ids exist before the
harness runs them); U0.2 feeds U0.4 (seeds target the schema).

| Unit | Delivers                                 | Done when            |
| ---- | ---------------------------------------- | -------------------- |
| U0.1 | Criterion map: read all 111 spine        | spine-map.json       |
|      | entries from the corpus, class each      | exists, 111 entries, |
|      | (direct/adapted/content), draft adapted  | none unclassed; gate |
|      | wordings, assign test ids. Output:       | summary written      |
|      | spine-map.json + gate summary (counts    |                      |
|      | per class, every adapted wording listed  |                      |
|      | for James's review)                      |                      |
| U0.2 | Schema, paper-design first: single fact  | schema.sql applies   |
|      | store, matter registry, audit trail on   | clean to a fresh     |
|      | every mutation, tombstone soft delete,   | SQLite db; design    |
|      | users/permissions/2FA-ready. Output:     | note maps each       |
|      | schema.sql + design note tying every     | invariant to its     |
|      | invariant to its enforcing structure     | enforcing structure  |
| U0.3 | Test harness skeleton: runner loads      | harness runs, emits  |
|      | spine-map.json, executes per-entry       | report with all 111  |
|      | acceptance tests (all pending at first), | entries pending, no  |
|      | emits verify/spine-report.txt; the four  | crashes; supporting  |
|      | supporting checks wired (audit sweep,    | checks execute       |
|      | fact-store lint, soft-delete sweep,      | against the empty    |
|      | synthetic guard)                         | schema               |
| U0.4 | Synthetic seed generator: deterministic, | seeds load into the  |
|      | SYNTHETIC-marked fixtures covering       | schema; synthetic    |
|      | contacts/matters/users at spine-testing  | guard passes; reruns |
|      | scale                                    | are byte-identical   |
| U0.5 | Gate package: assemble map + schema +    | James ratifies map   |
|      | harness + seed evidence; supervised      | + schema; Phase 1    |
|      | gate                                     | units drafted next   |

Phase 0 runs UNATTENDED after James red-pens this unit table (MIXED
mode: units ratified before solo execution). The gate at U0.5 is
supervised.

## Phase 1 units (RATIFIED by James 2026-08-01, zero kills; ALL DONE)

U1.1 auth core / U1.2 users+permissions / U1.3 contacts / U1.4
matters / U1.5 notes / U1.6 accountability surface -- 28 entries,
all green 2026-08-01 (worklog has per-unit receipts). Boundary
calls: expiry-date-reminders -> P3; csv-export, universal-search,
notification-settings -> P4; matter-status-automations stayed P1;
notes-export stayed with its module.

## Phase 2 units (RATIFIED by James 2026-08-01, zero kills)

Gate rulings (P2 gate, 2026-08-01): (1) official AcroForm route --
fill real agency PDFs via pypdf; spikes G-28/I-129/I-130/N-400
imported after edition verification; one-time ETA-9089 DOL fetch
approved; tests assert by reading AcroForm fields back. (2) Client
HTTP surface option A -- stdlib localhost server, token-auth'd
client intake routes; invitation/permission/tracking/mobile/upload
tests drive real HTTP; firm side stays module-level until a later
UI phase; mobile-intake proxy = intake completable as plain form
POST, no JS. (3) Unit table ratified as amended, zero kills.

Order is dependency order: engine -> fill -> intake -> custom ->
client surface; packet rides on fill; packages ride on intake +
packet.

| Unit | Delivers                                | Entries              |
| ---- | --------------------------------------- | -------------------- |
| U2.1 | Form-schema engine + starter library:   | forms-library,       |
|      | per-form definition (fields, types,     | form-updates-        |
|      | repeats, conditionals, PDF field map),  | versioning,          |
|      | edition model w/ auto-migration +       | form-version-toggle, |
|      | revert; 5 starter forms G-28 first      | smart-form-          |
|      | (spikes PDFs verified + imported;       | collections          |
|      | ETA-9089 fetched); named collections    |                      |
| U2.2 | Fill + render: facts -> AcroForm fill;  | pdf-values-view,     |
|      | DB-values vs PDF-values override        | form-download-print, |
|      | layer; print settings (editable/        | editable-pdf-toggle, |
|      | flattened, N/A autofill); Print All;    | na-autofill,         |
|      | preparer default + per-form override;   | preparer-population, |
|      | import controls (stored value,          | data-import-into-    |
|      | interpreter, I-129 answers)             | forms, interpreter-  |
|      |                                         | import, i129-answer- |
|      |                                         | import               |
| U2.3 | Intake core: selected forms -> ONE      | single-intake-       |
|      | combined questionnaire deduped by fact  | autofill, question-  |
|      | key; answers write fact store once,     | flagging, question-  |
|      | flow to every form; flag/hide;          | hiding, question-    |
|      | comments + mentions (outbox); search;   | comments, intake-    |
|      | Lite variant                            | search, smart-forms- |
|      |                                         | lite                 |
| U2.4 | Custom intakes: builder (pre-made       | custom-intakes,      |
|      | questions save to contact record +      | custom-questions,    |
|      | custom tabs); types Text/Number/Date/   | document-requests,   |
|      | Boolean/List/Expiry Date/Document       | client-file-upload,  |
|      | Request w/ save-to-custom-attribute;    | templated-intakes    |
|      | doc-request uploads land under          |                      |
|      | contact+matter (custody minimal, mgmt   |                      |
|      | P4); intake templates. PLUS owed        |                      |
|      | custom-attributes intake assertion      |                      |
| U2.5 | Client surface + invitations: stdlib    | intake-invitations,  |
|      | localhost server, invitee token         | invitation-          |
|      | routes; email (outbox) + shareable      | permissions,         |
|      | link; tab-level access; status walk     | invitation-tracking, |
|      | Sent/Accepted/Returned for Review w/    | invitation-settings, |
|      | resend/copy/revoke; default             | multilingual-intake, |
|      | invitation message; translation arch    | mobile-intake,       |
|      | (per-question strings, lang at          | document-sharing     |
|      | invitation, re-translate, 1 demo        |                      |
|      | pack); share completed docs             |                      |
| U2.6 | Packet assembly: forms + files          | packet-assembly,     |
|      | combined, order persisted, rename for   | packet-toc, packet-  |
|      | TOC; auto TOC page w/ page numbers;     | addenda, eta9089-    |
|      | ETA-9089 conditional appendices/final   | conditional-assembly |
|      | determination; addenda as distinct      |                      |
|      | packet part                             |                      |
| U2.7 | Submission-ready packages: validation   | efiling-validation,  |
|      | w/ per-question error list + links,     | uscis-efiling-sync,  |
|      | export blocked until re-validate;       | efiling-paper-       |
|      | package = form artifact + field         | toggle, h1b-         |
|      | payload + attached G-28; N-400          | electronic-          |
|      | e-file/paper toggle; H-1B bulk          | registration         |
|      | registration (employer + up to 20)      |                      |

Owed test extensions (state.md is authority): question-comments
client-responds-in-place gets its HTTP leg when U2.5 lands (logged
same as custom-attributes P1->P2 pattern).

## Phase 3 units (RATIFIED by James 2026-08-01, zero kills)

Gate rulings (P3 gate, 2026-08-01): (1) Visa Bulletin dataset =
one-time fetch of real published bulletin months from
travel.state.gov (public gov data, no PII), stored immutable under
data/visa_bulletin/ w/ README provenance + sha256, per the
ETA-9089 DOL-fetch precedent; months chosen to exercise forward
movement, a flat month, and a retrogression. Receipt-status
dataset stays fully synthetic (receipt numbers must be fake).
(2) Unit table ratified as drafted, zero kills.

Design notes (agent territory, logged): scheduler is a tick(now)
dispatcher w/ injected clock, no daemon, tests drive time; in-app
notifications get a minimal store now, settings surface stays P4;
monthly digest generated by the tick at month boundaries into the
outbox.

Order is dependency order: U3.1's tick feeds U3.2 (expiry
reminders) and U3.5 (auto-checks); U3.4/U3.5 independent; U3.3
freestanding.

| Unit | Delivers                                | Entries              |
| ---- | --------------------------------------- | -------------------- |
| U3.1 | Events core + reminder engine: event    | events.module-       |
|      | CRUD on firm calendar; attendees (firm  | exists, event-       |
|      | members + contacts, name/email search); | attendees, event-    |
|      | email reminders at value+unit offsets,  | reminders, default-  |
|      | multiple per event (SMS refused by      | reminder-settings    |
|      | adaptation); firm default reminders     |                      |
|      | applied to new events; SHARED SCHEDULER |                      |
|      | TICK (injected clock, due-work ->       |                      |
|      | outbox), reused by U3.2 + U3.5          |                      |
| U3.2 | Expiry auto-calendaring + VMAX: per-    | contacts-and-        |
|      | type reminder config (lead time,        | matters.expiry-      |
|      | recipients admin/all/assignees); 8      | date-reminders,      |
|      | built-in types + custom expiry dates    | reports.vmax-        |
|      | via custom attributes (contact-level);  | tracking             |
|      | date entry auto-creates event +         |                      |
|      | reminder; VMAX date + report ordered by |                      |
|      | time remaining, corpus columns, date-   |                      |
|      | range filter                            |                      |
| U3.3 | Tasks: type+Enter creation on index or  | case-tracking.tasks, |
|      | contact/matter surface (creator =       | task-lists, task-    |
|      | default assignee, auto-attach);         | reference-date-due-  |
|      | reusable task lists w/ default          | dates                |
|      | durations + assignees, Import Task      |                      |
|      | List; reference-date due dates          |                      |
|      | (contact-level date, +/- N days)        |                      |
| U3.4 | Priority-date tracking: matter gains    | case-tracking.       |
|      | priority date + preference category +   | priority-date-       |
|      | chargeability; bulletin replay adapter  | tracking, priority-  |
|      | over captured dataset (ruling 1);       | date-notifications   |
|      | status-for-filing + status-for-final-   |                      |
|      | action computed; later bulletin month   |                      |
|      | flips a tracked matter -> in-app        |                      |
|      | notification + monthly email digest     |                      |
| U3.5 | USCIS receipt tracking: receipts on     | case-tracking.       |
|      | matter; replay adapter over synthetic   | module-exists,       |
|      | captured responses; status on matter +  | uscis-receipt-       |
|      | primary contact; manual Update;         | tracking, receipt-   |
|      | scheduled auto-checks at firm-setting   | status-manual-check, |
|      | frequency riding the tick; change ->    | receipt-status-auto- |
|      | email + in-app notification to          | checks, receipt-     |
|      | assignees; module-exists lands here     | status-notifications |
|      | (surface shows both statuses)           |                      |

## Phase 4 units (RATIFIED by James 2026-08-01, zero kills)

Gate rulings (P4 gate, 2026-08-01): (1) e-signature capture is
image-class per the corpus attestation (fx-0194 "drawn or typed")
-- draw = stroke data posted over the client HTTP surface,
rendered to an image; type = name rendered in a signature style;
values stamped into the PDF artifact; audit trail records signer,
timestamp, and sha256 of the signed artifact for tamper-evidence.
No cryptographic signatures, no new dependencies. (2) Unit table
ratified as drafted, zero kills.

Design notes (agent territory, logged): notification-settings is
a firm-wide email routing default (admin/assignee/all staff); the
more-specific P3 expiry per-type recipient config takes precedence
where set. E-signature client signing rides the P2 stdlib
localhost client surface (secure token link); tests drive real
HTTP. Template engine edits document XML inside the .docx zip --
stdlib only.

Order is dependency order: U4.1's file store feeds U4.2 (e-signing
operates on stored PDFs) and U4.4 (search/export read custody
surfaces); U4.3 freestanding; U4.4 last (notification-settings
retrofits existing email senders).

| Unit | Delivers                                | Entries              |
| ---- | --------------------------------------- | -------------------- |
| U4.1 | File store core: Files index (firm +    | files-and-documents. |
|      | client uploads together); upload w/     | module-exists, file- |
|      | contact/matter/folder assignment +      | upload, folders,     |
|      | rename-at-upload; folders (matter       | subfolders, file-    |
|      | assignment requires its primary         | assignment, file-    |
|      | contact), subfolders; re-assignment;    | renaming, file-      |
|      | rename; single + bulk download;         | download, bulk-file- |
|      | preview (pdf/png/jpeg/jpg/txt/csv per   | download, file-      |
|      | adapted wording); print surface. OWED   | preview, file-       |
|      | EXTENSIONS: P2 client-file-upload /     | printing             |
|      | document-request files and produced     |                      |
|      | form artifacts/packets + notes-export   |                      |
|      | output gain real custody surfaces here  |                      |
| U4.2 | E-signature subsystem on stored PDFs:   | esignature,          |
|      | setup (signers + field placement/       | esignature-          |
|      | assignment, editable until requested,   | preparation,         |
|      | locked after); email requests (Send to  | esignature-requests, |
|      | Unsigned, re-send; adapted: SMS         | esignature-signing,  |
|      | deferred); signing over the P2 client   | esignature-          |
|      | HTTP surface via secure link (capture   | completion,          |
|      | model per gate ruling 1; firm members   | esignature-status,   |
|      | sign in-app; date fields auto-fill);    | esignature-signed-   |
|      | completion copies to every signer       | notifications,       |
|      | (outbox); status column + pending-      | esignature-auto-     |
|      | signers view + filter; signed           | filing               |
|      | notification to firm (email + in-app);  |                      |
|      | auto-filing of signed doc under the     |                      |
|      | associated contact/matter               |                      |
| U4.3 | Template automation: .docx merge-tag    | template-automation. |
|      | engine (tags replaced in document XML,  | module-exists,       |
|      | stdlib zip -- no new deps); template    | template-upload,     |
|      | registry (name + upload, selectable at  | template-export,     |
|      | export); export against client          | merge-tags           |
|      | (required) + matter (optional);         |                      |
|      | documented tag vocabulary subset        |                      |
|      | (contact, matter, date families).       |                      |
|      | OWED EXTENSION: custom-attributes       |                      |
|      | TEMPLATE leg -- custom attribute tags   |                      |
|      | resolve in exports                      |                      |
| U4.4 | Cross-cutting surfaces: CSV export on   | contacts-and-        |
|      | Contacts + Matters dashboards (all      | matters.csv-export,  |
|      | records); universal search over         | firm-settings.       |
|      | contacts/matters/forms by partial name  | universal-search,    |
|      | + USCIS receipt number (surfaces        | firm-settings.       |
|      | matter AND primary contact) + recents;  | notification-        |
|      | notification-settings: firm-wide email  | settings             |
|      | routing (admin / assignee / all staff)  |                      |
|      | applied to existing senders             |                      |

## Phase 5 units (RATIFIED by James 2026-08-01, zero kills; ALL DONE)

Gate rulings (P5 gate, 2026-08-01): (1) SPLIT on P0 deferred
weaknesses -- fact-integrity sweep BUILT as verifier-1 supporting
check (passes first run: write-path guard held); contact_relations
directional dedup stays deferred, disclosed in result.md with
trigger. (2) Unit table ratified as drafted, zero kills.

U5.1 anchor walk (verify/run_anchor.py: ten steps, fresh db, PASS
x2) / U5.2 fact-integrity sweep (verify/checks.py) / U5.3 close
(spine x2 byte-identical 8339a907..., result.md, wind-down).
Finding fixed en route: fresh-install gap -- app/bootstrap.py now
owns BASELINE_FACT_DEFS + install(); seed byte-identical.

## Next actions

PROJECT COMPLETE 2026-08-01. Nothing owed under the contract.
result.md is the authority on outcome, disclosed weaknesses, and
post-v1 pointers. Successor decisions are new conversations.
