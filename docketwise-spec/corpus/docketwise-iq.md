# module: docketwise-iq

Docketwise's own vocabulary (help-center category "Docketwise IQ", 3
articles, fx-0003). Phase 3 sparse-tail module: full extraction from
the collection page (fx-0201) and articles fx-0202..fx-0204, plus the
three unmined marketing ai-* pages captured as cross-family ground
(fx-0205 /features/ai-for-law-firms/, fx-0206
/features/ai-legal-document-extraction/, fx-0207
/features/ai-legal-writing-tool/). Carve: IQ anchor + access controls
(firm toggle, per-user opt-in) + the writing-assistant family (anchor,
improve, tone, translate, summarize, marketing-only drafting) + the
data-capture family (anchor, document requests, review-and-import).
NAMING NOTE: the help center says "Docketwise IQ" / "DocketWise IQ";
the marketing pages brand the same tools "8am IQ" (writing assistant /
document assistant) after the 8am rebrand -- same product surface,
help vocabulary used for ids.

## entry: docketwise-iq.module-exists
- name: Docketwise IQ
- named-by-us: no
- description: Docketwise IQ is the platform's generative-AI feature
  suite, purpose-built for legal practice management; it currently
  comprises two features, the AI writing assistant and AI data
  capture (fx-0201, fx-0202, fx-0205).
- criterion: User on a qualifying plan invokes a Docketwise IQ tool
  from a supported surface -> AI assistance runs inside Docketwise
  with no external AI tool involved
- sources: fx-0201, fx-0202, fx-0205, fx-0208, fx-0209
- tier: confirmed
- detail: Powered by an OpenAI Large Language Model accessed via the
  OpenAI API platform, not the consumer version of ChatGPT; per
  Docketwise's terms with OpenAI, customer data is not used to train
  OpenAI models, and prompts are customized for law firms and the
  task at hand (fx-0202). Marketing brands the suite "8am IQ"
  (fx-0206, fx-0207). Official promo video "8am IQ for DocketWise:
  AI built for immigration law" (I24AwVwvK3U, 48s, Nov 2025)
  attests intake speedup, English-Spanish translation, and
  manual-data-entry elimination (fx-0208). Reviews-family
  attestation: a practicing immigration lawyer (r/immigrationlaw,
  Nov 2025) confirms their firm uses Docketwise and its AI features
  exist, while reporting they "do not find its AI features
  satisfactory" -- existence attested, satisfaction contested
  (fx-0209).

## entry: docketwise-iq.writing-assistant
- name: DocketWise IQ Writing Assistant
- named-by-us: no
- description: A generative-AI writing tool built into Docketwise
  text surfaces: from the IQ sparkle icon a user applies Improve
  Writing, Change Tone, Translate, or Summarize to drafted text,
  then inserts, discards, copies, or regenerates the AI output
  (fx-0202, fx-0203, fx-0207).
- criterion: User types text in a supported surface, clicks the IQ
  sparkle icon, and picks an assistance option -> AI-generated text
  is offered with Insert / Discard / Copy / Regenerate controls
- sources: fx-0202, fx-0203, fx-0205, fx-0207, fx-0264
- tier: confirmed
- detail: The IQ overview blog post confirms the surface list
  (notes, email messages, Smart Form invitations, comments,
  invoice sharing) and names English-Spanish as the translation
  pair (fx-0264). Available only on Pro and Advanced subscriptions
  (fx-0203). Attested surfaces: Email Messages, Bulk Messaging
  (email and text), Notes, Sharing Smart Form Questionnaires,
  Sharing Invoices, Smart Form Comments; Text Message Conversations
  and Tasks are flagged Coming Soon (fx-0203). Insert replaces the
  user's text with the AI text; Discard removes it; Copy and
  Regenerate act on the generated text (fx-0203).

## entry: docketwise-iq.writing-improvement
- name: Improve Writing
- named-by-us: no
- description: The writing assistant's Improve Writing option
  corrects and polishes drafted text -- grammar, spelling,
  formatting, clarity, and professionalism -- and returns an
  improved version for review (fx-0203, fx-0207).
- criterion: User selects Improve Writing on drafted text ->
  corrected, polished replacement text is generated for review
- sources: fx-0203, fx-0207
- tier: confirmed

## entry: docketwise-iq.tone-adjustment
- name: Change Tone
- named-by-us: no
- description: The writing assistant's Change Tone option rewrites
  drafted text in a tone the user selects from the sparkle menu
  (fx-0203, fx-0207).
- criterion: User mouses over Change Tone and selects a tone -> the
  text is regenerated in the selected tone
- sources: fx-0203, fx-0207
- tier: confirmed

## entry: docketwise-iq.ai-translation
- name: Translate
- named-by-us: no
- description: The writing assistant translates drafted text into a
  selected language directly inside Docketwise, with no external
  translation tool (fx-0203, fx-0205, fx-0207).
- criterion: User mouses over Translate and selects a language ->
  the text is rendered in that language for insert or discard
- sources: fx-0203, fx-0205, fx-0207, fx-0208
- tier: confirmed
- detail: Marketing states support is currently English-to-Spanish
  and Spanish-to-English only (fx-0207), and the official promo
  video says the same ("translate between English and Spanish",
  fx-0208); the help article's menu simply says select the language
  you wish to use (fx-0203) -- both readings kept. Marketing's
  translation surfaces: notes, emails, Smart Form invitations,
  comments, and invoices (fx-0207).

## entry: docketwise-iq.ai-summarization
- name: Summarize
- named-by-us: no
- description: The writing assistant's Summarize option condenses
  written content into a generated summary (fx-0203, fx-0207).
- criterion: User selects Summarize on written content -> a
  generated summary is offered for insert, copy, or discard
- sources: fx-0203, fx-0207
- tier: confirmed
- detail: A Regenerate icon re-runs the generation with the same
  prompt (fx-0203). Surfaced by the Phase 5 reproduction audit;
  admitted in-place per [G2] ruling 2026-08-01.

## entry: docketwise-iq.ai-drafting
- name: AI drafting
- named-by-us: yes
- description: Marketing claims the writing assistant drafts new
  content -- emails, case summaries, and responses -- rather than
  only transforming text the user has already written (fx-0205,
  fx-0207).
- criterion: User invokes the writing assistant to draft a new email
  or response -> AI-generated draft text is produced
- sources: fx-0205, fx-0207
- tier: provisional
- detail: Marketing-only claim, admitted per the decision default.
  The help article's sparkle menu lists only Improve Writing /
  Change Tone / Translate / Summarize, all operating on text the
  user typed first (fx-0203); no draft-from-scratch option is
  help-attested. Both fixtures are the marketing family, so the
  tier carries the skepticism.

## entry: docketwise-iq.firm-ai-access-toggle
- name: Allow all firm users to access AI / IQ feature
- named-by-us: no
- description: Admins enable or disable Docketwise IQ for the whole
  account by checking or unchecking "Allow all firm users to access
  AI / IQ feature" under Settings > User Access (fx-0202, fx-0203).
- criterion: Admin unchecks the AI / IQ option under Settings > User
  Access -> Docketwise IQ tools are unavailable to every user on the
  account
- sources: fx-0202, fx-0203
- tier: provisional

## entry: docketwise-iq.user-ai-optin
- name: Docketwise IQ opt-in
- named-by-us: yes
- description: Docketwise IQ is consent-gated per user: the first
  time a user clicks an IQ feature they must opt in via an
  Understood button, and no data is sent to the LLM unless the user
  agrees to try the feature (fx-0202, fx-0203).
- criterion: User clicks a Docketwise IQ feature for the first time
  -> an opt-in prompt appears, and no data is transmitted to the
  LLM before the user confirms
- sources: fx-0202, fx-0203
- tier: provisional
- detail: The user controls the data inputs, including whether they
  contain personal data; the OpenAI terms prohibit transmitting
  sensitive health information and personal data of minors under 13
  (fx-0202).

## entry: docketwise-iq.data-capture
- name: DocketWise IQ Data Capture
- named-by-us: no
- description: AI extraction of data from uploaded client documents
  -- currently Passport, Green Card / LPR Card, EAD Card
  (Employment Authorization Document), and I-94 -- to automatically
  populate Smart Forms and contact details (fx-0202, fx-0204,
  fx-0205, fx-0206).
- criterion: User uploads a supported document to an AI data-capture
  request -> key fields are extracted and offered to populate the
  Smart Form and contact record
- sources: fx-0202, fx-0204, fx-0205, fx-0206, fx-0208, fx-0261, fx-0264
- tier: confirmed
- detail: Blog posts attest the extraction pipeline (OCR, document
  classification, form population) and the extracted fields per
  document class -- names, birthdates, nationalities, passport
  numbers, A-numbers, expiration dates, category codes, visa types
  (fx-0261); the IQ overview names the same supported document
  types: passports, green cards, I-94s, EAD cards (fx-0264). The official promo video attests "eliminate manual data
  entry with AI" (fx-0208). In closed beta, available only to select accounts, with a
  public waitlist that does not guarantee participation (fx-0204);
  the marketing pages sell it unqualified (fx-0205, fx-0206).
  Marketing brands it "document assistant" / "8am IQ Document
  Assistant" (fx-0205, fx-0206). Handles scanned documents and PDFs
  (fx-0205, fx-0206). The supported-type list is stated as growing
  (fx-0204). Which fields are extracted per document type is not
  publicly enumerated -- not flagged as gap: potentially resolvable
  from the Loom walkthrough embedded in the help article (Loom is
  outside the five source families).

## entry: docketwise-iq.data-capture-document-requests
- name: AI Data Capture Document Request
- named-by-us: no
- description: Data capture runs through a dedicated document-request
  type on Smart Forms: in the form's 2. Documents step the user
  creates a document request, selects the AI Data Capture type, and
  assigns it to a contact involved in the Smart Form; the request
  then appears under that contact's questions in the Document subtab
  (fx-0204, fx-0206).
- criterion: User creates a document request with the AI Data
  Capture type and assigns it to a contact -> the intelligent
  document request appears under that contact's Document subtab,
  ready for upload
- sources: fx-0204, fx-0206
- tier: confirmed
- detail: Requests sit inside Smart Form questionnaires, so the firm
  or the client can upload against them (fx-0204). fx-0206 attests
  the Smart Forms embedding at lower resolution ("built into Smart
  Forms"; upload happens within the existing Smart Form workflow).

## entry: docketwise-iq.data-capture-review-import
- name: Reviewing and Updating Information
- named-by-us: no
- description: Extracted data is never applied silently: after a
  document finishes processing, Review & Edit opens a modal with
  every extracted field, where the user edits fields, ignores fields
  to omit them, and applies changes to the contact and Smart Form
  only via the Confirm & Import button (fx-0204).
- criterion: User clicks Review & Edit on a processed document,
  edits or ignores fields, and clicks Confirm & Import -> only then
  are the contact and Smart Form updated with the reviewed data
- sources: fx-0204
- tier: provisional
- detail: Importing an I-94 additionally saves a new US entry
  (period of stay) under the associated contact (fx-0204).
  Marketing's general claim that all AI outputs are "optional,
  user-reviewed" (fx-0205) is consistent but too generic to attest
  this specific mechanic; not cited as a source.
