# module: reports

Docketwise's own vocabulary (help-center category "Reports", 10
articles, fx-0003). Phase 3 fan-out module: full extraction from 10
help articles (fx-0160..fx-0169), collection page fx-0159, marketing
custom-reports feature page fx-0170, the official "Introducing Custom
Reports" video fx-0171, and the Matter Workflows webinar fx-0158
(agenda item "Reporting with Matter Workflows"), captured in module
4. Two subsystems: a standard report engine (one selectable category
per data type, shared filter/column/export mechanics) and the Custom
Reports builder (save/share/download lifecycle).

## entry: reports.module-exists
- name: Reports
- named-by-us: no
- description: The product carries a reporting capability with a
  dedicated 10-article help category (fx-0003, fx-0159): reports run
  over Contacts, Leads, Matters, Invoices, Payments, Tasks, and
  Users, with filters, selectable columns, and CSV export (fx-0169).
  Marketing lists Reporting as a product feature (fx-0170) and an
  official video introduces custom reporting (fx-0171). Decomposed
  into this file's entries in Phase 3.
- criterion: User clicks Create New and selects Report -> report
  categories for contacts, leads, matters, invoices, payments,
  tasks, and users are available to run
- sources: fx-0003, fx-0159, fx-0169, fx-0170, fx-0171
- tier: confirmed

## entry: reports.custom-report-builder
- name: Custom Reports
- named-by-us: no
- description: Custom Reports are created from the Select a Report
  page by choosing a data type and clicking Create +; the new report
  is saved automatically and is then edited by choosing columns,
  applying filters, and naming it (fx-0160). Available data types:
  Contacts, Leads, Matters, Invoices, Invoice Charges, Payments,
  Tasks, and Time Entries (fx-0160). Marketing attests granular
  custom data reporting (fx-0170); the official launch video
  introduces the feature (fx-0171).
- criterion: User selects a data type on the Select a Report page
  and clicks Create + -> a new custom report is created and saved,
  with editable columns, filters, and name
- sources: fx-0160, fx-0170, fx-0171
- tier: confirmed
- detail: Columns are chosen via the gear icon: add from Available
  Columns, remove from Selected Columns, drag-and-drop reorder, then
  Update; unsaved filters are lost when columns are updated
  (fx-0160). Advanced filtering filters by any data field in the
  report; filter groups act like parentheses with And/Or operators
  between filters and groups, operators inside a group must all
  match (as must those outside), and text-field filters are
  case-sensitive (fx-0160). The report is named via the pencil icon;
  only the creator can edit the name (fx-0160).

## entry: reports.custom-report-saving
- name: Saving a Custom Report
- named-by-us: no
- description: A custom report's filters are saved with the Save
  Report button; saved reports are reopened later from the Select a
  Report page under their data type (fx-0160). Marketing attests
  saved report configurations with one-click access to unlimited
  saved reports (fx-0170), as does the launch video (fx-0171).
- criterion: User clicks Save Report and later returns to the Select
  a Report page -> the saved report is listed under its data type
  and opens with its saved filters
- sources: fx-0160, fx-0170, fx-0171
- tier: confirmed
- detail: Save Report is available only to the report's creator; if
  a shared report's default filters need updating, the creator must
  do it (fx-0160). A saved report is deleted from the Select a
  Report page via its trash icon, creator-only (fx-0160).

## entry: reports.custom-report-sharing
- name: Sharing a Custom Report
- named-by-us: no
- description: A Share Report toggle makes a custom report visible
  to all members of the firm; shared reports appear on the Select a
  Report page with a reference to their creator's name (fx-0160).
  Marketing attests firm-wide report sharing (fx-0170).
- criterion: Creator toggles Share Report to active -> all firm
  members can access the report from the Select a Report page
- sources: fx-0160, fx-0170
- tier: confirmed
- detail: Non-creators can apply new filters to a shared report but
  cannot save them, and cannot unshare the report, edit its name, or
  delete it (fx-0160).

## entry: reports.custom-report-export
- name: Downloading a Custom Report
- named-by-us: no
- description: An open custom report is downloaded via the Export &
  Download button (fx-0160).
- criterion: User clicks Export & Download on a custom report -> the
  report downloads
- sources: fx-0160
- tier: provisional

## entry: reports.hr-portal-reports
- name: HR Portal Reports
- named-by-us: no
- description: Firms with an activated HR Portal expose reports
  inside the portal: an Employees Report (company employees shared
  with the portal) and a Matter Report (the company's matters), with
  advanced filtering for the portal user (fx-0160). The portal-side
  guide confirms the two data types (Contacts/Employees, Matters)
  and the portal user's editing surface: a gear icon chooses and
  orders columns, filters and filter groups combine with And/Or
  operators, and an Export & Download button downloads the report
  (fx-0187).
- criterion: HR Portal user opens reports inside the portal ->
  Employees and Matter reports are available with filtering
- sources: fx-0160, fx-0187, fx-0276
- tier: confirmed
- detail: The Q4 2022 features-roundup video names HR Portal
  Reports as a release (fx-0276, chapter at 4:55). Filter groups act like parentheses; operators inside a
  group must match, and text-field filters are case-sensitive
  (fx-0187). Contact and matter custom attributes are excluded from HR
  Portal reports by default and are enabled per attribute type at
  Settings > Portal Settings; individual fields cannot be selected
  one-by-one (fx-0160). Filters cannot be updated while a firm user
  previews the portal -- only the logged-in portal account updates
  filters (fx-0160). The HR Portal feature requires a Pro or
  Advanced subscription (fx-0160).

## entry: reports.contact-reports
- name: Contact Reports
- named-by-us: no
- description: Standard reports over contacts: Contacts Over Time
  (contact roster with immigration-specific optional columns), VMAX
  Report, Expiry Dates Report (current status, I-94, visa, advance
  parole, and/or EAD expirations), and Form Invitations Report
  (Smart Form invitations sent to clients and their status)
  (fx-0162, fx-0169).
- criterion: User creates a Report and selects the contacts category
  -> contacts-over-time, VMAX, expiry-dates, and form-invitations
  reports are available
- sources: fx-0159, fx-0162, fx-0169
- tier: provisional
- detail: Contacts Over Time optional columns include Alien
  Registration Number, citizenship fields, EAD, EOIR, SEVIS, ITIN,
  passport and travel-document numbers, US status with start and
  expiry dates, marital and biographic fields; filters cover date
  created, assignees, person vs company, and attribute filters such
  as date of birth or US status (fx-0162). Expiry Dates rows order
  by most recent expiration with expiry-type, date-range, and
  assignee filters (fx-0162). Form Invitations rows order by most
  recent invitation with status and date-created filters (fx-0162).

## entry: reports.lead-reports
- name: Lead Reports
- named-by-us: no
- description: Standard reports over leads: Leads Over Time, Lead
  Conversions Over Time, and Leads By Status (fx-0164, fx-0169).
- criterion: User creates a Report and selects the Leads category ->
  leads-over-time, lead-conversions-over-time, and leads-by-status
  reports are available
- sources: fx-0159, fx-0164, fx-0169, fx-0235, fx-0236
- tier: confirmed
- detail: Promoted provisional -> confirmed at module 17: the CRM
  help article attests reports on lead conversions over time and
  other lead metrics (fx-0235) and marketing attests Lead Reports
  sortable by status, conversion rate, and creation date (fx-0236).
  Columns: full name, phone, email, status, last outreach,
  plus updated; filters: date created and lead status (fx-0164).
  The overview article carries a note, placed under Leads By Status,
  that the report is available only to Pro and Advanced subscribers
  (fx-0169).

## entry: reports.matter-reports
- name: Matter Reports
- named-by-us: no
- description: Standard reports over matters: Matters Over Time,
  Matters By Type, Matters By Status, and Matters By Preference
  Category (fx-0163, fx-0169). The official Matter Workflows webinar
  covers reporting with matter workflows (fx-0158). The
  visa-bulletin blog post attests Matters by Preference Category on
  the release-notes family, organizing every case with a current
  priority date by preference category (fx-0270).
- criterion: User creates a Report and selects the Matter category
  -> matters-over-time, by-type, by-status, and
  by-preference-category reports are available
- sources: fx-0158, fx-0159, fx-0163, fx-0169, fx-0270
- tier: confirmed
- detail: Columns: title, client, description, updated, priority
  date status, assignees, type, and status, plus applicant,
  preference category, and priority date; filters: matter types,
  matter statuses, active or archived, assignees, date created, and
  late status, with attribute filters available only to Pro and
  Advanced subscribers (fx-0163).

## entry: reports.invoice-reports
- name: Invoice Reports
- named-by-us: no
- description: Standard reports over invoices: Invoices Over Time,
  Invoices Over Time (Payment Plans), Invoices By Client, Invoices
  By Matter, Due Invoices By Client, Due Invoices By Matter, and
  Invoice Charges Over Time (fx-0167, fx-0169).
- criterion: User creates a Report and selects the Invoice category
  -> the seven invoice report types are available
- sources: fx-0159, fx-0167, fx-0169, fx-0277
- tier: confirmed
- detail: The Q3 2022 features-roundup video names Reporting on
  Payment Plans as a release (fx-0277, chapter at 17:05) -- the
  payment-plan fields of this category. fx-0167 documents the full Invoices Over Time column
  dictionary -- bill vs trust-request type, totals and balances,
  discounts, invoice number, reminder fields, paid/unpaid status,
  trust level and trust-request amount, payment-plan status,
  frequency, and installment amount, and overdue-balance semantics
  under active vs inactive payment plans -- and its filters (payment
  status, invoice type, date created, date paid, due date, late
  status, payment-plan status); the by-client, by-matter, and due
  variants reuse these columns and filters with their own grouping
  (fx-0167). The payment-plans variant shows only invoices created
  after 09/09/2022 (fx-0167). Invoice Charges Over Time lists
  Service/Expense charges with description, amount, invoice number,
  client, and date created (fx-0167).

## entry: reports.payment-reports
- name: Payment Reports
- named-by-us: no
- description: Standard reports over invoice payments: Payments Over
  Time, Payments By Client, and Payments By Matter (fx-0161,
  fx-0169).
- criterion: User creates a Report and selects the payment category
  -> payments-over-time, by-client, and by-matter reports are
  available
- sources: fx-0159, fx-0161, fx-0169
- tier: provisional
- detail: Columns: client, payment type, invoice type, matter, date
  created, amount, plus updated; filters: payment type, invoice
  type, date created (fx-0161). Source discrepancy recorded: the
  overview lists Payment Reports as its own category (fx-0169),
  while the payment article's creation steps route through the
  Invoice category (fx-0161); both readings kept.

## entry: reports.task-reports
- name: Task Reports
- named-by-us: no
- description: Standard reports over tasks: Tasks By Client, Tasks
  By Matter, Late Tasks By Client, and Late Tasks By Matter
  (fx-0165, fx-0169).
- criterion: User creates a Report and selects the Task category ->
  tasks-by-client, tasks-by-matter, late-tasks-by-client, and
  late-tasks-by-matter reports are available
- sources: fx-0159, fx-0165, fx-0169
- tier: provisional
- detail: Columns: title, status, contact, matter, date created,
  due date, and assignees, plus complete and updated; filters: late
  status, assignees, date created, branch, and completed status
  (fx-0165).

## entry: reports.user-reports
- name: User Reports
- named-by-us: no
- description: Standard reports grouped by firm user: Invoices By
  User, Payments By User, Late Tasks By User, and Matters By User
  (fx-0166, fx-0169).
- criterion: User creates a Report and selects the User Reports
  category -> invoices, payments, late tasks, and matters grouped
  by user are available
- sources: fx-0159, fx-0166, fx-0169
- tier: provisional
- detail: Each report reuses the corresponding category's columns
  and filters, grouped by user; Matters By User adds optional matter
  columns (approval, case deadline, colors, court case date,
  retainer and case open/close dates, date of hire, funding source,
  grant type, internal file number, judge's name) (fx-0166).

## entry: reports.vmax-tracking
- name: VMAX Tracking
- named-by-us: no
- description: A VMAX date field on the contact overview records the
  last date a client can remain in their immigration status absent
  further extensions; the VMAX Report then orders clients by time
  remaining in nonimmigrant status, supporting export of impending
  expirations (fx-0168, fx-0162).
- criterion: User sets a contact's VMAX date and runs the VMAX
  Report -> the contact appears ordered by time remaining in status
- sources: fx-0162, fx-0168
- tier: provisional
- detail: VMAX report columns: contact, email, principal applicant,
  VMAX time remaining, and VMAX date; filter: date range (fx-0162).
  The VMAX date field lives on the contact Overview tab, under the
  Immigration subtab or via field search (fx-0168). Help gives the
  H-1B six-year limit and conditional-permanent-resident second
  year as worked examples (fx-0168).

## entry: reports.report-filters
- name: Applying Filters to Reports
- named-by-us: no
- description: Every standard report accepts filters, applied by
  selecting them and clicking the Update button; the available
  filters vary by the report being run (fx-0169, fx-0161, fx-0163).
- criterion: User selects filters on a report and clicks Update ->
  the report re-runs restricted to the filtered data
- sources: fx-0161, fx-0163, fx-0169
- tier: provisional
- detail: Custom Attributes, where set up, are usable as filters in
  Contact and Matter Reports; Matter Types and Statuses are usable
  as filters within Matter Reports (fx-0169). Attribute filters on
  Matter Reports are gated to Pro/Advanced subscribers (fx-0163).

## entry: reports.report-custom-columns
- name: Adding Custom Columns
- named-by-us: no
- description: Standard reports expose column customization via the
  gear icon: add columns from Available Columns, remove from
  Selected Columns, and drag-and-drop reorder, then save (fx-0169;
  the mechanics are repeated per category article, e.g. fx-0162,
  fx-0164, fx-0166).
- criterion: User clicks the gear icon on a customizable report,
  adjusts the Available and Selected Columns, and saves -> the
  report displays the chosen columns in the chosen order
- sources: fx-0162, fx-0164, fx-0166, fx-0169
- tier: provisional
- detail: Intra-family discrepancies recorded, both readings kept:
  the overview's customizable list is Contact (except VMAX and
  Expiry Dates), Matter, Invoice, Payment, Task, and User Reports
  (fx-0169), while the contact article limits custom columns to
  Contacts Over Time only (fx-0162), and the overview's list omits
  Lead Reports even though the lead article documents column
  editing (fx-0164).

## entry: reports.report-csv-export
- name: Exporting a Report to a CSV File
- named-by-us: no
- description: A created standard report is exported to a CSV file
  via the Export button, which downloads the report (fx-0169; the
  export is documented per category, e.g. fx-0161, fx-0163).
- criterion: User clicks Export on a created report -> the report
  downloads as a CSV file
- sources: fx-0161, fx-0163, fx-0169
- tier: provisional
- detail: Distinct from the Contacts and Matters dashboard CSV
  export, which is its own capability
  (contacts-and-matters.csv-export, fx-0090), and from the custom
  report download button (reports.custom-report-export, fx-0160).
