# module: smart-forms

Docketwise's own vocabulary (help-center category "Smart Forms",
fx-0003; marketing "Immigration Forms", fx-0002 -- same module, help
center name wins as the product-internal term). Phase 2 pilot module:
full extraction from 32 help articles (fx-0013..fx-0044), collection
page fx-0012, marketing fx-0002, release-note blog posts
fx-0045..fx-0047, and YouTube fixtures fx-0048/fx-0049.

## entry: smart-forms.forms-library
- name: Immigration Forms Library
- named-by-us: no
- description: A maintained library of immigration forms covering
  family, business, and humanitarian immigration practice; marketing
  claims every form required to complete immigration cases (fx-0002).
  Help center has a dedicated Smart Forms category, 32 articles
  (fx-0003). The library index article (fx-0044) enumerates the full
  list by agency: DOL, DOS, EOIR/DOJ, and USCIS forms.
- criterion: User selects an immigration case type -> system offers
  the required forms for that case type from a maintained library
- sources: fx-0002, fx-0003, fx-0044
- tier: confirmed
- detail: fx-0044 lists 4 DOL forms (ETA-750B, ETA-9035, ETA-9089
  with appendices, ETA-9141), 6 DOS forms (DS-117, DS-156E, DS-160,
  DS-260, DS-4240 C/R), 13 EOIR/DOJ forms (EOIR-26 through EOIR-61,
  I-589), and roughly 90 USCIS forms (G- and I- and N- series).
  Forms marked "Also available for e-filing": ETA-9035, ETA-9141,
  DS-160, DS-260, I-129, I-130, I-765, N-400.

## entry: smart-forms.single-intake-autofill
- name: Combined Intake Questionnaire with Auto-Population
- named-by-us: no
- description: Any number of immigration forms combine into a single
  client intake questionnaire; client responses auto-populate the
  mapped field areas on every selected form (fx-0002). The intake is
  built on an algorithm that determines which forms are required and
  prepares the full packet from the intake answers (fx-0045). The
  Intake tab is the questionnaire portion of the smart form, from
  which answers populate the included forms (fx-0020); official
  YouTube videos attest automated intake and auto-population of
  immigration forms (fx-0048, fx-0049).
- criterion: Client submits one combined intake questionnaire ->
  responses populate the mapped fields across all selected forms
  without re-entry
- sources: fx-0002, fx-0014, fx-0020, fx-0021, fx-0045, fx-0048, fx-0049, fx-0246, fx-0249, fx-0250, fx-0278
- tier: confirmed
- detail: Client-side answer formats are drop-down list, checkbox,
  and text box; repeating items (children, addresses, trips) are
  added with an Add button; date answers can be formatted as
  Month-Day-Year, Month-Year, Year, or Present (fx-0021). Marketing
  phrases the sync as Bulk Form Updates: change data once and it is
  reflected on all forms (fx-0002). Population logic is keyed to
  country/state field values; fx-0014 documents a workaround for
  U.S. territory addresses on Form I-589 (select United States as
  country and enter the territory's two-letter code manually). A
  vendor-curated review-page testimonial attests the flow from the
  user side: client answers populate onto the USCIS forms
  (fx-0246). The SmartForms launch video attests "a single intake
  questionnaire that auto-completes every form" (fx-0278,
  back-catalog via uploads-playlist enumeration). Firsthand r/LawFirm users independently attest the
  questionnaire and forms surface: "works well for forms" and "I
  liked their questionnaires" (fx-0249), "I like the forms
  feature. And the questionnaire feature" (fx-0250) -- the first
  reviews-family attestations for this module; both threads also
  carry negative-valence assessments of other surfaces (case
  management depth, customer service), recorded per the valence
  reading queued for [G2].

## entry: smart-forms.multilingual-intake
- name: Multilingual Questionnaires
- named-by-us: no
- description: Intake questionnaires can be translated for clients
  and firm members; marketing claims auto-translation (fx-0002), and
  help articles document a Translate action on the Intake tab plus
  per-invitation language selection (fx-0033, fx-0039, fx-0020).
- criterion: Firm selects a supported language on an intake or its
  invitation -> client sees the questionnaire in that language
- sources: fx-0002, fx-0020, fx-0021, fx-0033, fx-0039, fx-0045, fx-0243
- tier: confirmed
- detail: 12 language options attested: English, Spanish,
  Portuguese, French, Hindi, Russian, Chinese (Mandarin), Korean,
  Turkish, Haitian Creole, Arabic, Vietnamese (fx-0033, fx-0039);
  Vietnamese is flagged as the first machine-translated language
  (fx-0033). Invited contacts see the language chosen at invitation
  time and can re-translate themselves (fx-0039, fx-0021). Custom
  Questions are not translated (fx-0029). Marketing adds delivery by
  email and SMS text and mobile browser support (fx-0002). The
  dedicated Translations feature page lists 11 languages -- the
  help-family list minus Vietnamese -- and scopes the capability:
  only form questions are translated for intake; certified document
  translation is partner ground (ImmiTranslate/MotaWord)
  (fx-0243).

## entry: smart-forms.uscis-efiling
- name: E-Filing Forms with USCIS
- named-by-us: no
- description: Help center carries an article titled "E-Filing Forms
  with USCIS" under recommended articles (fx-0003), attesting an
  e-filing capability from the product to USCIS.
- criterion: User submits a completed eligible form -> form is
  e-filed with USCIS from within the application
- sources: fx-0003
- tier: provisional
- superseded-by: smart-forms.uscis-efiling-sync
- detail: Superseded 2026-07-31 (Phase 2): the full article body
  (fx-0017) shows the flow syncs a validated questionnaire to a
  draft on my.uscis.gov which the user then completes, reviews, and
  signs on the USCIS platform -- the seed criterion overclaimed
  fully in-app filing from a title-only reading.

## entry: smart-forms.uscis-efiling-sync
- name: E-Filing Forms with USCIS
- named-by-us: no
- description: Eligible USCIS forms can be e-filed from Docketwise:
  the questionnaire is validated, then synced into a new draft
  filing on the user's my.uscis.gov account using the firm's USCIS
  credentials and an authenticator-app OTP secret; the user
  completes review, evidence upload, and signing on the USCIS
  platform (fx-0017). A step-by-step e-File tab drives the process,
  including an attached G-28 sync step (fx-0017). E-filing with
  USCIS, DOL FLAG, and DOS CEAC is an umbrella capability of Smart
  Forms (fx-0015); the H-1B I-129 e-filing was publicly announced
  on the blog (fx-0046).
- criterion: User with a validated questionnaire clicks e-File and
  provides USCIS account credentials -> Docketwise creates a synced
  draft of the form on my.uscis.gov for completion there
- sources: fx-0015, fx-0017, fx-0043, fx-0046, fx-0271
- tier: confirmed
- detail: The 2024 year-in-review lists I-129 e-filing among the
  year's released features (fx-0271). USCIS forms attested as e-filable: I-130, N-400, I-765,
  I-129 (with optional I-907), and H-1B Electronic Registration,
  each with attached G-28 (fx-0017). Only attorney/legal
  representative USCIS accounts are supported; OTP secret comes
  from the USCIS authenticator-app setup (fx-0017, fx-0043). On
  failure the app shows a screenshot taken at the moment of error
  plus an in-app bell notification; on success the sync is queued
  and confirmed by notification (fx-0017). The G-28 step syncs
  G-28 data to the case via a USCIS continue-G-28 URL pasted by the
  user (fx-0017). Docketwise cannot update an e-filing draft after
  submission (fx-0017). Feature gated to Pro and Advanced
  subscription plans (fx-0015, fx-0017).

## entry: smart-forms.efiling-validation
- name: E-Filing Questionnaire Validation
- named-by-us: no
- description: Before any e-filing sync, Docketwise validates the
  questionnaire against the target agency's conventions and, on
  failure, lists every error in the e-File tab with a Go to
  question link; each flagged question is highlighted on the intake
  with an explanation, and a Re-Validate button re-runs the check
  (fx-0017, fx-0016, fx-0022).
- criterion: User starts e-filing with an incomplete questionnaire
  -> a validation error list appears with per-question links and
  explanations, and e-filing is blocked until re-validation passes
- sources: fx-0016, fx-0017, fx-0019, fx-0022
- tier: provisional

## entry: smart-forms.ceac-ds160-efiling
- name: E-Filing Form DS-160
- named-by-us: no
- description: The DS-160 can be e-filed to the DOS CEAC platform:
  once the intake is complete and formatted to CEAC specifications,
  Docketwise creates a new DS-160 application on the CEAC website
  containing all provided answers; the user retrieves it on CEAC
  with the Application ID and security question answers from
  Docketwise and completes filing there (fx-0019, fx-0015).
- criterion: User completes a DS-160 intake and starts CEAC
  e-filing with a location and security question -> a retrievable
  DS-160 application containing the answers exists on
  ceac.state.gov
- sources: fx-0015, fx-0019
- tier: provisional
- detail: Pro/Advanced plans only (fx-0019). A bell notification
  delivers the CEAC access information (Application ID, security
  answers) after a successful sync (fx-0019).

## entry: smart-forms.ceac-ds260-efiling
- name: E-Filing Form DS-260
- named-by-us: no
- description: The DS-260 immigrant-visa application can be e-filed
  to CEAC: a dedicated e-file DS-260 Smart Form is validated and
  synced to the CEAC platform using Case Number and Invoice ID; the
  filing itself is then submitted manually by the user on CEAC
  (fx-0016, fx-0015).
- criterion: User provides Case Number and Invoice ID for a
  validated DS-260 -> the application data is synced onto the CEAC
  platform ready for manual submission
- sources: fx-0015, fx-0016
- tier: provisional
- detail: Related processing fees must show status PAID in CEAC
  before e-filing; a separate DS-260 is required per applicant
  (principal/derivative); Docketwise cannot update the draft after
  submission; failures include a screenshot taken at error time
  (fx-0016). Pro/Advanced plans only (fx-0016).

## entry: smart-forms.dol-flag-efiling
- name: E-Filing Forms with DOL FLAG
- named-by-us: no
- description: ETA-9141 and ETA-9035/9035E can be e-filed to the
  DOL FLAG platform through the user's secure.login.gov account
  with an authenticator-app OTP secret; Docketwise creates the
  application draft on the synced FLAG account, where the user
  reviews and completes the filing (fx-0022, fx-0015). ETA-9035
  e-filing via FLAG integration was publicly announced on the blog
  (fx-0046).
- criterion: User with a completed ETA-9141 or ETA-9035 intake
  provides login.gov credentials -> a draft application containing
  the answers is created on the user's flag.dol.gov account
- sources: fx-0015, fx-0022, fx-0046, fx-0267, fx-0271
- tier: confirmed
- detail: The ETA-9141 blog post walks the full login.gov OTP sync
  flow and gates eFiling to "Docketwise Suite" (fx-0267); the 2024
  year-in-review lists ETA-9035 e-filing among the year's releases
  for "Pro and Advanced users" (fx-0271) -- plan-name history
  discrepancy, current names control. Requires a secure.login.gov account; login.gov allows at
  most two authenticator apps, so one may need deleting during
  setup (fx-0022). Pro/Advanced plans only (fx-0022). The
  PWD-after-ETA-9141 workflow is documented as not supported
  (fx-0022). Success/failure delivered by in-app notification.

## entry: smart-forms.h1b-electronic-registration
- name: H-1B Electronic Registration
- named-by-us: no
- description: H-1B Electronic Registrations can be prepared as
  Smart Forms and e-filed with USCIS, including bulk preparation of
  registrations for multiple prospective employees from the
  employer's contact page (fx-0013). H-1B Registration availability
  through Docketwise was publicly announced on the blog (fx-0046).
- criterion: User selects prospective employees on an employer
  contact and starts an H-1B Registration -> a registration Smart
  Form is created for the employer and selected beneficiaries and
  can be e-filed to my.uscis.gov
- sources: fx-0013, fx-0046
- tier: confirmed
- detail: Bulk preparation is limited to 20 beneficiaries; the
  feature is in Beta behind Settings > Beta Access and gated to Pro
  and Advanced plans (fx-0013). Creation paths: Bulk Actions on the
  employer's Employees tab, or Create New > Form > H-1B
  Registration e-Filing (fx-0013).

## entry: smart-forms.efiling-paper-toggle
- name: Toggling Between Electronic and Paper Filing
- named-by-us: no
- description: An e-filing Smart Form can be switched between the
  electronic and paper version of the form from the Intake tab;
  currently supported only for the N-400 + G-28 combination
  (fx-0017).
- criterion: User toggles an N-400 e-filing Smart Form to paper ->
  the form switches to the paper version without recreating the
  intake
- sources: fx-0017
- tier: provisional

## entry: smart-forms.form-updates-versioning
- name: Form Updates and Versioning
- named-by-us: no
- description: Docketwise commits to updating forms within 5
  business days of a new version's announcement by USCIS or other
  agencies, and automatically migrates previously prepared forms to
  the newer version (fx-0027). The I-765/I-765WS edition
  announcement shows the policy in practice: new editions published
  side-by-side, then automatic conversion of all prepared forms on
  the acceptance cutoff date (fx-0047).
- criterion: An agency releases a new form edition -> Docketwise
  carries the new edition within 5 business days and previously
  prepared forms migrate to it automatically
- sources: fx-0027, fx-0047, fx-0243
- tier: confirmed
- detail: The Translations feature page FAQ attests the policy on
  the marketing family: Docketwise tracks USCIS form changes so
  only current versions are used on the platform (fx-0243).

## entry: smart-forms.form-version-toggle
- name: Toggling the Form Version
- named-by-us: no
- description: When a previous form edition is still accepted by
  USCIS, a prepared form can be reverted to the previous edition
  and back with Switch to the previous/latest version buttons;
  applies only to USCIS forms updated in Docketwise since March
  2023 (fx-0027).
- criterion: User clicks Switch to the previous version on an
  updated USCIS form still accepted at the older edition -> the
  form reverts to the previous edition
- sources: fx-0027
- tier: provisional
- detail: DS, DOL, and EOIR forms do not carry multiple versions;
  if several included forms have previous versions, all revert
  together (fx-0027).

## entry: smart-forms.packet-assembly
- name: Packet Assembly
- named-by-us: no
- description: The Assemble tab combines forms and evidentiary
  files into a single Smart Form packet: add forms individually or
  via collections/templates, attach files searched by contact or
  file name, and drag-and-drop the order of forms and files
  (fx-0020). Packet Assembly was the headline capability of the
  Smart Forms 3.0 release announcement (fx-0045).
- criterion: User adds forms and files on the Assemble tab and
  reorders them -> the packet contains those forms and files in
  the chosen order
- sources: fx-0020, fx-0045
- tier: confirmed
- detail: Forms and files can be renamed for the packet's table of
  contents with an inline edit control (fx-0020).
  Password-protected files cannot be included in the downloaded
  packet (fx-0020). Contact, Matter, and Preparer assignment also
  live on the Assemble tab (fx-0020).

## entry: smart-forms.packet-toc
- name: Automatic Table of Contents
- named-by-us: no
- description: Checking Include Table of Contents on the Assemble
  tab adds an automatically generated table of contents page at
  the start of the packet, listing all included forms and
  documents with page numbers (fx-0020, fx-0045).
- criterion: User checks Include Table of Contents -> the packet
  gains a first page listing every form and document with its page
  number
- sources: fx-0020, fx-0045
- tier: confirmed

## entry: smart-forms.smart-form-collections
- name: Smart Form Collections
- named-by-us: no
- description: Any custom combination of forms can be saved as a
  named collection under Settings > Smart Form Collections and
  reused when creating new Smart Forms; marketing calls the same
  capability Save Packages (fx-0034, fx-0002). Saving form
  combinations for later reuse is also attested in the Smart Forms
  3.0 announcement (fx-0045).
- criterion: User creates a named collection of forms -> the
  collection appears in the forms list when creating a new Smart
  Form and adds all its forms at once
- sources: fx-0002, fx-0020, fx-0034, fx-0045
- tier: confirmed

## entry: smart-forms.templated-intakes
- name: Templated Smart Form Intakes
- named-by-us: no
- description: A configured intake can be saved as a reusable
  template capturing included forms and questions, custom tabs and
  questions, and question settings (hides, flags, comments), with
  customizable roles per included individual; reusing a template
  follows the normal new-Smart-Form flow (fx-0041, fx-0020). Named
  as a Templated Smart Forms release in the Q4 2022
  features-roundup video (fx-0276, chapter at 34:09).
- criterion: User saves an intake as a template and creates a new
  Smart Form from it -> the new intake carries the template's
  forms, custom questions, and question settings
- sources: fx-0020, fx-0041, fx-0276
- tier: confirmed
- detail: Invitee comments and mention/tagging comments are not
  saved to templates; overwriting a template requires deleting the
  old one under Settings > Smart Form Collections; each custom role
  may be used once per template (fx-0041).

## entry: smart-forms.intake-invitations
- name: Smart Form Invitations
- named-by-us: no
- description: Contacts are invited to complete a Smart Form
  questionnaire by email invitation, text message invitation,
  shareable link, or the Client Portal (fx-0039, fx-0020);
  marketing attests sharing questionnaires by email or SMS text
  (fx-0002). Invitations can go to included contacts or any other
  contact (fx-0020).
- criterion: User sends an invitation by any supported method ->
  the contact gains secure access to complete the questionnaire
- sources: fx-0002, fx-0020, fx-0039, fx-0246
- tier: confirmed
- detail: Email invitations appear to come from, and reply to, the
  firm user's own email address (fx-0039). Invitation entry points:
  Forms index Invites column, Invite tab, or More Actions > Share
  (fx-0039). A vendor-curated review-page testimonial attests the
  invite flow from the user side: clients invited to fill out the
  questions online (fx-0246).

## entry: smart-forms.invitation-permissions
- name: Customize Invitation and Access
- named-by-us: no
- description: When inviting a contact, the firm can restrict
  which tabs of the questionnaire the invitee sees by unchecking
  tabs under Customize Invitation and Access, and can include a
  customized invitation message (fx-0039, fx-0020).
- criterion: User unchecks a tab in Customize Invitation and
  Access before sending -> the invitee does not see that tab in
  their questionnaire
- sources: fx-0020, fx-0039
- tier: provisional
- detail: Tab-level permissioning excepts the Green Card Smart
  Form (fx-0039).

## entry: smart-forms.invitation-tracking
- name: Invitation Status Tracking
- named-by-us: yes
- description: Sent invitations are tracked with the invited
  contact, the address used, and a status with its date: Sent,
  Accepted, or Returned for Review; invitations can be resent,
  their links copied, or revoked so the intake is no longer
  accessible (fx-0039, fx-0020). The INSZoom comparison page
  attests the capability on the marketing family: track form
  progress in real time (fx-0245).
- criterion: Client submits the intake for review -> the
  invitation status changes to Returned for Review with the date
- sources: fx-0020, fx-0039, fx-0245
- tier: confirmed
- detail: Portal-shared forms show status Shared to portal, which
  does not update further; revoking portal shares requires
  un-sharing from the portal (fx-0039).

## entry: smart-forms.invitation-settings
- name: Invitation Settings
- named-by-us: no
- description: Firm-level invitation defaults under Settings >
  Invitation Settings: block invited contacts from commenting on
  questions, and set default messages for email and text
  invitations (fx-0039). The same article also files under the
  Firm Settings help category (fx-0096, Phase 3).
- criterion: User sets a default email invitation message in
  Invitation Settings -> subsequent email invitations carry that
  message without retyping
- sources: fx-0039, fx-0096
- tier: provisional

## entry: smart-forms.question-flagging
- name: Question Flagging
- named-by-us: no
- description: Any intake question can be flagged to draw the
  client's attention; a Flagged Questions filter shows only
  flagged questions, and the invitation can be resent for review
  (fx-0031, fx-0020). Clients see the red flag markers on their
  questionnaire (fx-0021). Flag-and-reshare is attested in the
  Smart Forms 3.0 announcement (fx-0045).
- criterion: User flags a question and reshares the intake -> the
  client sees the flagged question marked, and a flagged-only view
  is available
- sources: fx-0020, fx-0021, fx-0031, fx-0041, fx-0045
- tier: confirmed

## entry: smart-forms.question-comments
- name: Question Comments and Mentions
- named-by-us: no
- description: Attorneys, staff, and clients can comment on
  individual intake questions and tag each other with @ mentions
  to hold conversations inside the Smart Form; tagging an
  uninvited client prompts granting access, and tagged parties
  get email notifications with a link to the comment (fx-0028,
  fx-0031, fx-0020, fx-0021). Commenting and tagging inside the
  intake is attested in the Smart Forms 3.0 announcement (fx-0045).
- criterion: User comments on a question and tags a contact with @
  -> the contact receives an email notification linking to the
  comment and can respond in place
- sources: fx-0020, fx-0021, fx-0028, fx-0031, fx-0045
- tier: confirmed

## entry: smart-forms.question-hiding
- name: Question Hiding
- named-by-us: no
- description: Individual intake questions can be marked hidden
  with the eye control so clients and other invitees do not see
  them (fx-0020, fx-0041). Named as a Hide Questions release in
  the Q3 2022 features-roundup video (fx-0277, chapter at 0:57).
- criterion: User hides a question on the intake -> the invitee's
  questionnaire does not show that question
- sources: fx-0020, fx-0041, fx-0277
- tier: confirmed

## entry: smart-forms.intake-search
- name: Searching Smart Forms
- named-by-us: no
- description: A search box over the intake finds questions by
  keyword across all tabs, for both firm users and clients filling
  out the questionnaire (fx-0030, fx-0020, fx-0021). The pricing
  matrix names Searchable Questionnaires as a Forms feature row
  (fx-0108).
- criterion: User enters a keyword in the Smart Form search ->
  matching questions are located without tab-by-tab navigation
- sources: fx-0020, fx-0021, fx-0030, fx-0108
- tier: confirmed

## entry: smart-forms.custom-intakes
- name: Custom Intakes
- named-by-us: no
- description: Firms build unlimited custom questionnaire
  templates under Settings > Custom Intakes, combining
  Docketwise's pre-made questions (whose answers save to the
  contact record) with custom questions and document requests,
  organized into custom tabs; custom intakes are created as Smart
  Forms and shared by email, SMS, link, or portal (fx-0029,
  fx-0026). Marketing attests customized intakes gathering form
  information plus additional questions and document requests in
  one communication (fx-0002).
- criterion: User builds a custom intake template and shares it
  with a client -> the client completes the combined questionnaire
  and pre-made question answers save to their contact record
- sources: fx-0002, fx-0026, fx-0029
- tier: confirmed
- detail: Pre-made intakes (for example Basic Intake, AoS document
  requests) can be imported from a library and then edited
  (fx-0029). Sharing points: on contact creation, on Smart Form
  creation, from the Invite tab, or Share to Portal from the forms
  index (fx-0026).

## entry: smart-forms.custom-questions
- name: Custom Questions
- named-by-us: no
- description: Custom questions can be added to any smart form
  intake on custom tabs; question types are Text, Number, Date,
  Boolean, List, Expiry Date, and Document Request, and answers
  can be saved to custom attributes; previously created questions
  live in a library and can be imported into any other intake
  (fx-0020, fx-0029, fx-0041). Building intakes with custom
  questions is attested in the Smart Forms 3.0 announcement
  (fx-0045).
- criterion: User adds a custom question to a custom tab -> the
  invitee sees and answers it in the intake, and the answer can be
  saved to a custom attribute
- sources: fx-0020, fx-0029, fx-0041, fx-0045
- tier: confirmed
- detail: Custom tabs require unique names; custom tabs are not
  available on the Family Green Card Smart Form; in custom
  intakes, tabs and questions are managed in the custom intake
  settings (fx-0020). Custom intake question formats include
  short-answer text field (about 75 characters) and long-answer
  text area (fx-0029).

## entry: smart-forms.document-requests
- name: Document Requests
- named-by-us: no
- description: Document Request questions collect file uploads
  from clients inside an intake: invitees can upload multiple
  files per request, and uploads save under the contact and
  matter to which the intake is attached (fx-0029, fx-0020).
  Marketing attests requesting documents within the single intake
  communication (fx-0002).
- criterion: Client uploads files against a document request ->
  the files are saved in Docketwise under the associated contact
  and matter
- sources: fx-0002, fx-0020, fx-0029, fx-0196, fx-0197
- tier: confirmed
- detail: Setup path: Settings > Custom Intakes > New Intake+ >
  Custom tab > Add Question, with "Document request" as the
  question type; the client sees the request text and an upload
  box, and the invite goes out via the standard form invitation
  flow (fx-0197). The translation feature does not convert custom
  questions; a request in another language must be authored in
  that language (fx-0197). The Files and Documents help category
  cross-attests client upload through a document request question
  on a custom intake (fx-0196).

## entry: smart-forms.client-file-upload
- name: Client File Upload in Questionnaire
- named-by-us: yes
- description: While completing a questionnaire, a client can
  upload files through More Actions > Upload File, by drag and
  drop or file picker (fx-0021).
- criterion: Client uses Upload File in the questionnaire -> the
  file is attached and available to the firm
- sources: fx-0021
- tier: provisional

## entry: smart-forms.document-sharing
- name: Share Documents
- named-by-us: no
- description: Completed forms, the entire packet, or selected
  parts can be shared with a contact via the Share Documents
  action on the Intake or Review tab, optionally as an editable
  PDF (fx-0020). One-click sharing of the completed packet or any
  part of it is attested in the Smart Forms 3.0 announcement
  (fx-0045).
- criterion: User selects Share Documents, picks a contact, and
  unchecks excluded parts -> the contact receives the selected
  completed documents
- sources: fx-0020, fx-0045
- tier: confirmed

## entry: smart-forms.pdf-values-view
- name: Database Values and PDF Values Views
- named-by-us: no
- description: The Review tab toggles between Database values
  (fields populated from the questionnaire and Docketwise
  database) and PDF values (direct edits on the form itself);
  PDF-view edits do not sync back, and Sync Database Values
  refreshes the form from the database, overwriting manual edits
  (fx-0020). Smart Forms Lite relies on the PDF values view for
  petition-specific fields (fx-0032).
- criterion: User switches to PDF values and edits a field -> the
  edit appears on the form but not in the questionnaire, until a
  database sync overwrites it
- sources: fx-0020, fx-0032
- tier: provisional
- detail: Assemble-tab edits are blocked while toggled to PDF
  values or holding unsaved PDF-view changes (fx-0020).

## entry: smart-forms.form-download-print
- name: Downloading and Printing Forms
- named-by-us: no
- description: Completed forms can be downloaded/printed one by
  one (print icon on the form) or all at once as a single
  combined PDF (Print All), from the Review/Forms tab (fx-0025,
  fx-0035, fx-0020).
- criterion: User clicks Print All -> a single PDF containing
  every form in the packet is produced
- sources: fx-0020, fx-0025, fx-0035
- tier: provisional
- detail: Print Settings offers editable/non-editable PDF, shrink
  PDF font, and N/A autofill options (fx-0025).

## entry: smart-forms.editable-pdf-toggle
- name: Editable or Non-Editable PDF Download
- named-by-us: no
- description: A global Print Settings option controls whether
  downloaded forms are editable PDFs (default) or flattened
  non-editable PDFs (fx-0024, fx-0025).
- criterion: User unchecks Print Editable PDF in Print Settings ->
  subsequently downloaded forms are flattened and cannot be edited
- sources: fx-0024, fx-0025
- tier: provisional

## entry: smart-forms.na-autofill
- name: Autofill Empty Fields with N/A
- named-by-us: no
- description: A Print Settings option fills every empty field
  with N/A on printed forms, matching USCIS guidance that forms
  with empty fields may be rejected (fx-0037, fx-0025).
- criterion: User enables the N/A print setting -> every empty
  field on printed forms reads N/A
- sources: fx-0025, fx-0037
- tier: provisional

## entry: smart-forms.data-import-into-forms
- name: Importing into Forms
- named-by-us: no
- description: Data already in Docketwise -- contacts, addresses,
  and other stored values -- can be imported into form fields
  while preparing a Smart Form or PDF form instead of retyping,
  for example reusing the petitioner's home address as the
  beneficiary's intended U.S. address (fx-0036).
- criterion: User invokes the import control on a form field ->
  the stored value populates the field without retyping
- sources: fx-0036
- tier: provisional

## entry: smart-forms.interpreter-import
- name: Interpreter Import
- named-by-us: no
- description: An interpreter saved as a contact can be imported
  into a Smart Form questionnaire via the lightning-icon import:
  name, physical address, phone, cell, and email populate
  automatically; language and business/organization are entered
  manually, and the organization name auto-populates on
  subsequent imports of the same interpreter (fx-0023, fx-0036).
- criterion: User answers yes to the interpreter question and
  imports an interpreter contact -> the interpreter's stored
  fields populate the form
- sources: fx-0023, fx-0036
- tier: provisional

## entry: smart-forms.i129-answer-import
- name: Import Answers for Form I-129
- named-by-us: no
- description: Answers from a previously prepared I-129 petition
  can be imported into a new I-129 via an Import Answers button on
  the Application section of the Intake tab; import covers the
  Application tab only, not contact-specific information, and
  overwrites prior answers in that tab (fx-0018).
- criterion: User imports answers from an existing I-129 -> the
  new I-129's Application tab is populated with those answers
- sources: fx-0018, fx-0277
- tier: confirmed
- detail: Named as a release in the Q3 2022 features-roundup video
  (fx-0277, chapter at 4:28).

## entry: smart-forms.preparer-population
- name: Preparer Information Population
- named-by-us: no
- description: Firm and preparer information populates the
  preparer fields of all forms; the account-level preparer can be
  any user, and a form-specific preparer can override the default
  per form (fx-0038).
- criterion: User sets a preparer on the account -> preparer
  fields on all printed forms populate with that user's
  information unless a form-specific preparer overrides it
- sources: fx-0038
- tier: provisional

## entry: smart-forms.smart-forms-lite
- name: Smart Forms Lite
- named-by-us: no
- description: A second questionnaire type that contains all
  contact-specific questions (biographical, work and education,
  addresses, family) but not petition-specific questions;
  petition fields are completed directly on the PDF via the PDF
  values view (fx-0032).
- criterion: User opens a Smart Forms Lite questionnaire -> only
  contact-specific questions appear, and petition fields are
  edited on the PDF directly
- sources: fx-0032, fx-0268
- tier: confirmed
- detail: The smart-forms explainer blog post names the capability
  on the release-notes family: "one of the best smart form
  features for immigration law firms, as well as smart forms
  lite" (fx-0268).

## entry: smart-forms.eta9089-conditional-assembly
- name: ETA-9089 with Conditional Appendices
- named-by-us: yes
- description: The ETA-9089 Smart Form includes its appendices and
  final determination, which are added conditionally based on
  intake answers: Appendix A, B, and D and the Final Determination
  each key off specific questionnaire responses (fx-0042). The
  library lists ETA-9089 as including appendices and final
  determination (fx-0044).
- criterion: User answers the ETA-9089 intake trigger questions ->
  the corresponding appendices and final determination are added
  to the prepared form
- sources: fx-0042, fx-0044
- tier: provisional

## entry: smart-forms.form-addenda
- name: Automatic Addendum Pages
- named-by-us: yes
- description: Overflow or additional information beyond a form's
  capacity is placed on automatically added addendum pages; the
  Review tab navigates forms, addenda, and files as distinct
  packet parts (fx-0020), and the ETA-9089 article notes addendum
  pages added for additional information in place of Appendix C
  (fx-0042).
- criterion: User provides more information than a form section
  holds -> addendum pages carrying the overflow are added to the
  packet
- sources: fx-0020, fx-0042
- tier: provisional
- superseded-by: smart-forms.packet-addenda
- detail: Superseded 2026-07-31 ([G1] ruling 5, James): the
  module-wide overflow claim generalized beyond the captured
  attestations (a navigation label plus one form-specific note) --
  the inference crossed goal.md's no-inferred-features line.
  Narrowed to attested scope in the replacement.

## entry: smart-forms.packet-addenda
- name: Addenda in Smart Form Packets
- named-by-us: yes
- description: Addenda are a distinct, navigable packet part
  alongside forms and files on the Review tab (fx-0020). Attested
  generation: the ETA-9089 Smart Form automatically adds addendum
  pages for additional information in place of Appendix C
  (fx-0042). Whether other forms generate overflow addenda is not
  attested by any captured source; fan-out articles may broaden
  this entry if they attest more.
- criterion: User's ETA-9089 intake carries additional information
  in place of Appendix C -> addendum pages holding it are added to
  the packet and navigable as a distinct packet part
- sources: fx-0020, fx-0042
- tier: provisional

## entry: smart-forms.mobile-intake
- name: Mobile-Friendly Questionnaires
- named-by-us: no
- description: Clients can provide form information on any device
  with a browser, including smartphones (fx-0002).
- criterion: Client opens their questionnaire on a smartphone
  browser -> the intake can be completed on that device
- sources: fx-0002
- tier: provisional
