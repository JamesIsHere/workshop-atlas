# module: client-communication

Docketwise's own vocabulary (help-center category "Client
Communication", 10 articles, fx-0003). Phase 3 fan-out module: full
extraction from 10 help articles (fx-0173..fx-0182), collection page
fx-0172, and two embedded official videos found by the embed-grep
route: "Bulk Text Messages and Emails" (fx-0183, the bulk-messaging
video predicted by the fx-0101 embed debt) and "Email Templates"
(fx-0184). Three channels: email (single and bulk, with signatures,
CC/BCC, merge tags, attachments, templates), SMS (2-way
conversations plus the carrier-registration and consent compliance
surface), and secure portal messaging.

## entry: client-communication.email-messages
- name: Email Messages
- named-by-us: no
- description: Users email clients from inside Docketwise via Create
  New > Message: a recipient and content are required, the email can
  optionally be filed under a client and matter, and any firm member
  can be set as the sender, which determines where replies go
  (fx-0182). Sent emails land in the Messages tab (fx-0182). An
  official video covers the email flow (fx-0184).
- criterion: User clicks Create New, selects Message, provides a
  recipient and content, and sends -> the email is sent and appears
  in the Messages tab
- sources: fx-0172, fx-0182, fx-0184
- tier: confirmed
- detail: A sent email can be re-sent from the Messages tab to
  remind clients of action items (fx-0182). The compose flow offers
  drafting new content or importing a template (fx-0180, fx-0182).

## entry: client-communication.message-templates
- name: Emailing Custom Templates
- named-by-us: no
- description: Frequently sent emails (action items, welcome
  messages, checklists) are saved as reusable Templates: check Save
  as Template below the compose area, import a template into any new
  message, and create or edit unlimited templates from account
  settings (fx-0182). The official Email Templates video attests the
  feature (fx-0184).
- criterion: User checks Save as Template on an email and later
  imports it into a new message -> the saved template populates the
  message content
- sources: fx-0182, fx-0184
- tier: confirmed
- detail: Templates are also selectable in bulk messaging (fx-0181)
  and in secure portal messages (fx-0175). Message templates are the
  object that matter-status automations send
  (contacts-and-matters.matter-status-automations, fx-0152).

## entry: client-communication.email-signatures
- name: Email Signatures
- named-by-us: no
- description: Each user sets a personalized email signature under
  Settings > Personal Information, either pasted from an outside
  client or built manually in the text editor with text, images, and
  links; an Include Email Signature Automatically toggle sets the
  default, and every message retains a per-message slider to include
  or omit the signature (fx-0176). Named as a release in the Q3
  2022 features-roundup video (fx-0277, chapter at 12:06).
- criterion: User saves a signature under Settings > Personal
  Information with the automatic toggle active -> outgoing email
  messages include the signature
- sources: fx-0176, fx-0277
- tier: confirmed
- detail: Signatures work in single email messages and in bulk email
  messages from the Contacts dashboard (fx-0176). A pasted signature
  with an image on its last line can distort if Enter is hit after
  the image; spacing should be added before pasting (fx-0176).

## entry: client-communication.email-cc-bcc
- name: CCing and BCCing in Email Messages
- named-by-us: no
- description: Outgoing single email messages accept firm members
  and/or contacts in CC and BCC fields; the CC field suggests the
  recipient's related contacts. Not available in bulk email
  (fx-0177).
- criterion: User selects firm members or contacts in the CC or BCC
  fields of an email message -> the outgoing message is also sent to
  those individuals
- sources: fx-0177
- tier: provisional

## entry: client-communication.email-merge-tags
- name: Merge Tags in Email Messages
- named-by-us: no
- description: Email messages and email message templates accept
  merge tags that render contact information, plus matter
  information when the message is related to a matter; tags are
  inserted from a popular-tags list (including custom attributes),
  the full tag list, or typed manually via the # Merge Tags button
  (fx-0178).
- criterion: User inserts merge tags into an email related to a
  contact -> the sent message renders the contact's (and related
  matter's) information in place of the tags
- sources: fx-0178, fx-0219
- tier: provisional
- detail: A Preview button shows the rendered message before
  sending, except in bulk emails (fx-0178). Matter merge tags cannot
  be used in bulk emails (fx-0178). Usable in single emails, bulk
  emails, and templates (fx-0178). The Template Automation merge-tags
  article attests the same vocabulary serves email messages and
  email message templates (fx-0219; tag list owned by
  template-automation.merge-tags).

## entry: client-communication.email-attachments
- name: Sending Messages with Attachments
- named-by-us: no
- description: Email messages can carry file attachments picked from
  a contact's files already in Docketwise, via the Attach Files
  option in the compose flow (fx-0180).
- criterion: User selects Attach Files on an email message and picks
  files related to a contact -> the message is sent with those files
  attached
- sources: fx-0180
- tier: provisional
- detail: Unavailable in bulk messaging and text messaging; files
  over 18.74 MB are not supported (fx-0180).

## entry: client-communication.bulk-messaging
- name: Bulk Text Messages and Emails
- named-by-us: no
- description: From the Contacts dashboard, users select multiple
  contacts and use Bulk Actions > Send Message to send an email or
  text to all of them, drawing content from a template or manual
  entry, with a confirmation step to review, edit, add, or remove
  recipients before sending (fx-0181). Pro/Advanced subscriptions
  only (fx-0181). The official bulk-messaging video attests the
  feature (fx-0183).
- criterion: User selects contacts on the Contacts dashboard and
  completes Bulk Actions > Send Message -> the email or text is sent
  to every confirmed recipient
- sources: fx-0181, fx-0183
- tier: confirmed
- detail: Recipient emails and mobile numbers are editable in the
  confirmation window (fx-0181). Bulk SMS messages cap at 160
  characters (fx-0181); CC/BCC, attachments, matter merge tags, and
  message preview are unavailable in bulk (fx-0177, fx-0178,
  fx-0180).

## entry: client-communication.secure-portal-messaging
- name: Secure Portal Messaging
- named-by-us: no
- description: Firm users message clients through the client portal:
  Create New > Message > Secure Portal, pick a portal-active
  contact, compose (or import a template), and send; the client
  receives an email notification and reads and replies from the
  portal, while the firm sees responses as in-app notifications and
  full thread history in the Message index (fx-0175). Clients can
  also start new secure threads from their portal's messages tab
  (fx-0175). Named as a Secure Message Portal release in the Q4
  2022 features-roundup video (fx-0276, chapter at 8:37).
- criterion: User sends a Secure Portal message to a portal-active
  contact -> the client is notified by email and can read and reply
  to the thread from their client portal
- sources: fx-0172, fx-0175, fx-0186, fx-0191, fx-0276
- tier: confirmed
- detail: A client portal must be activated before a contact can
  receive secure messages (fx-0175). Notification routing when a
  client starts a new thread follows the account's Notification
  Settings (assignees only, assignees plus owner, all members, or
  no one); replies to existing threads notify all firm members
  in-app (fx-0175, fx-0191). The Client Portal module's captures
  attest both ends of the same flow: the firm-side Create New >
  Message > Secure Portal path (fx-0191) and the client-side
  Messages navbar with Read, Reply, and Create New Conversation
  (title plus body) actions (fx-0186).

## entry: client-communication.text-message-conversations
- name: Text Message Conversations
- named-by-us: no
- description: Two-way SMS conversations with clients inside
  Docketwise: enabled under Settings > Subscription (Add Text
  Messaging), accessed via the cellphone icon, with one conversation
  per mobile number, optional filing under a client/matter (editable
  later via the pencil icon), and message send/receive in-thread
  (fx-0179). Pro/Advanced subscriptions only (fx-0179).
- criterion: User creates a conversation from the cellphone icon and
  sends a text -> the SMS is delivered and the client's replies
  appear in the same in-app conversation
- sources: fx-0172, fx-0173, fx-0179
- tier: provisional
- detail: 100 free outgoing texts on first enablement, then
  automatic top-ups at $20 per 1,000 outgoing messages; the
  remaining count shows under Settings > Subscription (fx-0179).
  Conversation SMS cap at 480 characters (fx-0179; bulk SMS caps at
  160, fx-0181 -- different features, both readings kept). Texts are
  stored a maximum of 13 months (fx-0179). Clients cannot initiate
  conversations; the firm must contact them first (fx-0179). Only
  account admins/owners can enable the feature (fx-0179).

## entry: client-communication.sms-carrier-registration
- name: A2P Carrier Registration
- named-by-us: yes
- description: Firms using 2-way SMS must complete the US telecom
  carriers' Application-to-Person (A2P) approval process: an in-app
  popup form collects the organization's official business details
  (matching EIN/registration records), submitted by an admin user;
  carriers verify manually over several weeks and the platform
  notifies the firm on approval (fx-0173).
- criterion: Admin user submits the firm's business details in the
  in-app registration form -> the firm passes carrier approval for
  continued SMS service and is notified in the platform
- sources: fx-0173
- tier: provisional
- detail: Carriers reject applications over minor inconsistencies
  with public records (fx-0173).

## entry: client-communication.client-sms-consent
- name: Client Consent for SMS Notifications
- named-by-us: no
- description: Clients must explicitly consent before receiving SMS
  notifications: a firm user sends the SMS Opt-In Consent Form from
  the Request Consent option under the contact's Phone Numbers tab,
  by email or copied direct link; the client verifies their number,
  checks the consent box, and submits, receiving a confirmation
  text with opt-out instructions (fx-0174). Contacts added before
  regulatory enforcement are grandfathered as consented unless they
  opt out; new contacts must complete the workflow before SMS
  features activate (fx-0173).
- criterion: Firm user sends the SMS Opt-In Consent Form and the
  client submits it -> SMS notifications become active for the
  client and a confirmation text is sent
- sources: fx-0173, fx-0174
- tier: provisional
- detail: Client-side opt-in governs SMS for questionnaire
  invitations, invoice sharing, and e-signature invitations
  (fx-0174). A consented client opts out by replying Stop in the
  text thread (fx-0174).

## entry: client-communication.user-sms-optin
- name: Attorney/Firm User Opt-in Settings
- named-by-us: no
- description: Each firm user individually opts in or out of SMS
  notifications for event/expiry-date reminders and e-signature
  invitations via a consent checkbox under the Mobile Phone Number
  field at Settings > Preparer Information; SMS notifications are
  disabled by default (fx-0174).
- criterion: User checks the SMS consent box under Settings >
  Preparer Information and saves -> the user receives SMS reminders
  for events, expiry dates, and e-signature invitations
- sources: fx-0174
- tier: provisional
