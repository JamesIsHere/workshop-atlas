# spine-map summary -- U0.1 gate artifact (map RATIFIED 2026-08-01)

Generated 2026-08-01 from ../docketwise-spec/corpus/ against the ratified
111-entry spine. The machine authority is spine-map.json; this file is the
gate reading copy. Mechanical checks passed: 111 entries, zero missing from
corpus, zero superseded, zero duplicate ids/tests, every adapted entry
carries a wording.

## Class counts

| Class   | Count | Meaning                                        |
| ------- | ----- | ---------------------------------------------- |
| direct  | 83    | criterion tests as written                     |
| adapted | 23    | wording adjusted; what v1 proves stated below  |
| content | 1     | engine + starter set; library growth post-v1   |
| parked  | 4     | out of green requirement until trigger fires   |

Adapted landed at 27, not the ~10 the goal table anticipated. The overage
is not new scope-cutting: it is the ratified rulings (email-only, replay
adapters, single-firm architecture, soft-delete invariant) applied
mechanically to every entry they touch. Each wording is listed below.

## Review flags

1. RESOLVED (gate ruling 1, James 2026-08-01): ceac-ds160-efiling,
   ceac-ds260-efiling, dol-flag-efiling are PARKED -- out of the green
   requirement until their forms enter the library (per-entry triggers
   in the map). Rationale: without the forms, all three reduce to one
   shared mechanism test; testing that three times is wheel-spinning.
2. RESOLVED (gate ruling 2, James 2026-08-01): login.firm-custom-
   subdomain PARKED, trigger: multi-tenancy ever enters scope.
   Rationale: architecture-moot under single-firm; any wording would
   pass automatically -- a free green, not a criterion.

## Starter set (resolves the content class; decision default 4)

| Form     | Why chosen                                             |
| -------- | ------------------------------------------------------ |
| G-28     | anchor workflow; attaches to every e-file package      |
| N-400    | paper/e-file-package toggle entry names it             |
| I-129    | answer-import entry names it; repeating sections       |
| I-130    | family petition; e-filable family                      |
| ETA-9089 | conditional appendices + addenda entries name it; DOL  |

Chosen so every form-specific spine entry (efiling-paper-toggle,
i129-answer-import, eta9089-conditional-assembly, packet-addenda) tests
against a real starter form instead of needing its own adaptation. The
friend's actual practice mix replaces this guess when feedback arrives
(parked trigger, worklog).

## Adapted wordings by ruling family

### Email-only (SMS deferred with prejudice; portal deferred) -- 7 entries

- contacts-and-matters.matter-status-automations: task list fires as
  written; message automation sends a templated EMAIL to the primary
  contact (v1's own email templates; Message Templates belong to the
  deferred client-communication module).
- smart-forms.intake-invitations: supported methods are email and
  shareable link; SMS and portal sharing deferred.
- smart-forms.invitation-settings: default EMAIL invitation message
  only; text defaults deferred.
- files-and-documents.esignature-requests: signature requests go by
  email; SMS channel deferred.
- events.event-reminders: email reminders at the chosen offset;
  multiple reminders supported; SMS deferred with prejudice.
- firm-settings.two-factor-authentication: OTP by authenticator app or
  email; SMS delivery deferred; trial-enrollment mechanics N/A.
- smart-forms.multilingual-intake: translation architecture (per-
  question strings, language at invitation, client re-translate) with
  one demonstration language pack; machine-translation service is
  post-v1 and approval-gated (external service).

### Replay adapters (external services out; captured data in) -- 6 entries

- case-tracking.priority-date-tracking: status for filing / final
  action computed against a loaded Visa Bulletin dataset via replay
  adapter over captured bulletin data.
- case-tracking.priority-date-notifications: in-app notification +
  monthly email digest driven by replayed bulletin updates.
- case-tracking.uscis-receipt-tracking: receipt status sourced from
  the replay adapter over captured USCIS responses.
- case-tracking.receipt-status-manual-check: Update button queries the
  replay adapter.
- case-tracking.receipt-status-auto-checks: scheduled re-checks against
  the adapter dataset; plan-tier frequencies N/A -- frequency is a firm
  setting.
- case-tracking.receipt-status-notifications: email + in-app to matter
  assignees when a scheduled check detects a change.

### E-filing family (government accounts out; packages in) -- 4 entries

- smart-forms.uscis-efiling-sync: validated questionnaire -> submission-
  ready package (form artifact + structured field payload) with attached
  G-28; my.uscis.gov sync out.
- smart-forms.efiling-validation: incomplete questionnaire -> per-
  question error list with links; package export blocked until
  re-validation passes.
- smart-forms.h1b-electronic-registration: bulk registration instances
  (employer + up to 20 beneficiaries); e-filing out.
- smart-forms.efiling-paper-toggle: N-400 toggles between e-file-package
  mode and paper without recreating the intake.

### Vendor-operations claims trimmed to mechanics -- 2 entries

- smart-forms.form-updates-versioning: new edition loaded into library
  -> prepared forms migrate automatically; the 5-business-day vendor SLA
  is out of mechanical scope.
- smart-forms.form-version-toggle: revert/re-advance works when a
  previous edition exists in the library; agency version history is
  vendor fact, not mechanics.

### Deferred-module surfaces trimmed -- 2 entries

- contacts-and-matters.custom-attributes: available in custom intakes
  and automated templates; the reports surface deferred with reports.
- contacts-and-matters.activity-feeds: feed tracks in-scope types
  (contacts, matters, forms, tasks, notes, events, files); invoices and
  messages join with their modules.

### Architecture consequences -- 2 entries

- firm-settings.managing-users: deactivate/reactivate as written;
  deletion is tombstone soft delete (hard delete forbidden by goal.md);
  license mechanics N/A.
- files-and-documents.file-preview: v1 supported preview types are pdf,
  png, jpeg/jpg, txt, csv; Office formats post-v1 (conversion
  dependency).

## Content class -- 1 entry

- smart-forms.forms-library: schema-driven engine + the 5-form starter
  set above; criterion tested against the starter set; library growth is
  post-v1 content work.
