# exclusion-log -- inventory items and fixtures ruled out of corpus
# mapping, each with rationale. Read by oracle check 2 (orphan
# fixtures) and check 3 (inventory items excluded from coverage).

- fx-0001 :: fixture captured for surface link discovery (nav tree,
  feature-page URLs, help-center and YouTube locations), not as a
  feature attestation; it seeds the Phase 1 marketing inventory. No
  corpus entry cites it yet; entries may cite it later, which lifts
  this exclusion naturally.
- fx-0004, fx-0006 :: sitemap captures -- inventory-discovery
  fixtures (373 unique URLs -> audit/sitemap-urls.txt, marketing +
  release-notes inventories), not feature attestations.
- fx-0005 :: YouTube videos-tab capture is a JS shell; video list not
  server-rendered. Kept as evidence of the enumeration attempt;
  channel RSS (fx-0007) is the working route, capped at ~15 recent.
- fx-0007 :: youtube inventory source (RSS feed), not itself a
  feature attestation; video-body fixtures come in fan-out.
- fx-0008 :: G2 bot-walled (DataDome challenge page, 1.7KB). Capture
  is block evidence, 2026-07-31.
- fx-0009 :: Capterra bot-walled (Cloudflare challenge, 5.5KB).
  Block evidence, 2026-07-31.
- fx-0010 :: TrustRadius bot-walled (Cloudflare challenge, 5.5KB).
  Block evidence, 2026-07-31.
- fx-0011 :: reddit.com JSON search endpoint returned a JS shell
  (zero content hits); superseded by fx-0011b (old.reddit static
  HTML, working). Kept as route evidence.
- fx-0011b :: reviews inventory source (forum thread discovery), not
  itself a feature attestation; thread-body fixtures come in fan-out.
- fx-0012 :: Smart Forms collection page capture -- article
  enumeration for the Phase 2 pilot (32 article URLs), not a feature
  attestation; same ruling class as fx-0001/fx-0003 discovery
  captures.
- fx-0040 :: "Getting Started with DocketWise" article sits in the
  Smart Forms help category but attests onboarding/support services
  (webinars, live chat, training booking), not Smart Forms features.
  Candidates rejected -- see rejection-log module smart-forms.
- fx-0051 :: "Request a W9 Form" article sits in the Invoicing and
  Trust Accounting help category but only offers the vendor's own
  W-9 PDF for download -- administrative/support content, not a
  product capability. Same ruling class as fx-0040. See
  rejection-log module invoicing-and-trust-accounting.
- fx-0080 :: QuickBooks integration marketing page, captured during
  the invoicing fan-out as a candidate second-family source; its
  attestations (expense tracking, invoice sync) belong to the
  Integrations module and will be cited by that module's extraction.
  Held, not orphaned.
- fx-0084 :: Firm Settings collection page capture -- article
  enumeration for the Phase 3 module (23 article URLs, matches
  fx-0003's published count), not a feature attestation; same
  ruling class as fx-0012.
- fx-0085 :: "8am DocketWise Brand FAQ" article sits in the Firm
  Settings help category but attests only the AffiniPay-to-8am
  corporate rebrand (names, logos, entity); it explicitly states
  product functionality is unchanged. No product capability to
  extract. Same ruling class as fx-0040/fx-0051.
- fx-0100 :: "Docketwise Training and Help" article attests
  onboarding/support services (weekly webinar, learning center,
  live chat hours, training and support-call booking), not product
  capabilities. Same ruling class as fx-0040. See rejection-log
  module firm-settings.
- fx-0110 :: Integrations collection page capture -- article
  enumeration for the Phase 3 module (15 article URLs, matches
  fx-0003's published count), not a feature attestation; same
  ruling class as fx-0012/fx-0084.
- fx-0142 :: Contacts and Matters collection page capture --
  article enumeration for the Phase 3 module (14 article URLs,
  matches fx-0003's published count). Discovery class
  (fx-0012/fx-0084/fx-0110); later cited by entries for the
  category's article-title attestations, which lifts the
  exclusion naturally.
- fx-0185 :: Client Portal collection page capture -- article
  enumeration for the Phase 3 module (6 article URLs, matches
  fx-0003's published count). Discovery class
  (fx-0012/fx-0084/fx-0110); cited by client-portal.module-exists
  and client-portal.hr-portal for the category attestation, which
  lifts the exclusion naturally.

- fx-0247 :: /support/learning-center/ capture (2026-08-01) -- the
  DocketWise Learning Center is a training-course catalog
  (DocketWise 101: From Intake to Billing; advanced-series
  teasers). Onboarding/training services, not product
  capabilities: fx-0040/fx-0100 ruling class. Marketing inventory
  item excluded on the same rationale.

- fx-0251 :: r/LawFirm "Filevine for immigration" (1g5eede,
  captured 2026-08-01). The only Docketwise content is one
  commenter's "We use Docketwise, switched from INSzoom, and I
  really like it" -- a firsthand use endorsement naming no
  capability. Unlike fx-0216 (non-user hearsay) the use is real,
  but with no feature named there is nothing to attest; fixture
  retained as the ruling's evidence.
- fx-0253 :: r/LawFirm "I went solo" (1edkvrg, captured
  2026-08-01). Docketwise appears once, inside a solo attorney's
  startup cost list ("software (M365, Adobe, and Docketwise)");
  no capability named, nothing to map. Fixture retained as
  evidence.
- fx-0254 :: r/LawFirm "Solo immigration caseload" (1jojli0,
  captured 2026-08-01). The OP asks whether "Docketwise or other
  software" would be necessary; none of the 3 comments mentions
  the product. Zero attestation. Fixture retained as evidence.

- fx-0255, fx-0256, fx-0257 :: brand/thought-leadership videos from
  the channel RSS tail (captured 2026-08-01). Interpretive ruling
  (queued for [G2]): capability phrases that are CHANNEL
  BOILERPLATE -- the "simplify forms, track cases, and power
  practice growth" block repeated across every video description --
  do not attest; only video-specific content does. fx-0255 and
  fx-0256 carry nothing beyond boilerplate; fx-0257's one specific
  clause (disclosures, engagement letters, acknowledgements,
  referrals, automated workflows) names no distinct testable
  capability (rejection log, cross-module Phase 4). Fixtures
  retained as ruling evidence.
- fx-0258, fx-0259, fx-0260 :: Immigration Uncovered podcast
  episodes/clips (captured 2026-08-01): enforcement-data interview
  (fx-0258) and policy-change discussion clips (fx-0259, fx-0260,
  same episode). Editorial content, no product attestation.
  Fixtures retained as ruling evidence.

- reviews item "r/legaltech: Green card visa bulletin every month
  (1qtbdim)" -- EXCLUDED from corpus sourcing after thread-body
  capture (fx-0216, 2026-07-31): the OP asks whether immigration
  software tracks the visa bulletin without naming Docketwise, and
  the single comment recommends docketwise.com while stating "I
  haven't used them" -- popularity hearsay from a non-user, no
  product attestation. Fixture retained as the ruling's evidence;
  the priority-date ground it gestures at is fully attested by
  fx-0211/fx-0214 (case-tracking.priority-date-tracking).
- fx-0272 :: uploads-playlist page capture (2026-08-01), the Phase 4
  youtube back-catalog enumeration source: server-renders the 100
  newest upload ids of a stated 185 total. Discovery class
  (fx-0007 RSS precedent); per-id rulings in
  audit/youtube-enumeration.txt.
- fx-0274, fx-0275 :: "Meet (8am) DocketWise" brand overview video
  and its duplicate upload (captured 2026-08-01): the description
  is generic capability listing (forms, case management,
  collaboration, payments) -- channel-boilerplate class per the
  fx-0255/fx-0256/fx-0257 ruling. Fixtures retained as evidence.
- fx-0280 :: "From Cerenade to Docketwise" switch-story video
  (captured 2026-08-01): names no capability ("all-in-one
  immigration software") -- fx-0251 use-endorsement class. The
  INSZoom counterpart fx-0279 IS cited (names form completion and
  CRM). Fixture retained as evidence.
