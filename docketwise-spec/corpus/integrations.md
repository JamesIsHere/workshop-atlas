# module: integrations

Docketwise's own vocabulary (help-center category "Integrations",
15 articles, fx-0003; marketing /integrations/ index, 17 partner
pages). Phase 3 module: full extraction from 15 help articles
(fx-0111..fx-0125), collection page fx-0110, marketing index
fx-0126 and partner pages fx-0127..fx-0141 plus the earlier
fx-0079 (LawPay) and fx-0080 (QuickBooks, held from module 1).
Natural carve: one entry per integration -- each is a capability a
user notices as present or absent. The help overview article
(fx-0112) attests the full roster on the help family, so
marketing-listed partners without their own article still reach
confirmed; Candle AI appeared on marketing only and sat
provisional until the Phase 4 blog sweep confirmed it (fx-0263,
2026-08-01). Phase 4 additions from the same sweep: open-api
(promoted via fx-0262) and everify (provisional, fx-0269).

## entry: integrations.lawpay
- name: LawPay Integration
- named-by-us: no
- description: Connects a LawPay account so clients can pay
  Docketwise invoices by credit card or eCheck into the firm's
  LawPay bank accounts; LawPay accounts are linked to Docketwise
  bank accounts (existing or imported), with default client payment
  accounts per operating and trust account, and accepted payment
  forms (CC/eCheck) toggleable (fx-0123). Marketing attests secure
  online payments with automatic sync (fx-0079).
- criterion: Firm activates LawPay under Settings > Integrations
  and links accounts -> client credit card and eCheck payments on
  invoices are processed into the linked LawPay account and
  recorded in Docketwise
- sources: fx-0079, fx-0123
- tier: confirmed
- detail: Credit card surcharges enabled on the LawPay side are
  passed on automatically (percentage-based, all CC transactions);
  surcharges do not appear on the invoice itself, only in Payment
  Reports, and are unsupported on automatic payment plans
  (fx-0123). Refunds recorded in Docketwise auto-trigger the LawPay
  refund (fx-0123). Payments made directly in LawPay outside the
  integration are not reflected; client credit financing (pay
  later) is unsupported (fx-0123). Deleting an invoice with an
  active payment plan deletes its scheduled payments in LawPay;
  deactivating the integration deletes integration-created
  scheduled payments (fx-0123).

## entry: integrations.quickbooks
- name: QuickBooks Integration
- named-by-us: no
- description: Connects QuickBooks Online so invoices, payments,
  and trust account transactions created in Docketwise are synced
  into QuickBooks; activation maps Docketwise services, expenses,
  and discounts to QuickBooks accounts and (optionally) a trust
  account and trust liability account for trust bookkeeping
  (fx-0117, fx-0080). Docketwise Pro or Advanced required (fx-0117,
  fx-0101).
- criterion: Firm activates QuickBooks and creates a bill with
  charges in Docketwise -> a synced invoice appears in QuickBooks
  Online with its charges, discounts, and subsequent payments
- sources: fx-0080, fx-0101, fx-0117, fx-0262
- tier: confirmed
- detail: The 2022 integrations review gates the integration to
  Docketwise Suite or Enterprise (fx-0262) where current help
  says Pro or Advanced (fx-0117) -- a plan-name history
  discrepancy, current names control. QuickBooks Online only (not Desktop); sync is one
  direction, Docketwise to QuickBooks, and only for transactions
  after activation (fx-0117). Contacts without a QuickBooks
  customer are auto-created; invoices without charges are not
  created; edits to charges and payments sync, deletions do not;
  bill refunds do not sync (fx-0117). Trust requests post as
  journal entries (debit trust account, credit trust liability) on
  payment receipt; disbursements post the reverse; trust transfers
  post the journal entry plus invoice payment (undeposited funds /
  accounts receivable) (fx-0117).

## entry: integrations.mycase
- name: MyCase Integration
- named-by-us: no
- description: Two-way sync of contacts and matters/cases between
  Docketwise and MyCase (optionally one-way, MyCase to Docketwise);
  initial activation matches contacts by first name, last name, and
  email, syncs matches (MyCase values win conflicts), and creates
  Docketwise contacts for unmatched MyCase contacts (fx-0114).
  Completed Docketwise forms can be saved directly to the synced
  case's documents in MyCase (fx-0114).
- criterion: Firm activates the MyCase integration and creates a
  matter in Docketwise -> the matter is created and kept in sync in
  MyCase
- sources: fx-0114, fx-0138, fx-0266
- tier: confirmed
- detail: The October 2024 press release announces a MyCase
  Immigration Add-On powered by Docketwise: Smart Forms
  auto-population, USCIS case tracking, e-filing to USCIS, DOL
  FLAG, and DOS CEAC, and priority date tracking surfaced inside
  MyCase itself (fx-0266). Synced contact fields: first/last name, email, physical
  address, mobile and work phone; synced matter fields: name,
  description, contacts (fx-0114). MyCase-to-Docketwise updates
  sync nightly or manually (profile > Sync MyCase);
  Docketwise-to-MyCase updates sync instantly (fx-0114). Email and
  matter name are unique in MyCase (duplicate matter names get the
  Docketwise Matter ID appended); company contacts do not sync;
  matters do not sync on the initial pass (fx-0114). Requires a
  MyCase Pro or Advanced subscription (fx-0114).

## entry: integrations.clio
- name: Clio Integration
- named-by-us: no
- description: Two-way sync of contacts and matters between
  Docketwise and Clio: on activation existing contacts and matters
  migrate both ways, and later edits to syncing attributes reflect
  across both platforms; two-way sync can be turned off to sync
  only Clio to Docketwise (fx-0125).
- criterion: Firm activates the Clio integration -> contacts and
  matters migrate and stay synced between Clio and Docketwise
- sources: fx-0121, fx-0125, fx-0137
- tier: confirmed
- detail: Synced contact attributes: name, email, phone, physical
  address; matter attributes: title, description, client
  (fx-0125). Clio matters must have Public permission for the Clio
  API to expose them; the integration supports one Clio account at
  a time (fx-0121).

## entry: integrations.practicepanther
- name: PracticePanther Integration
- named-by-us: no
- description: Syncs contacts and matters with PracticePanther: on
  activation existing PracticePanther contacts migrate into
  Docketwise, and thereafter contact/matter creates and edits
  reflect across both platforms via a nightly comprehensive sync or
  an on-demand manual sync (fx-0124).
- criterion: Firm activates the PracticePanther integration ->
  PracticePanther contacts migrate into Docketwise and later
  changes sync across both platforms
- sources: fx-0124, fx-0135
- tier: confirmed

## entry: integrations.google-calendar
- name: Google Calendar Integration
- named-by-us: no
- description: Two-way event sync between Docketwise and selected
  Google calendars: events created or edited on either platform
  reflect on the other (fx-0122). On Pro/Advanced every user can
  connect their own Google account; on Basic one user per firm can
  connect at a time (multiple calendars allowed) (fx-0122).
- criterion: User activates the Google Calendar integration and
  selects calendars -> events created or edited in either platform
  appear on both
- sources: fx-0122, fx-0139
- tier: confirmed
- detail: Docketwise-native calendars cannot sync (events may be
  reassigned to a synced Google calendar); recurring-event sync is
  unsupported; Google and Outlook calendar integrations are
  mutually exclusive per user (fx-0122). Pro/Advanced users
  activate under Settings > Personal Information, Basic under
  Settings > Integrations (fx-0122).

## entry: integrations.outlook-calendar
- name: Outlook Calendar Integration
- named-by-us: no
- description: Two-way event sync between Docketwise and selected
  Outlook calendars: events created or edited on either platform
  reflect on the other (fx-0119). On Pro/Advanced every user can
  connect their own Outlook account; on Basic one user per firm at
  a time (fx-0119).
- criterion: User activates the Outlook Calendar integration and
  selects calendars -> events created or edited in either platform
  appear on both
- sources: fx-0119, fx-0133
- tier: confirmed
- detail: Docketwise-native calendars cannot sync; recurring-event
  sync is unsupported; mutually exclusive with the Google Calendar
  integration per user (fx-0119, fx-0122). Pro/Advanced users
  activate under Settings > Personal Information, Basic under
  Settings > Integrations (fx-0119).

## entry: integrations.gmail-addon
- name: Gmail Add-on
- named-by-us: no
- description: A Docketwise add-on inside Gmail saves emails and
  attachments to a contact and matter in Docketwise; the add-on
  auto-suggests the matching contact from the sender's address, and
  attachments can be filed to a chosen folder (fx-0118, fx-0132).
- criterion: User opens an email in Gmail and clicks Save this
  email as a message in the Docketwise add-on -> the email is saved
  as a message under the selected contact/matter in Docketwise
- sources: fx-0118, fx-0132
- tier: confirmed
- detail: Requires Chrome signed into the same Google account and
  add-on installation from the Gmail add-ons marketplace with a
  one-time Connect/Authorize step (fx-0118). Sub-folders cannot be
  selected when saving attachments (fx-0118).

## entry: integrations.outlook-email-addin
- name: Outlook Email Add-in
- named-by-us: no
- description: A Docketwise add-in inside Outlook (web or desktop
  app) saves emails and attachments to a contact and matter in
  Docketwise, with the sender auto-suggested as the contact and
  folder selection for attachments (fx-0115, fx-0136).
- criterion: User opens an email in Outlook and clicks Save this
  email as a message in the Docketwise add-in -> the email is saved
  as a message under the selected contact/matter in Docketwise
- sources: fx-0115, fx-0136
- tier: confirmed
- detail: Installed from the Outlook add-ins marketplace; requires
  admin-enabled add-ins and, for desktop, the current Outlook
  version (fx-0115). Sub-folders cannot be selected (fx-0115).

## entry: integrations.immitranslate
- name: ImmiTranslate Integration
- named-by-us: no
- description: Selected files are sent directly from Docketwise
  (Files dashboard or a contact's/matter's Files tab, More Actions
  > Translate) to ImmiTranslate for professional translation;
  completed translations are automatically returned to the same
  matter/client in Docketwise (fx-0116, fx-0131).
- criterion: User selects files and chooses Translate (with
  ImmiTranslate) -> the files upload to an ImmiTranslate order and
  the completed translations return to the same matter/client
- sources: fx-0116, fx-0131
- tier: confirmed
- detail: First use auto-creates an ImmiTranslate account and
  prompts a one-time authorization (fx-0116). Order options:
  source/target language, certified vs certified-and-notarized,
  digital vs digital-plus-physical delivery; payment by credit
  card or PayPal at ImmiTranslate's standard pricing; available to
  all Docketwise users at no added fee; translations carry a USCIS
  acceptance guarantee (fx-0116).

## entry: integrations.zapier
- name: Zapier Integration
- named-by-us: no
- description: Docketwise connects to Zapier as an app, exposing
  contact events for automation with 3,000+ other apps: triggers
  fire when a contact is created or updated in Docketwise, and
  actions create or update Docketwise contacts from other apps
  (fx-0120, fx-0140).
- criterion: User builds a Zap with a Docketwise trigger or action
  -> contact creations/updates flow between Docketwise and the
  connected app automatically
- sources: fx-0120, fx-0140
- tier: confirmed
- detail: Trigger payload fields include name parts, company,
  email, physical address components, and created/updated stamps
  with IDs; action fields additionally cover biographical (DOB,
  country of birth, gender), marital status, employment status,
  and immigration fields (country of citizenship, A-Number, USCIS
  ELIS account, passport/travel document numbers and dates)
  (fx-0120).

## entry: integrations.casestatus
- name: Case Status Integration
- named-by-us: no
- description: Integration with Case Status, a client-communication
  platform that gives clients a mobile app with automated case
  status updates, appointment scheduling, reminders, document
  collection, and NPS surveys as cases progress (fx-0111, fx-0141).
- criterion: Firm integrates Case Status -> clients receive
  automated case status updates through the Case Status mobile app
- sources: fx-0111, fx-0141
- tier: confirmed
- detail: The integration is set up directly with Case Status on
  their website, not from inside Docketwise; support is through
  Case Status's team (fx-0111).

## entry: integrations.visalaw-ai
- name: Visalaw AI Integration
- named-by-us: no
- description: Connects Visalaw AI (immigration-focused drafting,
  research, and document-analysis platform) to Docketwise via
  single-click OAuth: users select Docketwise matters inside
  Visalaw AI, pull the matter's documents into drafting workflows,
  and push finalized petitions and materials back into the matter
  record as new files (fx-0113, fx-0128).
- criterion: User connects Visalaw AI and selects a Docketwise
  matter -> matter documents import into Visalaw AI and finalized
  work product syncs back to the same matter record
- sources: fx-0113, fx-0128
- tier: confirmed
- detail: Docketwise Pro or Advanced required (fx-0113). Returned
  files are added as new files, never overwriting existing matter
  documents (fx-0113). Visalaw AI's own plans at capture: Core
  $220/user/month, Pro $480/user/month, Enterprise custom
  (fx-0113).

## entry: integrations.candle-ai
- name: Candle AI Integration
- named-by-us: no
- description: Candle AI connects the user's inbox (Outlook and
  Gmail) to Docketwise so client emails arrive with the full
  matter context attached, for faster in-inbox responses
  (fx-0126, fx-0127). The launch announcement attests the
  behaviors: real-time client, matter, and case activity shown
  alongside each email, one-step email logging to the correct
  matter, case-note creation from the thread, message templates,
  and automatic sync back to Docketwise (fx-0263).
- criterion: User connects Candle AI to Docketwise and their inbox
  -> incoming client emails display the matching Docketwise matter
  context
- sources: fx-0126, fx-0127, fx-0263
- tier: confirmed
- detail: AI drafting uses the matter context in view (fx-0263).
  Positioned as built into Docketwise rather than a bolt-on email
  sync (fx-0263).

## entry: integrations.laborless
- name: LaborLess Integration
- named-by-us: no
- description: Integration with LaborLess, a web platform for
  electronic LCA posting, tracking, and compliance management for
  H-1B, H-1B1, and E-3 candidates (fx-0129, fx-0112); announced
  alongside H-1B e-filing on the product blog as handling LCA
  posting and Public Access File management (fx-0046).
- criterion: Firm connects LaborLess -> LCA postings for H-1B-class
  candidates can be posted and tracked electronically
- sources: fx-0046, fx-0112, fx-0129
- tier: confirmed

## entry: integrations.motaword
- name: MotaWord Integration
- named-by-us: no
- description: Translates legal documents across 120 languages
  from the Docketwise dashboard via MotaWord, with instant quotes,
  free certifications, and digital notarization (fx-0130, fx-0112).
- criterion: User sends a document to MotaWord from Docketwise ->
  an instant quote is produced and the certified translation is
  delivered
- sources: fx-0112, fx-0130, fx-0198, fx-0265, fx-0271
- tier: confirmed
- detail: Announced as a new integration in 2024 (fx-0271, fx-0265).
  Translated documents are automatically saved in the same folder
  as the original file in Docketwise (fx-0265). Route: select
  files, then More Actions > Translate /
  Evaluate (with MotaWord); selected documents are processed for a
  real-time quote (fx-0198). Three services: professional
  translation, certified translation, and academic evaluation --
  evaluations take a source language, evaluation method, and
  target organization (fx-0198). First use prompts an Authorize
  step, and a MotaWord account is auto-created if none exists
  (fx-0198). Finalized documents are automatically sent back to
  the same client/matter in Docketwise (fx-0198).

## entry: integrations.legalboards
- name: Legalboards Integration
- named-by-us: no
- description: Integration with Legalboards, a workflow tool for
  planning, building, and executing customized legal workflows on
  lean/agile-style boards (fx-0134, fx-0112).
- criterion: Firm connects Legalboards -> Docketwise work can be
  driven through customized Legalboards workflows
- sources: fx-0112, fx-0134
- tier: confirmed

## entry: integrations.open-api
- name: Open API
- named-by-us: no
- description: A public developer surface (the /developers/ page and
  site-wide Open API nav link) attests a RESTful API with
  JSON-formatted responses for accessing essential Docketwise
  resources, so developers can build applications on top of
  Docketwise or connect an existing application to Docketwise data
  (fx-0248, fx-0002). API access is requested through the firm's
  Customer Success Manager or the support team; approved apps can
  be listed in an App Directory (fx-0248). The integrations-review
  blog post attests the API on the release-notes family, claiming
  Docketwise was the first immigration software product to offer
  an open API (fx-0262).
- criterion: Developer of a firm granted API access issues a
  request against the documented REST endpoints -> a JSON-formatted
  response with the requested Docketwise resource data is returned
- sources: fx-0248, fx-0002, fx-0262
- tier: confirmed
- detail: Public API documentation is linked from the page; the
  vendor states the API surface is continuously expanding
  (fx-0248). Phase 4 addition (2026-08-01) from the /developers/
  inventory item.

## entry: integrations.everify
- name: E-Verify Integration
- named-by-us: yes
- description: A blog post on I-9 compliance attests that
  Docketwise integrates with E-Verify: E-Verify checks can be
  initiated directly from the platform where the I-9 was
  completed, without navigating to a separate system or
  re-entering data (fx-0269).
- criterion: User initiates an E-Verify check on a completed I-9
  from within Docketwise -> the verification is submitted to
  E-Verify without re-entering the form data
- sources: fx-0269
- tier: provisional
- detail: Attested only by this SEO-leaning blog post; no help
  article, partner page, or current integrations roster line names
  E-Verify. Phase 4 addition (2026-08-01); admitted under the
  marketing-only decision default with the tier carrying the
  skepticism. Admission RATIFIED at [G2] (James, 2026-08-01) after
  an approved scoped out-of-family check found no reachable second
  family: e-verify.gov bot-walled (403), DHS publishes no public
  Web Services developer roster, 8am/AffiniPay corporate surface
  silent on E-Verify (worklog [G2] item 4). Permanently provisional
  absent a new public source.
