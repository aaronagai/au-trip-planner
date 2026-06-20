# Australia Trip Dashboard

Single-file static dashboard (`index.html`) for a Sydney & Melbourne trip (Nov 2026).
Data is fetched live from a published Google Sheet (CSV export) and rendered client-side.
Charts use Plotly; everything else is vanilla JS/CSS. Hosted on GitHub Pages.

## Design
Dark dashboard theme: `#090909` background, `#111` surfaces, `#7c6aff` accent, Inter font.
See `DESIGN.md` for the full palette. Do not change colors/fonts without explicit user approval.

## Performance
- Keep the data fetch in `<head>` (`window.__sheetData`) so it runs in parallel with downloads.
- Keep Plotly on the **basic** bundle + `defer`. Only pie/bar are used; do not switch to the full bundle.
- Text/tables/calendar must render without waiting on Plotly (`tryCharts` draws charts when both data and Plotly are ready).
