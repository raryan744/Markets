# Kalshi vs BTC Divergence Analyzer

## Overview
This project is a Streamlit dashboard designed to analyze and visualize divergences between Kalshi's KXBTC 15-minute prediction market YES% prices and Polygon.io's spot BTC/USD OHLCV data. Its primary purpose is to surface convergences and divergences, aiding in strategy development for cryptocurrency trading. The application integrates live data feeds from CF Benchmarks BRTI and Kalshi's order book, with full persistence to a PostgreSQL database. It also incorporates advanced machine learning models (CNN-LSTM and XGBoost) for real-time prediction and includes an automated trading system for the Kalshi markets. The broader vision is to create a robust tool for identifying exploitable patterns in prediction markets relative to underlying asset movements, potentially leading to profitable trading strategies.

## User Preferences
I prefer iterative development with frequent, small updates. Before making any major architectural changes or introducing new external dependencies, please ask for my approval. Ensure that all code is well-commented and follows standard Python best practices. I appreciate detailed explanations for complex logic or design decisions. Do not make changes to the `.streamlit/config.toml` file without explicit instruction.

## System Architecture
The application is built using **Streamlit (Python)**, serving as both the UI and the core engine. A critical architectural decision is the use of a `background_runner.py` companion process. This separate process, launched alongside Streamlit, is responsible for initializing and maintaining long-running tasks such as live BRTI WebSocket feeds, Kalshi WebSocket feeds, Bobby BRTI calculations, and machine learning model training/auto-trading, decoupled from the Streamlit UI's lifecycle. This ensures continuous data collection and processing without being affected by Streamlit's refresh cycles or user sessions.

**Cross-Process Data Bridge:**
The background_runner and Streamlit processes communicate via a shared state file (`/tmp/ensemble_ui_state.json`). The background_runner writes this file every second with the latest ensemble prediction, XGBoost prediction, all indicator values (RSI, volatility, imbalance, etc.), temperature calibration values, and training stats (sample counts, train counts, accuracy/loss). The Streamlit display-only process reads this file for all UI rendering — `get_ensemble_latest()`, temperature display, gauges, and online training status all fall back to this shared file when in-memory state is empty. The file is written atomically (tmp + `os.replace`) and errors are logged to `/tmp/bobby_debug.log`.

**Data Flow and Persistence:**
- **BTC Data:** Sourced from Polygon.io REST API (aggregates and 1-second bars).
- **Kalshi Data:** Fetched via an RSA-PSS authenticated API for candlesticks and active order book data.
- **BRTI Live:** Real-time data obtained from CF Benchmarks WebSocket.
- **BobbyBRTI:** Calculated in real-time from async WebSocket feeds of 7 cryptocurrency exchanges using `ccxt.pro`.
- **Database:** PostgreSQL is used for persistent storage of all historical data, including BTC prices, Kalshi candlesticks, BRTI ticks, BobbyBRTI ticks, ensemble predictions, training samples, book image snapshots, and auto-trade logs. Database pruning mechanisms are implemented to manage data retention.

**UI/UX and Features:**
The dashboard is streamlined to a single-page view focused entirely on the **Ensemble Predictor**. All other tabs (Overlay Chart, YES/NO vs BTC, Divergence Detail, Statistics & Analysis, Raw Data, BRTI Live, Order Book) have been removed from the UI to maximize responsiveness. Their background data collection, DB persistence, and model-feeding pipelines remain fully active — only the rendering is removed. Within the ensemble view, three charts were also removed (Confidence, Probability, Hawkes Intensity) — their data continues to be logged and fed into the model. The remaining UI includes:
- **BobbyBRTI + Prediction Direction chart:** Single-panel chart showing live BobbyBRTI price with UP/DOWN/NEUTRAL direction markers.
- **Signal Monitor:** Gauges for signal run count, RSI-14, and volatility regime; indicator tiles for RSI-7/21, Vol-60s, VWAP deviation, imbalance, depth ratio; entry gate checklist.
- **Feature Contribution Breakdown:** Expandable horizontal bar chart of model feature contributions.
- **Prediction History:** Table of recent ensemble ticks with all fields (direction, confidence, model, hawkes, probabilities).
- **Multi-Timeframe XGBoost (15s · 1min):** Two separate XGBoost models trained on 15s and 60s forward BRTI price labels. Display-only (not wired to auto-trader). Live direction + confidence + probability breakdown shown for both horizons. Training stats (train count, sample count, in-sample accuracy) shown per model. Live DB accuracy metrics (correct/total resolved rows) shown from `xgb_mtf_predictions` table. Outcomes resolved by background thread every 30s; rows logged every ~10s during live inference.
- **Online Training Status:** Metrics for labeled samples, XGBoost/CNN-LSTM train counts, accuracy/loss.
- **Auto-Trading:** Full trading controls, position display, trade log, exit/buy-more buttons.
- **Fragment interval:** 3 seconds (reduced from 5s for improved responsiveness since it's now the only rendering fragment).

**Key Design Patterns:**
- **`@st.cache_resource` Singletons:** Used extensively to manage long-lived objects like WebSocket connections, data queues, and background threads, ensuring they are initialized once and shared across Streamlit sessions.
- **Daemon Threads:** Employed for continuous background tasks (e.g., BRTI/Kalshi WS, order book polling, data collection, auto-trading, model training) to operate independently of the main Streamlit application flow. The trailing-exit logic runs in its own daemon thread per position so the main auto-trader loop stays free to scan for new signals. Helper closures (`_get_live_bid`, `_time_remaining_s`, `_market_sell`) bind ticker/side/contracts via default-arg capture to prevent stale-closure bugs.
- **Position File (`/tmp/auto_trade_position.json`):** Single-position JSON file written atomically via `tempfile.mkstemp` + `os.replace`. The main loop reads the open ticker from this file and skips it when scanning markets, preventing duplicate exposure. `last_trade_ts` is set at buy time (not just sell) to enforce cooldown between entries.
- **Early Exit Triggers:** Stale exit (held >60s and never been profitable), stop-loss (held >90s and losing >2¢), force-exit (<90s remaining). `_ever_profitable` flag tracks whether bid ever exceeded entry price.
- **Asynchronous Processing:** `asyncio` and `ccxt.pro` are used for concurrent handling of multiple exchange WebSocket feeds for BobbyBRTI calculation, ensuring high-frequency data processing.
- **Keep-Alive Mechanism:** A module-level daemon thread pings external Replit URLs to prevent idle pausing.
- **Performance Optimizations:** All chart data is downsampled to 300-500 points via `_downsample()` before rendering. `_show_chart()` wrapper enforces `width="stretch"`, hides mode bar, and disables scroll zoom via `_PLOTLY_CONFIG`. Rangesliders are disabled (they re-render all trace data). Only the ensemble fragment renders (3s interval), all other tabs removed from UI. Ensemble ticks capped at 300. Non-ensemble background processes still run but produce no UI output.
- **Manual Buy More:** Signal file `/tmp/auto_trade_buy_more` triggers +1 contract buy at bid+2 inside the trailing exit thread. Updates averaged entry price, contract count, and fees in-place; position file written immediately after fill.

## External Dependencies
- **Kalshi API:** `https://api.elections.kalshi.com/trade-api/v2` (primary) and `https://trading-api.kalshi.com/trade-api/v2` (fallback). Used for market data, candlesticks, and order book information for KXBTC series. Requires `KALSHI_API_KEY` and `KALSHI_PRIVATE_KEY` for RSA-PSS authentication.
- **CF Benchmarks WebSocket:** `wss://www.cfbenchmarks.com/ws/v4`. Provides real-time BRTI price feeds. Requires basic authentication with `cfbenchmarksws2` and a secret key.
- **Polygon.io REST API:** `https://api.polygon.io/v2`. Used to fetch historical and live BTC/USD OHLCV data for `X:BTCUSD` ticker. Requires `POLYGON_API_KEY`.
- **PostgreSQL Database:** Used for persistent storage of all operational and historical data. Configured via `DATABASE_URL`.
- **ccxt (with ccxt.pro):** Python library for interacting with cryptocurrency exchanges, specifically used for asynchronous WebSocket order book feeds from multiple exchanges (Bitstamp, Coinbase, Kraken, Gemini, Crypto.com, Bitfinex, Bullish) to calculate BobbyBRTI.
- **torch:** Python library for building and training the CNN-LSTM deep learning model.
- **xgboost:** Gradient boosting library used for the XGBoost prediction model.
- **Other Python Libraries:** `streamlit`, `plotly`, `pandas`, `requests`, `numpy`, `matplotlib`, `cryptography`, `psycopg2-binary`, `websocket-client`, `joblib`, `scikit-learn` are used for various functionalities like UI, data manipulation, plotting, cryptographic operations, database connectivity, and machine learning utilities.