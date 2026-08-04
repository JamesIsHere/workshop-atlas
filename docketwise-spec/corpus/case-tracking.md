# module: case-tracking

Docketwise's own vocabulary (help-center category "Case Tracking", 3
articles, fx-0003; marketing /features/immigration-case-tracking/).
Phase 3 sparse-tail module: full extraction from the collection page
(fx-0210), articles fx-0211..fx-0213, the unmined marketing case-
tracking page (fx-0214), and -- via the tripwire cross-inventory
sweep -- the official "How to reduce client check-ins with real-time
case visibility" video (fx-0215, d192jH3oxcQ). Carve: module anchor +
priority-date family (tracking, notifications) + USCIS-receipt family
(tracking, manual check, auto-checks, notifications) + tasks family
(tasks, task lists, reference-date due dates). Four cross-module
in-place joins instead of duplicates: portal receipt view and share
(client-portal), portal task completion (client-portal), task lists
in matter workflows (contacts-and-matters), receipt-number search
(firm-settings.universal-search).

## entry: case-tracking.module-exists
- name: Case Tracking
- named-by-us: no
- description: Docketwise automates immigration case tracking in a
  Case Tracking tab on the Matter Overview Page and on the Contact
  Overview Page of the matter's primary contact, covering priority
  date status and real-time USCIS case status (fx-0210, fx-0211,
  fx-0212, fx-0214, fx-0215).
- criterion: User opens the Case Tracking tab on a matter or its
  primary contact -> the matter's tracked case statuses (priority
  date, USCIS receipts) are displayed
- sources: fx-0210, fx-0211, fx-0212, fx-0214, fx-0215, fx-0273
- tier: confirmed
- detail: The official tips video attests "8am Docketwise automates
  this transparency with centralized case tracking and USCIS
  updates" (fx-0215, 76s, Nov 2025 era feed). A dedicated product
  video attests automated USCIS updates replacing manual tracking
  (fx-0273, back-catalog via uploads-playlist enumeration).

## entry: case-tracking.priority-date-tracking
- name: Priority Date Tracking
- named-by-us: no
- description: Docketwise tracks an immigrant petition's priority
  date: the user enters the Priority Date and Preference Category
  when creating or updating a matter, and Docketwise reports
  up-to-date status for filing and status for final action, with
  cutoff dates refreshed from the Visa Bulletin just before the
  beginning of each month (fx-0211, fx-0214).
- criterion: User enters a Priority Date and Preference Category on
  a matter -> the matter's Case Tracking tab shows current status
  for filing and status for final action against the latest Visa
  Bulletin
- sources: fx-0211, fx-0214, fx-0270
- tier: confirmed
- detail: The visa-bulletin blog post attests the same mechanics on
  the release-notes family and adds the display surface: a Case
  Tracking tab on both the Matter Overview and Contact Overview
  pages showing preference category, priority date, priority date
  case status, and matter name (fx-0270). Set at matter creation (Create New) or later via Update
  Matter Details (fx-0211). Priority date status is also available
  in matter reports, including custom matter reports (fx-0211) --
  reporting surface folded here; the report engine lives in the
  reports module.

## entry: case-tracking.priority-date-notifications
- name: Priority Date Status Notifications
- named-by-us: no
- description: Docketwise notifies the firm of priority date status
  changes: in-app notifications per change and monthly email
  digests listing matters that became Current or retrogressed to
  Not current, for both status for filing and status for final
  action (fx-0211, fx-0214).
- criterion: A monthly Visa Bulletin update changes a tracked
  matter's priority date status -> the firm receives an in-app
  notification and the change appears in the monthly email digest
- sources: fx-0211, fx-0214, fx-0270
- tier: confirmed
- detail: In-app notifications appear under the bell icon at the
  top-right of the screen (fx-0270). No notification is sent when a bulletin update changes
  nothing for the firm's matters; email digest delivery itself
  triggers an in-app notification; preferences are configured
  under the firm's Notification Settings (fx-0211).

## entry: case-tracking.uscis-receipt-tracking
- name: USCIS Receipt Number Tracking
- named-by-us: no
- description: Docketwise tracks a petition's or application's
  status with USCIS by receipt number: the user adds a receipt
  number (with optional form description) on the matter's Case
  Tracking tab and Docketwise shows the last-updated USCIS case
  status in real time (fx-0212, fx-0214).
- criterion: User clicks + Add Receipt on the Case Tracking tab and
  enters a USCIS receipt number -> the receipt's current USCIS case
  status is displayed on the matter and its primary contact
- sources: fx-0212, fx-0214
- tier: confirmed
- detail: The Case Status text links to the USCIS Case Status
  website for the update date and details (fx-0212). Statuses for
  multiple matters are viewable at once from the matters index by
  adding the USCIS Receipts custom column, and from matter reports
  (fx-0212). Receipt numbers are searchable (full or partial) from
  the universal search bar and the contact/matter index search
  bars -- surface folded into firm-settings.universal-search.

## entry: case-tracking.receipt-status-manual-check
- name: Manual Checks for Updates
- named-by-us: no
- description: An Update button beside each receipt number on the
  Case Tracking tab checks USCIS for a status change on demand and
  updates the stored status if it changed (fx-0212).
- criterion: User clicks Update beside a receipt number -> Docketwise
  queries USCIS and refreshes the stored case status if it has
  changed
- sources: fx-0212
- tier: provisional

## entry: case-tracking.receipt-status-auto-checks
- name: Automatic Checks for Updates
- named-by-us: no
- description: Docketwise automatically re-checks tracked receipt
  numbers against USCIS on a schedule set by subscription plan:
  Basic none, Pro weekly (updated on Saturdays), Advanced daily
  (fx-0212, fx-0214).
- criterion: A tracked receipt's USCIS status changes -> the stored
  status updates without user action within the plan's check
  interval (weekly on Pro, daily on Advanced)
- sources: fx-0212, fx-0214
- tier: confirmed
- detail: Marketing attests automatic pulling of case updates
  without manual checks (fx-0214); the plan-frequency table is
  help-attested (fx-0212).

## entry: case-tracking.receipt-status-notifications
- name: Update Notifications for Automatic Checks
- named-by-us: no
- description: When an automatic check detects a USCIS case status
  change, Docketwise sends an email and an in-app notification to
  the assignees of the matter carrying the receipt number (fx-0212,
  fx-0214).
- criterion: An automatic check detects a status change on a
  matter's receipt -> the matter's assignees receive an email and
  in-app notification
- sources: fx-0212, fx-0214
- tier: confirmed
- detail: Only users assigned to the matter as matter assignees
  receive these notifications (fx-0212). Marketing bills them as
  real-time alerts on status changes (fx-0214).

## entry: case-tracking.tasks
- name: Tasks
- named-by-us: no
- description: Docketwise tasks track work items: created from the
  Tasks index or a contact/matter overview page tasks tab by typing
  the task and hitting Enter; tasks created from a contact/matter
  are auto-assigned to it, default-assign to their creator, and are
  assignable to any staff member on the account (fx-0213). The
  marketing features index attests the capability: set due dates
  on case-specific tasks and assign to members of your team
  (fx-0244).
- criterion: User types a task on the Tasks index or a
  contact/matter tasks tab and hits Enter -> the task is created
  with the creator as default assignee and the contact/matter
  attached where applicable
- sources: fx-0213, fx-0244
- tier: confirmed

## entry: case-tracking.task-lists
- name: Task Lists
- named-by-us: no
- description: Reusable task lists (Settings > Task Lists) generate
  a full set of tasks in one action: the user builds a named list
  of tasks with optional default durations and default assignees,
  then imports it onto a client or matter via the Import Task List
  button, choosing client, matter, and staff assignees (fx-0213).
  The marketing features index names Tasks and Task Lists as a
  case-management capability (fx-0244).
- criterion: User clicks Import Task List on the Tasks index or a
  contact/matter tasks tab and picks a list -> the list's tasks are
  created with their default durations and assignees applied
- sources: fx-0213, fx-0244
- tier: confirmed
- detail: Duration-based due dates assign each task a due date a
  set number of days after task creation (fx-0213). List edits in
  settings save automatically (fx-0213). Task lists also fire from
  matter workflows -- folded into
  contacts-and-matters.matter-status-automations.

## entry: case-tracking.task-reference-date-due-dates
- name: Automatic Due Dates Using Reference Dates
- named-by-us: no
- description: A task in a task list can take its automatic due
  date from a reference date -- an immigration date stored at the
  contact level such as date of birth or US status expiry date --
  set as a number of days before or after that date, instead of
  days after task creation (fx-0213).
- criterion: User sets a task's automatic due date to From
  Reference Date with a date, direction, and day count -> imported
  copies of the task carry a due date computed from the contact's
  reference date
- sources: fx-0213
- tier: provisional
- detail: In Alpha and not available to all customers (fx-0213).
  Reference dates are contact-level only; custom attributes and
  matter attributes are not yet supported (fx-0213).
