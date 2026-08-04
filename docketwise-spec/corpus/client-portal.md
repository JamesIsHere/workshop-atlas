# module: client-portal

Docketwise's own vocabulary (help-center category "Client Portal", 6
articles, fx-0003). Phase 3 fan-out module: full extraction from 6
help articles (fx-0186..fx-0191), collection page fx-0185, and the
official "Human Resources Portal" video (fx-0192) found by embed-grep
in the HR Portal article. Two portal types share one surface: the
Standard (client) portal at client.docketwise.com and the HR Portal
for corporate clients (Pro/Advanced gated). Firm-side mechanics
(activation, sharing, settings) and client-side capabilities (tasks,
questionnaires, USCIS tracking, invoices, files, messaging) are
carved separately. Portal invoice payment lives in
invoicing-and-trust-accounting.online-card-payment; portal messaging
lives in client-communication.secure-portal-messaging; HR portal
reports live in reports.hr-portal-reports -- this module's captures
joined those entries in place rather than duplicating them.

## entry: client-portal.module-exists
- name: Client Portal
- named-by-us: no
- description: The product carries a secure client portal with a
  dedicated 6-article help category (fx-0003, fx-0185): a central
  place for a firm's client to communicate with the firm, complete
  tasks, complete electronic questionnaires, check USCIS receipt
  tracking status, view and pay invoices, and upload and download
  files (fx-0186), reached at client.docketwise.com (fx-0186,
  fx-0191). Decomposed into this file's entries in Phase 3. The
  marketing features index attests the module: invite clients to
  their own portal, where they can access questionnaires, complete
  tasks, pay invoices, and more (fx-0244). In an r/LawFirm thread
  asking which software provides client dashboards, a commenter
  names "Mycase and Docketwise" (fx-0252) -- reviews-family
  attestation that the product carries a client portal.
- criterion: Client with an activated portal logs in at
  client.docketwise.com -> a portal dashboard with the shared
  resources for that client is presented
- sources: fx-0185, fx-0186, fx-0191, fx-0244, fx-0252
- tier: confirmed
- detail: Two portal types exist on the same surface: Standard
  Portal for individual clients and HR Portal for corporate clients
  (fx-0188, fx-0191).

## entry: client-portal.portal-activation
- name: Setting Up the Client Portal
- named-by-us: no
- description: A firm user activates the portal from the contact's
  overview page: Portal tab, Allow Portal Access slider, enter the
  email address, select Standard Portal as the Portal Type, and
  Submit; the contact receives an invitation email (sent by
  no-reply@notifications.docketwise.com) asking them to set a
  password, after which they log in anytime at client.docketwise.com
  (fx-0191, fx-0186).
- criterion: User enables Allow Portal Access on a contact with an
  email address -> the contact receives a portal invitation, sets a
  password, and can log in to their portal
- sources: fx-0186, fx-0191
- tier: provisional
- detail: The same slider deactivates the portal, revoking access;
  invitations can be re-sent from the Portal tab; clients reset
  forgotten passwords from the login page via a reset email
  (fx-0191, fx-0186). A copy-paste HTML snippet linking
  client.docketwise.com/c/sign_in adds a portal login button to the
  firm's own website (fx-0191).

## entry: client-portal.portal-two-factor
- name: Client Portal Two-Factor Authentication
- named-by-us: no
- description: Two-factor authentication is enforced per portal by
  the firm: on the contact's Portal tab, an Enable 2FA button turns
  it on and a Disable 2FA button turns it off (fx-0191, fx-0188).
  With 2FA enforced, the client enrolls an authenticator app
  (Google Authenticator, Microsoft Authenticator, Authy, Duo, etc.)
  by scanning a QR code at first login and thereafter enters the
  OTP code as part of every login (fx-0186).
- criterion: User clicks Enable 2FA on a contact's portal -> the
  client must complete authenticator-app OTP entry to log in to
  their portal
- sources: fx-0186, fx-0188, fx-0191
- tier: provisional
- detail: Applies to both Standard and HR portals (fx-0191,
  fx-0188). Distinct from firm-user two-factor authentication
  (firm-settings.two-factor-authentication) -- this is client-side
  auth on the portal surface. A client without 2FA enabled must ask
  the firm to enable it (fx-0186).

## entry: client-portal.portal-dashboard
- name: Client Portal Dashboard
- named-by-us: no
- description: Logging in lands the client on the portal Dashboard:
  summary cards for Tasks, Forms, USCIS Receipts, Invoices, and
  Files each show a few items, with a See All option and a side
  navbar entry opening the exhaustive list for each resource
  (fx-0186).
- criterion: Client logs in to the portal -> a dashboard with
  summary cards for Tasks, Forms, USCIS Receipts, Invoices, and
  Files is shown, each expandable via See All
- sources: fx-0186
- tier: provisional

## entry: client-portal.portal-resource-sharing
- name: Sharing Resources to the Client Portal
- named-by-us: no
- description: Firm users share Tasks, Forms, USCIS Receipts,
  Invoices, and Files to a contact's portal from the resource's own
  tab on the contact or matter: check the item(s), Bulk Actions >
  Share to Portal (invoices use a per-row Actions icon; USCIS
  receipts a Share to Portal icon on the Case Tracking tab), select
  the contact's portal, Submit. The client is notified that a new
  resource was added and prompted to log in (fx-0191). Un-sharing
  removes the item via the trash-can icon in the same Share to
  Portal dialog (fx-0191).
- criterion: User selects a resource and applies Share to Portal ->
  the resource appears in the client's portal and the client is
  notified
- sources: fx-0186, fx-0188, fx-0191
- tier: provisional
- detail: File sharing carries folders with their full structure
  (main folder, files, subfolders), and shared folders become valid
  destinations for client uploads (fx-0191). The same mechanic
  serves HR portals with extra employee-association options
  (client-portal.hr-portal-resource-sharing).

## entry: client-portal.portal-task-completion
- name: Viewing and Completing Tasks
- named-by-us: no
- description: Shared tasks appear in the portal's Tasks card and
  Tasks navbar list; the client marks a task complete by clicking
  the checkbox beside it (fx-0186). The marketing features index
  attests clients complete tasks in the portal (fx-0244).
- criterion: Client clicks the checkbox beside a shared task in the
  portal -> the task is reflected as completed
- sources: fx-0186, fx-0191, fx-0213, fx-0244
- tier: confirmed
- detail: Task sharing requires the client's portal or HR portal to
  be activated first; once the client marks a shared task complete,
  the firm can see what remains pending (fx-0213) (case-tracking
  module join, 2026-07-31).

## entry: client-portal.portal-questionnaire-completion
- name: Completing Your Electronic Questionnaire
- named-by-us: no
- description: Forms and questionnaires shared to the portal appear
  in the Forms card and Forms navbar list; the client opens a
  questionnaire via the pencil icon beside it and completes it in
  the portal (fx-0186). The marketing features index attests
  clients access questionnaires in the portal (fx-0244).
- criterion: Client opens a shared questionnaire from the portal's
  Forms list -> the electronic questionnaire opens for completion
- sources: fx-0186, fx-0191, fx-0244
- tier: confirmed
- detail: The portal is one of Smart Forms' send channels
  (smart-forms.intake-invitations; portal-shared forms show status
  Shared to portal, fx-0039).

## entry: client-portal.portal-uscis-tracking-view
- name: Viewing USCIS Receipt Tracking Status
- named-by-us: no
- description: USCIS receipt tracking statuses shared to the portal
  appear in the USCIS Receipts card and Receipts navbar list; the
  client sees up-to-date USCIS case status inside the portal, and
  the status text links to the case status on the USCIS website
  (fx-0186).
- criterion: Client opens Receipts in the portal -> current USCIS
  case status information for shared receipts is displayed
- sources: fx-0186, fx-0191, fx-0212, fx-0214
- tier: confirmed
- detail: The tracking capability itself belongs to the Case
  Tracking category (help category, fx-0003); this entry is its
  portal surface. Sharing happens from the matter's Case Tracking
  tab: the firm clicks the Share icon beside the receipt number,
  confirms the client, and submits; the client needs an activated
  portal first (fx-0191, fx-0212). Marketing attests clients "can
  track their case anytime, from anywhere" through the portal
  without checking in with the firm (fx-0214) -- the cross-family
  attestation that lifted this entry to confirmed (case-tracking
  module join, 2026-07-31).

## entry: client-portal.portal-file-sharing
- name: Portal File and Folder Sharing
- named-by-us: yes
- description: Files and folders a firm shares to the portal appear
  in the client's Files card and Files navbar list; folders arrive
  with their full structure (fx-0191, fx-0190). The client
  downloads any file -- shared or self-uploaded -- by checking its
  box and using Bulk Actions > Download the File(s) (fx-0186).
- criterion: User shares files or folders to a contact's portal ->
  the client sees them in the portal's Files area with folder
  structure intact and can download them
- sources: fx-0186, fx-0190, fx-0191
- tier: provisional

## entry: client-portal.portal-client-file-upload
- name: Uploading Files to the Client Portal
- named-by-us: no
- description: The client uploads files from the portal's Files
  area: Upload Files button, choose or drag-and-drop files, Upload
  -- optionally after navigating into a shared folder to target it
  (fx-0190, fx-0186). Firm side, client uploads land under the
  contact's dashboard Files, where the firm can rename a file via
  the pencil icon or, via More Actions, change its associated
  matter or client, download it, or delete it (fx-0189).
- criterion: Client uploads a file via the portal's Files area ->
  the file appears under the contact's Files on the firm side
- sources: fx-0186, fx-0189, fx-0190, fx-0196
- tier: provisional
- detail: The client can relocate their own uploads with the move
  icon (single file) or Move Files (multiple), choosing a new
  folder destination in a modal (fx-0190, fx-0186). A mischosen
  file can be cleared before upload (fx-0190). Portal uploads
  accept any number of files up to 100 MB total per upload, and
  clients can rename files while uploading (fx-0196). Client
  uploads show the client's email address in the file's
  "uploaded by" field, distinguishing firm from client uploads
  (fx-0196).

## entry: client-portal.portal-auto-sharing
- name: Auto-Sharing to the Client Portal
- named-by-us: no
- description: Newly created resources can be shared to portals
  automatically. Firm-level: Settings > Portal Settings, check the
  resource types to auto-share on creation across all contacts,
  Save Changes. Individual-level: the contact's Portal tab carries
  the same per-resource checkboxes for that contact only (fx-0191,
  fx-0188).
- criterion: User enables auto-sharing for a resource type -> newly
  created resources of that type are shared to the portal without a
  manual share step
- sources: fx-0188, fx-0191
- tier: provisional
- detail: Available for both Standard and HR portals (fx-0191,
  fx-0188).

## entry: client-portal.portal-section-visibility
- name: Showing and Hiding Portal Sections
- named-by-us: no
- description: Sections of the portal can be hidden from clients.
  Firm-level: Settings > Portal Settings sets which sections are
  hidden on newly created portals across all contacts.
  Individual-level: unchecking section boxes on the contact's
  Portal tab hides those sections in that client's portal (fx-0191,
  fx-0188).
- criterion: User unchecks a section for a contact's portal -> that
  section is hidden from the client's portal view
- sources: fx-0188, fx-0191
- tier: provisional

## entry: client-portal.portal-preview
- name: Portal Preview
- named-by-us: yes
- description: A firm user views a contact's portal as the client
  would see it: contact overview page > Portal tab > Preview Portal
  button (fx-0191, fx-0188).
- criterion: User clicks Preview Portal on a contact's Portal tab
  -> the portal opens as the client would see it
- sources: fx-0188, fx-0191
- tier: provisional
- detail: In an HR portal preview, the firm user sees all
  Employees, Tasks, Forms, USCIS Receipts, Invoices, and Files, and
  can filter to a single employee's resources (fx-0188).

## entry: client-portal.hr-portal
- name: HR Portal
- named-by-us: no
- description: A portal type for corporate clients: the firm shares
  foreign national employees and their related resources (Tasks,
  Forms/Questionnaires, USCIS Receipts, Invoices, Files) plus
  employee matter statuses to the company's portal, organized by
  employee (fx-0188). The official Human Resources Portal video
  attests sharing employees with their forms, receipts, documents,
  and tasks (fx-0192). Set up from the contact's Portal tab by
  selecting HR Portal as the Portal Type (fx-0188).
- criterion: User activates a portal with HR Portal as the Portal
  Type on a corporate contact -> the company's portal presents
  shared employees and their resources organized by employee
- sources: fx-0185, fx-0187, fx-0188, fx-0192
- tier: confirmed
- detail: Pro or Advanced subscription required (fx-0188). An
  existing Standard portal converts to an HR Portal (and back) by
  switching the Portal Type on the Portal tab (fx-0188). The
  Employees index is searchable by name or email
  (client-portal.hr-portal-employee-management).

## entry: client-portal.hr-portal-employee-management
- name: HR Portal Employee Management
- named-by-us: yes
- description: A company contact's Employees tab records its
  employees, either by creating a new contact (first and last name
  required) or importing an existing contact (fx-0188). Recorded
  employees are added to the company's HR Portal via checkbox +
  Bulk Actions > Share to Portal, and removed the same way via the
  trash-can icon (fx-0188). The official video attests sharing
  foreign national employees to the client's portal (fx-0192).
- criterion: User shares recorded employees to the company's HR
  Portal -> those employees appear in the portal's Employees index
- sources: fx-0188, fx-0192
- tier: confirmed
- detail: Archived contacts are not shown in the HR portal even if
  shared (fx-0188). The portal's Employees index is searchable by
  first name, last name, or email address (fx-0188).

## entry: client-portal.hr-portal-resource-sharing
- name: HR Portal Resource Sharing
- named-by-us: yes
- description: Resources shared to an HR Portal use the standard
  Share to Portal mechanic with employee options: for Tasks, Forms,
  USCIS Receipts, and Files the dialog optionally associates the
  employee, optionally shares the same resource simultaneously to
  that employee's own Client Portal, and takes the employee's email
  address (fx-0188). The official video attests sharing employees'
  forms, receipts, documents, and tasks to the client's portal
  (fx-0192).
- criterion: User shares a resource to the HR Portal with the
  employee-portal option checked -> the resource appears in both
  the company's HR Portal and the employee's own Client Portal
- sources: fx-0188, fx-0192
- tier: confirmed
- detail: Invoice sharing to the HR Portal carries no employee
  options -- portal selection only (fx-0188). Clients are notified
  when a resource is shared (fx-0188).

## entry: client-portal.hr-portal-matter-status-visibility
- name: HR Portal Matter Status Visibility
- named-by-us: yes
- description: Employees' matter types and matter statuses are
  visible in the HR Portal so corporate clients can track case
  progress. A matter reflects in the portal when the corporate
  client is its Primary Contact, the employee is listed as
  Applicant, and the employee is shared to the HR Portal (fx-0188).
- criterion: User assigns the corporate client as Primary Contact
  and the shared employee as Applicant on a matter -> the matter's
  type and status are visible in the HR Portal
- sources: fx-0188
- tier: provisional
- detail: Status updates flow through the normal matter-status edit
  (contacts-and-matters.matter-types-statuses); the article walks
  the same Create Matter / Update Matter Details flows (fx-0188).

## entry: client-portal.hr-portal-additional-contacts
- name: HR Portal Additional Contacts
- named-by-us: yes
- description: Access to a company's HR Portal extends to
  additional points of contact: from the company's Portal tab,
  Invite More Contacts selects a contact and sends an email
  invitation the contact must accept; a Revoke Access option beside
  each additional contact withdraws it (fx-0188).
- criterion: User invites an additional contact from the company's
  Portal tab and the contact accepts -> that contact can log in to
  the company's HR Portal
- sources: fx-0188
- tier: provisional

## entry: client-portal.hr-portal-employee-creation
- name: Creating Contacts Via the HR Portal
- named-by-us: no
- description: Corporate clients create new foreign national
  employees from the HR Portal's Employees dashboard (first name,
  last name, and email required; phone and message optional); the
  created employee arrives in Docketwise as a lead, is
  automatically added as an employee of the corporate client, and
  is shared to the HR Portal (fx-0188). A firm-level Portal
  Settings checkbox (Allow HR Portal clients to create employees)
  allows or restricts the capability (fx-0188).
- criterion: HR Portal user creates an employee from the Employees
  dashboard -> a lead is created in Docketwise, listed as the
  company's employee and shared to the HR Portal
- sources: fx-0188
- tier: provisional
- detail: Settings > Notifications selects which firm users get the
  in-app notification when an employee is created via the HR portal
  (options include the client's assignees -- the assignees of the
  corporate contact); the lead lists the company that created it
  (fx-0188). Leads belong to the Leads CRM category (fx-0003).
