# onDiem Marketing Update Dashboard

A single-page, self-contained marketing performance dashboard for onDiem —
consolidating campaigns, the marketplace (app.ondiem.com), marketing site (ondiem.com),
paid search, visibility in AI answers, social (Instagram / Facebook / LinkedIn),
partnership link tracking, and pro profile completion.

**Reporting window:** Aug 6 – 12, 2026, compared against Jul 30 – Aug 5, 2026.
Two sections run on their own windows and are labelled as such in the report:
AI visibility is measured Jul 12 – Aug 13, and Short.io is measured Aug 1 – 13
against Jul 1 – 31.
Style modeled on the Figment Creative report template.

## Structure

- `index.html` — the deployable dashboard. Fully self-contained: inline CSS and
  hand-rendered inline-SVG charts, **no external dependencies or network calls.**
- `generate.py` — the Python generator that produces the dashboard from the source
  numbers. Edit the data arrays in the BUILD section and re-run `python3 generate.py`
  (writes `onDiem_Weekly_Report.html`; copy it to `index.html`).
- `.gitignore` — excludes `report docs/`, the folder of raw source exports used to
  compile the report. Those files are inputs, not deliverables, and must not deploy.

## Sections

1. Week over week — four metrics with daily series, five trailing weeks
2. Updates — gift-card promo, partner widget, DOMA 2026
3. Campaigns — promo conversion funnel, promo codes, mailer correction, RDH nurture
4. Marketplace — daily cycle, core actions, where the decline sits
5. Marketing site — channel mix, top pages, form completion
6. Paid search — brand defence, auction insights
7. AI visibility — share of voice, engines, citation sources, sentiment
8. Social — Instagram context, LinkedIn documents, competitors
9. Link tracking — Short.io / ADA partnership
10. Profile completion

## Notes carried forward

- **The spring gift-card mailer is restated from 15 booked shifts to 48.** The earlier
  figure was recorded while timecards were still clearing. Gift-card results need
  roughly two months before they can be read as final.
- The profile completion cohort changed: this report tracks the 555 pros present in
  all three pulls (Jul 13, Jul 20, Aug 6). The previous report tracked 765 on a
  different definition. The two counts are not comparable.
- Marketing site weekly values through Jul 29 come from the prior 30-day export and
  differ slightly in page coverage from the current 7-day exports.
- Auction insights `outranking share` means how often **onDiem** ranked above the
  competitor named on that row.
- Platform active users in the week-over-week panel are summed daily figures and are
  not deduplicated.
- Short.io is excluded from the week-over-week panel this cycle: the export only
  produces calendar-month windows. A Click Stream export would restore daily
  granularity.
- Exclude `/administrator` from platform page data. `professional_accepted_offer` is
  the reliable booking proxy; `temp_shift_offered` and `temp_shift_confirmed` are
  activity event counts dominated by a handful of accounts.

## Deploy

Static site — `index.html` at the repo root. On Vercel, import with
**Framework Preset = Other** and no build command.

## Data sources

GA4 (marketplace + marketing site), Metricool (social), Google Ads, Short.io,
HubSpot (email campaigns, promo code redemption, AI visibility, profile completion).
Internal use.
