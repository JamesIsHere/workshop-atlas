## case-tracking.task-reference-date-due-dates
- description: In addition to duration-based due dates (a fixed number of days after a task is created), Docketwise lets you set a task's due date based on a "reference date" - a specific immigration-related date stored at the contact level, such as date of birth or US status expiry date. When configuring a task in a task list, you select the reference date from a dropdown and specify a number of days before or after it for the due date to be calculated.
- evidence-note: fx-0213.html explicitly labels this "Setting Automatic Due Dates Using Reference Dates (Alpha)" and notes it is an Alpha feature not available to all customers, and that reference dates are currently only available at the contact level (not custom attributes or Matter attributes).

## client-portal.hr-portal-employee-management
- description: The HR Portal lets a firm indicate a corporate client's employees (by creating new contacts or linking existing ones under the contact's Employees tab), then add or remove those employees from the client's HR Portal via bulk actions ("Share to Portal"), so the employees and their related Tasks, Forms, USCIS Receipts, Invoices, and Files/matter status can be viewed by the corporate client and simultaneously shared to each foreign national employee's own portal.
- evidence-note: fx-0188.html (help article "HR Portal") is the primary source, with detailed steps for "Adding Employees to a Company," "Adding Employees to the HR Portal," "Removing Employees from the HR Portal," and "Searching for Employees in the HR Portal." fx-0192.html is a YouTube video whose description corroborates at a higher level: "The HR Portal enables you to share foreign national employees to your client's portal along with their forms, receipts, documents, tasks and more."

## client-portal.portal-two-factor
- description: Docketwise's client portal (including the HR Portal variant) supports two-factor authentication, which a firm can enable or disable per contact from the Portal tab. Once enabled, the client/employee must use an authenticator app (e.g. Google Authenticator, Microsoft Authenticator, Authy, Duo) to scan a QR code and enter an OTP/secure login code as part of logging into their portal.
- evidence-note: fx-0186.html (client-facing "Accessing & Using Your Portal as a Client") describes the client-side setup flow (scan QR code, enter OTP). fx-0188.html (HR Portal article) and fx-0191.html (Client Portal article) both describe the firm-side "Enabling Two-Factor Authentication" / "Disabling Two-Factor Authentication" steps via the contact's Portal tab.

## contacts-and-matters.matter-creation
- description: A new matter is created by clicking "Create New" on the dashboard, selecting "Matter" from the dropdown, and filling out matter details on the creation page: the associated contact and matter name are required, with optional fields for description, matter type/status, preference category/priority date, and firm member assignee (with an option to auto-assign related tasks to that assignee). Clicking "Create Matter" finalizes it.
- evidence-note: fx-0148.html ("Creating a Matter" help article) is the direct source. fx-0142.html is only the "Contacts and Matters" collection index page, which lists "Creating a Matter" as a one-line link description ("Learn how to quickly set up a new matter and assign crucial details for your case") but contains no procedural detail itself.

## docketwise-iq.ai-summarization
- description: "Summarize" is one of the generative-AI writing-assistance options in the DocketWise IQ Writing Assistant (alongside Improve Writing, Change Tone, and Translate), accessed via a sparkle icon in text fields such as notes, email messages, bulk messaging, and Smart Form questionnaires/comments. Selecting Summarize generates AI text that can be inserted to replace what was written, discarded, copied, or regenerated.
- evidence-note: fx-0203.html (help article "DocketWise IQ Writing Assistant") lists "Summarize" as one of the writing-assistance functions and gives the UI steps. fx-0207.html (marketing page) corroborates at a higher level, referring to the tool as "8am IQ Writing Assistant" and stating it can "Summarize notes, translate content, and edit your writing faster, right inside Docketwise."

## docketwise-leads-crm.contact-to-lead-conversion
- description: Docketwise lets you convert an existing Contact into a Lead: from the Contacts tab, selecting the More Actions icon on a contact and choosing "Convert to Lead" moves that record into the Leads CRM. The fixture notes this option is only visible on a Docketwise Pro or Advanced subscription.
- evidence-note: fx-0235.html ("Docketwise Leads CRM" help article) states this in one sentence near the end of the "Convert Leads to Clients" section: "you can also convert Contacts to Leads by navigating to your Contacts tab, selecting the More Actions icon and selecting 'Convert to Lead.'" No further detail (e.g., what data carries over) is given.

## docketwise-leads-crm.custom-lead-statuses
- description: Docketwise Leads lets a firm define its own set of custom statuses (e.g. Visitor, Contacted, Scheduled Consultation, Converted to Client) via "More Actions > Manage Lead Statuses," and then filter the Leads list by status using the "Lead Status" button, in order to track a lead's progress from visitor to client.
- evidence-note: fx-0235.html, section "Track Leads Across Custom Statuses" (matching the entry name exactly), is the sole and direct source.

## files-and-documents.file-printing
- description: A file stored in Docketwise can be printed directly from the platform without first downloading it: mousing over the file and clicking the printer icon opens the file in a new browser tab, from which it can be printed.
- evidence-note: fx-0195.html, section "Printing Files" within the "Files and Folders" help article, is the sole and direct source; the steps given are exactly: locate the file, mouse over it, click the printer icon, print from the newly opened tab.

## internal-chat.group-chats
- description: Docketwise Chat lets firm members create group chats with multiple colleagues: from the Chat area, clicking "Create Group," entering a title, and selecting colleagues to include (via + / - icons) creates the group once an initial message is sent. Per the fixture, a group's name and members cannot be edited after creation.
- evidence-note: fx-0231.html ("Docketwise Chat" help article), section "Group Chats," is the sole and direct source.

## invoicing-and-trust-accounting.automatic-late-fees
- description: Docketwise can automatically apply late fees to an invoice whose balance is not fully paid by its due date, run overnight, and can optionally apply recurring late fees at a configurable day-frequency until the balance is paid or the option is disabled. The fee amount can be set as either a fixed dollar amount or a percentage of the outstanding balance, configurable on an individual invoice or as a firm-wide default in Invoice Settings.
- evidence-note: fx-0058.html ("Automatic Late Fees on Invoices" help article) is the primary, fully detailed source. fx-0076.html ("Global Invoice Settings" help article) corroborates the same mechanics within its "Set up Automatic Late Fees" section as part of firm-wide default invoice settings.

## invoicing-and-trust-accounting.invoice-translation
- description: Docketwise can translate an invoice for the client's preferred language by toggling a Language option in Invoice Settings, after which the invoice instantly displays in that language for both firm and client. Per the fixture, translation is currently limited to Spanish only, and certain manually-entered fields (charge/discount/invoice descriptions, late fees, and custom email/message text) are not automatically translated.
- evidence-note: fx-0052.html ("Translating Invoices" help article) is the direct, detailed source. fx-0271.html (a "2024 Highlights: Year in Review" blog post) corroborates only briefly, listing "Translate Invoices to Spanish: Translate invoices directly through the Docketwise platform" as one of 63 features shipped that year, without further mechanical detail.

## notes.note-assignment
- description: A note is assigned by default to the firm member who creates it, but can be reassigned to any other firm member by clicking the note's assignee field, clicking into the blank assignee space, and selecting the desired firm member, then clicking Update. An assignee can also be removed by clicking the X next to their name.
- evidence-note: fx-0223.html ("Notes" help article), section "Assigning a Note to a Firm Member," is the sole and direct source, matching the entry name exactly.

## reports.custom-report-saving
- description: A custom report's applied filters are saved by clicking the "Save Report" button, which persists the filter configuration for later one-click access via the "Select a Report" page. Per the fixture, only the report's creator can save updated filters; for a shared report, other users can apply filters temporarily but cannot save changes to it.
- evidence-note: fx-0160.html ("Custom Reports" help article), section "Saving a Custom Report," is the direct, detailed source. fx-0170.html (marketing "Reporting" feature page) corroborates at a higher level ("Save report configurations," "Save time on commonly-used reports"). fx-0171.html is a YouTube video on custom reports whose description also emphasizes saving report configurations for reuse, but does not add saving-specific mechanics beyond what fx-0160 states.

## reports.custom-report-sharing
- description: A custom report can be shared with the rest of the firm by toggling the "Share Report" slider to active, after which all firm members can see and access the report; shared users can view the report and apply their own (unsaved) filters but cannot save updated filters or unshare/change the report's visibility back to private.
- evidence-note: fx-0160.html ("Custom Reports" help article), section "Sharing a Custom Report," is the direct, detailed source. fx-0170.html (marketing "Reporting" page) corroborates at a general level ("Share reports — Make reports accessible to your team members so that everyone can get the latest insights") without the access-restriction detail.

## reports.hr-portal-reports
- description: HR Portal Reports let a corporate client (logging into their HR Portal) run and filter reports on their foreign national employees and related matters, specifically an "Employees Report" (shared employees) and a "Matter Report" (company matters). Firm-side, HR Portal Reports can be configured to include contact/matter custom attributes via Settings > Portal Settings, though filters within the report itself can only be adjusted by the individual logged into the HR Portal, not previewed/edited by the firm.
- evidence-note: fx-0160.html ("Custom Reports" article, "HR Portal Reports" section) and fx-0187.html (dedicated "HR Portal Reports" article, aimed at the HR Portal end-user) both give direct, matching procedural detail. fx-0276.html is a Q4 2022 features-update YouTube video whose description lists "HR Portal Reports (4:55)" as a chapter/timestamp only, with no further descriptive text attesting what the feature does.
