# inventory: youtube (source family: official YouTube channel)
# Source: fx-0007 (channel RSS feed, channel_id UCfGhmt2TsymPPDVpro-
# JSIA). KNOWN CAP: RSS returns only the ~15 most recent uploads; the
# videos-tab HTML (fx-0005) is a JS shell and did not enumerate. Full
# back-catalog enumeration is a fan-out work item; this inventory is
# the feed snapshot of 2026-07-31, deduplicated. Phase 3 addition:
# back-catalog videos discovered via embeds in captured help
# articles are appended as found (floor grows; enumeration debt
# stays open).

- Immigration law is about more than paperwork (vf8fBNLIgqg, fx-0255) :: excluded: brand video; capability phrases are channel boilerplate (simplify forms, track cases) repeated across descriptions, no video-specific capability content (exclusion log 2026-08-01)
- How to reduce client check-ins with real-time case visibility (d192jH3oxcQ, fx-0215; RSS also lists duplicate upload pNbhHnzE5rE) :: entries: case-tracking.module-exists
- Grow your immigration practice by meeting rising client demand (sfsSt27VrWw, fx-0256; RSS also lists duplicate upload hB74hLPb_r0) :: excluded: thought-leadership video; body copy is not even Docketwise-specific (exclusion log 2026-08-01)
- Immigration client intake forms lead to better consultations :: entries: smart-forms.single-intake-autofill
- How immigration professionals build client trust through communication (cJguxcujytY, fx-0257; RSS also lists duplicate upload hSiLJprJku8) :: excluded: brand video; the one capability clause (disclosures, engagement letters, referrals, automated workflows) names no distinct testable capability -- rejection log, cross-module Phase 4 (exclusion log 2026-08-01)
- 8am IQ for DocketWise: AI built for immigration law (I24AwVwvK3U, fx-0208) :: entries: docketwise-iq.module-exists, docketwise-iq.ai-translation, docketwise-iq.data-capture
- Simplify your client intake process with 8am DocketWise Smart Forms :: entries: smart-forms.single-intake-autofill
- IU Episode 056: Unpacking Immigration Enforcement: Data, Trends, and Transparency (ZkrcON0m1m8, fx-0258) :: excluded: Immigration Uncovered podcast episode on enforcement data and FOIA; no product content (exclusion log 2026-08-01)
- Smart Spend = Worth a Look (bHweEsDFftA, fx-0259) :: excluded: Immigration Uncovered podcast clip on policy changes (payment mandates, fees, Gold Card); no product content (exclusion log 2026-08-01)
- Anxiety about change? You're not alone. (NHaegl5VLAE, fx-0260) :: excluded: Immigration Uncovered podcast clip, same episode/description as bHweEsDFftA; no product content (exclusion log 2026-08-01)
- Webinar: Invoicing and Trust Accounting (kIVDe765Bhg, fx-0081) :: entries: invoicing-and-trust-accounting.module-exists, invoicing-and-trust-accounting.invoice-creation, invoicing-and-trust-accounting.trust-bank-accounts, invoicing-and-trust-accounting.trust-disbursements, invoicing-and-trust-accounting.time-entry-invoice-import, invoicing-and-trust-accounting.default-invoice-settings
- Trust Requests in Docketwise (1nO0C2YYSX0, fx-0082) :: entries: invoicing-and-trust-accounting.trust-requests
- Saved Charges for Invoices (G23wZo2PXZs, fx-0083) :: entries: invoicing-and-trust-accounting.saved-charges
- Webinar: Matter Workflows (zZen4TiOYPE, fx-0158) :: entries: contacts-and-matters.matter-types-statuses, contacts-and-matters.matter-status-automations, reports.matter-reports
- Introducing Custom Reports from Docketwise (dOKWbfsj440, fx-0171) :: entries: reports.module-exists, reports.custom-report-builder, reports.custom-report-saving
- Bulk Text Messages and Emails (VR9jnheW9AE, fx-0183) :: entries: client-communication.bulk-messaging
- Email Templates (Sd2xzuZhklA, fx-0184) :: entries: client-communication.email-messages, client-communication.message-templates
- Human Resources Portal (Pm7vjWYP7DI, fx-0192) :: entries: client-portal.hr-portal, client-portal.hr-portal-employee-management, client-portal.hr-portal-resource-sharing
- Introducing e-Signatures from Docketwise (xCpkXjKPqVM, fx-0200) :: entries: files-and-documents.esignature
- Automated Templates in Docketwise (Kl4ItwRpCZQ, fx-0220; back-catalog 2020-04-24 via embed in fx-0218) :: entries: template-automation.module-exists, template-automation.template-upload
- Docketwise Leads (abFLWaQc1K4, fx-0237; back-catalog 2020-12-21, embedded by both fx-0235 help and fx-0236 marketing; fx-0101 debt list wrongly presumed this was QuickBooks) :: entries: docketwise-leads-crm.module-exists, docketwise-leads-crm.website-lead-form, docketwise-leads-crm.lead-conversion
- Custom Attributes (j6KonbWdl6I, fx-0238; back-catalog 2021-06-22, fx-0101 debt list wrongly presumed Leads CRM; QuickBooks webinar was never embedded -- debt line retired) :: entries: contacts-and-matters.custom-attributes

# Phase 4 back-catalog enumeration (2026-08-01): the uploads-playlist
# page (fx-0272, list=UUfGhmt2TsymPPDVpro-JSIA) server-renders the
# 100 newest upload ids of a STATED 185 total; titles via the public
# oEmbed endpoint. Per-id class rulings: audit/youtube-enumeration.txt
# (17 already inventoried above, 5 product-attesting captured
# fx-0273..fx-0278/0279, 3 captured-and-excluded, 58 podcast, 17
# editorial). RESIDUAL DEBT, documented cap: the oldest ~85 uploads
# are unreachable by ordinary page fetch (continuation needs the
# robots-disallowed youtubei POST API). Known routes into that tail
# for future work: help-article embeds (proven, fx-0220/0237/0238)
# and named playlists from fx-0276/fx-0277 descriptions -- Building a
# Successful Immigration Practice Webinar Series
# (PLYhr9VzYOl78r-av5PCVKA4U7GzUSHnsF) and Docketwise Training
# Webinar Series (PLYhr9VzYOl79GSDeB9q0ygDXLt1Fe1eog) -- same
# first-100 render limit applies per playlist.
- New ?Gold Card Visa??Buy a Green Card for $1 million? (NZVPXYmsRVI) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- How to protect clients? payment info with virtual cards (-cHIqN_eT5I) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- It?s 2025?Why are we still mailing payments? (7XanLYQ6RIk) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- USCIS will no longer accept paper checks, money orders, or other manual forms of payment (kUg8w8ADzN8) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Meet 8am? DocketWise: The #1 immigration law software to streamline your practice (r9sT9rnaBDg, fx-0274) :: excluded: brand overview video; description is channel boilerplate, no video-specific capability content (exclusion log 2026-08-01)
- Meet DocketWise: The #1 immigration law software to streamline your practice (4HBVeUVrGs4, fx-0275) :: excluded: duplicate upload of r9sT9rnaBDg, same boilerplate ruling (exclusion log 2026-08-01)
- IU Episode 055: The Gold Card, the $100K H?1B Fee, and the End of Paper Checks (nfi7EPZ30OQ) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- Balancing innovation and ethics with AI tools for immigration law (4aFHDcR8obg) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Balancing innovation and ethics with AI tools for immigration law (PRtHBji4GLQ) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Immigration law is about more than paperwork (hIz8KdbvpCc) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- How to start and grow your immigration law firm (LyVx1ijLKmE) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Why legal tech is the key to better client communication (ESfJFh5He58) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Eliminate Manual USCIS Case Tracking with DocketWise (eU91vT4-R3Y, fx-0273) :: entries: case-tracking.module-exists
- IU Episode 054: EB-5 Investor Visas vs. Trump Gold Card (XCHCcQ9zSC0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 053: Pre-AILA Conference Special & 2025 Immigration Report Preview (VkE-qQbtqBQ) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 052: Status Revoked, Voices Suppressed: Immigration Crackdown on International Students (cmxFQMojXTc) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- Why Immigration Lawyers Should Write USCIS Cover Letters (sN8OO3HFoug) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- How Immigration Lawyers Can Avoid Form I-130 Delays (FBhxXe1ybxg) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- How Immigration Lawyers Can Stay Organized During the H-1B Visa Process (e0FGCbNsLjY) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- IU Episode 051: Understanding Immigration Related Worksite Visits (JeyVkVem7e0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 050: New Executive Order Targets Immigration Lawyers and Rights Defenders (c6l9SWfmdcQ) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 049: Transforming Online Translation - A Conversation with Motaword Co-founder Oytun Tez (tJ_ies22az8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 048: Business Immigration Under Trump 2.0: O & P Visas, EB-1, and AI in Immigration (FopzXLbmWeY) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 047: Golden Visas - Your Ticket to European Residency with Andre Bothma (MV1_Bm2MxSQ) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 046: Trump's Inauguration 2025: Immediate Immigration Policy Changes and Their Impact (SpGIiWv2z2o) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 045: Section 287(g) Exposed: The Real Cost of Collaboration with Rosanna Berardi (Jl2bdVmAra8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 044: Unlocking Success: Digital Marketing Strategies for Immigration Lawyers (k2f4Hiyw93U) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 043: Trump Administration Immigration Policy - Short, Medium and Long-Term Changes (wR4Zz4wuBs8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 042: Revolutionizing Translation with AI ? Insights from Ian Hawes of ImmiTranslate (JrsVF4F3JQM) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 041: Maximizing Every Minute with Nadine Heitz, Co-Founder and CEO of Case-Flow (dVbSKD1R6S4) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 040: Access 61: Helping Asylum Seekers With Innovative AI-Assisted Solutions (mWxmXTpJo0E) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 039: Achieving Outstanding Outcomes for Your Clients w/AILA President-Elect Jeff Joseph (4tqvLGHfZVI) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 038: Ineffective Assistance of Counsel in The Immigration Context (H2vwqcqO1Yk) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 037: State of the Global Talent Race - Immigration Insights (m2-0w5bInag) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 036: Second Residencies and Citizenship with David Lesperance (KMKU9ukQk6o) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 035: Living Up to Your Client's Trust with Immigration Attorney Tsui Yee (NqcP1nxzfqE) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 034: Immigration Policy & Foreign Relations with Gil Guerra (DfrUeirvxH0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 033: Caseblink: Reinventing legal workflow with AI agents. (i3Tc7dv0z9g) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 032: Understanding Nationality, Citizenship, and Statelessness (LSAxzklIhYo) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 031: Update on the Evolving Regulation of AI in Legal Practice (7xngrgm_PzQ) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 030: Immigration from Turkey to the US: Patterns and Trends (-bIDCcwkXz8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 029: Inside the Lawsuit Challenging the USCIS Fee Increase (IgKQW1wkn7Y) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 028: Controversial Texas Immigration Law - Will SB-4 be allowed? (18DQ0lQG0es) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 027: A Hierarchical Decision Model to Evaluate U.S. immigration Policies (td7WuinRn04) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 026: A Novel Strategy to Overcome the H-1B Cap with Danielle Goldman (abEmt3gPQ9o) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 024: Transforming Immigration Law: Insights from Catherine Haight, Founder of Lista (QDeFjS98YR0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 025: Empowering the LGBTQ+ Community: Andrea Montavon McKillip (nF0Fs5oI7G8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 023: Secrets of Building a Successful Law Practice in the Latino Community (5oQ7K3fYijk) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 022: Greg Siskind on Immigration Law Practice and the AI Revolution (sXNaSshGSEk) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 021: VAILL Unveiled: Revolutionizing Legal Access with AI (aOfURA1G67A) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 020: New Year's Resolutions for Immigration Lawyers, Non-citizens, and the Government (DrmsYZGeHlM) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- Perspective 2024 (Wlw1Gc9hhdc) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- IU Ep 018: Disrupting the Legal World with Thomas Martin (A-EUZg4sq9s) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 019: Legal Engineering with Andrew Thrasher (S4f3c4nEgL0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 017: AI Revolutionizing Immigration Practices with Nadine Navarro and Antuan Vazquez (JO9jwGQrAJA) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 016: Becoming a Successful Immigration Lawyer Without Losing Your Mind with Ruby Powers (XN5oHZzArNE) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 015: The Implications of Recent Immigration Bills and the AI Executive Order (7NYAogChBQs) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 014: Palestinian Crisis: US Immigration Challenges with Marty Rosenbluth & Haia Abdel (So4qp1XuvOo) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 013: The Journalist's Responsibility in Shaping Immigration Narratives with Andrew Kreighbaum (hwGRY8ncJA8) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 012: Dr. Austin Kocher on Geopolitics, Borders, and Immigration Enforcement (0R5SRQA_L0A) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 011: Resolving Delays and Reversing Denials: Federal Court Litigation with Joseph Gentile (KkWSAW-kvL4) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 010: Inside Docketwise - Meet Our Team (zbp1MqxN6NM) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 009: Leveraging Social Science Expertise to Win Immigration Cases with Sharon Abramowitz (23VXr9OMeQE) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 008: Meet Am?lie Vavrovsky, Founder of AI-Assisted Immigration Tech Platform 'Formally' (neg9h285XsI) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU: SoloTPSEpisodes Trump Video (b4QotaE884g) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU: SoloTPSEpisodes Ukraine Video (Qunjg2MjWRc) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU: SoloTPSEpisodes Sudan Video (TQcZa7Sl5TY) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 007:  Reid Trautz of AILA on Future-Proofing Your Immigration Practice (eMeepMYOWxg) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Ep 006: Starting a New Law Firm in 2023 with Carolyn Elefant (LHTyPykILiM) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 005: Immigration Finder's Rise: Ian Almasi's Unique Journey to Law (6b_0GExe2Ac) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 004: Tech Strategies For Seasoned Immigration Lawyers (3lpLJHtJkFU) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 003: Effective Marketing Strategies for Immigration Law (_CV0rYvlPeU) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 002: A Discussion With?Ira Kurzban (xS6erxTIsf0) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- IU Episode 001: Exploring the Practical Application of Chat GPT in Immigration Law Practice (OuyeLL6h_dM) :: excluded: Immigration Uncovered podcast episode -- editorial class per fx-0258/fx-0259/fx-0260 rulings, title-ruled (enumeration 2026-08-01)
- Docketwise New Features Roundup (Q4 of 2022) (xXhHf3rzaII, fx-0276) :: entries: reports.hr-portal-reports, client-communication.secure-portal-messaging, firm-settings.accounting-notes, smart-forms.templated-intakes
- Introducing SmartForms from Docketwise (6OoCWPJlGXg, fx-0278) :: entries: smart-forms.single-intake-autofill
- The Ultimate Guide to Immigration Law for Startups - Everything You Need to Know! (-ShurxfYsVk) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Why I Switched from INSZoom to Docketwise Immigration Software (EBNoew2wuqc, fx-0279) :: entries: smart-forms.single-intake-autofill, docketwise-leads-crm.module-exists
- The Metaverse, Web 3.0 and Immigration Law (0e2sXIrZShQ) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- From Cerenade to Docketwise - The Switch (l0tV4Tye5Kk, fx-0280) :: excluded: customer switch-story naming no capability ("all-in-one immigration software") -- fx-0251 use-endorsement class (exclusion log 2026-08-01)
- Religious Workers as an Immigration Practice Niche (WJ4f3BRyTyI) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- How to Think About and Maximize Your In-House Use of Legal Tech (nPi9ko5TGGg) :: excluded: practice-tips/policy/brand video, no product capability in title or class -- fx-0255/fx-0256 boilerplate class, title-ruled (enumeration 2026-08-01)
- Docketwise New Features Roundup (Q3 2022) (TQMq22ENXgM, fx-0277) :: entries: smart-forms.question-hiding, smart-forms.i129-answer-import, notes.note-categories, events.event-reminders, reports.invoice-reports, client-communication.email-signatures, contacts-and-matters.expiry-date-reminders
