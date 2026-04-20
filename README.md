# 📈 Bloomberg Terminal — Portfolio Tracker

A live portfolio tracking web app with Bloomberg Terminal aesthetics, built with Streamlit + yfinance.
Upload your Trading 212 CSV export and get real-time P&L, fundamental analysis, intrinsic value estimates, and candlestick charts.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Live P&L** | Real-time gains/losses via yfinance (5-min cache) |
| **Stock Analysis** | P/E, Forward P/E, PEG, Dividend Yield, Beta, 52-week range |
| **Intrinsic Value** | Graham's Number + DCF fair value with margin of safety |
| **Candlestick Charts** | 1mo–2y charts with MA20/MA50, volume, and avg entry line |
| **Asset Allocation** | Donut chart, sector breakdown, gain/loss bar chart |
| **Bloomberg Theme** | Full dark mode, neon green/orange/red accents, monospace fonts |

---

## 📂 CSV Format Support

**History Export** (`Account → History → Export CSV`):
- Parses all buy/sell transactions
- Computes weighted average entry price per ticker
- Shows only currently held positions

**Portfolio Export** (`Account → Portfolio → Export CSV`):
- Direct snapshot of current holdings

---

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/portfolio-tracker.git
cd portfolio-tracker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## ☁️ Deploy to Streamlit Cloud (Free)

### Step 1 — Push to GitHub

```bash
# In your project folder:
git init
git add .
git commit -m "Initial commit — Bloomberg Portfolio Tracker"

# Create a repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/portfolio-tracker.git
git branch -M main
git push -u origin main
```

### Step 2 — Connect Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository**: `YOUR_USERNAME/portfolio-tracker`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **"Deploy"**

Your app will be live at:
`https://YOUR_USERNAME-portfolio-tracker-app-XXXXX.streamlit.app`

---

## ⚠️ Disclaimer

This app is for informational purposes only. Intrinsic value estimates (DCF, Graham's Number) are mathematical models based on available data — not financial advice. Always do your own research.

---

## 🏗️ Stack

- **Streamlit** — web framework
- **yfinance** — live market data
- **Pandas** — portfolio math
- **Plotly** — interactive charts
- **Fonts**: Share Tech Mono + Rajdhani (Google Fonts)
