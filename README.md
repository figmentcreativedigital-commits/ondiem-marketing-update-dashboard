# onDiem Marketing Update Dashboard

A single-page, self-contained marketing performance dashboard for onDiem —
consolidating the marketplace (app.ondiem.com), marketing site (ondiem.com),
paid search, visibility in AI answers, social (Instagram / Facebook / LinkedIn),
partnership link tracking, email & survey, event conversion, and pro profile
completion.

**Reporting window:** Jul 7 – Aug 5, 2026.
AI visibility data is measured Jun 29 – Aug 6 and is labelled as such in the report.
Style modeled on the Figment Creative report template.

## Structure

- `index.html` — the deployable dashboard. Fully self-contained: inline CSS and
  hand-rendered inline-SVG charts, **no external dependencies or network calls.**
- `generate.py` — the Python generator that produces the dashboard from the source
  numbers. Edit the data arrays in the BUILD section and re-run `python3 generate.py`
  (writes `onDiem_Weekly_Report.html`; copy it to `index.html`).

## Sections

1. Updates — what shipped this period
2. Marketplace — Monday cycle, two-sided funnel, gift-card mailer result
3. Marketing site — channel mix, form completion
4. Paid search — brand defence, auction insights
5. AI visibility — share of voice, engines, citation sources, Google reviews
6. Social — content type performance, LinkedIn formats, competitors
7. Link tracking — Short.io / ADA partnership
8. Email, survey & event conversion
9. Profile completion

## Notes carried forward

- Marketing site daily values are not comparable across periods: the Jun/Jul export
  captured ~75% of pages per day against ~97% here.
- Profile completion shows clicks only this period; the tracked count and completion
  rate are carried forward from the previous report pending new data.
- Auction insights `outranking share` means how often **onDiem** ranked above the
  competitor named on that row. The previous report read this inverted.

## Deploy

Static site — `index.html` at the repo root. On Vercel, import with
**Framework Preset = Other** and no build command.

## Data sources

GA4 (marketplace + marketing site), Metricool (social), Google Ads, Short.io,
HubSpot (email, AI visibility, event conversion, profiles). Internal use.
