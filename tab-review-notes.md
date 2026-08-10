# tab-review-notes.md -- RETIRED 2026-08-10

RETIRED at casework-tabs/goal.md ratification (2026-08-10, same
day it was started). Content folded into casework-tabs/goal.md
Appendix A (design rulings) and Appendix B (program amendment,
ratified into atlas/CLAUDE.md). This file is an archive of the
review discussion, kept per delete=archive; it is NOT a live
authority. Live authority: casework-tabs/goal.md.

# ORIGINAL CONTENT BELOW (the six-tab review ledger)

Started 2026-08-10 at James's call: review what we plan to house at
each never-discussed nav tab (Calendar, Files, Tasks, Notes, Search,
Settings). Precedent: next-child-notes.md -- a pre-contract decision
ledger at program root; content folds into a successor contract's
goal.md at ratification and this file then retires. NOT a contract;
James ratifies rulings, this is working memory. Requirements here are
candidates for red-pen, nothing more.

Method notes: corpus criteria define what must be POSSIBLE (cite by
entry id, never edit); interaction design is explicitly free; zero
interaction parity binds -- copying Docketwise screens is the failure
mode. Build work needs a contract; none of this authorizes code.

## Standing rulings banked in this review

- 2026-08-10 CALENDAR BAR (James): designed calendar surface, not
  parity-completion. "We need a good calendar... better than the
  current state." The same fork will be asked per tab; rulings land
  here per tab.
- 2026-08-10 CALENDAR REACH (James): UNIFIED DATE VIEW ruled --
  "I think we need everything": events, expirations, task due
  dates, vmax clocks, invoice due dates on one calendar, with a
  kind filter (dropdown) to see all at once or any single kind
  ("tone it down to just events"). Rationale in his words: one
  calendar that has everything important, whether the seat is
  lawyer, CFO, or finance-at-a-law-company. Candidate requirement 1
  is now a ruling; candidate 2 (visual vocabulary) is flagged by
  James as needing real design thought ("how we display that in
  colors and make it look good").
- 2026-08-10 CALENDAR PER-USER (James): filters and defaults, not
  permissions. (1) Mine/Firm scope toggle riding existing
  relationships (attendees, matter assignees, task assignees);
  (2) seat defaults -- which kind-filters start checked per user
  (lawyer: deadlines/expirations/appointments; finance seat:
  invoice due dates/period close) -- defaults only, every user can
  widen to everything; (3) role ENFORCEMENT stays deferred per the
  s11 status-page precedent (audience tags now, enforcement is a
  future contract). One surface, tuned per seat, never partitioned
  per seat.
- 2026-08-10 CALENDAR VIEWS (James): both views built -- agenda
  (upcoming list) and month grid -- with a two-button toggle to
  switch. Landing ruled: toggle is sticky per user (calendar
  reopens in the view last used); first-ever visit lands on
  agenda.

## Calendar

### Ground truth (verified 2026-08-10)

Corpus (docketwise-spec/corpus/events.md, 4 entries, sealed):
create/edit events -- appointments, deadlines, important dates -- on
a firm calendar (confirmed); attendees = firm members + contacts
searched by name/email (provisional); multiple reminders per event,
offset value+unit, email and/or SMS (confirmed; SMS deferred with
prejudice by casework ruling -- core refuses the channel); firm
default reminders under Settings (provisional). External sync is
integrations territory (google-calendar, outlook-calendar), PARKED
2026-08-01 with the named trigger: ask the friend whether "calendar"
means in-app or Google/Outlook staying in sync. MEETING QUESTION.

Core (casework/app, spine-tested, COMPLETE):
- events.py: full CRUD (title, description, starts/ends, contact,
  matter links), windowed list API (start/end params), attendee
  search across users+contacts, multiple email reminders, firm
  default reminders get/set, dispatch via scheduler.tick.
- expiry.py "Expiry auto-calendaring: dates in, deadlines out":
  set_expiry_date writes the fact ONCE and auto-creates the calendar
  event + reminder with provenance (source='expiry_auto',
  source_fact_id); re-entering a date supersedes its own auto events
  and never touches manual ones. Per-type reminder config (lead
  days, recipients, optional client attendee). The
  enter-once-flow-everywhere invariant already reaches the calendar
  for expirations.
- tasks.py: tasks carry due_date, including due dates DERIVED from a
  reference date via reusable task lists (missing reference date ->
  no due date, no crash). Not calendar-wired.
- reports.py: visa max-out (vmax) machinery -- the corpus carve that
  moved vmax from reports into case-tracking's date engine. Not
  calendar-wired. (Function-level shape unread this session.)
- Billing: invoice due dates exist on billing screens
  (UNVERIFIED at schema level this session). Not calendar-wired.

UI today (casework-ui/app_ui/server.py:702-793, U1.6 era):
flat all-time table (Event | When (UTC)) over events.list_events
with no window arguments; "New deadline" form (title, matter, date,
single reminder; creator auto-added as sole attendee, server.py:764);
detail page (When / Linked / reminders). Matter page lists its
events; dashboard tallies events.

### Parity gaps (core built it, UI never surfaced it)

| Gap                    | Evidence                                 |
| ---------------------- | ---------------------------------------- |
| Attendees UI           | No search/add surface; detail page       |
|                        | omits attendees; creator hard-wired as   |
|                        | the only attendee (server.py:764)        |
| Default reminders UI   | Zero references in app_ui               |
| Time windowing         | list_events takes start/end; UI passes   |
|                        | neither -- every event ever, one table   |
| End time / description | Form captures neither; core takes both   |
| Date formatting        | "When (UTC)" raw ISO -- defect class the |
|                        | billing walk killed with MM/DD/YYYY      |

### Candidate requirements (strawman for red-pen -- not ruled)

1. UNIFIED DATE VIEW: the calendar renders every date-bearing
   object, not just events rows -- appointments, deadlines,
   expirations (already flow in), task due dates, vmax clocks,
   invoice due dates. One surface answers "what is coming at this
   firm." OPEN DECISION -- the fork below.
2. KINDS ARE VISIBLY DISTINCT: appointment vs deadline vs
   expiration vs due date get a named visual vocabulary (precedent:
   the signed dollars-in-buckets vocabulary from billing).
3. PROVENANCE ON EVERY DERIVED ROW: a deadline/expiry row says what
   produced it (which fact, which matter, which clock) and links
   there -- the six-invariants deadline-engine-with-provenance
   requirement surfacing in UI. expiry.py's source_fact_id is the
   existing mechanism.
4. VIEWS: an upcoming/agenda view and a month grid at minimum;
   which is default is a design ruling (agenda-first hypothesis:
   lawyers triage by what is next; grids are for density scanning).
5. PARITY COMPLETION RIDES ALONG: attendees UI, default-reminders
   surface (Settings tab interaction), end times, descriptions,
   MM/DD/YYYY formatting, windowed queries.
6. REMINDERS STAY EMAIL-ONLY per the standing casework ruling; the
   calendar surfaces what reminders exist per row.
7. SYNC STAYS PARKED; the trigger question joins the meeting
   question queue.

### Open questions (queued, not asked)

- RULED 2026-08-10 (see banked rulings): unified reach; per-user =
  filters + seat defaults, enforcement deferred; both views with
  sticky toggle, agenda first-ever; TWO create paths ("New
  appointment" / "New deadline" -- two lean pre-shaped forms, the
  interaction-cost thesis at the button level; James: "2 forms").
- Visual vocabulary for kinds (colors, chips) -- flagged as a real
  design act; land it at a rendered-artifact gate, not in prose.
- Where does the build live: successor child contract (this
  review's output feeds its goal.md); casework-ui remains ON HOLD
  untouched. Defer until all six tabs are reviewed -- the contract
  shape depends on total scope.

### Calendar review status: requirements-complete 2026-08-10.
Remaining design (visual vocabulary, form field lists) is
artifact-gate territory for the build child.

## Files

### Ground truth (verified 2026-08-10)

Corpus (docketwise-spec/corpus/files-and-documents.md, 18 entries,
sealed): central Files area, firm + client uploads + produced
documents together (confirmed); upload with contact/matter
assignment; folders + subfolders; re-assignment; rename; download;
bulk download; preview; print (all provisional); plus the
e-Signature subsystem -- prepare fields on a stored PDF, request
via email/SMS, secure-link signing, completion copies, status
column with pending-signer visibility, auto-filing (mixed
confirmed/provisional; the marquee marketing feature).

Core (spine-tested, COMPLETE): files.py U4.1 = the whole custody
surface -- content-addressed sha256 storage, folders/subfolders
(primary-contact assignment rule), rename, single + bulk-zip
download, preview (pdf/png/jpg/txt/csv; Office post-v1), print;
one files table for firm uploads, client uploads, produced
artifacts, each with a source label. esign.py U4.2 = full
lifecycle draft -> requested -> completed; image-class capture
(drawn strokes or typed name, P4 gate ruling, no crypto); custody
+ audit via esign_events; auto-filing. Email only, SMS deferred.

UI today (server.py:186-192, 845-891): three GET routes. /files =
flat all-firm table (File | Linked to | Size | Uploaded);
/files/<id> = fact card, sole action Download; /files/<id>/download.
NO POST routes: cannot upload, rename, move, assign, preview,
print, or e-sign from screens. Files arrive only from form-package
production and client intake uploads. Matter/contact pages do not
list their files. E-signature has zero UI surface.

### Rulings

- 2026-08-10 FILES BAR (James): DESIGNED surface. Rationale
  accepted: there is no neutral parity UI -- corpus criteria are
  capability-level and the Docketwise interaction model (folder
  tree, mouseover icons, manual filing) is what zero interaction
  parity forbids; parity-completion would make every design
  decision unconsciously and pull toward the shape we bet against.

### Candidate requirements (strawman for red-pen -- not ruled)

1. ORGANIZING PRINCIPLE: matter-centric first -- matter and
   contact pages grow Files sections (links already exist in
   data); the global Files tab is the firm-wide index with
   filters, not the primary filing cabinet. OPEN -- next ruling.
2. FOLDERS DEMOTED, NOT DROPPED: capability stays (corpus + core
   have it); surfaced as secondary organization.
3. CUSTODY VISIBLE: source (produced / firm upload / client
   upload) and sha256 rendered -- chain-of-custody story, free.
4. E-SIGN FIRST-CLASS FLOW: the one inherently expensive UI
   (field-placement prep editor is a custom page regardless of
   bar); request/sign/status/auto-filing ride the core lifecycle.
5. PARITY RIDES ALONG: upload (with assignment), rename, preview,
   print, bulk download surfaced within the designed model.

### Rulings (continued)

- 2026-08-10 FILES ORGANIZING PRINCIPLE (James): MATTER-CENTRIC.
  His words: "if I'm a lawyer clicking through stuff, that's what
  I want to find 90% of the time. If I don't know something, I
  might want to click matter first." Matter/contact pages grow
  Files sections; global Files tab = firm-wide index with filters
  (matter, client, source, e-sign status); folders secondary.

### Open questions (deferred to contract time)

- E-sign build staging: with the tab or its own phase (the prep
  editor's cost may deserve its own gate).
- Office-format preview stays post-v1 (core ruling) -- confirm at
  contract drafting.

### Files review status: requirements-complete 2026-08-10.
## Tasks

### Ground truth (verified 2026-08-10)

Corpus: no tasks module -- the task family is 3 of case-tracking's
10 entries (case-tracking.tasks, task-lists,
task-reference-date-due-dates). Type-and-Enter creation from the
Tasks index or a contact/matter tab; creator default assignee,
auto-attach, any staff assignable (confirmed). Reusable Task Lists
built in Settings, imported onto a client/matter with default
durations + assignees (confirmed). Reference-date due dates: due
computed from a contact-level immigration date, days before/after
(provisional; Docketwise alpha).

ADJACENT, NOT THIS TAB: case-tracking's other 7 entries (priority-
date tracking + notifications, USCIS receipt tracking, manual
check, auto-checks, update notifications) are matter/contact-page
surfaces. Matter pages are not on the six-tab list -- flagged here
so the family is not orphaned; core built receipts machinery
(app/receipts.py, receipt_status_history).

Core (tasks.py U3.3, spine-tested): everything -- type-and-Enter
contract (creator default assignee, matter attaches primary
contact), multi-assignee sets, complete_task, filtered lists
(contact/matter, completed excluded by default), task lists with
duration-days OR validated reference-date rules,
import_task_list = also the engine behind matter-status
automations (status change spawns the task set).

UI today (server.py:895-935): read-only, third tab running. Flat
all-firm table (Task | Due | Linked to | Status pill, completed
included) + detail card with zero actions. No create, complete,
assign, import, or Settings list-builder surface.

### Rulings

- 2026-08-10 TASKS BAR (James): DESIGNED surface.

### Candidate requirements (strawman for red-pen -- not ruled)

1. MY-TASKS-FIRST INDEX: default scope = my open tasks, Firm
   toggle, completed hidden by default -- the calendar per-user
   ruling (filters + defaults, never partitions) applied here.
   OPEN -- next ruling.
2. TYPE-AND-ENTER RETAINED: the one corpus interaction detail
   worth keeping -- quick-add at the top of the index and on
   matter/contact task sections; minimal interaction cost is the
   point.
3. ONE-CLICK COMPLETE from the row (no detail-page round trip).
4. MATTER/CONTACT TASK SECTIONS: tasks visible where the work
   lives (mirrors the Files matter-centric ruling).
5. TASK LISTS SURFACED: a list-builder (Settings territory) +
   Import Task List on matter/contact; the automation linkage
   (status change fires a list) made visible, not buried.
6. REFERENCE-DATE RULES SURFACED in the list-builder (core
   validates contact-level date/expiry facts already).
7. DUE DATES FEED THE CALENDAR (already ruled there): Tasks =
   work-management view; Calendar = time view of the same facts.

### Rulings (continued)

- 2026-08-10 TASKS DEFAULT SCOPE (James): index opens on MY OPEN
  tasks; Firm toggle and completed filter one click away, never
  partitioned.

### Open questions (deferred to artifact gates)

- Whether the task detail page earns richer content (activity,
  notes linkage) or stays a card.

### Tasks review status: requirements-complete 2026-08-10.
## Notes

### Ground truth (verified 2026-08-10)

Corpus (notes.md, 7 entries): Notes Dashboard + contact/matter
Notes tabs (confirmed); creation with optional title, category,
assignees, notify-whole-firm checkbox (provisional); creator
default assignee, reassignable (provisional); association follows
creation surface, editable via Set a Client (provisional);
categories -- 4 premade (Government Action, Memo, Meeting, Phone
Call) + firm-shared custom under Settings, filterable (confirmed);
pinning to top of lists (provisional); PDF export per
contact/matter (provisional). Corpus framing worth designing to:
all of a matter's notes = "a full timeline of the life of the
matter."

Core (notes.py U1.5, spine-tested): everything -- scoped creation
contract, notify-all writes real notifications, assignee sets,
set_client, categories, pinning, PDF export.

UI today (server.py:936-981): read-only index (Note | Pinned |
Linked to | Created; pinned shown as a pill but list not sorted by
it) + detail card. No Add Note, pin, assign, category, or export
action. Fourth tab with the whole write surface missing.

### Rulings

- 2026-08-10 NOTES BAR (James): DESIGNED surface.

### Design question queue (James asked for the questions)

1. TIMELINE FORK -- RULED 2026-08-10 (James): (a) for now. The
   matter-page Notes section is a chronological NOTES timeline,
   pinned on top. (b), the interleaved case timeline (notes woven
   between audit-trail system events -- the Docketwise-can't-match
   story), is PARKED as a named design idea for the successor
   contract's gate: judge it as a rendered artifact, not prose.
2. QUICK-CAPTURE SHAPE -- RULED 2026-08-10 (James): MINIMAL. Body
   box + save, everything defaulted (creator assigned,
   association from the current page, no category), expand
   affordance for title/category/assignees/notify-all. The tasks
   type-and-Enter ruling applied to prose.
3. NOTIFY-ALL PLACEMENT -- RULED 2026-08-10 (James): expanded
   form only; a broadcast is a deliberate act, never a stray
   click on the minimal box.
4. INDEX DEFAULTS -- RULED 2026-08-10 (James): ALL notes, pinned
   first then newest first, filter chips for category and mine;
   per-user seat defaults can re-tune later (calendar precedent).

Minor, deferred to contract/Settings review: category management
lives in Settings; Export button placement on matter/contact
sections (corpus-shaped, uncontroversial).

### Notes review status: requirements-complete 2026-08-10.
## Search

### Ground truth (verified 2026-08-10)

Corpus (firm-settings.universal-search, provisional): a universal
search BAR over Contacts, Matters, Forms by partial name;
jump-to-record on select; Recents button (recently accessed
contacts/matters); USCIS receipt numbers full/partial surface the
carrying matter AND its primary contact (case-tracking join).

Core (search.py, spine-tested): all of it -- partial-name search
(contacts/matters/forms), receipt hits with matter+contact
pairing, open_record feeding the record_access log, recents()
reader.

UI today (server.py:985-1015): WORKS -- the only tab of the six
with a functioning surface. Search page with autofocus form,
honest empty states, linked results (Type | Record | Receipt #).
Gaps: Recents never surfaced (core logs + reader exist, no
caller); it is a destination page where the corpus shape is an
always-present bar -- travel-to-the-tool cost.

### Rulings

- 2026-08-10 SEARCH BAR (James): DESIGNED, "chrome-level" -- one
  search bar present in the shared chrome, reachable from every
  page, plus widened coverage.

### Candidate requirements (strawman -- not ruled)

1. COVERAGE -- RULED 2026-08-10 (James): full list confirmed --
   contacts, matters, forms, receipt numbers, invoice display
   codes, file names, note titles AND bodies (content search
   accepted), task titles, event titles.
2. RECENTS surfaced (empty-bar state: recent records).
3. GROUPED RESULTS by type, jump on select; /search page remains
   as the full-results fallback.
4. Keyboard-first behavior (focus shortcut, arrow + Enter) --
   artifact-gate detail, noted for the interaction-cost thesis.
## Settings

### Ground truth (verified 2026-08-10)

Corpus: the 2026-08-01 split ruling BINDS (closed -- do not
re-propose): 8 IN (managing-users, user-permissions,
user-permission-groups, 2FA, time-zone, notification-settings,
universal-search -> owned by Search, trash-can), 6 OUT as design
position (custom-dashboard, custom-columns, results-per-page,
firm-logo, firm-branches, accounting-notes -- config depth is
complexity-as-feature), 3 N/A. personal-settings adds the
user-role label. Corpus details: Docketwise 2FA is mandatory,
three delivery methods, admin reset; trash is PER-DASHBOARD Trash
views over eight record types (fx-0088).

Core: users.py (management, roles, admin, deactivation), auth.py
(MFA = email method, static per-login code by ruling, TOTP
killed), trash.py (tombstoned soft delete), notify.py,
firm_settings storage. Plus four machinery homes ruled here by
earlier tabs: Task Lists builder, note categories, event default
reminders, expiry reminder config.

UI today (server.py:1017-1039): raw firm_settings key/value dump
("Read-only in v1") + read-only users table. No management
surface at all.

### Rulings

- 2026-08-10 SETTINGS BAR (James): DESIGNED WITHIN THE RULED-IN
  SET -- a small, opinionated admin surface (Users, Permissions/
  groups, Trash, Notifications, Firm basics, and the four
  machinery homes), one screen per concern, no engines. The six
  killed config-depth entries stay killed.

### Rulings (continued)

- 2026-08-10 TRASH PLACEMENT (James): BOTH -- one central Trash
  screen in Settings (all record types, filterable, Restore per
  row) plus a cheap "View trash" link on each list once the
  central screen exists.

### Settings review status: requirements-complete 2026-08-10.

## Review status: ALL SIX TABS requirements-complete 2026-08-10

Bars: all six DESIGNED (Calendar, Files, Tasks, Notes, Search,
Settings). Every load-bearing organizing ruling taken; remaining
detail is artifact-gate territory. This file is now goal-shaping
input for the successor build contract -- the "where does the
build live" decision is the review's one open successor question.
