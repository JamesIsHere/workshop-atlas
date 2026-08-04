# reproduction-audit.md -- verifier 2 diff report (Phase 5)

Run 2026-08-01. Status: RULED 2026-08-01 (James): the 3 variances
are TRANSCRIPTION NOISE, not extraction error -- corpus ACCEPTED,
verifier 2 diff gate PASSED. Remaining [G2] items (micro-fixes,
interpretive queue, criterion spot-check) ruled separately.

## Protocol

| Item            | Value                                            |
| --------------- | ------------------------------------------------ |
| Sample frame    | 239 live entries (superseded excluded), sorted   |
| Sample method   | python random.Random(20260801).sample(frame, 15) |
| Seed rationale  | run date, committed before the draw              |
| Verifier model  | Sonnet (single non-Fable model, [G1] ruling 8)   |
| Extractor model | Fable (sole extractor, Phases 0-4)               |
| Isolation       | fresh agent, isolated package dir: entry id +    |
|                 | module + name + copies of cited fixtures ONLY;   |
|                 | no corpus text, no answer key, no web access     |
| Verifier task   | 1-3 sentence description per entry from the      |
|                 | cited fixtures alone, plus evidence-notes        |
| Raw output      | scratchpad repro-audit/derivations.md (session   |
|                 | dir; full text reproduced per entry below)       |

The verifier saw corpus descriptions never. The comparison below is
against each entry's description AND detail field, because several
verifier statements reproduce facts the corpus stores in detail.

## Classification scheme

| Class      | Meaning                                             |
| ---------- | --------------------------------------------------- |
| MATCH      | same reading; wording differences only              |
| VARIANCE   | same reading; detail-level or emphasis differences  |
|            | (either side compressed or expanded), no meaning    |
|            | change                                              |
| DIVERGENCE | substantive difference in what the feature is or    |
|            | does -- extraction-error candidate                  |

## Result summary

| Class      | Count |
| ---------- | ----- |
| MATCH      | 12    |
| VARIANCE   | 3     |
| DIVERGENCE | 0     |

Cross-cutting finding: every fact the verifier surfaced that is
absent from a corpus DESCRIPTION is present in that entry's DETAIL
field -- Alpha status (task-reference-date-due-dates), Pro/Advanced
gating (contact-to-lead-conversion), Spanish-only plus untranslated
fields (invoice-translation), non-editable group name/members
(group-chats), creator-only saving (custom-report-saving),
portal-preview filter restriction and custom-attribute settings
(hr-portal-reports). The independent re-derivation reproduced the
corpus's reading and its detail capture without access to either.

## Per-entry diffs

### 1. case-tracking.task-reference-date-due-dates -- MATCH
Verifier: due date computed from a contact-level reference date
(birth date, US status expiry), set as days before/after, vs the
default days-after-creation; flags Alpha status and contact-level
limitation. Corpus description says the same; Alpha and
contact-level-only are in detail. No divergence.

### 2. client-portal.hr-portal-employee-management -- VARIANCE
Verifier: employees recorded on the contact's Employees tab (new or
linked contacts), added/removed from the HR Portal via bulk actions,
shared items visible to company and employee portals. Corpus: same
mechanics; corpus specifies removal via trash-can icon where the
verifier compressed removal into "bulk actions". Verifier-side
compression; the verifier also enumerated the video's shared-item
list more fully. No meaning change.

### 3. client-portal.portal-two-factor -- MATCH
Verifier: firm enables/disables 2FA per contact from the Portal tab;
client enrolls an authenticator app via QR code and enters OTP at
login. Corpus description is the same reading, near point-for-point
(apps list, QR, OTP).

### 4. contacts-and-matters.matter-creation -- MATCH
Verifier: Create New > Matter; required contact + matter name;
optional description, type/status, preference category/priority
date, assignee with task auto-assign; Create Matter finalizes.
Corpus description identical in substance. Verifier evidence-note:
fx-0142 is a collection index page whose one-line blurb carries no
procedural detail -- consistent with the corpus, which draws its
description from fx-0148 only.

### 5. docketwise-iq.ai-summarization -- VARIANCE
Verifier: Summarize is one of the IQ Writing Assistant options
(sparkle icon in notes, email, bulk messaging, questionnaires);
output can be inserted, discarded, copied, or REGENERATED. Corpus
description is thinner (condenses content into a generated summary)
and the criterion lists insert/copy/discard but not regenerate.
Verifier-found micro-fact: the regenerate option (fx-0203) appears
nowhere in the corpus entry. Detail-level omission, no meaning
change.

### 6. docketwise-leads-crm.contact-to-lead-conversion -- VARIANCE
Verifier: convert an existing Contact into a Lead via More Actions >
Convert to Lead; Pro/Advanced only (corpus stores the gating in
detail). Corpus description says a contact "converts BACK to a
lead" -- a directional coloring the fixture sentence ("you can also
convert Contacts to Leads") does not itself state, though it sits in
a section about converting leads to clients. Candidate wording fix;
mechanics identical.

### 7. docketwise-leads-crm.custom-lead-statuses -- MATCH
Near-verbatim agreement: firm-defined statuses via More Actions >
Manage Lead Statuses, filtering via Lead Status button, same example
status list.

### 8. files-and-documents.file-printing -- MATCH
Near-verbatim agreement: mouse over file, printer icon, print from
newly opened tab, no download needed.

### 9. internal-chat.group-chats -- MATCH
Verifier: Create Group, title, members via +/- selection, group
exists once first message sent; name/members immutable after
creation. Corpus: identical; immutability is in detail.

### 10. invoicing-and-trust-accounting.automatic-late-fees -- MATCH
Verifier: overnight application on unpaid balance past due date,
fixed or percentage amount, optional recurring fee at configurable
day frequency, per-invoice or firm-wide default. Corpus: identical;
the per-invoice/firm-default split is in detail.

### 11. invoicing-and-trust-accounting.invoice-translation -- MATCH
Verifier: Language toggle in invoice settings, instant display for
firm and client, Spanish-only at capture, enumerated untranslated
fields. Corpus: identical; Spanish-only and the untranslated-fields
list are in detail.

### 12. notes.note-assignment -- MATCH
Verifier: creator is default assignee, reassignment via assignee
field + Update, removal via X. Corpus: same reading; Update
mechanics live in the criterion.

### 13. reports.custom-report-saving -- MATCH
Verifier: Save Report persists filters for one-click reopening from
Select a Report; creator-only saving. Corpus: identical;
creator-only is in detail.

### 14. reports.custom-report-sharing -- MATCH
Verifier: Share Report toggle exposes the report firm-wide;
non-creators filter temporarily but cannot save or change
visibility. Corpus: identical; the non-creator restrictions are in
detail.

### 15. reports.hr-portal-reports -- MATCH
Verifier: Employees Report + Matter Report inside the HR Portal,
portal-user filtering, custom attributes enabled at Settings >
Portal Settings, firm preview cannot edit filters. Corpus:
identical, all points in description or detail. Verifier
evidence-note: fx-0276 attests only the chapter title "HR Portal
Reports (4:55)" -- exactly how the corpus detail records it.

## Items for the [G2] ruling

1. The ruling itself: are the 3 VARIANCE diffs transcription noise
   or extraction error? (Report's classification: noise -- zero
   substantive divergences in 15 of 15.)
2. Entry 5 micro-fact: admit "regenerate" to the ai-summarization
   entry (in-place source-detail addition per [G1] ruling 1, or
   leave)?
3. Entry 6 wording: drop "back" from contact-to-lead-conversion's
   description (supersede-level meaning change or in-place fix)?

## Verifier-run facts

Single Sonnet agent, one pass, no retries; 22 fixture files copied
to the package; verifier reported all 15 entries clearly attested by
their fixtures, with thin-attestation observations on fx-0142
(index blurb), fx-0276 (chapter title only), and fx-0235's
single-sentence contact-to-lead attestation -- each consistent with
how the corpus already records those sources.
