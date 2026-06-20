# Australia Trip Dashboard

Single-file static dashboard (`index.html`) for a Sydney & Melbourne trip (Nov 2026).
Data is fetched live from a published Google Sheet (CSV export) and rendered client-side.
Charts use Plotly; everything else is vanilla JS/CSS. Hosted on GitHub Pages.

## Design System
Always read `DESIGN.md` before making any visual or UI decisions.
All font choices, colors, spacing, and aesthetic direction are defined there.
Do not deviate without explicit user approval. Specifically:
- Fonts: Fraunces (display), Geist (body), Geist Mono (numbers). Never reintroduce Inter.
- Accent is outback ochre `#E08A4B`. Never use the old purple `#7c6aff`.
- Use the CSS custom properties in `:root` rather than hardcoding hex values.

## Performance
- Keep the data fetch in `<head>` (`window.__sheetData`) so it runs in parallel with downloads.
- Keep Plotly on the **basic** bundle + `defer`. Only pie/bar are used; do not switch to the full bundle.
- Text/tables/calendar must render without waiting on Plotly (`tryCharts` draws charts when both data and Plotly are ready).
