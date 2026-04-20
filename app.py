import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Portfolio Terminal", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

html, body { background: #0a0a0a !important; }
.stApp, .main, .block-container {
    background-color: #0a0a0a !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: #e0e0e0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid #1a3a1a !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Share Tech Mono', monospace !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: #00ff41 !important;
}
section[data-testid="stSidebar"] input {
    background: #111 !important;
    border: 1px solid #1a3a1a !important;
    color: #00ff41 !important;
    border-radius: 0 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #111 !important;
    border: 1px solid #1a3a1a !important;
    border-radius: 0 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * { color: #00ff41 !important; }
[data-testid="stFileUploader"] {
    background: #0f0f0f !important;
    border: 1px dashed #1a3a1a !important;
}
[data-testid="stFileUploader"] * { color: #00ff41 !important; }

/* Header */
.term-header {
    background: linear-gradient(90deg, #0a0a0a, #0c1c0c, #0a0a0a);
    border-top: 2px solid #00ff41;
    border-bottom: 2px solid #00ff41;
    padding: 14px 22px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.term-title {
    font-family: 'Orbitron', monospace;
    font-size: 24px;
    font-weight: 900;
    color: #00ff41;
    letter-spacing: 6px;
    text-shadow: 0 0 18px #00ff4170;
}
.term-sub { color: #444; font-size: 10px; letter-spacing: 3px; margin-top: 3px; }
.term-time { color: #ff6b00; font-size: 12px; letter-spacing: 2px; }

/* Metric cards */
.mc {
    background: #0f0f0f;
    border: 1px solid #1c2e1c;
    border-left: 3px solid #00ff41;
    padding: 13px 15px;
    margin: 2px 0;
    font-family: 'Share Tech Mono', monospace;
}
.mc-lbl { color: #454545; font-size: 9px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 5px; }
.mc-grn { color: #00ff41; font-size: 17px; font-weight: bold; }
.mc-red { color: #ff3333; font-size: 17px; font-weight: bold; }
.mc-org { color: #ff6b00; font-size: 17px; font-weight: bold; }
.mc-wht { color: #e0e0e0; font-size: 17px; font-weight: bold; }

/* Section headings */
.sec-h {
    border-bottom: 1px solid #1a3a1a;
    padding-bottom: 4px;
    margin-bottom: 10px;
    color: #00ff41;
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    letter-spacing: 4px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0a0a0a !important;
    border-bottom: 1px solid #1a3a1a !important;
}
.stTabs [data-baseweb="tab"] {
    color: #444 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #00ff41 !important;
    border-bottom: 2px solid #00ff41 !important;
}
.stTabs [data-baseweb="tab-panel"] { background: #0a0a0a !important; }

/* Dataframe */
[data-testid="stDataFrame"] th {
    background: #0d1a0d !important;
    color: #00ff41 !important;
    font-size: 10px !important;
}

/* Main area selectbox */
.stSelectbox [data-baseweb="select"] > div {
    background: #0f0f0f !important;
    border: 1px solid #1a3a1a !important;
    color: #e0e0e0 !important;
    border-radius: 0 !important;
}
.stSelectbox [data-baseweb="select"] * { color: #e0e0e0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #1a3a1a; }
::-webkit-scrollbar-thumb:hover { background: #00ff41; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Expander */
details { background: #0f0f0f !important; border: 1px solid #1a3a1a !important; border-radius: 0 !important; }
summary { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace !important; }

/* Divider */
hr { border-color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly base layout ────────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="#0a0a0a", plot_bgcolor="#0a0a0a",
    font=dict(family="Share Tech Mono, monospace", color="#888", size=11),
    xaxis=dict(gridcolor="#141414", linecolor="#1a3a1a", tickfont=dict(color="#555"), zeroline=False),
    yaxis=dict(gridcolor="#141414", linecolor="#1a3a1a", tickfont=dict(color="#555"), zeroline=False),
    margin=dict(t=50, b=40, l=60, r=20),
    legend=dict(bgcolor="#0f0f0f", bordercolor="#1a3a1a", borderwidth=1, font=dict(color="#888")),
)

# ── European ticker suffix map ────────────────────────────────────────────────
EU_MAP = {
    "ASML":"ASML.AS","ADYEN":"ADYEN.AS","VWRA":"VWRA.L",
    "SAF":"SAF.PA","RMS":"RMS.PA","AIR":"AIR.PA",
    "MC":"MC.PA","OR":"OR.PA","SAN":"SAN.PA",
    "BNP":"BNP.PA","AXA":"AXA.PA","TTE":"TTE.PA",
    "SIE":"SIE.DE","ALV":"ALV.DE","BMW":"BMW.DE",
    "SAP":"SAP.DE","DTE":"DTE.DE","VOW3":"VOW3.DE",
    "NOVO":"NOVO-B.CO","SHELL":"SHEL.L",
}

def yft(tk): return EU_MAP.get(tk.upper(), tk.upper())

# ── CSV Parser ────────────────────────────────────────────────────────────────
def parse_csv(file):
    content = file.read()
    try:
        raw = pd.read_csv(io.BytesIO(content))
    except Exception:
        raw = pd.read_csv(io.BytesIO(content), encoding="latin-1")

    raw.columns = [c.strip() for c in raw.columns]

    if "Action" not in raw.columns:
        st.error("❌ 'Action' column not found. Please export History from Trading 212.")
        return pd.DataFrame()

    mask  = raw["Action"].str.lower().str.contains("buy|sell", na=False)
    trades = raw[mask].copy()

    if trades.empty:
        st.error("❌ No trades found in this file.")
        return pd.DataFrame()

    trades.rename(columns={
        "No. of shares":            "qty",
        "Price / share":            "price",
        "Currency (Price / share)": "price_ccy",
        "Exchange rate":            "fx",
        "Total":                    "total_eur",
        "Currency (Total)":         "total_ccy",
        "Ticker":                   "ticker",
        "Name":                     "name",
        "Time":                     "time",
        "Action":                   "action",
    }, inplace=True)

    for col in ["qty", "total_eur"]:
        if col in trades.columns:
            trades[col] = pd.to_numeric(trades[col], errors="coerce").fillna(0)

    trades["ticker"] = trades["ticker"].astype(str).str.strip().str.upper()
    trades.loc[trades["action"].str.lower().str.contains("sell"), "qty"] *= -1

    if "time" in trades.columns:
        trades["time"] = pd.to_datetime(trades["time"], errors="coerce")
        trades.sort_values("time", inplace=True)

    result = []
    for tk, grp in trades.groupby("ticker"):
        tq, tc = 0.0, 0.0
        nm = grp["name"].iloc[-1] if "name" in grp.columns else tk
        for _, r in grp.iterrows():
            q   = float(r["qty"])
            eur = abs(float(r["total_eur"]))
            if q > 0:
                tc += eur; tq += q
            elif tq > 0 and q < 0:
                frac = min(abs(q) / tq, 1.0)
                tc  *= (1 - frac)
                tq   = max(0.0, tq + q)
        if tq > 0.0001:
            result.append({
                "ticker":   tk,
                "name":     str(nm)[:26],
                "qty":      round(tq, 6),
                "avg_eur":  round(tc / tq, 4),
                "cost_eur": round(tc, 2),
                "yf_tk":    yft(tk),
            })
    return pd.DataFrame(result)

# ── Live data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_live(tks):
    out = {}
    for t in tks:
        try:
            info = yf.Ticker(t).info
            out[t] = {
                "price":     float(info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose") or 0),
                "ccy":       info.get("currency", "USD"),
                "pe":        info.get("trailingPE"),
                "fpe":       info.get("forwardPE"),
                "peg":       info.get("pegRatio"),
                "div":       info.get("dividendYield"),
                "cap":       info.get("marketCap"),
                "h52":       info.get("fiftyTwoWeekHigh"),
                "l52":       info.get("fiftyTwoWeekLow"),
                "eps":       info.get("trailingEps"),
                "epsf":      info.get("forwardEps"),
                "sector":    info.get("sector", "Other"),
                "beta":      info.get("beta"),
                "book":      info.get("bookValue"),
                "name":      info.get("shortName", t),
            }
        except Exception:
            out[t] = {"price": 0, "ccy": "USD", "name": t, "sector": "Other"}
    return out

@st.cache_data(ttl=300, show_spinner=False)
def get_fx(fr_ccy, to_ccy="EUR"):
    if fr_ccy == to_ccy: return 1.0
    try:
        h = yf.Ticker(f"{fr_ccy}{to_ccy}=X").history(period="1d")
        if not h.empty: return float(h["Close"].iloc[-1])
    except Exception: pass
    return {"USD": 0.92, "GBP": 1.17, "GBp": 0.0117, "CHF": 1.05}.get(fr_ccy, 1.0)

@st.cache_data(ttl=600, show_spinner=False)
def fetch_hist(t, period):
    try: return yf.Ticker(t).history(period=period)
    except: return pd.DataFrame()

# ── Valuation ─────────────────────────────────────────────────────────────────
def graham(eps, book):
    if eps and book and eps > 0 and book > 0:
        return round((22.5 * eps * book) ** 0.5, 2)
    return None

def dcf(epsf, g, d, tg, yrs):
    if not epsf or epsf <= 0: return None
    try:
        cf, pvs = epsf, []
        for y in range(1, yrs+1):
            cf *= (1+g); pvs.append(cf/(1+d)**y)
        return round(sum(pvs) + (cf*(1+tg)/(d-tg))/(1+d)**yrs, 2)
    except: return None

# ── Format helpers ────────────────────────────────────────────────────────────
def fm(v, s="€"):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    if abs(v) >= 1e12: return f"{s}{v/1e12:.2f}T"
    if abs(v) >= 1e9:  return f"{s}{v/1e9:.2f}B"
    if abs(v) >= 1e6:  return f"{s}{v/1e6:.2f}M"
    return f"{s}{v:,.2f}"
def fp(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "N/A"
    return f"{v*100:.2f}%"
def fr(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "N/A"
    return f"{v:.2f}x"
def card(l, v, c="mc-wht"):
    return f'<div class="mc"><div class="mc-lbl">{l}</div><div class="{c}">{v}</div></div>'
def pnl_c(v): return "mc-grn" if v>0 else ("mc-red" if v<0 else "mc-wht")
def sgn(v): return "+" if v>0 else ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:Orbitron,monospace;color:#00ff41;font-size:13px;letter-spacing:3px;">⚡ TERMINAL CONFIG</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Trading 212 CSV", type=["csv"])
    st.markdown("---")
    st.markdown('<p style="color:#444;font-size:9px;letter-spacing:2px;">DCF PARAMETERS</p>', unsafe_allow_html=True)
    dcf_g  = st.number_input("Growth Rate (%)",     0.0, 50.0, 12.0, 0.5) / 100
    dcf_d  = st.number_input("Discount Rate (%)",   1.0, 30.0, 10.0, 0.5) / 100
    dcf_tg = st.number_input("Terminal Growth (%)", 0.0, 10.0,  3.0, 0.5) / 100
    dcf_yr = st.slider("Projection Years", 5, 20, 10)
    st.markdown("---")
    chart_p = st.selectbox("Chart Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3)

# ── Header ────────────────────────────────────────────────────────────────────
now_s = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class="term-header">
  <div>
    <div class="term-title">◈ PORTFOLIO TERMINAL</div>
    <div class="term-sub">LIVE MARKET ANALYTICS  ·  TRADING 212 CSV SYNC</div>
  </div>
  <div class="term-time">⬤ LIVE &nbsp;|&nbsp; {now_s}</div>
</div>""", unsafe_allow_html=True)

# ── Landing ───────────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
      <div style="font-family:Orbitron,monospace;font-size:60px;color:#00ff41;opacity:0.06;letter-spacing:12px;">◈</div>
      <div style="font-family:Orbitron,monospace;font-size:15px;color:#00ff41;letter-spacing:6px;margin:16px 0 10px;">AWAITING DATA INPUT</div>
      <div style="color:#272727;font-size:11px;letter-spacing:2px;line-height:2.4;">
        UPLOAD YOUR TRADING 212 CSV EXPORT IN THE SIDEBAR<br>
        <span style="color:#181818;">──────────────────────────────</span><br>
        1. OPEN TRADING 212 APP<br>
        2. TAP HISTORY → ··· → EXPORT AS CSV<br>
        3. UPLOAD THE FILE IN THE LEFT SIDEBAR
      </div>
    </div>""", unsafe_allow_html=True)

    with st.expander("📋  Expected CSV format (Trading 212 History export)"):
        st.dataframe(pd.DataFrame({
            "Action":["Market buy","Market buy","Market sell"],
            "Time":["2025-09-03 13:44:16","2025-09-18 17:07:15","2026-04-15 14:34:36"],
            "Ticker":["GOOGL","MCO","MCO"],
            "Name":["Alphabet","Moody's","Moody's"],
            "No. of shares":[0.31,0.052,1.0],
            "Price / share":[229.07,496.19,442.48],
            "Exchange rate":[1.1647,1.1790,1.1796],
            "Total":[60.88,22.00,374.56],
            "Currency (Total)":["EUR","EUR","EUR"],
        }), use_container_width=True, hide_index=True)
    st.stop()

# ── Parse ─────────────────────────────────────────────────────────────────────
with st.spinner("Parsing CSV…"):
    holdings = parse_csv(uploaded)

if holdings.empty:
    st.stop()

# ── Fetch live ────────────────────────────────────────────────────────────────
yf_tks = tuple(holdings["yf_tk"].unique().tolist())
with st.spinner(f"Fetching live data for {len(yf_tks)} tickers…"):
    live = fetch_live(yf_tks)

usd_eur = get_fx("USD"); gbp_eur = get_fx("GBP"); gbx_eur = gbp_eur / 100

def to_eur(price, ccy):
    if ccy == "EUR": return price
    if ccy == "USD": return price * usd_eur
    if ccy == "GBP": return price * gbp_eur
    if ccy in ("GBp","GBX"): return price * gbx_eur
    return price

# ── Enrich ────────────────────────────────────────────────────────────────────
rows = []
for _, h in holdings.iterrows():
    tk   = h["ticker"]; yt = h["yf_tk"]
    ld   = live.get(yt, {})
    ccy  = ld.get("ccy", "USD")
    pe   = to_eur(float(ld.get("price") or 0), ccy)
    qty  = float(h["qty"]); ae = float(h["avg_eur"]); ce = float(h["cost_eur"])
    mv   = pe * qty; pnl = mv - ce; pct = (pnl/ce*100) if ce else 0
    rows.append({
        "Ticker":tk,"Name":str(ld.get("name",h["name"]))[:24],
        "Sector":ld.get("sector","Other"),"Qty":qty,"Avg(€)":ae,
        "Price(€)":round(pe,2),"Val(€)":round(mv,2),"Cost(€)":round(ce,2),
        "P&L(€)":round(pnl,2),"P&L(%)":round(pct,2),
        "P/E":ld.get("pe"),"FwdP/E":ld.get("fpe"),"PEG":ld.get("peg"),
        "DivYld":ld.get("div"),"52Hi":ld.get("h52"),"52Lo":ld.get("l52"),
        "MktCap":ld.get("cap"),"Beta":ld.get("beta"),
        "EPS":ld.get("eps"),"EPSf":ld.get("epsf"),"Book":ld.get("book"),
        "CCY":ccy,"YFT":yt,
    })

df = pd.DataFrame(rows)

# ── KPIs ──────────────────────────────────────────────────────────────────────
tc = df["Cost(€)"].sum(); tv = df["Val(€)"].sum()
tp = tv-tc; tpct = (tp/tc*100) if tc else 0
best = df.loc[df["P&L(%)"].idxmax()]; worst = df.loc[df["P&L(%)"].idxmin()]
wins = (df["P&L(%)"]>0).sum(); losses = (df["P&L(%)"]<=0).sum()

c1,c2,c3,c4 = st.columns(4)
c1.markdown(card("PORTFOLIO VALUE", fm(tv)),               unsafe_allow_html=True)
c2.markdown(card("TOTAL INVESTED",  fm(tc), "mc-org"),     unsafe_allow_html=True)
c3.markdown(card("UNREALISED P&L",  f"{sgn(tp)}{fm(tp)}", pnl_c(tp)), unsafe_allow_html=True)
c4.markdown(card("TOTAL RETURN",    f"{sgn(tpct)}{tpct:.2f}%", pnl_c(tpct)), unsafe_allow_html=True)

c5,c6,c7,c8 = st.columns(4)
c5.markdown(card("POSITIONS",      str(len(df))),          unsafe_allow_html=True)
c6.markdown(card("BEST",  f"{best['Ticker']} +{best['P&L(%)']:.1f}%",  "mc-grn"), unsafe_allow_html=True)
c7.markdown(card("WORST", f"{worst['Ticker']} {worst['P&L(%)']:.1f}%", "mc-red"), unsafe_allow_html=True)
c8.markdown(card("WIN/LOSS", f"{wins}W / {losses}L"),      unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4 = st.tabs(["📊  HOLDINGS","📈  CHARTS","🔬  DEEP DIVE","💡  FAIR VALUE"])

# ═══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    cl,cr = st.columns([3,2], gap="medium")
    with cl:
        st.markdown('<div class="sec-h">◈ LIVE HOLDINGS TABLE</div>', unsafe_allow_html=True)
        disp = df[["Ticker","Name","Qty","Avg(€)","Price(€)","Val(€)","Cost(€)","P&L(€)","P&L(%)","P/E","FwdP/E","PEG","DivYld","Beta"]].copy()
        disp["P&L(%)"]  = disp["P&L(%)"].apply(lambda v: f"+{v:.2f}%" if v>=0 else f"{v:.2f}%")
        disp["P/E"]     = disp["P/E"].apply(fr)
        disp["FwdP/E"]  = disp["FwdP/E"].apply(fr)
        disp["PEG"]     = disp["PEG"].apply(fr)
        disp["DivYld"]  = disp["DivYld"].apply(fp)
        disp["Beta"]    = disp["Beta"].apply(lambda v: f"{v:.2f}" if pd.notna(v) else "N/A")
        st.dataframe(disp, use_container_width=True, hide_index=True,
                     column_config={
                         "Val(€)":  st.column_config.NumberColumn("Val(€)",  format="€%.2f"),
                         "Cost(€)": st.column_config.NumberColumn("Cost(€)", format="€%.2f"),
                         "Avg(€)":  st.column_config.NumberColumn("Avg(€)",  format="€%.4f"),
                         "Price(€)":st.column_config.NumberColumn("Price(€)",format="€%.2f"),
                         "P&L(€)":  st.column_config.NumberColumn("P&L(€)",  format="€%.2f"),
                     })
    with cr:
        st.markdown('<div class="sec-h">◈ ALLOCATION DONUT</div>', unsafe_allow_html=True)
        pal = ["#00ff41","#ff6b00","#4488ff","#ff3333","#ffcc00",
               "#00ccff","#ff44aa","#88ff00","#cc44ff","#ff8844",
               "#44ffcc","#ffaa44","#4444ff","#ff4488","#aaffaa"]
        fig_d = go.Figure(go.Pie(
            labels=df["Ticker"], values=df["Val(€)"], hole=0.60,
            marker=dict(colors=pal[:len(df)], line=dict(color="#0a0a0a",width=2)),
            textfont=dict(family="Share Tech Mono",size=10),
            hovertemplate="<b>%{label}</b><br>€%{value:,.2f}<br>%{percent}<extra></extra>",
        ))
        fig_d.add_annotation(text=f"<b>{fm(tv)}</b><br><span style='font-size:9px;color:#666'>TOTAL</span>",
                             x=0.5, y=0.5, showarrow=False,
                             font=dict(family="Orbitron,monospace",size=11,color="#00ff41"))
        fig_d.update_layout(**PL, height=300, showlegend=True,
                            legend=dict(orientation="v",x=1.02,y=0.5))
        st.plotly_chart(fig_d, use_container_width=True)

        st.markdown('<div class="sec-h">◈ SECTOR EXPOSURE</div>', unsafe_allow_html=True)
        sec = df.groupby("Sector")["Val(€)"].sum().reset_index().sort_values("Val(€)")
        fig_s = go.Figure(go.Bar(
            x=sec["Val(€)"], y=sec["Sector"], orientation="h",
            marker=dict(color=sec["Val(€)"], colorscale=[[0,"#0d1a0d"],[1,"#00ff41"]],
                        line=dict(color="#00ff41",width=0.5)),
            hovertemplate="%{y}: €%{x:,.0f}<extra></extra>"))
        fig_s.update_layout(**PL, height=max(150, len(sec)*35), showlegend=False)
        st.plotly_chart(fig_s, use_container_width=True)

# ═══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-h">◈ P&L BY POSITION</div>', unsafe_allow_html=True)
    dfs = df.sort_values("P&L(€)", ascending=False)
    fig_p = go.Figure(go.Bar(
        x=dfs["Ticker"], y=dfs["P&L(€)"],
        marker=dict(color=["#00ff41" if v>=0 else "#ff3333" for v in dfs["P&L(€)"]],
                    line=dict(color="#0a0a0a",width=1)),
        hovertemplate="<b>%{x}</b><br>P&L: €%{y:,.2f}<extra></extra>",
        text=[f"{sgn(v)}€{abs(v):.0f}" for v in dfs["P&L(€)"]],
        textposition="outside", textfont=dict(color="#666",size=9),
    ))
    fig_p.add_hline(y=0, line_color="#333", line_width=1)
    fig_p.update_layout(**PL, height=320, yaxis_title="P&L (€)",
                        title=dict(text="UNREALISED P&L BY POSITION",
                                   font=dict(family="Orbitron,monospace",size=10,color="#555")))
    st.plotly_chart(fig_p, use_container_width=True)

    cl2,cr2 = st.columns(2, gap="medium")
    with cl2:
        st.markdown('<div class="sec-h">◈ P/E COMPARISON</div>', unsafe_allow_html=True)
        pe_df = df[df["P/E"].apply(lambda x: x is not None and pd.notna(x) and float(x)>0)].sort_values("P/E")
        if not pe_df.empty:
            fig_pe = go.Figure()
            fig_pe.add_trace(go.Bar(name="Trailing P/E", x=pe_df["Ticker"], y=pe_df["P/E"],
                                    marker_color="#00ff41"))
            fwd = pe_df[pe_df["FwdP/E"].apply(lambda x: x is not None and pd.notna(x) and float(x)>0)]
            if not fwd.empty:
                fig_pe.add_trace(go.Bar(name="Forward P/E", x=fwd["Ticker"], y=fwd["FwdP/E"],
                                        marker_color="#ff6b00"))
            fig_pe.update_layout(**PL, height=280, barmode="group",
                                 title=dict(text="P/E RATIOS",font=dict(family="Orbitron,monospace",size=10,color="#555")))
            st.plotly_chart(fig_pe, use_container_width=True)
        else:
            st.info("P/E data not available for current holdings.")
    with cr2:
        st.markdown('<div class="sec-h">◈ 52-WEEK RANGE</div>', unsafe_allow_html=True)
        rdf = df[df["52Hi"].notna() & df["52Lo"].notna()].copy()
        if not rdf.empty:
            fig_r = go.Figure()
            for _, row in rdf.iterrows():
                lo,hi,px_r = float(row["52Lo"]),float(row["52Hi"]),float(row["Price(€)"])
                rng = hi-lo if hi!=lo else 1
                fig_r.add_trace(go.Bar(x=[rng],y=[row["Ticker"]],base=[lo],orientation="h",
                                       marker=dict(color="#101a10",line=dict(color="#1a3a1a",width=1)),
                                       showlegend=False,
                                       hovertemplate=f"<b>{row['Ticker']}</b><br>Lo: {lo:.2f}<br>Hi: {hi:.2f}<br>Now: {px_r:.2f}<extra></extra>"))
                fig_r.add_trace(go.Scatter(x=[px_r],y=[row["Ticker"]],mode="markers",
                                           marker=dict(color="#00ff41",size=10,symbol="diamond"),
                                           showlegend=False,hoverinfo="skip"))
            fig_r.update_layout(**PL, height=280,
                                title=dict(text="52-WEEK RANGE  ◈ = CURRENT",
                                           font=dict(family="Orbitron,monospace",size=10,color="#555")))
            st.plotly_chart(fig_r, use_container_width=True)
        else:
            st.info("52-week range data not available.")

# ═══ TAB 3 ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-h">◈ INDIVIDUAL STOCK ANALYSIS</div>', unsafe_allow_html=True)
    sel_tk = st.selectbox("Select Ticker", df["Ticker"].tolist())
    sel_row = df[df["Ticker"]==sel_tk].iloc[0]
    ld = live.get(sel_row["YFT"], {})

    s1,s2,s3,s4,s5,s6 = st.columns(6)
    s1.markdown(card("PRICE(€)",  fm(sel_row["Price(€)"],"€"), "mc-grn"), unsafe_allow_html=True)
    s2.markdown(card("P/E",       fr(ld.get("pe")), "mc-org"), unsafe_allow_html=True)
    s3.markdown(card("FWD P/E",   fr(ld.get("fpe")), "mc-org"), unsafe_allow_html=True)
    s4.markdown(card("PEG",       fr(ld.get("peg")), "mc-wht"), unsafe_allow_html=True)
    s5.markdown(card("MKT CAP",   fm(ld.get("cap"),"€"), "mc-wht"), unsafe_allow_html=True)
    s6.markdown(card("DIV YIELD", fp(ld.get("div")), "mc-grn"), unsafe_allow_html=True)

    hist = fetch_hist(sel_row["YFT"], chart_p)
    if not hist.empty:
        fig_c = make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.03,row_heights=[0.75,0.25])
        fig_c.add_trace(go.Candlestick(
            x=hist.index, open=hist["Open"], high=hist["High"],
            close=hist["Close"], low=hist["Low"],
            increasing=dict(line=dict(color="#00ff41"),fillcolor="#00ff4155"),
            decreasing=dict(line=dict(color="#ff3333"),fillcolor="#ff333355"),
            name="OHLC"), row=1, col=1)
        if len(hist)>=20:
            fig_c.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(20).mean(),
                mode="lines", line=dict(color="#ff6b00",width=1.2,dash="dot"), name="MA20", opacity=0.8), row=1, col=1)
        if len(hist)>=50:
            fig_c.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(50).mean(),
                mode="lines", line=dict(color="#4488ff",width=1.2,dash="dash"), name="MA50", opacity=0.8), row=1, col=1)

        # avg entry in native currency
        ae = sel_row["Avg(€)"]
        ccy = sel_row["CCY"]
        if ccy=="USD" and usd_eur>0: avg_n = ae/usd_eur
        elif ccy=="GBP" and gbp_eur>0: avg_n = ae/gbp_eur
        else: avg_n = ae
        fig_c.add_hline(y=avg_n, line_color="#ffcc00", line_width=1.5, line_dash="longdash",
                        annotation_text=f" AVG {avg_n:.2f}", annotation_font=dict(color="#ffcc00",size=10),
                        row=1, col=1)

        vc = ["#00ff41" if c>=o else "#ff3333" for c,o in zip(hist["Close"],hist["Open"])]
        fig_c.add_trace(go.Bar(x=hist.index, y=hist["Volume"], marker_color=vc, name="Vol", opacity=0.5), row=2, col=1)

        fig_c.update_layout(**PL, height=520, xaxis_rangeslider_visible=False,
                            title=dict(text=f"{sel_tk}  ·  {ld.get('name',sel_tk)}  ·  {chart_p.upper()}",
                                       font=dict(family="Orbitron,monospace",size=12,color="#00ff41")))
        fig_c.update_xaxes(gridcolor="#101010"); fig_c.update_yaxes(gridcolor="#101010")
        st.plotly_chart(fig_c, use_container_width=True)

        # RSI
        delta=hist["Close"].diff(); gain=delta.clip(lower=0).rolling(14).mean()
        loss=(-delta.clip(upper=0)).rolling(14).mean(); rsi=100-(100/(1+gain/loss))
        fig_rsi = go.Figure(go.Scatter(x=hist.index, y=rsi, mode="lines",
                                       line=dict(color="#00ff41",width=1.5),
                                       fill="tozeroy", fillcolor="#00ff4110", name="RSI(14)"))
        fig_rsi.add_hline(y=70,line_color="#ff3333",line_dash="dot",
                          annotation_text=" OVERBOUGHT (70)",annotation_font=dict(color="#ff3333",size=9))
        fig_rsi.add_hline(y=30,line_color="#4488ff",line_dash="dot",
                          annotation_text=" OVERSOLD (30)",annotation_font=dict(color="#4488ff",size=9))
        fig_rsi.update_layout(**PL, height=190, yaxis=dict(range=[0,100],gridcolor="#101010"),
                              title=dict(text="RSI (14)",font=dict(family="Orbitron,monospace",size=10,color="#555")))
        st.plotly_chart(fig_rsi, use_container_width=True)
    else:
        st.warning(f"⚠️ No price history for {sel_row['YFT']}. The ticker may need a different exchange suffix.")

# ═══ TAB 4 ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-h">◈ INTRINSIC VALUE ESTIMATOR</div>', unsafe_allow_html=True)
    iv_rows = []
    for _, row in df.iterrows():
        ld2 = live.get(row["YFT"],{})
        dv  = dcf(ld2.get("epsf"), dcf_g, dcf_d, dcf_tg, dcf_yr)
        gv  = graham(ld2.get("eps"), ld2.get("book"))
        px  = row["Price(€)"]

        def mos(fv_native):
            if not fv_native: return None
            fv_eur = to_eur(fv_native, row["CCY"])
            if fv_eur <= 0: return None
            return round((1 - px/fv_eur)*100, 1)

        vals = [v for v in [dv, gv] if v is not None]
        comp = round(np.mean(vals), 2) if vals else None
        mc   = mos(comp)

        def verdict(m):
            if m is None: return "—"
            if m > 30:    return "🟢 UNDERVALUED"
            if m > 0:     return "🟡 FAIR"
            if m > -20:   return "🟠 SLIGHTLY RICH"
            return "🔴 OVERVALUED"

        iv_rows.append({
            "Ticker":row["Ticker"],"Price(€)":px,"DCF($)":dv,"Graham($)":gv,"CompFV($)":comp,
            "MoS(DCF)": f"{mos(dv):+.1f}%"  if mos(dv) is not None else "N/A",
            "MoS(Gra)": f"{mos(gv):+.1f}%"  if mos(gv) is not None else "N/A",
            "MoS(Comp)":f"{mc:+.1f}%"        if mc      is not None else "N/A",
            "Verdict":  verdict(mc or mos(dv)),
        })
    iv_df = pd.DataFrame(iv_rows)
    st.dataframe(iv_df, use_container_width=True, hide_index=True,
                 column_config={
                     "Price(€)":  st.column_config.NumberColumn(format="€%.2f"),
                     "DCF($)":    st.column_config.NumberColumn(format="$%.2f"),
                     "Graham($)": st.column_config.NumberColumn(format="$%.2f"),
                     "CompFV($)": st.column_config.NumberColumn(format="$%.2f"),
                 })

    plot_iv = iv_df[iv_df["CompFV($)"].notna()].copy()
    if not plot_iv.empty:
        st.markdown('<div class="sec-h" style="margin-top:14px;">◈ PRICE vs FAIR VALUE</div>', unsafe_allow_html=True)
        plot_iv["FV(€)"] = plot_iv.apply(lambda r: to_eur(r["CompFV($)"], df[df["Ticker"]==r["Ticker"]]["CCY"].values[0]), axis=1)
        fig_iv = go.Figure()
        fig_iv.add_trace(go.Bar(name="Current Price (€)", x=plot_iv["Ticker"], y=plot_iv["Price(€)"], marker_color="#ff6b00"))
        fig_iv.add_trace(go.Bar(name="Fair Value (€)",    x=plot_iv["Ticker"], y=plot_iv["FV(€)"],    marker_color="#00ff41", opacity=0.75))
        fig_iv.update_layout(**PL, height=300, barmode="group", yaxis_title="Price (€)",
                             title=dict(text="CURRENT PRICE vs FAIR VALUE (€)",
                                        font=dict(family="Orbitron,monospace",size=10,color="#555")))
        st.plotly_chart(fig_iv, use_container_width=True)

    st.markdown("""<div style="background:#0d0d0d;border-left:3px solid #ff6b00;
         padding:10px 14px;margin-top:10px;font-size:9px;color:#444;letter-spacing:1px;line-height:1.9;">
    ⚠️  DISCLAIMER: Figures are estimates based on DCF &amp; Graham's Formula using yfinance data.
    NOT financial advice. Adjust sidebar parameters to reflect your assumptions.
    </div>""", unsafe_allow_html=True)
