import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, date, timedelta

CSV_PATH = "Japan_Trip.csv"

st.set_page_config(page_title="Japan · Oct 2026", layout="wide", page_icon="🇯🇵")

import streamlit.components.v1 as components

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #090909; }
.block-container { padding: 2rem 2rem 4rem 2rem; max-width: 1400px; }

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

.label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 4px;
}

.big-num {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}

.sub { font-size: 12px; color: #555; margin-top: 2px; }

.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #555; margin-bottom: 28px; }

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

.progress-wrap { margin: 8px 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-bottom: 4px; }
.progress-track { background: #1a1a1a; border-radius: 3px; height: 4px; width: 100%; }
.progress-fill { height: 4px; border-radius: 3px; }

.stPlotlyChart { animation: fadeInUp 0.7s ease-out; }
.card-sm { animation: fadeInUp 0.5s ease-out; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }

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

/* Calendar toggle */
div[data-testid="stRadio"] label p { font-size: 11px !important; }

div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
details { border: none !important; box-shadow: none !important; }
details summary { border: none !important; }
.streamlit-expanderHeader { border: none !important; box-shadow: none !important; }
.streamlit-expanderContent { border: none !important; }
div[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #1a1a1a; }

@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .big-num { font-size: 20px !important; }
    div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .page-title { font-size: 18px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 3s)", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="label">Trip</div><div style="color:#fff;font-size:14px;font-weight:600;">Osaka, Japan</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Duration</div><div style="color:#fff;font-size:14px;">5 Oct – 11 Oct 2026</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Pax</div><div style="color:#fff;font-size:14px;">Andrea & Mummy</div>', unsafe_allow_html=True)

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
flight_total    = sum(filter(None, [parse_rm(get(r,7)) for r in [4,5]]))
accom_total     = sum(filter(None, [parse_rm(get(r,7)) for r in [13,14]]))
food_total      = sum(filter(None, [parse_rm(get(r,4)) for r in [19,20]]))
transport_total = sum(filter(None, [parse_rm(get(r,4)) for r in [25,26]]))
act_total       = sum(filter(None, [parse_rm(get(r,2)) for r in [32,33,34]]))
grand_total     = flight_total + accom_total + food_total + transport_total + act_total
andrea = parse_rm(get(39,1))
mummy  = parse_rm(get(40,1))

# Page title
st.markdown('<div class="page-title">Japan Trip Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Osaka · 5 Oct – 11 Oct 2026 · Two Pax</div>', unsafe_allow_html=True)

# KPI row
kpi_items = [
    ("Grand Total",   rm(grand_total),  "All expenses"),
    ("Flights",       rm(flight_total), "2 segments"),
    ("Accommodation", rm(accom_total),  "6 nights"),
    ("Food",          rm(food_total),   "Osaka"),
    ("Transport",     rm(transport_total), "Osaka & Kyoto"),
]
kpi_html = '<div style="background:#111111;border:1px solid #1f1f1f;border-radius:10px;overflow:hidden;margin-bottom:16px;">'
for i, (label, val, sub) in enumerate(kpi_items):
    border = "border-top:1px solid #1f1f1f;" if i > 0 else ""
    kpi_html += f"""
    <div style="padding:16px 24px;{border}">
        <div class="label">{label}</div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin:2px 0;">{val}</div>
        <div class="sub">{sub}</div>
    </div>"""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# Charts
st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns([1, 1])

categories = ["Flights", "Accommodation", "Food", "Transport", "Utilities"]
values = [flight_total, accom_total, food_total, transport_total, act_total]
colors = ["#ec4899", "#3b82f6", "#22c55e", "#f59e0b", "#7c6aff"]

with ch1:
    fig_donut = go.Figure(go.Pie(
        labels=categories,
        values=values if any(v > 0 for v in values) else [1,1,1,1,1],
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
    andrea_contrib = andrea or 0
    mummy_contrib  = mummy or 0
    fig_contrib = go.Figure(data=[
        go.Bar(name="Andrea", y=["Contribution"], x=[andrea_contrib], orientation="h", marker_color="#7c6aff", width=0.3),
        go.Bar(name="Mummy",  y=["Contribution"], x=[mummy_contrib],  orientation="h", marker_color="#ec4899", width=0.3),
    ])
    fig_contrib.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=40, b=20, l=60, r=20),
        barmode="stack",
        xaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555", size=11), linecolor="#1a1a1a"),
        yaxis=dict(showgrid=False, tickfont=dict(color="#888", size=12), linecolor="#1a1a1a"),
        height=180,
        title=dict(text="Contribution Split", font=dict(color="#666", size=12), x=0.02),
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

# Progress bars
st.markdown('<div class="section-header">Budget vs Estimate</div>', unsafe_allow_html=True)
for label, val, total, color in [
    ("Flights",       flight_total,    grand_total, "#ec4899"),
    ("Accommodation", accom_total,     grand_total, "#3b82f6"),
    ("Food",          food_total,      grand_total, "#22c55e"),
    ("Transport",     transport_total, grand_total, "#f59e0b"),
    ("Utilities",     act_total,       grand_total, "#7c6aff"),
]:
    p = round((val / total) * 100) if total else 0
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label"><span>{label}</span><span style="color:#fff">{rm(val)} &nbsp;<span style="color:#444">({p}%)</span></span></div>
        <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

# Calendar View
st.markdown('<div class="section-header">Calendar View</div>', unsafe_allow_html=True)

cal_mode = st.radio("", ["Travel", "Office Leave"], horizontal=True, label_visibility="collapsed")

cal_start = date(2026, 9, 28)   # Monday — week before trip
cal_end   = date(2026, 10, 18)  # Sunday — week after trip

flight_dates = {date(2026, 10, 5), date(2026, 10, 11)}
osaka_dates  = {date(2026, 10, d) for d in range(5, 11)}  # Oct 5–10 (checkout Oct 11)
leave_dates   = {date(2026, 10, d) for d in range(5, 10)}   # Mon–Fri office leave
weekend_dates = {date(2026, 10, d) for d in [3, 4, 10, 11]}  # weekends

cells_html = ""
cur = cal_start
while cur <= cal_end:
    month_tag = "" if cur.month == 10 else f"<div style='font-size:8px;color:#3a3a3a;line-height:1;margin-bottom:2px;'>SEP</div>"
    day_label = f"<div style='font-size:10px;color:#555;'>{cur.day}</div>"

    if cal_mode == "Travel":
        if cur in flight_dates:
            bg, border = "#2a1f4a", "#7c6aff"
        elif cur in osaka_dates:
            bg, border = "#2a0d1a", "#ec4899"
        else:
            bg, border = "#111111", "#1f1f1f"
    else:
        if cur in leave_dates:
            bg, border = "#2a1500", "#f59e0b"
        elif cur in weekend_dates:
            bg, border = "#0d2010", "#22c55e"
        else:
            bg, border = "#111111", "#1f1f1f"

    cells_html += (
        "<div style='background:" + bg + ";border:1px solid " + border + ";border-radius:6px;"
        "padding:10px 8px;min-height:56px;display:flex;flex-direction:column;justify-content:space-between;'>"
        + month_tag + day_label + "</div>"
    )
    cur += timedelta(days=1)

if cal_mode == "Travel":
    legend_html = """
<div style="display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a1f4a;border:1px solid #7c6aff;"></div>
        <span style="font-size:13px;color:#888;">Flight day</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a0d1a;border:1px solid #ec4899;"></div>
        <span style="font-size:13px;color:#888;">Osaka</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#111111;border:1px solid #1f1f1f;"></div>
        <span style="font-size:13px;color:#888;">No event</span>
    </div>
</div>"""
else:
    legend_html = """
<div style="display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a1500;border:1px solid #f59e0b;"></div>
        <span style="font-size:13px;color:#888;">Office Leave</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#0d2010;border:1px solid #22c55e;"></div>
        <span style="font-size:13px;color:#888;">Weekend</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#111111;border:1px solid #1f1f1f;"></div>
        <span style="font-size:13px;color:#888;">No event</span>
    </div>
</div>"""

headers_html = "".join(
    "<div style='text-align:center;font-size:10px;color:#444;padding:3px 0;'>" + h + "</div>"
    for h in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
)

cal_full = (
    "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap' rel='stylesheet'>"
    "<div style='font-family:Inter,sans-serif;background:#111111;border:1px solid #1f1f1f;border-radius:8px;padding:16px;'>"
    "<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:8px;'>"
    + headers_html + cells_html +
    "</div>" + legend_html + "</div>"
)
components.html(cal_full, height=380)

# Tables
st.markdown('<hr style="border:none;border-top:1px solid #1a1a1a;margin:12px 0;">', unsafe_allow_html=True)
with st.expander("Flights"):
    notes = [get(r,8) for r in [4,5]]
    flights_df = pd.DataFrame({
        "Date":        [get(r,0) for r in [4,5]],
        "Destination": [get(r,1) for r in [4,5]],
        "Departure":   [get(r,2) for r in [4,5]],
        "Arrival":     [get(r,3) for r in [4,5]],
        "Airline":     [get(r,4) for r in [4,5]],
        "Flight No.":  [get(r,5) for r in [4,5]],
        "Dep / Arr":   [get(r,6) for r in [4,5]],
        "Cost":        [get(r,7) for r in [4,5]],
        "Lounge":      [lounge_url(n) for n in notes],
    })
    st.dataframe(flights_df, hide_index=True, use_container_width=True, column_config={
        "Lounge": st.column_config.LinkColumn("Lounge", display_text="Available", width="small")
    })

with st.expander("Accommodation"):
    show({
        "Date":          [get(r,0) for r in [13,14]],
        "City":          [get(r,1) for r in [13,14]],
        "Accommodation": [get(r,2) for r in [13,14]],
        "Check In":      [get(r,3) for r in [13,14]],
        "Check Out":     [get(r,4) for r in [13,14]],
        "Nights":        [get(r,5) for r in [13,14]],
        "Budget/Night":  [get(r,6) for r in [13,14]],
        "Total":         [get(r,7) for r in [13,14]],
    })

with st.expander("Food"):
    show({
        "Dates":          [get(r,0) for r in [19,20]],
        "City":           [get(r,1) for r in [19,20]],
        "Days":           [get(r,2) for r in [19,20]],
        "Daily Estimate": [get(r,3) for r in [19,20]],
        "Total":          [get(r,4) for r in [19,20]],
    })

with st.expander("Transportation"):
    show({
        "Dates":          [get(r,0) for r in [25,26]],
        "City":           [get(r,1) for r in [25,26]],
        "Days":           [get(r,2) for r in [25,26]],
        "Daily Estimate": [get(r,3) for r in [25,26]],
        "Total":          [get(r,4) for r in [25,26]],
        "Notes":          [get(r,5) for r in [25,26]],
    })

with st.expander("Utilities & Others"):
    show({
        "Item":           [get(r,1) for r in [32,33,34]],
        "Cost (Two Pax)": [get(r,2) for r in [32,33,34]],
    })

if auto_refresh:
    time.sleep(3)
    st.rerun()
