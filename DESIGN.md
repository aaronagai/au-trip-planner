# Design System — Australia Trip Dashboard

## Product Context
- **What this is:** A personal trip dashboard for Sydney & Melbourne (Nov 2026) — live expense breakdown, budget split, and a travel/leave calendar, fed from a published Google Sheet.
- **Who it's for:** Aaron & Andrea (personal use, mobile + desktop).
- **Space/industry:** Personal travel planning meets a lightweight finance dashboard.
- **Project type:** Single-page data dashboard, static, hosted on GitHub Pages.

## Memorable Thing
Opening it should feel like **the trip is already real** — warm, premium, a little editorial. Not a cold finance app, not a cheesy travel brochure. Every choice below serves that.

## Aesthetic Direction
- **Direction:** Warm editorial. Deep warm ink instead of pure black, a sunlit accent, serif headlines.
- **Decoration level:** Intentional — one faint warm radial glow at the top of the page, hairline borders, restrained hover states. No texture/pattern noise.
- **Mood:** Confident, calm, characterful. Reads like a well-set travel itinerary that happens to track money.

## Typography
- **Display / headers / section titles:** `Fraunces` (variable, optical sizing) — warm characterful serif. The deliberate risk: almost no dashboard uses a serif, which is exactly why this one feels personal.
- **Body / UI:** `Geist` — clean modern grotesque, sharp at small sizes.
- **Numbers (KPIs, money, dates):** `Geist Mono` with `tabular-nums` — figures align like a ledger; premium fintech cue.
- **Loading:** Google Fonts, trimmed weight ranges, `display=swap` (text never blocks on fonts).
- **Notes:** `Inter` was deliberately removed (the universal AI-default UI font).

## Color
- **Approach:** Restrained. Warm dark neutrals + one signature accent + city semantics.
- **Background:** `#17130F` (warm ink) with a faint ochre radial glow.
- **Surfaces:** `#211B15` (cards), `#2A231B` (raised/hover), `#1B160F` (faint panel).
- **Borders:** `#322A20` (on surface), `#241E17` (faint dividers).
- **Text:** `#F5EFE6` (primary), `#A89C8A` (dim), `#6B6051` (labels/faint).
- **Accent — Outback Ochre `#E08A4B`:** primary accent, links, active states. Replaces the old AI-default purple `#7c6aff`.
- **Chart palette (Australian range):** ochre `#E08A4B`, terracotta `#C75D4A`, eucalyptus `#6FB6A3`, harbour blue `#5B9BD5`, golden `#E0A23C`.
- **Calendar semantics (kept learnable):** Sydney = blue `#5B9BD5`, Melbourne = eucalyptus `#6FB6A3`, flight day = ochre `#E08A4B`, office leave = golden, special holiday = `#E06B57`.

## Spacing
- **Base unit:** 8px.
- **Density:** Comfortable — a touch more breathing room than the original.
- **Page padding:** `clamp(12px, 3vw, 24px)` with safe-area insets for notched phones.

## Layout
- **Approach:** Grid-disciplined with editorial touches (serif section headers break the data grid).
- **Max content width:** 1140px.
- **Border radius:** sm 6px, md 10px, lg 14px.
- **Responsive:** charts stack ≤880px; KPIs go 3-up ≥900px and single-column below; tables scroll horizontally on phones.

## Motion
- **Approach:** Minimal-functional. A soft `fadeUp` (0.5s) when data lands; progress bars ease their width; subtle hover lifts on calendar cells and KPI rows.
- **Respects `prefers-reduced-motion`** (all animation/transition disabled).

## Performance (load architecture)
- Data fetch is kicked off in `<head>` (`window.__sheetData`) so it runs in parallel with font + script downloads instead of after them.
- Charts use the **Plotly "basic" bundle** (~1.0 MB) instead of the full bundle (~3.5 MB) — only pie + bar are used.
- Plotly is loaded with `defer`; text/tables/calendar render the instant data arrives, charts fill in when the bundle is ready (`tryCharts`).
- `preconnect`/`dns-prefetch` to `docs.google.com` and the font hosts.

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-20 | Initial design system created | /design-consultation; warm editorial direction chosen to make the trip feel real |
| 2026-06-20 | Dropped Inter + purple accent | Both are AI-default "slop" signals; replaced with Geist/Fraunces + outback ochre |
| 2026-06-20 | Plotly basic bundle + deferred load + parallel fetch | Cut ~2.6 MB off the critical path; charts no longer block first paint |
