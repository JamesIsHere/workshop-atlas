# module: firm-settings

Docketwise's own vocabulary (help-center category "Firm Settings",
23 articles, fx-0003). Phase 3 module: full extraction from 23 help
articles (fx-0085..fx-0107), collection page fx-0084, and marketing
pages fx-0108 (pricing) and fx-0109 (security). One article
(Invitation Settings, fx-0096) duplicates the Smart Forms pilot
article fx-0039; its content lives in smart-forms.invitation-settings
(source added in-place, [G1] ruling 1). fx-0101 embeds four official
feature videos for Pro-gated capabilities (Leads CRM, bulk
messaging, QuickBooks, HR portal) -- material for those modules'
extractions, noted in the worklog.

## entry: firm-settings.two-factor-authentication
- name: Two-Factor Authentication (2FA)
- named-by-us: no
- description: Account logins are protected by two-factor
  authentication with a choice of three OTP delivery methods:
  authenticator app (QR-code setup), text message (US mobile numbers
  only), or email (fx-0087). 2FA is mandatory once the trial period
  ends, and new users must set it up at first login (fx-0087).
  Marketing attests two-factor authentication is available on all
  pricing plans (fx-0109).
- criterion: User with 2FA enabled logs in -> an OTP code from the
  chosen method (app, SMS, or email) is required to complete login
- sources: fx-0087, fx-0109, fx-0226, fx-0228
- tier: confirmed
- detail: Configured under Settings > Two-Factor Authentication;
  the method can be switched later via Update 2FA (fx-0087). An
  admin can reset a user's 2FA from Settings > User Access > Reset
  2FA, after which the user re-enrolls at next login (fx-0087).
  The Personal Settings MFA article attests MFA is mandatory for
  all accounts and cannot be disabled (fx-0226). The login guide
  corroborates the three delivery methods at first login and adds
  Remember this device for 30 days: MFA repeats only every 30 days
  per device, and a new or different device re-verifies; the option
  can be skipped for MFA on every login (fx-0228).

## entry: firm-settings.trash-can
- name: Trash Can
- named-by-us: no
- description: Deleted records are reviewable and restorable from a
  Trash view on each record type's dashboard; supported types are
  Contacts, Matters, Forms, Tasks, Notes, Invoices, Messages, and
  Files (fx-0088).
- criterion: User opens a dashboard's Trash view and clicks Restore
  on a deleted record -> the record returns to its dashboard
- sources: fx-0088
- tier: provisional

## entry: firm-settings.results-per-page
- name: Results Per Page in Dashboards and Reports
- named-by-us: no
- description: Users choose how many results display per page (10,
  25, or 50) on dashboards and reports via the View control; the
  preference is saved as a browser cookie per user and does not
  affect other users (fx-0089).
- criterion: User selects a results-per-page value in the View
  control -> the dashboard or report displays that many rows per
  page
- sources: fx-0089
- tier: provisional
- detail: Available on the Forms, Matters, Contacts, Tasks, Notes,
  Files, and Invoices dashboards and on the Contact, VMAX, Expiry
  Dates, Form Invitations, Lead, Matter, Invoice, and Payment
  report families (fx-0089).

## entry: firm-settings.universal-search
- name: Universal Search Bar
- named-by-us: no
- description: A universal search bar searches Contacts, Matters,
  and Forms by partial name and jumps to the selected record's
  overview page or Smart Form; a Recents button lists the most
  recently accessed contacts and matters (fx-0090).
- criterion: User types part of a contact, matter, or form name in
  the universal search bar -> matching records appear and selecting
  one opens its page
- sources: fx-0090, fx-0212
- tier: provisional
- detail: Also searches by USCIS receipt number (full or partial):
  matches surface both the matter carrying the receipt and that
  matter's primary contact, from the universal bar and from the
  contact/matter index search bars (fx-0212) (case-tracking module
  join, 2026-07-31).

## entry: firm-settings.firm-logo
- name: Uploading your Firm's Logo
- named-by-us: no
- description: Firms upload their logo under Settings > Logo
  (drag-and-drop, repositionable and scalable in the crop area);
  the logo then appears on client email notifications, invoices,
  and the firm's dashboard (fx-0091, fx-0076).
- criterion: Firm uploads a logo under Settings > Logo -> the logo
  appears on client-facing emails, invoices, and the dashboard
- sources: fx-0076, fx-0091
- tier: provisional
- detail: Recommended roughly 5:1 width-to-height, PNG or JPEG; an
  existing logo must be removed (Remove Logo) before uploading a
  replacement (fx-0091).

## entry: firm-settings.custom-dashboard
- name: Custom Dashboard
- named-by-us: no
- description: The dashboard is customizable per user: information
  boxes are shown or hidden via the Edit Dashboard menu and
  reordered by drag-and-drop (fx-0092).
- criterion: User checks or unchecks an information box under Edit
  Dashboard -> the box is shown or hidden on their dashboard
- sources: fx-0092
- tier: provisional
- detail: Available boxes: Contacts, Matters, Forms (5 most
  recently updated, assigned to the user), Events (5 upcoming),
  Tasks (5 by due date), Billing (paid/unpaid invoice totals and
  trust balance; owner/admin only), Notes (5 most recent), Form
  Invitations (6 most recently sent), and Firm Feed (20 most
  recent items; cannot be hidden or moved) (fx-0092).

## entry: firm-settings.custom-columns
- name: Custom Columns
- named-by-us: no
- description: Users add, remove, and reorder the columns of
  dashboards and reports via the gear icon; the customized column
  view is unique to each user (fx-0093).
- criterion: User edits columns via the gear icon and saves -> the
  dashboard or report displays the chosen columns in the chosen
  order for that user
- sources: fx-0093
- tier: provisional
- detail: Customizable dashboards: Forms, Matters, Contacts
  (including custom attributes), Invoices. Customizable reports:
  Contact (except VMAX and Expiry Date), Matter, Invoice, Payment,
  Task, and User reports (fx-0093).

## entry: firm-settings.subscription-tiers
- name: Subscription Tiers (Basic, Pro, Advanced)
- named-by-us: no
- description: The product is sold in three per-user subscription
  tiers -- Basic, Pro, and Advanced -- with feature gating: Pro
  unlocks Leads CRM, bulk emails and texts, QuickBooks integration,
  HR Portal, custom attributes, API access, and e-filing (ETA-9141,
  DS-160, DS-260, I-130, I-765, N-400); Advanced adds firm
  branches, user permission groups, multiple admins, enhanced file
  size limits (up to 5 GB), priority support, and tailored account
  setup (fx-0094, fx-0101). The public pricing page lists the same
  gating with per-user monthly/annual prices (fx-0108).
- criterion: Firm upgrades its subscription tier -> the tier's
  gated features become available on the account
- sources: fx-0094, fx-0101, fx-0106, fx-0108
- tier: confirmed
- detail: Pricing at capture: Basic 69, Pro 99, Advanced 119 USD
  per user per month billed yearly (79/109/129 monthly); Basic
  includes Smart Forms, case management, multilingual intakes,
  case and priority date tracking, client portal, document
  requests, calendaring, time tracking, unlimited cloud storage
  (fx-0108). Annual plans add free data migration and escalated
  feature requests (fx-0108). All users on an account share one
  subscription level (fx-0106).

## entry: firm-settings.subscription-management
- name: Managing Your Subscription
- named-by-us: no
- description: Admins manage the firm's subscription from Settings
  > Subscription: subscription level (Basic/Pro/Advanced), billing
  frequency (monthly or annual), and the number of user licenses
  (fx-0106). The pricing page attests the monthly/annual per-user
  structure publicly (fx-0108).
- criterion: Admin changes subscription level, billing frequency,
  or license count under Settings > Subscription and saves -> the
  subscription reflects the change
- sources: fx-0086, fx-0099, fx-0105, fx-0106, fx-0108, fx-0233
- tier: confirmed
- detail: All users on the account share one subscription level;
  levels cannot be differentiated per user (fx-0233). Annual
  billing saves roughly 15 percent (fx-0106).
  License count cannot drop below the number of active plus
  deactivated users (fx-0106); adding a user beyond the licensed
  count auto-adds a license (fx-0106, fx-0107). License reductions
  take effect at the next billing cycle, with no mid-term refunds
  (fx-0086). The vendor payment card is managed via profile icon >
  Payment Details (fx-0105). Cancellation is admin/owner-only via
  Settings > Subscription > Cancel Account plus a cancellation
  survey; paid invoices are non-refundable per terms (fx-0099).

## entry: firm-settings.user-permission-groups
- name: User Permission Groups
- named-by-us: no
- description: User Groups restrict access to specific contacts and
  matters: a contact or matter set to Private is viewable only by
  members of its designated group(s), while admins see everything
  (fx-0095). Groups can also carry accounting-note permission
  (fx-0095). Advanced-subscription feature (fx-0095, fx-0108,
  fx-0109).
- criterion: Admin sets a contact or matter to Private with a
  designated user group -> only members of that group and account
  admins can view it
- sources: fx-0095, fx-0108, fx-0109
- tier: confirmed
- detail: Groups are created under Settings > User Groups with a
  name and member list (fx-0095). Contacts and matters default to
  public; a contact's permission settings cascade to its matters
  and take precedence over matter-level settings (fx-0095).

## entry: firm-settings.accounting-notes
- name: Accounting Notes
- named-by-us: no
- description: Invoices can carry an accounting note, created,
  edited, and viewed via the invoice index's More Actions >
  View/Edit Accounting Note; access requires membership in a user
  group with the accounting-notes permission enabled (fx-0095).
- criterion: User in a group with accounting-note permission opens
  View/Edit Accounting Note on an invoice -> the note can be
  created, edited, and viewed
- sources: fx-0095, fx-0276
- tier: confirmed
- detail: An Accounting Note column on the invoice index shows
  which invoices carry notes (fx-0095). Named as a release in the
  Q4 2022 features-roundup video (fx-0276, chapter at 21:45).

## entry: firm-settings.firm-branches
- name: Firm Branches
- named-by-us: no
- description: Firm members are grouped by branch location:
  branches are defined under Settings > Branches and each member's
  branch is assigned in Settings > User Access; branch is then
  available as a report filter (fx-0098, fx-0107).
  Advanced-subscription feature ("Multiple Branches", fx-0108).
- criterion: Admin assigns firm members to branches -> supported
  reports can be filtered by branch
- sources: fx-0098, fx-0107, fx-0108
- tier: confirmed
- detail: Branch filtering is attested for Matter reports (over
  time, by type, by status, by preference category), Task reports
  (by client, by matter, late by client, late by matter), and User
  reports (late tasks by user, matters by user) (fx-0098). The
  account owner cannot be assigned to a branch (fx-0107).

## entry: firm-settings.data-security
- name: Docketwise Data Security
- named-by-us: no
- description: Client data is hosted on AWS with encryption in
  transit (all traffic over https) and at rest (AES-256), sensitive
  information irreversibly hashed, access control lists and
  permission checks, and SOC 1, 2, and 3 certified infrastructure
  (fx-0097, fx-0109). Backups run continuously (snapshots roughly
  every 5 minutes) with multi-availability-zone failover (fx-0109).
- criterion: User stores client data in the product -> the data is
  encrypted in transit and at rest on AWS infrastructure with
  continuous encrypted backups
- sources: fx-0097, fx-0109
- tier: confirmed
- detail: Marketing further attests third-party penetration
  scanning, employee SSO/2FA requirements, and an incident-response
  protocol (fx-0109); these are organizational practices, not
  in-product behaviors.

## entry: firm-settings.time-zone-setting
- name: Changing Time Zone
- named-by-us: no
- description: Each user sets an Events time zone from Settings >
  Personal Information via a drop-down; saving updates the
  account's time zone for events (fx-0103).
- criterion: User selects a time zone under Settings > Personal
  Information > Events time zone and saves -> the account's events
  use the selected time zone
- sources: fx-0103
- tier: provisional

## entry: firm-settings.notification-settings
- name: Notification Settings
- named-by-us: no
- description: Firms choose who receives email notifications: the
  firm's admin, the assignee of the particular matter, or all staff
  members; the setting applies firm-wide (fx-0104).
- criterion: Admin sets email notifications to route to admin,
  assignee, or all staff -> subsequent email notifications go to
  the selected parties
- sources: fx-0104
- tier: provisional

## entry: firm-settings.managing-users
- name: Managing Users
- named-by-us: no
- description: Account owners/admins manage users from Settings >
  User Access: adding firm members (email and name), deactivating
  and reactivating, deleting, and editing a user's name and email
  (fx-0107). Deactivation blocks login but retains the user's logs
  and data and keeps their license in use; deletion permanently
  removes the user and frees the license (fx-0107, fx-0086).
- criterion: Admin deactivates a user under Settings > User Access
  -> the user can no longer log in while their data and logs remain
  accessible
- sources: fx-0086, fx-0102, fx-0106, fx-0107, fx-0233
- tier: provisional
- detail: Adding a user beyond the licensed count auto-adds a
  license (fx-0107). On deletion, the user's firm-feed logs are
  removed and their assignments are cleared, except values retained
  in Matters (assignee values/filters), Notes (creator, assignee),
  and Events (staff calendar, attendees) (fx-0107). A member's
  name, email, and password are also self-served under Settings >
  Personal Information; admin-side password change works by
  re-pointing the email and using the login page reset (fx-0102,
  fx-0107). Replacing a deactivated user with a new one on the same
  license carries no additional cost (fx-0086).

## entry: firm-settings.user-permissions
- name: User Permissions
- named-by-us: no
- description: Each user carries a permission profile set in
  Settings > User Access: global permissions (delete, export,
  archive, and reassign firm records) plus per-record-type access
  levels for Invoices, Notes, Financial Data, Forms, Contacts,
  Matters, Tasks, Files, Messages, Events, and Leads
  (viewing/creating/editing/deleting) (fx-0107). Marketing attests
  user-level permission configuration by admins (fx-0109).
- criterion: Admin edits a user's permissions and saves -> the
  user's access to each record type reflects the specified levels
- sources: fx-0107, fx-0109
- tier: confirmed
- detail: A firm-wide toggle governs non-admin access to Firm
  Settings: checked (default) grants access to all options except
  Subscription, Beta Access, and User Groups; unchecked removes
  access entirely (fx-0107). Advanced subscribers can designate
  additional account admins with owner-equivalent abilities
  (fx-0107, fx-0095, fx-0108).
