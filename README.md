# onDiem Marketing Update Dashboard

A single-page, self-contained weekly marketing performance dashboard for onDiem —
consolidating the marketplace (app.ondiem.com), marketing site (ondiem.com),
Google Ads, social (Instagram / Facebook / LinkedIn), email & survey,
professional first-shift feedback, RDH Under One Roof event conversion, and
pro profile completion.

**Reporting window:** Jun 22 – Jul 21, 2026 (email & profile reports as of Jul 20).
Style modeled on the Figment Creative report template.

## Structure

- `index.html` — the deployable dashboard. Fully self-contained: inline CSS and
  hand-rendered inline-SVG charts, **no external dependencies or network calls.**
- `generate.py` — the Python generator that produces `index.html` from the source
  numbers. Edit the data arrays and re-run `python3 generate.py` to refresh for a
  new period (writes `onDiem_Weekly_Report.html`; copy it to `index.html`).

## Deploy

This is a static site — `index.html` at the repo root. On Vercel, import the repo
with **Framework Preset = Other** and no build command; Vercel serves `index.html`
directly.

## Data sources

GA4 (marketplace + marketing site), Metricool (social), Google Ads, HubSpot
(email, conversion, profiles). Internal use.
