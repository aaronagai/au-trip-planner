import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

CSV_PATH = "Melbourne_Sydney_Nov.csv"

st.set_page_config(page_title="AU Trip · Nov 2026", layout="wide", page_icon="✈")

import streamlit.components.v1 as components


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #090909; }
.block-container { padding: 2rem 2rem 4rem 2rem; max-width: 1400px; }

/* Cards */
.card {
    background: #111111;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.card-sm {
    background: #111111;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 16px 20px;
}

/* Section label */
.label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 4px;
}

/* Big number */
.big-num {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.big-num-sm {
    font-size: 18px;
    font-weight: 600;
    color: #fff;
}

/* Sub text */
.sub { font-size: 12px; color: #555; margin-top: 2px; }

/* Page title */
.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #555; margin-bottom: 28px; }

/* Section header */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #888;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 28px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a1a1a;
}

/* Badge */
.badge {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #888;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 500;
}

/* Progress bar */
.progress-wrap { margin: 8px 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-bottom: 4px; }
.progress-track { background: #1a1a1a; border-radius: 3px; height: 4px; width: 100%; }
.progress-fill { height: 4px; border-radius: 3px; }

/* Chart entrance animation */
.stPlotlyChart {
    animation: fadeInUp 0.7s ease-out;
}
.card-sm {
    animation: fadeInUp 0.5s ease-out;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }

/* Remove expander border */
div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
details { border: none !important; box-shadow: none !important; }
details summary { border: none !important; }
.streamlit-expanderHeader { border: none !important; box-shadow: none !important; }
.streamlit-expanderContent { border: none !important; }
div[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #1a1a1a; }

/* Mobile responsive */
@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .big-num { font-size: 20px !important; }
    div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .page-title { font-size: 18px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Dashboard ──────────────────────────────────────────────────
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 3s)", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="label">Trip</div><div style="color:#fff;font-size:14px;font-weight:600;">Melbourne & Sydney</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Duration</div><div style="color:#fff;font-size:14px;">7 Nov – 20 Nov 2026</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Pax</div><div style="color:#fff;font-size:14px;">Aaron & Andrea</div>', unsafe_allow_html=True)

def parse_rm(val):
    if pd.isna(val): return None
    val = str(val).replace("RM", "").replace(",", "").strip()
    try: return float(val)
    except: return None

def rm(val, decimals=0):
    if val is None: return "—"
    return f"RM {val:,.{decimals}f}"

def show(data):
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

df = pd.read_csv(CSV_PATH, header=None)

def get(r, c):
    try:
        v = df.iloc[r, c]
        return "" if pd.isna(v) else str(v).strip().replace("\r\n", "\n")
    except: return ""

def lounge_url(val):
    return val if val.startswith("http") else ""

# Parse data
flight_total = sum(filter(None, [parse_rm(get(r,7)) for r in [4,5,6,7,8]]))
accom_total  = sum(filter(None, [parse_rm(get(r,7)) for r in [13,14]]))
food_total   = sum(filter(None, [parse_rm(get(r,4)) for r in [19,20]]))
transport_total = sum(filter(None, [parse_rm(get(r,4)) for r in [25,26]]))
act_total    = sum(filter(None, [parse_rm(get(r,2)) for r in [32,33,34]]))
grand_total  = flight_total + accom_total + food_total + transport_total + act_total
aaron        = parse_rm(get(39,1))
andrea       = parse_rm(get(40,1))

# Page title
st.markdown('<div class="page-title">AU Trip Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Melbourne & Sydney · November 2026 · Two Pax</div>', unsafe_allow_html=True)

# Top KPI row
kpi_items = [
    ("Grand Total",    rm(grand_total),  "All expenses"),
    ("Flights",        rm(flight_total), "5 segments"),
    ("Accommodation",  rm(accom_total),  "9 nights"),
    ("Food",           rm(food_total),   "Both cities"),
    ("Transport",      rm(transport_total), "Both cities"),
]
r1, r2 = st.columns(2), st.columns(3)
for i, (label, val, sub) in enumerate(kpi_items):
    col = r1[i] if i < 2 else r2[i - 2]
    with col:
        st.markdown(f"""
        <div class="card-sm">
            <div class="label">{label}</div>
            <div class="big-num">{val}</div>
            <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# Charts row
st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns([1, 1])

categories = ["Flights", "Accommodation", "Food", "Transport", "Utilities"]
values = [flight_total, accom_total, food_total, transport_total, act_total]
colors = ["#7c6aff", "#3b82f6", "#22c55e", "#f59e0b", "#ec4899"]

with ch1:
    fig_donut = go.Figure(go.Pie(
        labels=categories,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color="#090909", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>RM %{value:,.0f}<br>%{percent}<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>{rm(grand_total)}</b>",
        x=0.5, y=0.5, font=dict(size=16, color="white"), showarrow=False
    )
    fig_donut.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color="#888", size=12), bgcolor="rgba(0,0,0,0)"),
        height=280,
        title=dict(text="Expense Distribution", font=dict(color="#666", size=12), x=0.02)
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with ch2:
    aaron_contrib = aaron or 0
    andrea_contrib = andrea or 0
    total_contrib = aaron_contrib + andrea_contrib
    aaron_pct = round((aaron_contrib / total_contrib) * 100) if total_contrib else 0
    andrea_pct = 100 - aaron_pct
    fig_contrib = go.Figure(data=[
        go.Bar(name="Aaron",  y=["Contribution"], x=[aaron_contrib],  orientation="h", marker_color="#7c6aff"),
        go.Bar(name="Andrea", y=["Contribution"], x=[andrea_contrib], orientation="h", marker_color="#ec4899"),
    ])
    fig_contrib.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=40, b=20, l=60, r=20),
        barmode="stack",
        xaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555", size=11), linecolor="#1a1a1a"),
        yaxis=dict(showgrid=False, tickfont=dict(color="#888", size=12), linecolor="#1a1a1a"),
        height=180,
        title=dict(text="Aaron <> Andrea Contribution", font=dict(color="#666", size=12), x=0.02),
        legend=dict(font=dict(color="#888", size=12), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_contrib, use_container_width=True, config={"displayModeBar": False})
    components.html("""
    <script>
    setTimeout(() => {
        const plots = window.parent.document.querySelectorAll('.js-plotly-plot');
        plots.forEach(p => { try { Plotly.animate(p, null); } catch(e) {} });
    }, 500);
    </script>
    """, height=0)

# Budget progress bars
st.markdown('<div class="section-header">Budget vs Estimate</div>', unsafe_allow_html=True)
estimate = parse_rm(get(39,1)) or grand_total
pct = min((grand_total / estimate) * 100, 100) if estimate else 0
bar_color = "#22c55e" if pct < 85 else "#f59e0b" if pct < 100 else "#ef4444"

for label, val, total, color in [
    ("Flights",       flight_total,    grand_total, "#7c6aff"),
    ("Accommodation", accom_total,     grand_total, "#3b82f6"),
    ("Food",          food_total,      grand_total, "#22c55e"),
    ("Transport",     transport_total, grand_total, "#f59e0b"),
    ("Activities",    act_total,       grand_total, "#ec4899"),
]:
    p = round((val / total) * 100) if total else 0
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label"><span>{label}</span><span style="color:#fff">{rm(val)} &nbsp;<span style="color:#444">({p}%)</span></span></div>
        <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

# Tables
st.markdown("---")
with st.expander("Flights"):
    notes = [get(r,8) for r in [4,5,6,7,8]]
    flights_df = pd.DataFrame({
        "Date":        [get(r,0) for r in [4,5,6,7,8]],
        "Destination": [get(r,1) for r in [4,5,6,7,8]],
        "Departure":   [get(r,2) for r in [4,5,6,7,8]],
        "Arrival":     [get(r,3) for r in [4,5,6,7,8]],
        "Airline":     [get(r,4) for r in [4,5,6,7,8]],
        "Flight No.":  [get(r,5) for r in [4,5,6,7,8]],
        "Dep / Arr":   [get(r,6) for r in [4,5,6,7,8]],
        "Cost":        [get(r,7) for r in [4,5,6,7,8]],
        "Lounge":      [lounge_url(n) for n in notes],
    })
    st.dataframe(flights_df, hide_index=True, use_container_width=True, column_config={
        "Lounge": st.column_config.LinkColumn("Lounge", display_text="Available")
    })

with st.expander("Accommodation"):
    show({
        "Date":         [get(r,0) for r in [13,14]],
        "City":         [get(r,1) for r in [13,14]],
        "Accommodation":[get(r,2) for r in [13,14]],
        "Check In":     [get(r,3) for r in [13,14]],
        "Check Out":    [get(r,4) for r in [13,14]],
        "Nights":       [get(r,5) for r in [13,14]],
        "Budget/Night": [get(r,6) for r in [13,14]],
        "Total":        [get(r,7) for r in [13,14]],
    })

tl, tr = st.columns(2)
with tl:
    with st.expander("Food"):
        show({
            "Dates":          [get(r,0) for r in [19,20]],
            "City":           [get(r,1) for r in [19,20]],
            "Days":           [get(r,2) for r in [19,20]],
            "Daily Estimate": [get(r,3) for r in [19,20]],
            "Total":          [get(r,4) for r in [19,20]],
        })

with tr:
    with st.expander("Transportation"):
        show({
            "Dates":          [get(r,0) for r in [25,26]],
            "City":           [get(r,1) for r in [25,26]],
            "Days":           [get(r,2) for r in [25,26]],
            "Daily Estimate": [get(r,3) for r in [25,26]],
            "Total":          [get(r,4) for r in [25,26]],
            "Notes":          [get(r,5) for r in [25,26]],
        })

with st.expander("Activities & Utilities"):
    show({
        "Item":           [get(r,1) for r in [32,33,34]],
        "Cost (Two Pax)": [get(r,2) for r in [32,33,34]],
    })

if auto_refresh:
    time.sleep(3)
    st.rerun()

# ── (old overlay code removed) ───
if False:
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }
    body { background: transparent; overflow: hidden; }
    .overlay {
        position: fixed; top:0; left:0; width:100vw; height:100vh;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        background: rgba(9,9,9,0.75);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        z-index: 9999;
    }
    .title { font-size:28px; font-weight:800; color:#fff; margin-bottom:6px; }
    .sub { font-size:14px; color:#555; margin-bottom:48px; }
    .peek-row { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:40px; }
    .card {
        background:#111; border:1px solid #222; border-radius:14px;
        padding:32px 24px; text-align:center; cursor:pointer;
        transition: transform 0.25s, box-shadow 0.25s, opacity 0.25s;
        width:160px;
    }
    .card.side { transform: scale(0.82) translateY(10px); opacity:0.35; pointer-events:none; }
    .card.center { transform: scale(1.05); border-color:#7c6aff; box-shadow: 0 0 40px rgba(124,106,255,0.25); }
    .card-btn { background:#111; border:1px solid #1f1f1f; border-radius:14px;
        padding:32px 24px; text-align:center; cursor:pointer;
        transition: transform 0.25s, box-shadow 0.25s;
        width:160px; }
    .card-btn:hover { transform:scale(1.08); border-color:#7c6aff; box-shadow:0 0 30px rgba(124,106,255,0.2); }
    .emoji { font-size:44px; margin-bottom:10px; }
    .name { font-size:16px; font-weight:700; color:#fff; }
    </style>
    </head>
    <body>
    <div class="overlay">
        <div style="font-size:40px;margin-bottom:14px;">✈️ 🦘</div>
        <div class="title">oi oi mate 👋</div>
        <div class="sub">before we start... which bubs are you??</div>
        <div class="peek-row">
            <div class="card side"><div class="emoji">🌏</div><div class="name">???</div></div>
            <div class="card-btn" onclick="select('Aaron')"><div class="emoji">🧑‍💻</div><div class="name">Aaron</div></div>
            <div class="card center" style="pointer-events:none"><div class="emoji">🫵</div><div class="name">You</div></div>
            <div class="card-btn" onclick="select('Andrea')"><div class="emoji">🥰</div><div class="name">Andrea</div></div>
            <div class="card side"><div class="emoji">🌏</div><div class="name">???</div></div>
        </div>
    </div>
    <script>
    // Expand iframe to fullscreen
    const iframe = window.frameElement;
    if (iframe) {
        iframe.style.position = 'fixed';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.width = '100vw';
        iframe.style.height = '100vh';
        iframe.style.zIndex = '9999';
        iframe.style.border = 'none';
        iframe.style.background = 'transparent';
    }
    function select(name) {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('bubs', name);
        window.parent.location.href = url.toString();
    }
    </script>
    </body>
    </html>
    """, height=1)

elif st.session_state.page == "greet":
    bubs = st.session_state.bubs
    if bubs == "Aaron":
        emoji, msg, sub = "🧑‍💻", "Hello, Aaron The Bubs.", "Identity confirmed. Initialising expense matrix and flight telemetry. Standby for full mission briefing."
    else:
        emoji, msg, sub = "🥰", "Hello, Andrea The Bubs.", "Identity confirmed. Loading trip parameters and itinerary data. Please proceed to the dashboard."

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }}
    body {{ background: transparent; overflow: hidden; }}
    .overlay {{
        position: fixed; top:0; left:0; width:100vw; height:100vh;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        background: rgba(9,9,9,0.75);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; z-index: 9999; padding: 40px;
    }}
    .emoji {{ font-size:72px; margin-bottom:20px; }}
    .title {{ font-size:32px; font-weight:800; color:#fff; margin-bottom:10px; }}
    .sub {{ font-size:14px; color:#555; margin-bottom:40px; max-width:400px; line-height:1.6; }}
    .btn {{
        background:#7c6aff; color:#fff; border:none; border-radius:8px;
        padding:12px 32px; font-size:15px; font-weight:600; cursor:pointer;
        transition: background 0.2s; margin:6px;
    }}
    .btn:hover {{ background:#6a58ee; }}
    .btn-ghost {{
        background:transparent; color:#444; border:1px solid #222; border-radius:8px;
        padding:10px 24px; font-size:13px; cursor:pointer; transition: color 0.2s; margin:6px;
    }}
    .btn-ghost:hover {{ color:#888; }}
    </style>
    </head>
    <body>
    <div class="overlay">
        <div class="emoji">{emoji}</div>
        <div class="title">{msg}</div>
        <div class="sub">{sub}</div>
        <div>
            <button class="btn" onclick="goStart()">🚀 Let's gooo</button>
        </div>
        <div>
            <button class="btn-ghost" onclick="goBack()">← not me lol</button>
        </div>
    </div>
    <script>
    const iframe = window.frameElement;
    if (iframe) {{
        iframe.style.position = 'fixed';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.width = '100vw';
        iframe.style.height = '100vh';
        iframe.style.zIndex = '9999';
        iframe.style.border = 'none';
        iframe.style.background = 'transparent';
    }}
    function goStart() {{
        const url = new URL(window.parent.location.href);
        url.searchParams.set('start', '1');
        window.parent.location.href = url.toString();
    }}
    function goBack() {{
        const url = new URL(window.parent.location.href);
        url.searchParams.set('back', '1');
        window.parent.location.href = url.toString();
    }}
    </script>
    </body>
    </html>
    """, height=1)
