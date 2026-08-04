# rejection-log -- candidate entries considered during extraction and
# rejected, with reasons, counted per module. This keeps the Trial 3
# invisible-churn signal observable (goal.md, Iteration and recovery).

## module: smart-forms (Phase 2 pilot) -- 9 rejections

- getting-started-onboarding (fx-0040): webinars, live chat support,
  training booking, learning center. Support/training services, not
  Smart Forms product capabilities; any product-side pieces (in-app
  chat, client portal login) belong to other modules and will be
  extracted in fan-out from their own categories.
- i589-territory-address-workaround (fx-0014): the article documents
  a defect workaround (U.S. territory addresses fail to populate
  Form I-589 Item 8), not a capability a user gains. The underlying
  population logic is captured as detail on
  smart-forms.single-intake-autofill, which cites fx-0014.
- bulk-form-updates (fx-0002): marketing bullet "change it once,
  reflected on all forms" restates the single-intake sync mechanism
  rather than attesting a distinct feature; merged as detail on
  smart-forms.single-intake-autofill.
- g28-attachment-efiling (fx-0017): the G-28 sync steps (5-7) are
  inseparable from the principal-form USCIS e-filing flow -- the
  G-28 cannot be e-filed alone. Folded into
  smart-forms.uscis-efiling-sync description/detail.
- shrink-pdf-font (fx-0025): single-line print-settings option with
  no dedicated article; folded into smart-forms.form-download-print
  detail rather than carried as a one-source micro-entry.
- pre-made-intake-import (fx-0029): the pre-made custom intake
  library (Basic Intake, AoS document requests) is an instance of
  Custom Intakes, not a separate capability; folded into
  smart-forms.custom-intakes detail.
- smart-forms-v3-redesign (fx-0045): "beautiful redesign and simpler
  navigation" is an aesthetic claim with no testable acceptance
  criterion; criterion lint (check 5) could not be satisfied
  honestly.
- crm-forms-organization (fx-0002): "forms are easily organized into
  your DocketWise CRM or can be connected to your existing CRM"
  attests CRM/case-management behavior, out of the Smart Forms
  module boundary; defer to the CRM module in fan-out.
- laborless-lca-posting (fx-0046): LaborLess integration for LCA
  posting and Public Access File management belongs to the
  Integrations module (marketing inventory lists a laborless partner
  page); defer to fan-out.

## module: invoicing-and-trust-accounting (Phase 3) -- 7 rejections

- w9-form-request (fx-0051): the article provides the vendor's own
  W-9 PDF for download -- a support/administrative service, not a
  product capability. Fixture excluded (see exclusion log).
- delinquent-payment-plan-reporting (fx-0054): a workflow recipe
  over the Reports module's invoice report types (filters + columns),
  not a distinct billing capability; the delinquency data points
  (Payment Plan Status, Late Status, Overdue Balance) are kept as
  detail on payment-plans, which cites fx-0054. Report engine
  defers to the Reports module extraction.
- client-payment-experience (fx-0067): the article is the client-side
  face of invoice sharing and online payment, not an orthogonal
  capability ([G1] ruling 3 floor); folded into online-card-payment
  and invoice-sharing, which cite fx-0067.
- secondary-contact-invoicing (fx-0068): choosing a non-primary
  contact as invoice recipient is a sub-behavior of invoice creation
  and sharing (contact picker), not an orthogonal flow; folded into
  invoice-sharing description/detail.
- invoice-discounts (fx-0065, fx-0052): discounts are attested only
  as a line inside the Invoice Settings tab enumeration and the
  translation exclusion list; a settings-tab modifier inside the
  invoice flow, fails the orthogonality floor; folded into
  invoice-creation detail.
- dashboard-invoicing-widgets (fx-0075): invoicing widgets on the
  dashboard are attested only via the option that hides them;
  folded into invoice-access-permissions detail rather than carried
  as a one-line micro-entry.
- quickbooks-sync-behaviors (fx-0055, fx-0080): QuickBooks Online
  sync (and its refund non-sync caveat) belongs to the Integrations
  module; the caveat is recorded as payment-refunds detail, the
  integration itself defers to fan-out of that module. fx-0080 held
  for that extraction (see exclusion log).

## module: firm-settings (Phase 3) -- 8 rejections

- brand-rebrand-faq (fx-0085): corporate rebrand FAQ (AffiniPay ->
  8am); article states functionality is unchanged -- no capability
  to extract. Fixture excluded (see exclusion log).
- training-and-help (fx-0100): support/onboarding services per the
  fx-0040 precedent; the in-app help entry points (chat icon, ?
  button bookings) are support surface, not firm-settings
  capabilities. Fixture excluded (see exclusion log).
- member-credential-transfer (fx-0102): the article is a how-to
  combining self-serve Personal Information editing (Personal
  Settings module) with the login-page password reset (Login
  module); admin-side rename/email mechanics folded into
  managing-users detail, which cites fx-0102; the rest defers to
  those modules.
- account-cancellation (fx-0099): cancellation is a step inside the
  Settings > Subscription flow (fails orthogonality); folded into
  subscription-management detail, which cites fx-0099.
- vendor-payment-details (fx-0105): updating the firm's own credit
  card for the Docketwise subscription is a sub-behavior of
  subscription administration; folded into subscription-management
  detail, which cites fx-0105.
- deactivation-billing-policy (fx-0086): billing-policy FAQ; the
  product-behavior pieces (deactivation semantics, license
  freeing, next-cycle adjustments) are folded into managing-users
  and subscription-management details, which cite fx-0086.
- dashboard-csv-export (fx-0090): CSV export lives on the Contacts
  and Matters dashboards; module-boundary deferral to the Contacts
  and Matters extraction.
- overview-page-composition (fx-0090): contact/matter overview page
  structure (resource tabs, create-new context defaulting) belongs
  to Contacts and Matters; module-boundary deferral. The
  navigation article's universal-search and recents claims are
  extracted here (firm-settings.universal-search).

## module: integrations (Phase 3) -- 1 rejection

- integrations-settings-hub (fx-0114, fx-0117, fx-0119, fx-0122,
  fx-0123): the Settings > Integrations activation page is the
  shared entry point of the per-integration flows, not an
  orthogonal capability of its own ([G1] ruling 3 floor);
  activation mechanics live in each integration entry's
  description/detail.

## module: contacts-and-matters (Phase 3) -- 2 rejections

- open-pending-closed-statuses (fx-0146): the article is a
  recommended workflow pattern (three statuses per matter type)
  built entirely from matter-workflow primitives, not a distinct
  capability; folded as a source and detail note into
  matter-types-statuses.
- learning-center-plugs (fx-0148, fx-0149): repeated Learning
  Center promos inside creation articles are support/training
  surface per the fx-0040 class; no candidate entry drafted.

## module: reports (Phase 3) -- 2 rejections

- per-type-report-entries (fx-0161..fx-0167, fx-0169): one entry
  per canned report type (Matters By Status, Payments By Client,
  etc., ~25 candidates) was considered and rejected: within a
  category the types share one column dictionary and one filter
  set and differ only in grouping (explicit in fx-0167's "all
  columns/filters of Invoices Over Time" reuse language), so the
  selectable CATEGORY is the orthogonal capability -- the
  per-integration carve precedent applied at category level. Types
  are enumerated in each category entry's description/detail. VMAX
  is the deliberate exception (dedicated article fx-0168 plus its
  own contact data field) and is carried as reports.vmax-tracking.
- saved-report-access-and-deletion (fx-0160): accessing a saved
  custom report from the Select a Report page and deleting one via
  the trash icon are lifecycle steps of the saved-report object,
  not orthogonal capabilities ([G1] ruling 3 floor); folded into
  custom-report-saving description/detail.

## module: client-communication (Phase 3) -- 2 rejections

- text-messaging-billing (fx-0179): the 100-free-message grant,
  $20-per-1,000 automatic top-up, and remaining-count display are
  commercial terms and telemetry of the conversations feature, not
  an orthogonal capability ([G1] ruling 3 floor); folded into
  text-message-conversations detail.
- message-resending (fx-0182): re-sending a sent email from the
  Messages tab is a lifecycle step of the sent-message object, per
  the saved-report-access precedent; folded into email-messages
  detail.

## module: client-portal (Phase 3) -- 3 rejections

- portal-deactivation-and-resend (fx-0191, fx-0186): deactivating
  via the same Allow Portal Access slider, re-sending an
  invitation, and the client password reset are lifecycle steps of
  the portal-access object, not orthogonal capabilities ([G1]
  ruling 3 floor); folded into portal-activation detail.
- portal-website-embed (fx-0191): the copy-paste HTML snippet
  linking client.docketwise.com/c/sign_in is a static anchor tag,
  not product behavior; folded into portal-activation detail.
- hr-portal-employee-search (fx-0188): searching the Employees
  index by name or email is navigation within the employee list,
  not an orthogonal capability ([G1] ruling 3 floor); folded into
  hr-portal-employee-management detail.

## module: files-and-documents (Phase 3) -- 4 rejections

- upload-time-renaming (fx-0196): choosing a distinct file name
  during upload is a sub-behavior of the upload flow ([G1] ruling 3
  floor); folded into file-upload detail.
- uploaded-by-attribution (fx-0196): the "uploaded by" email display
  on client uploads is the firm-side view of the portal upload flow,
  not an orthogonal capability ([G1] ruling 3 floor); folded into
  client-portal.portal-client-file-upload detail via the cross-module
  join.
- folder-renaming (fx-0195): considered as a separate entry from
  file renaming; merged -- same pencil-icon mechanic on the same
  surface, and Docketwise's own heading ("Renaming Files and
  Folders") treats them as one capability. No boundary doubt, so the
  split default was not triggered.
- esignature-fee-positioning (fx-0199): "all-in-one, no additional
  fees, remove HelloSign" is commercial positioning, not product
  behavior (text-messaging-billing precedent); the native/no-third-
  party claim itself lives in the esignature anchor entry's
  description and detail.

## module: docketwise-iq (Phase 3) -- 6 rejections

- wa-output-actions (fx-0203): Insert / Discard / Copy / Regenerate
  are controls of the writing-assistant flow, not orthogonal
  capabilities ([G1] ruling 3 floor); folded into writing-assistant
  detail.
- wa-availability-surfaces (fx-0203): the list of surfaces where the
  assistant appears is an attribute of the writing assistant, not a
  capability per surface; folded into writing-assistant detail.
- openai-llm-backend (fx-0202): which LLM vendor powers IQ is an
  architecture fact, not a capability a user could notice as present
  or absent; folded into module-exists detail.
- dc-supported-document-types (fx-0204): the Passport / Green Card /
  EAD / I-94 list is an enumeration attribute of data capture, and
  the article says it will grow; folded into the data-capture
  description and detail.
- wa-coming-soon-surfaces (fx-0203): Text Message Conversations and
  Tasks are flagged Coming Soon -- announced, not shipped; no
  testable criterion exists for an unshipped surface; recorded in
  writing-assistant detail with the Coming Soon qualifier.
- dc-auditability (fx-0206): "clear documentation and auditability"
  is marketing positioning language naming no observable behavior
  (esignature-fee-positioning precedent); not admitted even as
  provisional.

## module: case-tracking (Phase 3) -- 5 rejections

- priority-date-reporting (fx-0211): priority date status in matter
  reports is the report engine exposing case-tracking fields, not
  an orthogonal capability; folded into priority-date-tracking
  detail (reports module owns the engine).
- uscis-case-status-link (fx-0212): the Case Status text linking to
  the USCIS website is a navigation affordance of receipt tracking
  ([G1] ruling 3 floor); folded into uscis-receipt-tracking detail.
- matters-index-receipts-column (fx-0212): viewing receipt statuses
  from the matters index is the custom-columns surface applied to
  case-tracking data; folded into uscis-receipt-tracking detail.
- receipt-number-search (fx-0212): searching by receipt number is
  search-surface behavior, not a tracking capability; folded into
  firm-settings.universal-search detail via the cross-module join.
- task-list-import (fx-0213): considered as a separate entry from
  task lists; merged -- creating a list and importing it are one
  capability loop (the import is the list's purpose), no boundary
  doubt, split default not triggered.

## module: template-automation (Phase 3) -- 3 rejections

- word-processor-support (fx-0218): authoring templates in Word,
  Google Docs, or Apple Pages happens outside the product; the
  product-side capability is accepting the saved .docx ([G1] ruling
  3 floor); folded into module-exists detail.
- frequently-used-tags (fx-0219): the Frequently Used list is a
  presentation subset of the full tag vocabulary, not a distinct
  capability; folded into merge-tags detail.
- merge-tags-in-email-messages (fx-0219): the email surface of the
  merge-tag vocabulary is owned by
  client-communication.email-merge-tags; handled as a cross-module
  in-place source addition (+fx-0219), not a duplicate entry.

## module: notes (Phase 3) -- 3 rejections

- notes-dashboard (fx-0223): the Notes Dashboard is the module's
  index surface, not an orthogonal capability; folded into
  module-exists description.
- firm-wide-note-notification (fx-0223): the notify-all-members
  checkbox is an attribute of note creation; folded into
  note-creation detail.
- category-filtering (fx-0223): filtering note views by category is
  the viewing surface of categories; folded into note-categories
  description.

## module: personal-settings (Phase 3) -- 3 rejections

- personal-settings-anchor (fx-0224): "Personal Settings" is a help
  nav grouping over individual capabilities, not a product module a
  user could notice as present or absent; no anchor entry
  (firm-settings precedent).
- admin-role-editing (fx-0225): an admin setting another user's
  role is the User Access surface of the same capability, not an
  orthogonal one; both paths folded into the user-roles description.
- mandatory-mfa (fx-0226): MFA mandatoriness is an attribute of the
  existing two-factor capability; handled as a cross-module in-place
  source addition to firm-settings.two-factor-authentication, not a
  duplicate entry.

## module: login (Phase 3) -- 4 rejections

- login-anchor (fx-0227): "Login" is a help nav grouping; the
  entries are the capabilities (personal-settings precedent).
- remember-device (fx-0228): the 30-day device-trust checkbox is an
  attribute of the MFA flow; folded into
  firm-settings.two-factor-authentication detail via the
  cross-module join.
- multi-firm-account-access (fx-0228): attested only as a
  conditional aside ("if you have access to multiple firm
  accounts"); account-model attribute folded into
  email-password-login detail rather than admitted on one clause.
- troubleshooting-guidance (fx-0229): browser recommendation,
  incognito test, admin username check, and support channels are
  support guidance naming no product capability; no testable
  criterion exists.

## module: internal-chat (Phase 3) -- 2 rejections

- open-chats-list (fx-0231): the open-chats list is the index
  surface of individual chats; folded into individual-chats
  description.
- enter-to-send (fx-0231): the send mechanic is an attribute of
  messaging, not a capability; folded into criteria.

## module: free-trial (Phase 3) -- 2 rejections

- adding-users-during-trial (fx-0233): the add-user walkthrough is
  the managing-users capability restated for trial onboarding;
  cross-module in-place join (+fx-0233), not a duplicate entry.
- choosing-subscription (fx-0233): tier selection under Settings >
  Subscription is subscription-management ground; join (+fx-0233)
  carrying the new uniform-tier fact (all users share one level) as
  detail, not a duplicate entry.

## module: docketwise-leads-crm (Phase 3) -- 3 rejections

- lead-client-parity (fx-0235): "do pretty much anything with Leads
  that you can do with Clients" is a cross-cutting property of the
  lead record, not one capability; folded into module-exists detail.
- organize-leads-dashboard (fx-0236): the dashboard overview of
  leads is the module's index surface; folded into module-exists
  criterion.
- save-successful-templates (fx-0236): the marketing bullet's body
  text describes the questionnaire-to-forms workflow (smart-forms
  ground) under a leads heading -- garbled copy attesting no
  coherent lead capability; not admitted even as provisional.

## module: events (Phase 3) -- 2 rejections

- notification-type-channels (fx-0240): the Email/SMS channel enum
  is an attribute of the reminder, not a capability per channel;
  folded into event-reminders description (SMS plan gate in
  detail).
- multiple-reminders (fx-0240): + Add notification repetition is an
  attribute of the reminder mechanism; folded into descriptions.

## module: desktop-app (Phase 3) -- 2 rejections

- desktop-app-anchor (fx-0241): one capability IS the module; a
  separate anchor would duplicate the install entry.
- browser-support-matrix (fx-0242): the Chrome/Edge requirement is
  an attribute of the install path; folded into detail.

## module: cross-module (Phase 4 marketing + video reconciliation) -- 5 rejections

- lead-status-tracking join (fx-0244): the features index bullet
  "Status Tracking -- Track the status of your leads" names status
  tracking generally, not the custom-statuses capability that
  docketwise-leads-crm.custom-lead-statuses reads from fx-0235;
  bracket fail (nav/CTA-attestation ruling, modules 14/16) -- no
  join, entry stays provisional.
- portal-invoice-payment (fx-0244): "pay invoices" in the portal
  bullet is ground already carried by
  invoicing-and-trust-accounting.online-card-payment, whose
  description includes the portal Pay button (fx-0186); no new
  entry, no join needed (entry already confirmed).
- inszoom-migration-service (fx-0245): data export/migration from
  INSZoom with onboarding and training is a support service
  performed by the vendor's team, not a product capability;
  fx-0040 ruling class.
- app-directory (fx-0248): the App Directory appears only as a
  listing destination for approved partner apps ("send us your
  logo... so we can list you"); whether it is an in-product
  surface is not attested, and as a partner-facing listing it is
  not a capability a Docketwise user notices; folded into
  integrations.open-api detail.
- engagement-letter-management (fx-0257): the video description's
  clause "managing disclosures, engagement letters,
  acknowledgements, referrals, and automated workflows in one
  secure platform" is promo gloss naming no distinct testable
  capability; the ground it gestures at is template-automation
  plus matter-status-automations. Not admitted even as
  provisional.

## module: cross-module (Phase 4 release-notes sweep) -- 3 rejections

- mobile-responsiveness (fx-0271): "a more mobile-friendly
  Docketwise web application" is a cross-cutting property of the
  whole web app, not one capability (lead-client-parity
  precedent, module docketwise-leads-crm); no module home, not
  admitted.
- yotengo-bot integration (fx-0262): listed as an integration in
  the June 2022 review but absent from the current 17-partner
  marketing roster, the help-center integrations articles, and
  every other current-family source; admitting from a stale
  source would attest a present capability without current
  evidence. Recorded here, not admitted ([G2] queue: stale-source
  reading).
- legalmate integration (fx-0262): same ruling as yotengo-bot --
  2022-era integration absent from all current rosters.

## module: cross-module (Phase 4 fx-0108 pricing-matrix re-mine) -- 2 rejections

- reverse-autofill (fx-0108): a Forms feature row named "Reverse
  Autofill" with no definition anywhere on the page or in any
  captured source; the name is not confidently resolvable to an
  existing entry (closest candidate data-import-into-forms is a
  guess) and a new entry cannot carry a testable criterion from a
  bare row label. Not admitted; flagged for [G2] -- resolvable
  only by product observation or future documentation.
- multiple-account-admins join (fx-0108): the Administration row
  "Multiple Account Admins" names a plan allowance (admin-count),
  not the user-management capability firm-settings.managing-users
  reads from fx-0107; bracket fail (nav/CTA-attestation ruling),
  entry stays provisional.
