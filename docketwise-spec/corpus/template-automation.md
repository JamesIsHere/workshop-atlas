# module: template-automation

Docketwise's own vocabulary (help-center category "Template
Automation", 2 articles, fx-0003). Phase 3 sparse-tail module: full
extraction from the collection page (fx-0217) and articles
fx-0218..fx-0219, plus -- via embed-grep -- the official "Automated
Templates in Docketwise" video (fx-0220, Kl4ItwRpCZQ, published
2020-04-24, a pre-RSS back-catalog upload) and -- via the tripwire
cross-inventory sweep -- the pricing-page plan matrix row (fx-0108,
already captured at module 2). Carve: module anchor + template upload
+ template export + merge-tag vocabulary. One cross-module in-place
join instead of a duplicate: merge tags in email messages
(client-communication.email-merge-tags, +fx-0219).

## entry: template-automation.module-exists
- name: Template Automation
- named-by-us: no
- description: Docketwise turns .docx documents authored in any word
  processor into automated templates: merge tags placed in the
  document are populated with client and matter information when the
  template is exported against a client (fx-0217, fx-0218, fx-0219,
  fx-0220, fx-0108).
- criterion: User uploads a .docx containing merge tags as an
  automated template and exports it against a client -> a document
  with the client's information substituted for the tags is produced
- sources: fx-0217, fx-0218, fx-0219, fx-0220, fx-0108
- tier: confirmed
- detail: The official demo attests turning Word documents into
  dynamic automated templates (fx-0220, 248s, title + description).
  The pricing matrix lists Automated Templates as available on all
  three plans -- Basic, Pro, and Advanced (fx-0108). Authoring works
  from Word, Google Docs, Apple Pages, or any other word processor
  that saves .docx (fx-0218) -- authoring happens outside the
  product; the product-side capability is accepting the .docx.

## entry: template-automation.template-upload
- name: Upload your Document to Docketwise
- named-by-us: no
- description: A merge-tagged .docx is registered as an automated
  template from Account Settings (cog icon, bottom right corner) >
  Automated Templates, where the user gives the template a name and
  uploads the file (fx-0218, fx-0220).
- criterion: User names and uploads a .docx on the Account Settings
  Automated Templates page -> the template is stored and selectable
  when creating a new template export
- sources: fx-0218, fx-0220
- tier: confirmed

## entry: template-automation.template-export
- name: Export your Template
- named-by-us: no
- description: A stored automated template is generated against a
  client from the dashboard via Create New > Template, indicating
  Client (required), Matter (optional), and Template (required)
  (fx-0218).
- criterion: User selects Create New > Template and picks a client
  and a stored template -> a document is generated from the template
  with the client's (and optional matter's) information populated
- sources: fx-0218
- tier: provisional

## entry: template-automation.merge-tags
- name: Merge Tags
- named-by-us: no
- description: Docketwise defines a merge-tag vocabulary
  (#full_name#, #matter_title#, #today#, ...) that populates contact
  and matter information into automated templates and email messages
  (fx-0218, fx-0219).
- criterion: User inserts a documented merge tag (e.g. #full_name#)
  into a .docx template and exports it against a client -> the tag
  is replaced by that client's corresponding field value
- sources: fx-0218, fx-0219
- tier: provisional
- detail: The help article enumerates 229 tags in its All Available
  Tags list plus a 16-tag Frequently Used subset (fx-0219).
  Coverage spans contact biographics, immigration status and
  documents (A-number, naturalization/citizenship certificates,
  visas, passports, SEVIS, EAD, TPS), physical/mailing address
  sub-fields, phone numbers, financials (income, assets, expenses,
  liabilities, credit score, fee-waiver and public-benefits dates),
  employer/petitioner facts (E-Verify, NAICS, employee counts),
  military service, matter fields (#matter_title#,
  #matter_applicant#, #matter_description#), and date tags (#today#,
  #date_long#) (fx-0219). The email-message surface of the same
  vocabulary is owned by client-communication.email-merge-tags.
  Firm-defined custom attributes extend the documented vocabulary
  into templates (contacts-and-matters.custom-attributes, fx-0144).
