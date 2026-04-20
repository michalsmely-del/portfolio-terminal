import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import io
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TERMINAL | Portfolio Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── BLOOMBERG TERMINAL CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #080808;
        --bg-secondary: #0d0d0d;
        --bg-card: #0f0f0f;
        --bg-border: #1c1c1c;
        --neon-green: #00ff41;
        --neon-orange: #ff8c00;
        --neon-red: #ff2244;
        --neon-blue: #00b4d8;
        --neon-yellow: #ffd60a;
        --text-primary: #d4d4d4;
        --text-secondary: #666666;
        --font-mono: 'Share Tech Mono', monospace;
        --font-main: 'Rajdhani', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: var(--font-main);
        background-color: var(--bg-primary) !important;
        color: var(--text-primary);
    }
    .stApp { background-color: var(--bg-primary) !important; }
    #MainMenu, footer, header { visibility: hidden; }

    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #1a1a1a;
    }
    [data-testid="stSidebar"] * { font-family: var(--font-mono) !important; color: var(--text-primary); }

    ::-webkit-scrollbar { width: 3px; height: 3px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #2a2a2a; }

    [data-testid="metric-container"] {
        background: var(--bg-card) !important;
        border: 1px solid #1c1c1c;
        border-radius: 2px;
        padding: 14px 18px !important;
        position: relative;
    }
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 2px; height: 100%;
        background: var(--neon-green);
    }
    [data-testid="metric-container"] label {
        color: #555 !important;
        font-family: var(--font-mono) !important;
        font-size: 10px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    [data-testid="stMetricValue"] {
        font-family: var(--font-mono) !important;
        font-size: 24px !important;
        color: var(--neon-green) !important;
    }
    [data-testid="stMetricDelta"] { font-family: var(--font-mono) !important; font-size: 11px !important; }
    [data-testid="stMetricDelta"] svg { display: none; }

    .stButton > button {
        background: transparent !important;
        color: var(--neon-green) !important;
        border: 1px solid var(--neon-green) !important;
        border-radius: 1px !important;
        font-family: var(--font-mono) !important;
        font-size: 10px !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        padding: 8px 24px !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background: var(--neon-green) !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(0,255,65,0.25) !important;
    }

    [data-testid="stFileUploader"] {
        border: 1px dashed #2a2a2a !important;
        background: #0a0a0a !important;
        border-radius: 2px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #1a1a1a;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #444 !important;
        font-family: var(--font-mono) !important;
        font-size: 10px !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        padding: 12px 28px !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--neon-green) !important;
        border-bottom: 2px solid var(--neon-green) !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: #0a0a0a !important;
        border: 1px solid #2a2a2a !important;
        font-family: var(--font-mono) !important;
        color: var(--text-primary) !important;
        border-radius: 2px !important;
    }
    div[data-testid="stNumberInput"] input {
        background: #0a0a0a !important;
        border: 1px solid #2a2a2a !important;
        color: var(--neon-green) !important;
        font-family: var(--font-mono) !important;
        border-radius: 2px !important;
    }

    h1, h2, h3 {
        font-family: var(--font-main) !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        color: var(--text-primary) !important;
    }

    .block-container { padding: 2rem 2rem 2rem 2rem !important; }

    .stDataFrame { border: 1px solid #1a1a1a !important; }
    .stDataFrame table { font-family: var(--font-mono) !important; font-size: 11px !important; }

    .stAlert > div {
        background: #001a00 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 2px !important;
        font-family: var(--font-mono) !important;
        font-size: 11px !important;
        color: var(--neon-green) !important;
    }

    .stSpinner > div { border-top-color: var(--neon-green) !important; }

    .terminal-label {
        font-family: var(--font-mono);
        font-size: 9px;
        color: #444;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .section-title {
        font-family: var(--font-mono);
        font-size: 10px;
        color: var(--neon-green);
        letter-spacing: 4px;
        text-transform: uppercase;
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .gain-text { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace; }
    .loss-text { color: #ff2244 !important; font-family: 'Share Tech Mono', monospace; }
    .neutral-text { color: #888 !important; font-family: 'Share Tech Mono', monospace; }
</style>
""", unsafe_allow_html=True)


# ─── PLOTLY THEME ───────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='#080808',
    plot_bgcolor='#080808',
    font=dict(family='Share Tech Mono', color='#888888', size=11),
    xaxis=dict(gridcolor='#111111', linecolor='#1c1c1c', tickcolor='#333', zerolinecolor='#1c1c1c'),
    yaxis=dict(gridcolor='#111111', linecolor='#1c1c1c', tickcolor='#333', zerolinecolor='#1c1c1c'),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1c1c1c', borderwidth=1),
)
GREEN = '#00ff41'
RED = '#ff2244'
ORANGE = '#ff8c00'
BLUE = '#00b4d8'
YELLOW = '#ffd60a'


# ─── HELPERS ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_ticker_data(ticker: str):
    """Fetch yfinance info + history for a single ticker."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        hist = t.history(period="1y")
        return info, hist
    except Exception:
        return {}, pd.DataFrame()


def safe_get(d: dict, key: str, default=None):
    val = d.get(key, default)
    return default if val is None or val != val else val


def fmt_currency(v, sym="$"):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    if abs(v) >= 1e12:
        return f"{sym}{v/1e12:.2f}T"
    if abs(v) >= 1e9:
        return f"{sym}{v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"{sym}{v/1e6:.2f}M"
    return f"{sym}{v:,.2f}"


def fmt_pct(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"{v*100:.2f}%"


def fmt_num(v, decimals=2):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"{v:.{decimals}f}"


# ─── CSV PARSER ──────────────────────────────────────────────────────────────────
def parse_trading212_csv(file) -> tuple[pd.DataFrame, str]:
    """
    Handles Trading 212 History CSV and Portfolio CSV exports.
    Returns (dataframe, detected_type).
    """
    try:
        content = file.read()
        # Try different encodings
        for enc in ['utf-8', 'utf-8-sig', 'latin-1']:
            try:
                df = pd.read_csv(io.BytesIO(content), encoding=enc)
                break
            except Exception:
                continue

        df.columns = df.columns.str.strip()
        cols_lower = [c.lower() for c in df.columns]

        # ── PORTFOLIO export (simple snapshot)
        if any('ticker' in c for c in cols_lower) and any('shares' in c or 'quantity' in c for c in cols_lower):
            # Map common column name variations
            col_map = {}
            for col in df.columns:
                cl = col.lower()
                if 'ticker' in cl:
                    col_map['ticker'] = col
                elif 'quantity' in cl or ('shares' in cl and 'price' not in cl):
                    col_map['quantity'] = col
                elif 'avg' in cl and 'price' in cl:
                    col_map['avg_price'] = col
                elif 'current' in cl and 'price' in cl:
                    col_map['current_price'] = col
                elif 'name' in cl and 'company' not in cl:
                    col_map['name'] = col
                elif 'result' in cl or ('p&l' in cl) or ('profit' in cl and 'loss' in cl):
                    col_map['pnl'] = col

            df = df.rename(columns={v: k for k, v in col_map.items()})
            df['ticker'] = df['ticker'].astype(str).str.strip().str.upper()
            df['quantity'] = pd.to_numeric(df.get('quantity', 0), errors='coerce').fillna(0)
            df['avg_price'] = pd.to_numeric(df.get('avg_price', 0), errors='coerce').fillna(0)
            return df, 'portfolio'

        # ── HISTORY export (transaction log)
        elif any('action' in c for c in cols_lower) or any('type' in c for c in cols_lower):
            col_map = {}
            for col in df.columns:
                cl = col.lower()
                if cl == 'ticker' or cl == 'instrument':
                    col_map['ticker'] = col
                elif 'time' in cl or 'date' in cl:
                    col_map['time'] = col
                elif cl in ('action', 'type', 'transaction type'):
                    col_map['action'] = col
                elif 'shares' in cl or 'no. of shares' in cl or 'quantity' in cl:
                    col_map['quantity'] = col
                elif 'price per share' in cl or 'price / share' in cl or cl == 'price':
                    col_map['price'] = col
                elif 'currency conversion' not in cl and 'total' in cl:
                    col_map['total'] = col
                elif 'currency' in cl and 'conversion' not in cl and 'result' not in cl:
                    col_map['currency'] = col

            df = df.rename(columns={v: k for k, v in col_map.items()})

            # Filter to buy/sell rows only
            if 'action' in df.columns:
                df['action'] = df['action'].astype(str).str.lower()
                df = df[df['action'].str.contains('buy|sell|market buy|market sell|limit buy|limit sell', na=False)]

            df['ticker'] = df['ticker'].astype(str).str.strip().str.upper()
            df['quantity'] = pd.to_numeric(df.get('quantity', 0), errors='coerce').fillna(0)
            df['price'] = pd.to_numeric(df.get('price', 0), errors='coerce').fillna(0)
            df['total'] = pd.to_numeric(df.get('total', 0), errors='coerce').fillna(0)
            df = df[df['ticker'].str.len() > 0]
            df = df[df['ticker'] != 'NAN']
            return df, 'history'

        else:
            # Fallback: try to auto-detect
            return df, 'unknown'

    except Exception as e:
        st.error(f"CSV parsing error: {e}")
        return pd.DataFrame(), 'error'


def compute_holdings_from_history(df: pd.DataFrame) -> pd.DataFrame:
    """Compute current holdings and average entry price from transaction history."""
    holdings = {}
    for _, row in df.iterrows():
        ticker = row.get('ticker', '')
        if not ticker or ticker == 'nan':
            continue
        qty = float(row.get('quantity', 0))
        price = float(row.get('price', 0))
        action = str(row.get('action', '')).lower()

        if ticker not in holdings:
            holdings[ticker] = {'shares': 0.0, 'cost_basis': 0.0}

        if 'buy' in action:
            cost = qty * price
            holdings[ticker]['cost_basis'] = (
                (holdings[ticker]['cost_basis'] * holdings[ticker]['shares'] + cost)
                / (holdings[ticker]['shares'] + qty)
                if (holdings[ticker]['shares'] + qty) > 0 else 0
            )
            holdings[ticker]['shares'] += qty
        elif 'sell' in action:
            holdings[ticker]['shares'] = max(0, holdings[ticker]['shares'] - qty)
            if holdings[ticker]['shares'] == 0:
                holdings[ticker]['cost_basis'] = 0

    rows = []
    for ticker, data in holdings.items():
        if data['shares'] > 0.001:
            rows.append({'ticker': ticker, 'quantity': data['shares'], 'avg_price': data['cost_basis']})
    return pd.DataFrame(rows)


# ─── INTRINSIC VALUE ─────────────────────────────────────────────────────────────
def graham_number(eps: float, bvps: float) -> float:
    """Graham's Number: sqrt(22.5 * EPS * BVPS)"""
    if eps is None or bvps is None or eps <= 0 or bvps <= 0:
        return None
    return np.sqrt(22.5 * eps * bvps)


def dcf_valuation(fcf: float, growth_rate: float, terminal_growth: float,
                  discount_rate: float, shares: float, years: int = 10) -> float:
    """Simple DCF: project FCF for `years`, then terminal value."""
    if fcf is None or fcf <= 0 or shares is None or shares <= 0:
        return None
    fcfs = [fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]
    pv_fcfs = sum(f / ((1 + discount_rate) ** i) for i, f in enumerate(fcfs, 1))
    terminal_val = fcfs[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal_val / ((1 + discount_rate) ** years)
    intrinsic = (pv_fcfs + pv_terminal) / shares
    return intrinsic


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family: Share Tech Mono; font-size: 9px; color: #00ff41;
                letter-spacing: 4px; text-transform: uppercase; margin-bottom: 4px;'>
        ▶ BLOOMBERG TERMINAL
    </div>
    <div style='font-family: Share Tech Mono; font-size: 18px; color: #d4d4d4;
                letter-spacing: 2px; border-bottom: 1px solid #1c1c1c; padding-bottom: 12px;
                margin-bottom: 20px;'>
        Portfolio OS
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="terminal-label">Upload CSV Export</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Trading 212 CSV",
        type=['csv'],
        label_visibility="collapsed",
        help="Upload your Trading 212 'History' or 'Portfolio' CSV export"
    )

    st.markdown("---")
    st.markdown('<div class="terminal-label">Settings</div>', unsafe_allow_html=True)
    currency_symbol = st.selectbox("Base Currency", ["$", "£", "€"], index=0)
    refresh_data = st.button("↺  REFRESH LIVE DATA")

    st.markdown("---")
    st.markdown("""
    <div style='font-family: Share Tech Mono; font-size: 9px; color: #333; letter-spacing: 2px; line-height: 2;'>
        <div>TRADING 212 INTEGRATION</div>
        <div style='color: #555'>CSV → History Export</div>
        <div style='color: #555'>CSV → Portfolio Export</div>
        <div style='margin-top: 8px; color: #00ff41'>■ LIVE DATA: yfinance</div>
        <div style='color: #555'>5-min cache</div>
    </div>
    """, unsafe_allow_html=True)

    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    st.markdown(f"""
    <div style='font-family: Share Tech Mono; font-size: 9px; color: #333;
                margin-top: 20px; letter-spacing: 1px;'>
        {now}
    </div>
    """, unsafe_allow_html=True)


# ─── HEADER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display: flex; align-items: baseline; gap: 16px; margin-bottom: 8px;'>
    <span style='font-family: Rajdhani; font-weight: 700; font-size: 28px;
                 letter-spacing: 6px; text-transform: uppercase; color: #d4d4d4;'>
        PORTFOLIO
    </span>
    <span style='font-family: Share Tech Mono; font-size: 12px; color: #00ff41;
                 letter-spacing: 3px;'>
        TERMINAL v2.0
    </span>
    <span style='font-family: Share Tech Mono; font-size: 10px; color: #333;
                 letter-spacing: 2px; margin-left: auto;'>
        POWERED BY YFINANCE + TRADING 212
    </span>
</div>
<div style='height: 1px; background: linear-gradient(to right, #00ff41, #1c1c1c);
            margin-bottom: 28px;'></div>
""", unsafe_allow_html=True)


# ─── MAIN LOGIC ──────────────────────────────────────────────────────────────────
if uploaded_file is None:
    # ── Welcome / Demo screen
    st.markdown("""
    <div style='text-align: center; padding: 60px 0;'>
        <div style='font-family: Share Tech Mono; font-size: 11px; color: #333;
                    letter-spacing: 4px; margin-bottom: 16px;'>AWAITING DATA INPUT</div>
        <div style='font-family: Rajdhani; font-size: 42px; font-weight: 700;
                    color: #1a1a1a; letter-spacing: 4px;'>UPLOAD CSV</div>
        <div style='font-family: Share Tech Mono; font-size: 11px; color: #444;
                    letter-spacing: 2px; margin-top: 12px;'>
            Trading 212 → Account → History → Export CSV
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='border: 1px solid #1c1c1c; background: #0a0a0a; padding: 20px;
                    border-radius: 2px; border-left: 2px solid #00ff41;'>
            <div style='font-family: Share Tech Mono; font-size: 9px; color: #00ff41;
                        letter-spacing: 3px; margin-bottom: 8px;'>FEATURE 01</div>
            <div style='font-family: Rajdhani; font-size: 16px; font-weight: 600;
                        color: #d4d4d4;'>Live P&L Tracking</div>
            <div style='font-family: Share Tech Mono; font-size: 10px; color: #555;
                        margin-top: 6px; line-height: 1.6;'>
                Real-time gains/losses via yfinance market data
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='border: 1px solid #1c1c1c; background: #0a0a0a; padding: 20px;
                    border-radius: 2px; border-left: 2px solid #ff8c00;'>
            <div style='font-family: Share Tech Mono; font-size: 9px; color: #ff8c00;
                        letter-spacing: 3px; margin-bottom: 8px;'>FEATURE 02</div>
            <div style='font-family: Rajdhani; font-size: 16px; font-weight: 600;
                        color: #d4d4d4;'>Intrinsic Value</div>
            <div style='font-family: Share Tech Mono; font-size: 10px; color: #555;
                        margin-top: 6px; line-height: 1.6;'>
                DCF & Graham's Number fair value estimates
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='border: 1px solid #1c1c1c; background: #0a0a0a; padding: 20px;
                    border-radius: 2px; border-left: 2px solid #00b4d8;'>
            <div style='font-family: Share Tech Mono; font-size: 9px; color: #00b4d8;
                        letter-spacing: 3px; margin-bottom: 8px;'>FEATURE 03</div>
            <div style='font-family: Rajdhani; font-size: 16px; font-weight: 600;
                        color: #d4d4d4;'>Fundamental Analysis</div>
            <div style='font-family: Share Tech Mono; font-size: 10px; color: #555;
                        margin-top: 6px; line-height: 1.6;'>
                P/E, Forward P/E, PEG, Dividend Yield & more
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ── Parse uploaded file
with st.spinner("Parsing CSV..."):
    df_raw, csv_type = parse_trading212_csv(uploaded_file)

if df_raw.empty:
    st.error("Could not parse CSV. Please upload a valid Trading 212 History or Portfolio export.")
    st.stop()

# ── Build holdings DataFrame
if csv_type == 'history':
    holdings_df = compute_holdings_from_history(df_raw)
    st.success(f"✓ History CSV parsed — {len(df_raw)} transactions → {len(holdings_df)} active positions")
elif csv_type == 'portfolio':
    holdings_df = df_raw[['ticker', 'quantity', 'avg_price']].copy()
    st.success(f"✓ Portfolio CSV parsed — {len(holdings_df)} positions found")
else:
    st.warning("Could not auto-detect CSV type. Attempting generic parse...")
    holdings_df = pd.DataFrame()
    st.stop()

if holdings_df.empty:
    st.error("No active holdings found after parsing.")
    st.stop()

tickers = holdings_df['ticker'].unique().tolist()

# ── Fetch live data for all tickers
live_data = {}
with st.spinner(f"Fetching live market data for {len(tickers)} tickers..."):
    progress = st.progress(0)
    for i, ticker in enumerate(tickers):
        info, hist = fetch_ticker_data(ticker)
        live_data[ticker] = {'info': info, 'hist': hist}
        progress.progress((i + 1) / len(tickers))
    progress.empty()

# ── Enrich holdings_df with live prices
rows = []
for _, row in holdings_df.iterrows():
    ticker = row['ticker']
    qty = float(row['quantity'])
    avg_price = float(row['avg_price'])
    info = live_data.get(ticker, {}).get('info', {})
    current_price = safe_get(info, 'currentPrice') or safe_get(info, 'regularMarketPrice') or avg_price
    market_value = qty * current_price
    cost_basis = qty * avg_price
    gain = market_value - cost_basis
    gain_pct = (gain / cost_basis * 100) if cost_basis > 0 else 0
    rows.append({
        'ticker': ticker,
        'name': safe_get(info, 'shortName', ticker),
        'shares': qty,
        'avg_price': avg_price,
        'current_price': current_price,
        'market_value': market_value,
        'cost_basis': cost_basis,
        'gain': gain,
        'gain_pct': gain_pct,
        'pe_ratio': safe_get(info, 'trailingPE'),
        'forward_pe': safe_get(info, 'forwardPE'),
        'peg_ratio': safe_get(info, 'pegRatio'),
        'div_yield': safe_get(info, 'dividendYield'),
        'market_cap': safe_get(info, 'marketCap'),
        'week52_high': safe_get(info, 'fiftyTwoWeekHigh'),
        'week52_low': safe_get(info, 'fiftyTwoWeekLow'),
        'beta': safe_get(info, 'beta'),
        'eps': safe_get(info, 'trailingEps'),
        'forward_eps': safe_get(info, 'forwardEps'),
        'bvps': safe_get(info, 'bookValue'),
        'free_cashflow': safe_get(info, 'freeCashflow'),
        'shares_outstanding': safe_get(info, 'sharesOutstanding'),
        'revenue_growth': safe_get(info, 'revenueGrowth'),
        'sector': safe_get(info, 'sector', 'Unknown'),
    })

portfolio = pd.DataFrame(rows)

# ── Portfolio summary
total_value = portfolio['market_value'].sum()
total_cost = portfolio['cost_basis'].sum()
total_gain = portfolio['gain'].sum()
total_gain_pct = (total_gain / total_cost * 100) if total_cost > 0 else 0
best = portfolio.loc[portfolio['gain_pct'].idxmax()]
worst = portfolio.loc[portfolio['gain_pct'].idxmin()]


# ─── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  OVERVIEW  ", "  ANALYSIS  ", "  INTRINSIC VALUE  ", "  CHARTS  "
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — OVERVIEW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    # KPI row
    st.markdown('<div class="section-title">▸ Portfolio Summary</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Value", f"{currency_symbol}{total_value:,.2f}")
    c2.metric("Total Cost", f"{currency_symbol}{total_cost:,.2f}")
    gain_delta = f"▲ {total_gain_pct:.2f}%" if total_gain >= 0 else f"▼ {abs(total_gain_pct):.2f}%"
    c3.metric("Unrealised P&L", f"{'+' if total_gain>=0 else ''}{currency_symbol}{total_gain:,.2f}", gain_delta)
    c4.metric("Best Performer", f"{best['ticker']}  +{best['gain_pct']:.1f}%")
    c5.metric("Worst Performer", f"{worst['ticker']}  {worst['gain_pct']:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Donut chart + bar chart side by side
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-title">▸ Asset Allocation</div>', unsafe_allow_html=True)
        colors = [GREEN, ORANGE, BLUE, YELLOW, RED,
                  '#9b5de5', '#f15bb5', '#00bbf9', '#fee440', '#00f5d4']
        fig_donut = go.Figure(go.Pie(
            labels=portfolio['ticker'],
            values=portfolio['market_value'],
            hole=0.65,
            marker=dict(colors=colors[:len(portfolio)],
                        line=dict(color='#080808', width=2)),
            textfont=dict(family='Share Tech Mono', size=10, color='#888'),
            textposition='outside',
            hovertemplate="<b>%{label}</b><br>%{value:$,.2f}<br>%{percent}<extra></extra>",
        ))
        fig_donut.update_layout(**PLOT_LAYOUT, height=320, showlegend=True,
                                 legend=dict(orientation="v", x=1, y=0.5,
                                             font=dict(size=10, family='Share Tech Mono')),
                                 annotations=[dict(
                                     text=f"<b>{currency_symbol}{total_value/1000:.1f}K</b>",
                                     x=0.5, y=0.5, font_size=16,
                                     font_family='Share Tech Mono', font_color='#d4d4d4',
                                     showarrow=False
                                 )])
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">▸ Gain / Loss by Position</div>', unsafe_allow_html=True)
        portfolio_sorted = portfolio.sort_values('gain_pct', ascending=True)
        bar_colors = [GREEN if g >= 0 else RED for g in portfolio_sorted['gain_pct']]
        fig_bar = go.Figure(go.Bar(
            y=portfolio_sorted['ticker'],
            x=portfolio_sorted['gain_pct'],
            orientation='h',
            marker=dict(color=bar_colors, opacity=0.85,
                        line=dict(width=0)),
            text=[f"{v:+.1f}%" for v in portfolio_sorted['gain_pct']],
            textposition='outside',
            textfont=dict(family='Share Tech Mono', size=10),
            hovertemplate="<b>%{y}</b><br>%{x:.2f}%<extra></extra>",
        ))
        fig_bar.update_layout(**PLOT_LAYOUT, height=320,
                               xaxis_title="", yaxis_title="",
                               xaxis=dict(zeroline=True, zerolinecolor='#2a2a2a',
                                          gridcolor='#111'))
        st.plotly_chart(fig_bar, use_container_width=True)

    # Holdings table
    st.markdown('<div class="section-title">▸ Holdings</div>', unsafe_allow_html=True)
    display_cols = ['ticker', 'name', 'shares', 'avg_price', 'current_price',
                    'market_value', 'gain', 'gain_pct']
    df_display = portfolio[display_cols].copy()
    df_display.columns = ['Ticker', 'Name', 'Shares', 'Avg Price', 'Live Price',
                           'Market Value', 'Gain/Loss', 'Gain %']
    df_display['Avg Price'] = df_display['Avg Price'].map(lambda x: f"{currency_symbol}{x:.4f}")
    df_display['Live Price'] = df_display['Live Price'].map(lambda x: f"{currency_symbol}{x:.4f}")
    df_display['Market Value'] = df_display['Market Value'].map(lambda x: f"{currency_symbol}{x:,.2f}")
    df_display['Gain/Loss'] = df_display['Gain/Loss'].map(lambda x: f"{'+' if x>=0 else ''}{currency_symbol}{x:,.2f}")
    df_display['Gain %'] = df_display['Gain %'].map(lambda x: f"{'+' if x>=0 else ''}{x:.2f}%")
    df_display['Shares'] = df_display['Shares'].map(lambda x: f"{x:.4f}")

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Sector allocation
    if 'sector' in portfolio.columns:
        sector_df = portfolio.groupby('sector')['market_value'].sum().reset_index()
        sector_df = sector_df[sector_df['sector'] != 'Unknown']
        if not sector_df.empty:
            st.markdown('<div class="section-title" style="margin-top:20px">▸ Sector Breakdown</div>', unsafe_allow_html=True)
            fig_sector = go.Figure(go.Bar(
                x=sector_df['sector'],
                y=sector_df['market_value'],
                marker=dict(color=BLUE, opacity=0.7),
                hovertemplate="<b>%{x}</b><br>%{y:$,.2f}<extra></extra>",
            ))
            fig_sector.update_layout(**PLOT_LAYOUT, height=220, xaxis_tickangle=-30)
            st.plotly_chart(fig_sector, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — STOCK ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown('<div class="section-title">▸ Fundamental Metrics</div>', unsafe_allow_html=True)

    analysis_rows = []
    for _, row in portfolio.iterrows():
        info = live_data.get(row['ticker'], {}).get('info', {})
        current = row['current_price']
        high52 = row['week52_high']
        low52 = row['week52_low']
        from_high = ((current - high52) / high52 * 100) if high52 else None
        from_low = ((current - low52) / low52 * 100) if low52 else None

        analysis_rows.append({
            'Ticker': row['ticker'],
            'Name': row['name'],
            'Price': f"{currency_symbol}{current:.2f}",
            'P/E': fmt_num(row['pe_ratio']),
            'Fwd P/E': fmt_num(row['forward_pe']),
            'PEG': fmt_num(row['peg_ratio']),
            'Div Yield': fmt_pct(row['div_yield']) if row['div_yield'] else 'N/A',
            'Beta': fmt_num(row['beta']),
            '52W High': f"{currency_symbol}{high52:.2f}" if high52 else 'N/A',
            '52W Low': f"{currency_symbol}{low52:.2f}" if low52 else 'N/A',
            'From High': f"{from_high:.1f}%" if from_high else 'N/A',
            'From Low': f"+{from_low:.1f}%" if from_low else 'N/A',
            'Mkt Cap': fmt_currency(row['market_cap']),
        })

    df_analysis = pd.DataFrame(analysis_rows)
    st.dataframe(df_analysis, use_container_width=True, hide_index=True)

    # 52-week range visual
    st.markdown('<div class="section-title" style="margin-top:24px">▸ 52-Week Price Range</div>', unsafe_allow_html=True)
    for _, row in portfolio.iterrows():
        if row['week52_low'] and row['week52_high'] and row['week52_high'] > row['week52_low']:
            rng = row['week52_high'] - row['week52_low']
            pos = (row['current_price'] - row['week52_low']) / rng
            pct = min(max(pos * 100, 0), 100)
            color = GREEN if pct > 60 else (ORANGE if pct > 30 else RED)
            st.markdown(f"""
            <div style='margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 3px;'>
                    <span style='font-family: Share Tech Mono; font-size: 10px; color: #888;'>{row['ticker']}</span>
                    <span style='font-family: Share Tech Mono; font-size: 10px; color: #555;'>
                        {currency_symbol}{row['week52_low']:.2f} — {currency_symbol}{row['current_price']:.2f} — {currency_symbol}{row['week52_high']:.2f}
                    </span>
                </div>
                <div style='background: #111; height: 4px; border-radius: 2px; position: relative;'>
                    <div style='position: absolute; left: {pct}%; transform: translateX(-50%);
                                width: 8px; height: 8px; background: {color};
                                border-radius: 50%; top: -2px; box-shadow: 0 0 8px {color};'></div>
                    <div style='width: {pct}%; background: {color}; opacity: 0.25; height: 4px; border-radius: 2px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — INTRINSIC VALUE CALCULATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.markdown('<div class="section-title">▸ Fair Value Estimates</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 1])
    with col_r:
        st.markdown('<div class="terminal-label">DCF Parameters</div>', unsafe_allow_html=True)
        growth_rate = st.number_input("FCF Growth Rate (%)", 0.0, 50.0, 10.0, 0.5) / 100
        terminal_growth = st.number_input("Terminal Growth (%)", 0.0, 10.0, 2.5, 0.5) / 100
        discount_rate = st.number_input("Discount Rate / WACC (%)", 1.0, 30.0, 10.0, 0.5) / 100
        dcf_years = int(st.number_input("Projection Years", 5, 20, 10, 1))

    with col_l:
        iv_rows = []
        for _, row in portfolio.iterrows():
            ticker = row['ticker']
            current = row['current_price']
            eps = row['eps']
            bvps = row['bvps']
            fcf = row['free_cashflow']
            shares_out = row['shares_outstanding']

            graham = graham_number(eps, bvps)
            dcf_val = dcf_valuation(fcf, growth_rate, terminal_growth, discount_rate, shares_out, dcf_years)

            graham_margin = ((graham - current) / current * 100) if graham else None
            dcf_margin = ((dcf_val - current) / current * 100) if dcf_val else None

            def fmt_iv(v, cur):
                if v is None:
                    return "N/A"
                margin = (v - cur) / cur * 100
                color = GREEN if margin > 10 else (RED if margin < -10 else ORANGE)
                return f'<span style="color:{color};font-family:Share Tech Mono">{currency_symbol}{v:.2f} ({margin:+.1f}%)</span>'

            iv_rows.append({
                'Ticker': ticker,
                'Current': f"{currency_symbol}{current:.2f}",
                "Graham's Number": graham,
                "DCF Value": dcf_val,
                "Graham Margin": graham_margin,
                "DCF Margin": dcf_margin,
                "EPS": fmt_num(eps),
                "BVPS": fmt_num(bvps),
            })

        iv_df = pd.DataFrame(iv_rows)

        # Display with color-coding
        for _, row in iv_df.iterrows():
            graham_v = row["Graham's Number"]
            dcf_v = row["DCF Value"]
            g_margin = row["Graham Margin"]
            d_margin = row["DCF Margin"]
            cur = row['Current']

            def badge(v, m, sym):
                if v is None:
                    return '<span style="color:#333;font-family:Share Tech Mono">N/A</span>'
                color = GREEN if m and m > 10 else (RED if m and m < -10 else ORANGE)
                return f'<span style="color:{color};font-family:Share Tech Mono">{sym}{v:.2f} ({m:+.1f}%)</span>'

            st.markdown(f"""
            <div style='border: 1px solid #1a1a1a; background: #0a0a0a; padding: 14px 18px;
                        margin-bottom: 8px; border-left: 2px solid #1a1a1a;'>
                <div style='display: flex; align-items: center; gap: 16px; flex-wrap: wrap;'>
                    <span style='font-family: Rajdhani; font-weight: 700; font-size: 16px;
                                 color: #d4d4d4; letter-spacing: 2px; min-width: 60px;'>{row['Ticker']}</span>
                    <span style='font-family: Share Tech Mono; font-size: 11px; color: #555;'>
                        Live: <span style='color:#888'>{cur}</span>
                    </span>
                    <span style='font-family: Share Tech Mono; font-size: 11px; color: #555;'>
                        Graham: {badge(graham_v, g_margin, currency_symbol)}
                    </span>
                    <span style='font-family: Share Tech Mono; font-size: 11px; color: #555;'>
                        DCF: {badge(dcf_v, d_margin, currency_symbol)}
                    </span>
                    <span style='font-family: Share Tech Mono; font-size: 10px; color: #333; margin-left: auto;'>
                        EPS: {row['EPS']}  |  BVPS: {row['BVPS']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: Share Tech Mono; font-size: 9px; color: #333; margin-top: 16px; line-height: 1.8;'>
        ⚠ Graham's Number = √(22.5 × EPS × BVPS) — requires positive EPS & Book Value.
        DCF uses Free Cash Flow projection with your parameters above.
        N/A = insufficient fundamental data from yfinance.
        These are estimates only — not financial advice.
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — CHARTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.markdown('<div class="section-title">▸ Candlestick Charts</div>', unsafe_allow_html=True)
    selected_ticker = st.selectbox("Select Ticker", tickers, key="chart_ticker")

    period_opt = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    hist = live_data.get(selected_ticker, {}).get('hist', pd.DataFrame())

    if not hist.empty:
        # Filter by period approximation
        days_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730}
        cutoff = datetime.now() - timedelta(days=days_map[period_opt])
        hist_filtered = hist[hist.index >= pd.Timestamp(cutoff, tz=hist.index.tz)]

        # Candlestick
        avg_p = portfolio.loc[portfolio['ticker'] == selected_ticker, 'avg_price'].values
        avg_price_line = avg_p[0] if len(avg_p) > 0 else None

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.75, 0.25], vertical_spacing=0.02)

        fig.add_trace(go.Candlestick(
            x=hist_filtered.index,
            open=hist_filtered['Open'],
            high=hist_filtered['High'],
            low=hist_filtered['Low'],
            close=hist_filtered['Close'],
            increasing_line_color=GREEN, decreasing_line_color=RED,
            increasing_fillcolor=GREEN, decreasing_fillcolor=RED,
            name=selected_ticker,
        ), row=1, col=1)

        # Average entry line
        if avg_price_line:
            fig.add_hline(y=avg_price_line, line_dash="dash",
                          line_color=ORANGE, opacity=0.8,
                          annotation_text=f"Avg Entry {currency_symbol}{avg_price_line:.2f}",
                          annotation_font_color=ORANGE,
                          annotation_font_size=10,
                          row=1, col=1)

        # 20 & 50 day MAs
        if len(hist_filtered) >= 20:
            hist_filtered = hist_filtered.copy()
            hist_filtered['MA20'] = hist_filtered['Close'].rolling(20).mean()
            fig.add_trace(go.Scatter(
                x=hist_filtered.index, y=hist_filtered['MA20'],
                line=dict(color=BLUE, width=1, dash='dot'),
                name='MA20', opacity=0.7
            ), row=1, col=1)
        if len(hist_filtered) >= 50:
            hist_filtered['MA50'] = hist_filtered['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(
                x=hist_filtered.index, y=hist_filtered['MA50'],
                line=dict(color=YELLOW, width=1, dash='dot'),
                name='MA50', opacity=0.7
            ), row=1, col=1)

        # Volume bars
        vol_colors = [GREEN if hist_filtered['Close'].iloc[i] >= hist_filtered['Open'].iloc[i] else RED
                      for i in range(len(hist_filtered))]
        fig.add_trace(go.Bar(
            x=hist_filtered.index,
            y=hist_filtered['Volume'],
            marker_color=vol_colors,
            marker_opacity=0.5,
            name='Volume',
            showlegend=False,
        ), row=2, col=1)

        layout = PLOT_LAYOUT.copy()
        layout.update(height=520, xaxis_rangeslider_visible=False,
                      title=dict(text=f"{selected_ticker}  |  {period_opt.upper()}",
                                 font=dict(family='Share Tech Mono', size=13, color='#888'),
                                 x=0),
                      yaxis=dict(**PLOT_LAYOUT.get('yaxis', {}), title='Price', tickprefix=currency_symbol),
                      yaxis2=dict(gridcolor='#0d0d0d', linecolor='#1c1c1c', title='Volume'))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No historical data available for {selected_ticker}")

    # Portfolio performance over time (index-based)
    st.markdown('<div class="section-title" style="margin-top:24px">▸ Portfolio Value Over Time</div>', unsafe_allow_html=True)
    combined_value = None
    for ticker in tickers:
        hist = live_data.get(ticker, {}).get('hist', pd.DataFrame())
        if hist.empty:
            continue
        shares = portfolio.loc[portfolio['ticker'] == ticker, 'shares'].values
        if len(shares) == 0:
            continue
        ticker_val = hist['Close'] * shares[0]
        if combined_value is None:
            combined_value = ticker_val
        else:
            combined_value = combined_value.add(ticker_val, fill_value=0)

    if combined_value is not None and not combined_value.empty:
        combined_value = combined_value.dropna()
        fig_port = go.Figure()
        fig_port.add_trace(go.Scatter(
            x=combined_value.index,
            y=combined_value.values,
            fill='tozeroy',
            fillcolor='rgba(0,255,65,0.04)',
            line=dict(color=GREEN, width=2),
            name='Portfolio Value',
            hovertemplate=f"<b>%{{x|%Y-%m-%d}}</b><br>{currency_symbol}%{{y:,.2f}}<extra></extra>",
        ))
        fig_port.add_trace(go.Scatter(
            x=[combined_value.index[0], combined_value.index[-1]],
            y=[total_cost, total_cost],
            line=dict(color=ORANGE, width=1, dash='dash'),
            name='Cost Basis',
            hovertemplate=f"Cost Basis: {currency_symbol}{total_cost:,.2f}<extra></extra>",
        ))
        fig_port.update_layout(**PLOT_LAYOUT, height=280,
                                yaxis=dict(**PLOT_LAYOUT.get('yaxis', {}), tickprefix=currency_symbol))
        st.plotly_chart(fig_port, use_container_width=True)
