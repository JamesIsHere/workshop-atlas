# module: docketwise-leads-crm

Docketwise's own vocabulary (help-center category "Docketwise Leads
CRM", 1 article, fx-0003; feature name "Docketwise Leads"; marketing
nav "CRM"). Phase 3 sparse-tail module: full extraction from the
collection page (fx-0234), article fx-0235, the previously unmined
marketing /features/crm/ page (fx-0236, captured because this module
owns the ground), and the official "Docketwise Leads" video
(fx-0237, abFLWaQc1K4, published 2020-12-21) -- embedded by BOTH
fx-0235 (help) and fx-0236 (marketing), the cross-family anchoring
pattern from module 8. EMBED-DEBT CORRECTION: the fx-0101 debt list
presumed abFLWaQc1K4 was the QuickBooks video -- it is the Leads
video; the other debt id j6KonbWdl6I is the Custom Attributes video
(fx-0238, joined to contacts-and-matters.custom-attributes), so the
QuickBooks webinar was never embedded at all and that debt line is
retired. A Wistia embed on fx-0236 is outside the five families --
logged, not captured (Loom precedent). Carve: module anchor + lead
collection (manual, website form, chatbot) + tracking/engagement
(custom statuses, follow-up reminders, lead emailing) + conversion
(lead-to-client, contact-to-lead) + distribution. One tier-lifting
cross-module join: reports.lead-reports (+fx-0235, +fx-0236 --
promoted provisional -> confirmed).

## entry: docketwise-leads-crm.module-exists
- name: Docketwise Leads
- named-by-us: no
- description: Docketwise Leads is a built-in CRM for immigration
  lawyers: it collects leads from the firm's website or chatbot
  integrations, tracks and engages them with regular contact
  points, and converts them to clients in Docketwise (fx-0234,
  fx-0235, fx-0236, fx-0237).
- criterion: User opens the Leads tab -> the firm's leads are
  listed with tools to collect, track, engage, and convert them
- sources: fx-0234, fx-0235, fx-0236, fx-0237, fx-0279
- tier: confirmed
- detail: Pro/Advanced-gated: unlocking Leads CRM requires a Pro or
  Advanced subscription (fx-0235). Leads support most client
  operations -- intakes, events, tasks, and notes can be attached
  to a lead (fx-0235). A customer switch-story video names CRM
  among the platform's pillars: "form completion, CRM, and
  necessary workflow integrations" (fx-0279). Marketing bills it as "the first CRM
  specifically designed for immigration lawyers" (fx-0235,
  fx-0236); the official video attests the website-to-Docketwise
  automation and the track/convert feature set (fx-0237, 248s).

## entry: docketwise-leads-crm.manual-lead-creation
- name: Manually Creating a Lead
- named-by-us: no
- description: Leads are created manually from the Leads tab via
  the Add Lead button (fx-0235).
- criterion: User clicks Add Lead on the Leads tab and enters the
  lead's information -> the lead is created in the Leads tab
- sources: fx-0235
- tier: provisional

## entry: docketwise-leads-crm.website-lead-form
- name: Embeddable Contact Form
- named-by-us: no
- description: A link or button snippet copied from Leads > Collect
  Leads embeds on the firm's website; visitors who click it get a
  contact form in a new tab, and on submit they are added as a Lead
  in Docketwise automatically (fx-0235, fx-0236, fx-0237).
- criterion: Visitor submits the firm's embedded contact form ->
  they appear as a new Lead in the firm's Leads tab without staff
  action
- sources: fx-0235, fx-0236, fx-0237
- tier: confirmed
- detail: Snippet offered in link and button variants (fx-0235).
  Marketing brands the flow Pipeline Automation / Website
  Integration (fx-0236).

## entry: docketwise-leads-crm.chatbot-lead-collection
- name: Chatbot Integration (YoTengoBot)
- named-by-us: no
- description: Leads are also collected through chatbot
  integrations -- marketing names YoTengoBot over Facebook
  Messenger, WhatsApp, and SMS (fx-0235, fx-0236).
- criterion: Prospective client engages the firm's chatbot channel
  -> their information arrives as a Lead in Docketwise
- sources: fx-0235, fx-0236
- tier: confirmed
- detail: Help attests chatbot collection generically ("via our
  chatbot integrations", fx-0235); the named vendor and channel
  list are marketing-attested (fx-0236).

## entry: docketwise-leads-crm.custom-lead-statuses
- name: Track Leads Across Custom Statuses
- named-by-us: no
- description: Firms define their own set of lead statuses (e.g.
  Visitor, Contacted, Scheduled Consultation, Converted to Client)
  via More Actions > Manage Lead Statuses, and filter the Leads tab
  by status with the Lead Status button (fx-0235).
- criterion: User creates lead statuses and assigns one to a lead
  -> the Leads tab filters by that status
- sources: fx-0235
- tier: provisional

## entry: docketwise-leads-crm.followup-reminders
- name: Set Reminders for Following Up with Leads
- named-by-us: no
- description: Each lead carries a contact frequency (default
  bi-weekly on creation); when the interval elapses the lead is
  marked due and appears in the Due Leads tab, and clicking
  Contacted returns it to All Leads until the next cycle (fx-0235,
  fx-0236).
- criterion: A lead's contact frequency elapses -> the lead appears
  in the Due Leads tab until marked Contacted
- sources: fx-0235, fx-0236
- tier: confirmed
- detail: Frequency is adjustable per lead (e.g. monthly or longer
  as a lead cools) (fx-0235).

## entry: docketwise-leads-crm.lead-emailing
- name: Email Leads with Custom Templates
- named-by-us: no
- description: Leads are emailed from the CRM via More Actions >
  Email Lead, drafting from scratch or importing and editing an
  email template; templates are managed under More Actions > Manage
  Email Templates (fx-0235). The marketing features index attests
  the capability: email your leads directly from Docketwise,
  utilizing email templates to automate outreach (fx-0244).
- criterion: User selects Email Lead on a lead and sends a drafted
  or template-based email -> the email is sent to the lead from
  Docketwise
- sources: fx-0235, fx-0244
- tier: confirmed

## entry: docketwise-leads-crm.lead-conversion
- name: Convert Leads to Clients
- named-by-us: no
- description: A won lead converts to a contact via More Actions >
  Convert to Client, moving it from the Leads tab to the Contacts
  tab; conversions are tracked in lead reports (fx-0235, fx-0236,
  fx-0237).
- criterion: User selects Convert to Client on a lead -> the record
  moves to the Contacts tab and the conversion is countable in lead
  reports
- sources: fx-0235, fx-0236, fx-0237
- tier: confirmed

## entry: docketwise-leads-crm.contact-to-lead-conversion
- name: Convert Contacts to Leads
- named-by-us: no
- description: A contact converts back to a lead from the Contacts
  tab via More Actions > Convert to Lead (fx-0235).
- criterion: User selects Convert to Lead on a contact -> the
  record moves from the Contacts tab to the Leads tab
- sources: fx-0235
- tier: provisional
- superseded-by: docketwise-leads-crm.contacts-to-leads
- detail: Superseded 2026-08-01 ([G2] ruling, James): "converts
  back to a lead" implied the contact was previously a lead; the
  fixture sentence ("you can also convert Contacts to Leads")
  states no such precondition. Flagged by the Phase 5
  reproduction audit. Pro/Advanced gating carried forward.

## entry: docketwise-leads-crm.contacts-to-leads
- name: Convert Contacts to Leads
- named-by-us: no
- description: Any contact can be converted to a lead from the
  Contacts tab via More Actions > Convert to Lead (fx-0235).
- criterion: User selects Convert to Lead on a contact -> the
  record moves from the Contacts tab to the Leads tab
- sources: fx-0235
- tier: provisional
- detail: The option is visible only on Pro or Advanced
  subscriptions (fx-0235).

## entry: docketwise-leads-crm.lead-distribution
- name: Distribute Leads and Track Activity
- named-by-us: no
- description: Leads are distributed among team members with
  activity tracking to identify where additional support is needed
  (fx-0236).
- criterion: User assigns leads across team members -> each lead
  shows its owner and activity is trackable per lead
- sources: fx-0236
- tier: provisional
- detail: Marketing-only attestation; help's article does not
  describe distribution mechanics (fx-0236).
