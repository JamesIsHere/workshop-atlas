# module: invoicing-and-trust-accounting

Docketwise's own vocabulary (help-center category "Invoicing and
Trust Accounting", 27 articles, fx-0003). Phase 3 fan-out module:
full extraction from 27 help articles (fx-0051..fx-0077), collection
page fx-0050, release-note blog post fx-0078, and marketing
integration pages fx-0079 (LawPay; fx-0080 held for the Integrations
module, see exclusion log). No dedicated marketing feature page
exists for this module; the marketing family reaches it only through
the LawPay page, so most trust-side entries cap at provisional by
design ([G1] ruling 7).

## entry: invoicing-and-trust-accounting.module-exists
- name: Invoicing and Trust Accounting
- named-by-us: no
- description: The product carries an invoicing and trust accounting
  capability with a dedicated 27-article help category (fx-0003,
  fx-0050); invoicing updates are announced on the product blog
  (fx-0078). Decomposed into this file's entries in Phase 3.
- criterion: User opens the billing area -> invoicing and trust
  accounting functions are available as a distinct module
- sources: fx-0003, fx-0050, fx-0078, fx-0081
- tier: confirmed
- detail: An official webinar "Invoicing and Trust Accounting"
  covers the module end to end: bank accounts, default invoice
  settings, bills and trust requests, disbursements, billable time
  entries, LawPay features, flat-fee and time-and-expense billing
  with a retainer (fx-0081).

## entry: invoicing-and-trust-accounting.invoice-creation
- name: Invoices (Bills and Trust Requests)
- named-by-us: no
- description: Users create invoices from the Create New button,
  choosing between two invoice types: a Bill, whose payments are
  recorded into an operating account, or a Trust Request, whose
  payments are recorded into a trust account; each invoice is
  assigned a client and optionally a matter (fx-0065, fx-0070,
  fx-0071). The created invoice opens in the Invoice Builder, where
  charges and per-invoice settings are managed (fx-0065, fx-0070).
- criterion: User clicks Create New, selects Invoice, chooses Bill
  or Trust Request, and assigns a client -> an invoice of the chosen
  type is created and opens in the Invoice Builder for charges and
  settings
- sources: fx-0061, fx-0065, fx-0070, fx-0071, fx-0078, fx-0081,
  fx-0157
- tier: confirmed
- detail: Charges are Service or Expense fees with description,
  amount, and date, and can be associated to a specific matter
  (fx-0065); dates on charges and time entries were added September
  2021 and are editable past or future (fx-0078). The per-invoice
  Invoice Settings tab covers preparer, discounts, issued and due
  dates, invoice number, email reminders, customizable footer, color
  scheme, firm logo, and payment plan (fx-0061, fx-0065). Bank
  accounts must be set up before payments can be recorded (fx-0065).
  When an invoice's balance reaches zero it moves to the Paid
  Invoices tab (fx-0070, fx-0071).

## entry: invoicing-and-trust-accounting.trust-requests
- name: Trust Requests
- named-by-us: no
- description: A Trust Request is the invoice type that requests
  trust funds from a client; the funds are held at the client level
  or the matter level, and recorded payments deposit into a trust
  account (fx-0061, fx-0065, fx-0071). An official video "Trust
  Requests in Docketwise" attests requesting trust funds with
  invoices, and the module webinar covers trust request basics
  (fx-0082, fx-0081).
- criterion: User creates a Trust Request invoice and records a
  payment -> the funds are recorded into the selected trust account
  at the chosen client or matter level
- sources: fx-0061, fx-0065, fx-0071, fx-0081, fx-0082
- tier: confirmed
- detail: SOURCE CONFLICT recorded per goal.md decision default:
  fx-0071 states trust requests "can only be paid via Direct
  Transfer", while fx-0061 and fx-0065 list credit card or eCheck on
  file, sending to the client to pay, and payment plans (each
  requiring the LawPay integration) as collection options for trust
  requests. Both readings kept with provenance; not averaged. The
  conflict is confined to this payment-method sub-behavior; the
  entry's criterion (trust request exists and records funds into a
  trust account) is uncontested across three families, so the tier
  reflects the criterion and the conflict lives here and in the gap
  note. fx-0071 also notes reminders stop and the trust request
  moves to Paid Invoices at zero balance.
- gap: what: whether trust requests accept online card or eCheck
  payment via LawPay or only direct payment (the captured help
  articles conflict); source: trial-account billing flow (live
  product).

## entry: invoicing-and-trust-accounting.trust-bank-accounts
- name: Trust and Operating Accounts
- named-by-us: no
- description: Firms maintain unlimited trust accounts alongside
  operating accounts under Settings > Bank Accounts; a new account
  is created with account type Trust (fx-0069, fx-0070, fx-0071).
  Each trust account lists its balance and transactions, and a
  client's or matter's trust funds are viewable from a Trust Account
  tab on their overview page (fx-0069). The module webinar covers
  setting up bank accounts (fx-0081).
- criterion: User creates a bank account of type Trust under
  Settings > Bank Accounts -> the account is available for trust
  transactions and shows its own balance and transaction list
- sources: fx-0065, fx-0069, fx-0070, fx-0071, fx-0081
- tier: confirmed
- detail: Per-account transaction rows show transaction date,
  client, matter, type, and amount; transaction types include trust
  requests, trust transfers, and disbursements (fx-0069).

## entry: invoicing-and-trust-accounting.trust-ledger
- name: Trust Accounting Ledger
- named-by-us: no
- description: A dedicated Trust Accounting Ledger shows an overview
  of trust balances in three tabs -- firm-level bank accounts,
  matter-level sub-accounts, and client-level sub-accounts -- and
  clicking any account row opens a detailed transactions view with a
  granular breakdown of that account's trust transactions (fx-0053).
- criterion: User opens the Trust Accounting Ledger and clicks a
  trust account row -> a detailed transactions view lists that
  account's transactions with date, type, description, and amount
- sources: fx-0053
- tier: provisional
- detail: Matter and client tabs list only matters or clients with a
  drafted trust request or trust transactions at that level; both
  the overview tabs and the transactions view carry filters (balance
  and client on the overview; date, type, description, client,
  amount, and payment DW ID on transactions) (fx-0053).

## entry: invoicing-and-trust-accounting.trust-transfer-payment
- name: Paying an Invoice with a Trust Transfer
- named-by-us: no
- description: A bill can be paid from client trust funds: Record
  Payment with payment type Trust Transfer, selecting whether funds
  come from the client level or matter level, the source trust
  account (available amount displayed), the destination account,
  payment date, and amount (fx-0066, fx-0070).
- criterion: User records a payment of type Trust Transfer from a
  funded trust account -> the bill is paid and the amount is debited
  from the selected trust funds
- sources: fx-0065, fx-0066, fx-0070
- tier: provisional

## entry: invoicing-and-trust-accounting.trust-disbursements
- name: Disbursing Funds from a Trust Account
- named-by-us: no
- description: Trust funds can be disbursed for offline payments to
  third parties, such as USCIS filing fees, via Disburse Funds on
  the client's or matter's Trust Acct tab; the disbursement is
  automatically reflected as a debit against available funds
  (fx-0074). Disbursements appear as a transaction type in trust
  account reviews and the ledger (fx-0053, fx-0069), and the module
  webinar covers disbursing funds from a trust account (fx-0081).
- criterion: User clicks Disburse Funds on a client or matter Trust
  Acct tab and records a disbursement -> available trust funds
  decrease by the disbursed amount and the transaction is listed
- sources: fx-0053, fx-0069, fx-0074, fx-0081
- tier: confirmed

## entry: invoicing-and-trust-accounting.direct-payment-recording
- name: Recording a Direct Payment
- named-by-us: no
- description: Payments received outside the platform (e.g. cash or
  check) are recorded on a bill or trust request via Record Payment
  with payment type Direct Payment, entering the amount and an
  optional note (fx-0062, fx-0070).
- criterion: User records a Direct Payment on an invoice -> the
  invoice balance decreases by the recorded amount
- sources: fx-0062, fx-0065, fx-0070
- tier: provisional
- detail: Recording a payment asks for payment type, destination
  account, payment date, payment amount, and optional description
  (fx-0070).

## entry: invoicing-and-trust-accounting.payment-editing
- name: Edit Payments on Invoices
- named-by-us: no
- description: Payments previously recorded on bills and trust
  requests can be edited after the fact by opening the payment from
  the invoice and saving the changed values (fx-0077); the edit
  control also appears as a pencil icon next to the payment
  (fx-0055, fx-0057).
- criterion: User opens a recorded payment on an invoice and changes
  the amount -> the payment and the invoice balance update
- sources: fx-0055, fx-0057, fx-0077
- tier: provisional

## entry: invoicing-and-trust-accounting.payment-refunds
- name: Refunding Payments on Bills
- named-by-us: no
- description: A recorded payment can be marked as refunded by
  editing the payment and toggling Refund this payment, with an
  optional internal note for reporting; the invoice then reflects
  the refund (fx-0055).
- criterion: User toggles Refund this payment on a recorded payment
  and saves -> the invoice reflects the refunded payment
- sources: fx-0055
- tier: provisional
- detail: Refunds are full-amount only; a partial refund is achieved
  by refunding the payment and creating a new backdated payment for
  the realized amount. A payment recorded via the LawPay integration
  automatically triggers the associated refund in LawPay. Refunds
  are not automatically reflected in QuickBooks Online and must be
  updated there manually (fx-0055).

## entry: invoicing-and-trust-accounting.payment-charge-association
- name: Associating Payments to Specific Invoice Charges
- named-by-us: no
- description: A payment on an invoice can be associated with a
  specific charge on that invoice, either while recording the
  payment or afterwards by editing it; once associated, an entry
  appears under the charge detailing the payment date and amount
  (fx-0057).
- criterion: User selects an Associated Invoice Charge while
  recording or editing a payment -> the charge displays an entry
  with the payment date and payment amount
- sources: fx-0057
- tier: provisional
- detail: A payment larger than the charge cannot be broken down and
  associated across multiple charges (fx-0057).

## entry: invoicing-and-trust-accounting.online-card-payment
- name: Online Invoice Payment via LawPay
- named-by-us: yes
- description: With a LawPay account and the LawPay integration
  active, clients pay invoices online by credit card or eCheck: an
  invoice shared by email or SMS carries a Pay Online button, and an
  invoice shared to the client portal carries a Pay button, each
  leading to a secure payment page inside the platform (fx-0060,
  fx-0067). A card or eCheck on file can also be charged directly
  (fx-0061, fx-0065). Marketing attests secure online payments that
  sync automatically with case data (fx-0079).
- criterion: Client opens a shared invoice and completes the payment
  form -> the payment is processed by credit card or eCheck and
  recorded against the invoice
- sources: fx-0060, fx-0065, fx-0067, fx-0076, fx-0079, fx-0186
- tier: confirmed
- detail: The client-portal guide attests the client side: a Pay
  button on a shared invoice opens a secure payment form for credit
  card or eCheck, and a download icon fetches the invoice (fx-0186).
  The client can download a PDF copy of the invoice from the
  email link or the portal (fx-0067). A firm setting automatically
  sends clients a receipt when a payment is made via LawPay
  (fx-0076). The LawPay marketing page claims 1:1 expense-to-case
  tracking and invoices, payments, and case data connected in real
  time (fx-0079).

## entry: invoicing-and-trust-accounting.invoice-sharing
- name: Invoice Sharing
- named-by-us: yes
- description: An invoice is shared from the Invoice Builder's Share
  action by email or SMS text message, by printing, or to the
  client's portal (fx-0060, fx-0067, fx-0070). The receiving contact
  is chosen when the invoice is created and need not be the matter's
  primary contact -- a spouse, family member, sponsoring company, or
  other third party with a valid email address can receive and pay
  it (fx-0068). The marketing features index attests invoice
  sharing: share invoices with automated reminders (fx-0244).
- criterion: User clicks Share on an invoice and selects email or
  SMS -> the chosen contact receives the invoice with a link to view
  or download it
- sources: fx-0060, fx-0067, fx-0068, fx-0070, fx-0071, fx-0244
- tier: confirmed
- detail: The share window confirms the contact's information before
  sending (fx-0068). The invoice email shows the firm's logo in
  place of the default when configured (fx-0067). Portal sharing
  requires the client to have a client portal set up (fx-0067; the
  portal itself is the Client Portal module).

## entry: invoicing-and-trust-accounting.payment-reminders
- name: Invoice Reminders
- named-by-us: no
- description: Shared invoices can send automatic reminders with a
  copy of the invoice to the client on a configurable frequency
  until the balance is paid in full or reminders are turned off
  (fx-0060, fx-0068, fx-0076). The marketing features index attests
  both sharing and reminders: share invoices with automated
  reminders to speed up collection (fx-0244).
- criterion: User enables reminders when sharing an invoice -> the
  client receives recurring reminder messages until the invoice
  balance reaches zero
- sources: fx-0060, fx-0068, fx-0070, fx-0071, fx-0076, fx-0244
- tier: confirmed
- detail: Reminders stop automatically once the balance is reduced
  to zero (fx-0070, fx-0071). The default reminder frequency in days
  is a firm-level invoice setting (fx-0076). Payment-plan
  installment reminders are a separate cadence (see payment-plans).

## entry: invoicing-and-trust-accounting.bulk-invoice-sharing
- name: Bulk-Sharing Invoices
- named-by-us: no
- description: From the invoices index, multiple selected invoices
  are shared at once via More Actions > Share Invoice(s), by email
  or text message, in one of two modes: all invoices to one specific
  contact (delivered as a zip file; typical for company contacts
  sponsoring multiple foreign nationals), or each invoice to its own
  respective contact (each receives a link to download their
  individual invoice) (fx-0056).
- criterion: User selects multiple invoices and shares them in a
  chosen mode -> every selected invoice is delivered per that mode
- sources: fx-0056
- tier: provisional
- detail: The article's two step-by-step sections carry headings
  swapped against their step lists (each section's steps select the
  other mode's option); both modes and both step lists are attested,
  the pairing is the ambiguity (fx-0056).

## entry: invoicing-and-trust-accounting.bulk-invoice-download
- name: Bulk-Downloading Invoices
- named-by-us: no
- description: From the invoices index, multiple selected invoices
  are downloaded at once via More Actions > Download Invoice(s),
  producing a zip file containing the selected invoices (fx-0056).
- criterion: User selects multiple invoices and clicks Download
  Invoice(s) -> a zip file containing the selected invoices
  downloads
- sources: fx-0056
- tier: provisional

## entry: invoicing-and-trust-accounting.automatic-late-fees
- name: Automatic Late Fees on Invoices
- named-by-us: no
- description: Invoices can automatically apply late fees -- a fixed
  dollar amount or a percentage of the outstanding balance -- when
  the balance is not fully paid by the invoice due date; fees are
  applied overnight, and an optional recurring late fee repeats at a
  set frequency in days until the balance is paid or the option is
  disabled (fx-0058).
- criterion: User enables automatic late fees on an invoice that
  passes its due date unpaid -> the late fee charge is applied to
  the invoice automatically
- sources: fx-0058, fx-0076
- tier: provisional
- detail: Configured per individual invoice (Invoice Settings tab
  slider) or as a firm default in Settings > Invoice Settings, with
  the firm default applying to invoices created thereafter and
  overridable per invoice (fx-0058, fx-0076).

## entry: invoicing-and-trust-accounting.saved-charges
- name: Saved Charges for Invoices
- named-by-us: no
- description: Commonly-used flat-rate charges are saved at the firm
  level with a description, amount, and Service or Expense type, and
  imported into an invoice in bulk from the Invoice Charges tab
  (fx-0059, fx-0076). Publicly announced September 2021 with
  examples such as Consultation and I-485 Filing Fees (fx-0078).
- criterion: User clicks Saved Charges in an invoice's charges tab
  and selects saved charges -> the selected charges import into the
  invoice
- sources: fx-0059, fx-0076, fx-0078, fx-0083
- tier: confirmed
- detail: Saved charges are created under Settings > Invoice
  Settings; they can be added to Bills only, not Trust Requests
  (fx-0059).

## entry: invoicing-and-trust-accounting.payment-plans
- name: Payment Plans
- named-by-us: no
- description: An invoice balance can be scheduled into recurring
  installments instead of one lump sum, configured with a frequency,
  installment amount, and start date from the invoice's Payment Plan
  option (fx-0072). Without LawPay, plans send installment
  reminders; with the LawPay integration, clients can pay an
  installment directly from the reminder, or Automatic Payments can
  debit the client's card or account each time an installment is due
  (fx-0072). The help category tagline is "Charge your clients'
  credit cards on recurring payment plans" (fx-0050). The INSZoom
  comparison page attests the capability on the marketing family:
  flexible billing including payment plans and installment billing
  (fx-0245).
- criterion: User activates a Payment Plan on an invoice with a
  frequency, installment amount, and start date -> the balance is
  billed on the recurring installment schedule
- sources: fx-0050, fx-0054, fx-0061, fx-0065, fx-0070, fx-0072, fx-0245, fx-0271
- tier: confirmed
- detail: Non-automatic plans remind the client 7 days before an
  installment is due, on the due day, and 7 days after if unpaid;
  with LawPay those reminders include a pay option, and accepted
  payment forms (credit card, eCheck) are customizable (fx-0072).
  Automatic Payments require the LawPay integration (fx-0072).
  The 2024 year-in-review names Payment Plans 2.0 -- customized
  recurring plans including options that do not require
  auto-charging (fx-0271).
  Delinquent plans are tracked through invoice reports using the
  Payment Plan Status, Late Status, and Overdue Balance fields
  (fx-0054; the report engine is the Reports module).

## entry: invoicing-and-trust-accounting.time-tracking
- name: Time Tracking
- named-by-us: no
- description: Time spent on client work is tracked as time entries,
  created either in real time with a timer widget at the top of the
  dashboard or manually with an entered duration, each carrying
  duration, date, description, contact, and matter (fx-0064,
  fx-0073). Entries are viewable and editable from the contact
  overview, the matter overview, or a firm-wide time entries index,
  each with filters (fx-0073). Dates on time entries were publicly
  announced September 2021 (fx-0078).
- criterion: User starts the timer widget, stops it, and saves the
  entry -> a time entry with the recorded duration is stored against
  the chosen contact or matter
- sources: fx-0064, fx-0073, fx-0078, fx-0081
- tier: confirmed
- detail: Durations are recognized in hour and minute formats such
  as 2h, 36m, 2.8h, and 5.5m (fx-0064). A stopped timer can be
  resumed from recent entries, from the entry lists, or via Save
  Entry and Start Timer (fx-0073).

## entry: invoicing-and-trust-accounting.time-entry-invoice-import
- name: Importing Time Entries to an Invoice
- named-by-us: no
- description: Time entries for a contact or matter are imported
  into an invoice from the Invoice Charges tab via the Time Entries
  button, checking the entries to bill; imported entries appear on
  the invoice under Professional Services (fx-0063, fx-0073). The
  module webinar covers creating time entries which can be billed
  and billing by time and expenses (fx-0081).
- criterion: User selects time entries in the invoice's Time Entries
  picker and imports them -> the entries appear as Professional
  Services charges on the invoice
- sources: fx-0063, fx-0065, fx-0073, fx-0081
- tier: confirmed
- detail: No hourly-rate mechanism is attested in the captured
  articles; how a time entry's duration becomes a charge amount is
  not publicly documented (not flagged as gap: potentially
  resolvable from uncaptured public sources such as videos).

## entry: invoicing-and-trust-accounting.invoice-translation
- name: Translating Invoices
- named-by-us: no
- description: An invoice can be displayed and sent in another
  language by selecting a language from the invoice's settings; once
  toggled, the invoice instantly updates for both the firm and the
  client (fx-0052).
- criterion: User selects Spanish under the invoice's Language
  option -> the invoice displays in Spanish for firm and client
- sources: fx-0052, fx-0271
- tier: confirmed
- detail: Spanish is the only language available at capture time
  (fx-0052). Not translated: charge descriptions, discount
  descriptions, late fees, invoice descriptions, and custom email or
  message text sent with the invoice (fx-0052). The 2024
  year-in-review names Translate Invoices to Spanish among the
  year's released features (fx-0271).

## entry: invoicing-and-trust-accounting.invoice-access-permissions
- name: Restrict Invoice Access
- named-by-us: no
- description: Per-user invoice permissions are set under Settings >
  User Access with three levels: Unlimited Access; Limited Access
  (cannot edit or delete other users' invoices); and No Access
  (cannot view, create, edit, or delete invoices) (fx-0075).
- criterion: Admin sets a user's Invoice Permissions to No Access ->
  that user cannot view, create, edit, or delete invoices
- sources: fx-0075
- tier: provisional
- detail: Invoicing and billing widgets can also be hidden from the
  dashboard firm-wide via Settings > Dashboard > Hide invoices and
  billing (fx-0075).

## entry: invoicing-and-trust-accounting.default-invoice-settings
- name: Global Invoice Settings
- named-by-us: no
- description: Firm-wide default invoice settings under Settings >
  Invoice Settings cover saved charges, global invoice numbering,
  automatic late fees, invoice display (footer, color scheme, firm
  logo, hiding email/phone/address in the header, showing invoice ID
  and payment descriptions), invoice reminder frequency, automatic
  due dates, a default preparer, and automatic LawPay receipts
  (fx-0076). Firm-information display customization was publicly
  announced September 2021 (fx-0078).
- criterion: Firm changes a default invoice setting -> invoices
  created thereafter reflect the new default, overridable on the
  individual invoice
- sources: fx-0076, fx-0078, fx-0081
- tier: confirmed
- detail: Automatic due dates set invoices due on the 15th, the last
  day of the month, or whichever is sooner (fx-0076). The color
  scheme applies to the business name, associated matter, and
  outstanding balance (fx-0076). The invoice ID, when shown, is
  searchable from the invoice index (fx-0076).

## entry: invoicing-and-trust-accounting.global-invoice-numbering
- name: Global Invoice Numbering
- named-by-us: no
- description: Invoice numbering runs per-client by default (each
  client's invoices number up from 1); enabling Global Invoice
  Numbering gives each new invoice a unique number incrementing
  across all of the firm's clients, with a configurable starting
  number (fx-0076, fx-0078).
- criterion: Firm enables global invoice numbering -> each new
  invoice receives the next firm-wide invoice number instead of a
  per-client number
- sources: fx-0076, fx-0078
- tier: confirmed
- detail: Enabling does not renumber invoices created prior; the
  next invoice numbers up from the total created by the firm, and
  the beginning number is editable in Invoice Settings (fx-0076,
  fx-0078).
