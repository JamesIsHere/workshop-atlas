# module: contacts-and-matters

Docketwise's own vocabulary (help-center category "Contacts and
Matters", 14 articles, fx-0003). Phase 3 module: full extraction
from 14 help articles (fx-0143..fx-0156), collection page fx-0142,
marketing case-management page fx-0157, and the embedded official
webinar "Matter Workflows" (fx-0158, found by the embed-grep
route). Closes two module-boundary deferrals logged by earlier
modules (dashboard CSV export and overview-page related-contact
linking, both from fx-0090's navigation article).

## entry: contacts-and-matters.contact-creation
- name: Creating a Contact
- named-by-us: no
- description: Contacts are created from the Create New button as
  either a person or a company; after entering the name the
  contact opens on its overview page, where all further fields are
  edited via per-field pencil icons or field search (fx-0149).
- criterion: User clicks Create New, selects Contact, chooses
  person or company, and enters the name -> the contact is created
  and opens on its overview page for editing
- sources: fx-0142, fx-0149
- tier: provisional

## entry: contacts-and-matters.matter-creation
- name: Creating a Matter
- named-by-us: no
- description: Matters are created from the Create New button with
  a required associated contact and matter name, plus optional
  description, matter type/status, preference category and
  priority date, and a firm-member assignee (with an option to
  auto-assign all related tasks to them) (fx-0148).
- criterion: User clicks Create New, selects Matter, and assigns a
  contact and matter name -> the matter is created with the
  entered details
- sources: fx-0142, fx-0148
- tier: provisional

## entry: contacts-and-matters.matter-types-statuses
- name: Workflows with Matter Types and Statuses
- named-by-us: no
- description: Firms define Matter Workflows: named Matter Types
  (recommended one per application/petition type) each carrying an
  ordered sequence of Matter Statuses, with optional per-status
  durations (fx-0152). A matter is assigned a type and status at
  creation or later; its overview page shows a workflow progress
  bar, green while within the status duration and red when late,
  and statuses are updated by clicking the bar (fx-0152). The
  official Matter Workflows webinar covers creation, assignment,
  tracking, and reporting (fx-0158).
- criterion: User assigns a matter type and status to a matter ->
  the matter displays its workflow progress bar and is filterable
  by type, status, and late status
- sources: fx-0146, fx-0148, fx-0152, fx-0158
- tier: confirmed
- detail: Statuses can be created per type, imported one-by-one, or
  imported wholesale from an existing workflow; types and statuses
  are editable, reorderable by drag-and-drop, and deletable
  (fx-0152). A status name shared across types renames/deletes
  globally, while durations and automations stay per-type
  (fx-0152). Matters Dashboard and Matter Reports filter by type,
  status, and late status (fx-0146, fx-0152). The open/pending/
  closed convention is a recommended workflow pattern built from
  these primitives (fx-0146).

## entry: contacts-and-matters.matter-status-automations
- name: Matter Workflow Automations
- named-by-us: no
- description: A Matter Status can carry automations that fire
  when a matter enters the status: import an existing Task List,
  send a message from a Message Template to the matter's primary
  contact (optionally CCing the applicant), and advance to the
  next status automatically once all tasks are complete (fx-0152).
  Marketing attests task standardization, notifications, and
  reusable-template follow-ups (fx-0157); the Matter Workflows
  webinar covers automations (fx-0158).
- criterion: Matter enters a status carrying automations -> the
  configured task list is added and/or the templated message is
  sent without manual action
- sources: fx-0152, fx-0157, fx-0158, fx-0213
- tier: confirmed
- detail: Automated tasks can additionally be auto-shared to the
  client's portal (fx-0152). Imported statuses can carry their
  automations along (fx-0152). When task lists fire from matter
  workflows, both the tasks' default durations and default
  assignees are applied (fx-0213) (case-tracking module join,
  2026-07-31).

## entry: contacts-and-matters.expiry-date-reminders
- name: Expiry Date Reminders
- named-by-us: no
- description: Automatic calendaring and notification reminders
  for clients' expiry dates: per expiry-date type the firm sets
  the event calendar, the lead time before expiry, and the
  recipients (admin, all firm members, or assignees of the
  associated contact); entering a date on a contact's Expiration
  Dates tab then auto-creates the event and its reminder
  (fx-0147).
- criterion: User enters an expiry date on a contact's Expiration
  Dates tab with a reminder setting configured -> an event and
  notification reminder are created automatically
- sources: fx-0144, fx-0147, fx-0269, fx-0277
- tier: confirmed
- detail: Built-in types: US Status, Non-Immigrant Visa, Advanced
  Parole, Current Authorized Stay, Employment Authorization
  Document, Petition Expiration, Passport or Travel Document, LCA
  Expiration; Custom Expiry Dates extend the list via Custom
  Attributes, contact-level only (fx-0147, fx-0144). Multiple
  reminders per type are supported; the client can be added as an
  event attendee to receive the reminder too (fx-0147). The
  I-9/E-Verify blog post attests the capability on the
  release-notes family: alerts and notifications for expiring
  documents and approaching deadlines (fx-0269). Custom Expiry
  Dates named as a release in the Q3 2022 features-roundup video
  (fx-0277, chapter at 13:58).

## entry: contacts-and-matters.custom-attributes
- name: Custom Attributes
- named-by-us: no
- description: Firms create custom fields for contacts and matters
  in six types -- text, number, date, boolean, list, and expiry
  date (fx-0144). Values are tracked and filled on overview pages,
  asked in Custom Intakes, merged into Automated Templates via
  merge tags, and used as report columns and filters (fx-0144).
  Pro/Advanced-gated; listed on the public pricing page under Pro
  (fx-0108, fx-0101).
- criterion: Admin creates a custom attribute for contacts or
  matters -> the field is fillable on overview pages and available
  in custom intakes, automated templates, and reports
- sources: fx-0101, fx-0108, fx-0144, fx-0238
- tier: confirmed
- detail: The official "Custom Attributes" video (fx-0238,
  j6KonbWdl6I, 2021-06-22) attests the capability -- captured to
  settle the fx-0101 embed-debt list, whose identity guess
  (presumed Leads CRM) was wrong. Created under Settings > Custom
  Attributes with a name,
  type, and contact/matter assignment (fx-0144). Custom expiry
  dates behave like built-in expiry dates including reminders
  (fx-0144). Reportable in contact reports (contacts over time)
  and matter reports (over time, by status, by preference
  category) via Filter by Attributes (fx-0144). A matter custom
  attribute asked in a custom intake requires the smart form to be
  assigned to a matter to populate (fx-0144).

## entry: contacts-and-matters.related-contacts
- name: Indicating Related Contacts
- named-by-us: no
- description: Relations between contacts are recorded from a
  contact's Related Contacts tab (for people: family members,
  employer, school; for companies: employees via an Employees
  tab), by creating a new contact or importing an existing one;
  the relation is automatically reflected on the related contact
  and related contacts are included in forms (fx-0145).
- criterion: User links a related contact with a relation type ->
  the relation appears on both contacts and is available to forms
- sources: fx-0145
- tier: provisional

## entry: contacts-and-matters.matter-linked-contacts
- name: Linking Multiple Contacts to a Matter
- named-by-us: no
- description: A matter has one primary client, but additional
  related contacts (beneficiaries, employers, family members) can
  be linked from the matter's Overview tab via Link Contact, with
  an optional description or relationship title, so all associated
  individuals are visible on the matter (fx-0154).
- criterion: User links an additional contact to a matter -> the
  contact appears in the matter's Related Contacts section with
  its relationship title
- sources: fx-0154
- tier: provisional

## entry: contacts-and-matters.contact-archiving
- name: Archiving Contacts
- named-by-us: no
- description: Contacts are archived (and un-archived) from the
  Contacts dashboard by selecting them and using Bulk Actions >
  Archive the Contact(s); archived contacts live in a separate
  Archived Contacts view reached from the Primary Contacts
  selector (fx-0143).
- criterion: User archives selected contacts via Bulk Actions ->
  the contacts leave the primary view and appear under Archived
  Contacts
- sources: fx-0142, fx-0143
- tier: provisional

## entry: contacts-and-matters.matter-archiving
- name: Archiving Matters
- named-by-us: no
- description: Matters are archived (and un-archived) from the
  Matters dashboard by selecting them and using Bulk Actions >
  Archive the Matter(s); archived matters are viewed by switching
  the Status selector from Active to Archived (fx-0151).
- criterion: User archives selected matters via Bulk Actions ->
  the matters leave the active view and appear under the Archived
  status view
- sources: fx-0142, fx-0151
- tier: provisional

## entry: contacts-and-matters.contact-search
- name: Searching Contacts
- named-by-us: no
- description: Contacts are searchable by name, email, phone
  number, Alien Registration Number (A#), and unique identifier,
  either from the universal search bar or within the Contacts
  dashboard search (fx-0150).
- criterion: User searches by name, email, phone, A-Number, or
  unique identifier -> matching contacts are returned
- sources: fx-0150
- tier: provisional

## entry: contacts-and-matters.csv-export
- name: Export Contacts and Matters
- named-by-us: no
- description: The full contact list and matter list export to CSV
  files via an Export button on the respective dashboards, for
  local backup or offline use (fx-0155, fx-0090).
- criterion: User clicks Export on the Contacts or Matters
  dashboard -> a CSV file of all records downloads
- sources: fx-0090, fx-0155
- tier: provisional
- detail: The article's matter-export steps repeat the label
  "Export Contacts button" under the Matters tab -- an apparent
  doc copy-paste; the matter dashboard's own export control is
  attested by fx-0090 (fx-0155).

## entry: contacts-and-matters.contact-merging
- name: Merging Duplicate Contacts
- named-by-us: no
- description: Duplicate contacts are resolved by selecting the
  duplicates on the Contacts index and choosing Bulk Actions >
  Merge Contacts; the merged contact keeps the most recently
  updated data from each selected contact (fx-0156).
- criterion: User selects duplicate contacts and chooses Merge
  Contacts -> a single contact remains carrying the most recently
  updated data from the duplicates
- sources: fx-0142, fx-0156
- tier: provisional

## entry: contacts-and-matters.activity-feeds
- name: Firm, Contact, and Matter Feeds
- named-by-us: no
- description: A live activity feed tracks creations and updates
  of forms, tasks, invoices, notes, messages, contacts, matters,
  and events, at three scopes: a Firm Feed (searchable by firm
  member, client, matter, resource content, or resource type) and
  per-contact and per-matter feeds reached from the overview
  pages' More menu, filterable by category (fx-0153).
- criterion: User opens the Firm Feed -> creations and updates of
  firm resources are listed and searchable
- sources: fx-0092, fx-0153
- tier: provisional
- detail: The dashboard's Firm Feed information box shows the 20
  most recent items and cannot be hidden or moved (fx-0092).
