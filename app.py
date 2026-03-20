import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

_CHARTS_ENABLED = True
_PLOTLY_CONFIG = {
    "displayModeBar": False,
    "staticPlot": False,
    "scrollZoom": False,
}

def _show_chart(fig, **kw):
    if _CHARTS_ENABLED:
        kw["width"] = "stretch"
        kw.setdefault("config", _PLOTLY_CONFIG)
        st.plotly_chart(fig, **kw)


def _downsample(df, max_points=400):
    """Reduce a DataFrame to at most max_points rows via nth-row sampling,
    always keeping first and last rows for correct axis range."""
    if len(df) <= max_points:
        return df
    step = max(len(df) // max_points, 2)
    sampled = df.iloc[::step]
    last = df.iloc[[-1]]
    return pd.concat([sampled, last]).drop_duplicates().sort_values(df.columns[0]).reset_index(drop=True)
from datetime import datetime, timezone, timedelta
import time
import re
import numpy as np
import os
import base64
import collections
import threading
import json
import asyncio
from websocket._app import WebSocketApp as _WebSocketApp
from zoneinfo import ZoneInfo
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.backends import default_backend
import psycopg2
from psycopg2.extras import execute_values

st.set_page_config(
    page_title="Kalshi vs BTC Price — Divergence Analyzer",
    page_icon="📊",
    layout="wide",
)

KALSHI_HOSTS = [
    "https://api.elections.kalshi.com",
    "https://trading-api.kalshi.com",
]
KALSHI_BASE_PATH = "/trade-api/v2"
SERIES_TICKER    = "KXBTC"
SERIES_TICKER_15M = "KXBTC15M"
POLYGON_BASE = "https://api.polygon.io/v2"

KALSHI_API_KEY = os.environ.get("KALSHI_API_KEY", "")
KALSHI_PRIVATE_KEY_PEM = os.environ.get("KALSHI_PRIVATE_KEY", "")
POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY", "")

_kalshi_private_key = None
if KALSHI_PRIVATE_KEY_PEM:
    try:
        pem_data = KALSHI_PRIVATE_KEY_PEM.encode("utf-8")
        _kalshi_private_key = serialization.load_pem_private_key(
            pem_data, password=None, backend=default_backend()
        )
    except Exception:
        _kalshi_private_key = None

KALSHI_AUTH_READY = bool(KALSHI_API_KEY and _kalshi_private_key)

DATABASE_URL = os.environ.get("DATABASE_URL", "")

_KEEPALIVE_INTERVAL = 240  # seconds between pings (4 min)


def _keep_alive_loop():
    """Ping localhost health every 4 minutes to prevent Replit idle pausing.
    Only pings the external dev-domain URL in the editor environment — deployed
    apps are kept alive by Replit automatically and don't need the external ping."""
    _is_deployed = bool(os.environ.get("REPLIT_DEPLOYMENT"))
    domain = os.environ.get("REPLIT_DEV_DOMAIN", "") if not _is_deployed else ""
    external_url = f"https://{domain}/" if domain else None
    local_url = "http://localhost:5000/_stcore/health"
    time.sleep(60)
    while True:
        if external_url:
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    requests.get(external_url, timeout=15, verify=False)
            except Exception:
                pass
        try:
            requests.get(local_url, timeout=5)
        except Exception:
            pass
        time.sleep(_KEEPALIVE_INTERVAL)


threading.Thread(target=_keep_alive_loop, daemon=True, name="keep-alive").start()


def _db_conn():
    if not DATABASE_URL:
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception:
        return None

def db_save_btc_prices(btc_df: pd.DataFrame):
    if btc_df.empty or not DATABASE_URL:
        return
    rows = []
    for _, r in btc_df.iterrows():
        rows.append((
            r["ts"].isoformat(),
            float(r.get("open", r["close"])),
            float(r.get("high", r["close"])),
            float(r.get("low", r["close"])),
            float(r["close"]),
            float(r.get("volume", 0) or 0),
        ))
    if not rows:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO btc_prices (ts, open, high, low, close, volume)
                    VALUES %s
                    ON CONFLICT (ts) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                    """,
                    rows,
                )
    except Exception:
        pass
    finally:
        conn.close()

def db_load_btc_prices(lookback_mins: int) -> pd.DataFrame:
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ts, open, high, low, close, volume
                FROM btc_prices
                WHERE ts >= %s
                ORDER BY ts ASC
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

def db_save_kalshi_candlesticks(candles_df: pd.DataFrame, ticker: str):
    if candles_df.empty or not DATABASE_URL:
        return
    rows = []
    for _, r in candles_df.iterrows():
        rows.append((
            r["ts"].isoformat(),
            ticker,
            float(r.get("yes_price_pct", r.get("close", 0))),
        ))
    if not rows:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO kalshi_candlesticks (ts, ticker, yes_price_pct)
                    VALUES %s
                    ON CONFLICT (ts, ticker) DO UPDATE SET
                        yes_price_pct = EXCLUDED.yes_price_pct
                    """,
                    rows,
                )
    except Exception:
        pass
    finally:
        conn.close()

def db_load_kalshi_candlesticks(lookback_mins: int) -> pd.DataFrame:
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ts, ticker, yes_price_pct
                FROM kalshi_candlesticks
                WHERE ts >= %s
                ORDER BY ts ASC
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "ticker", "yes_price_pct"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["yes_price_pct"] = df["yes_price_pct"].astype(float)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

def db_row_counts():
    if not DATABASE_URL:
        return 0, 0, 0, 0, 0
    conn = _db_conn()
    if not conn:
        return 0, 0, 0, 0, 0
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    (SELECT COUNT(*) FROM kalshi_candlesticks),
                    (SELECT COUNT(*) FROM btc_prices),
                    (SELECT COUNT(*) FROM brti_ticks),
                    (SELECT COUNT(DISTINCT ts) FROM kalshi_orderbook),
                    (SELECT COUNT(*) FROM bobby_brti_ticks)
            """)
            return cur.fetchone()
    except Exception:
        return 0, 0, 0, 0, 0
    finally:
        conn.close()


def db_save_brti_ticks(ticks: list):
    if not ticks or not DATABASE_URL:
        return
    rows = [(t["ts"].isoformat(), float(t["price"])) for t in ticks]
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO brti_ticks (ts, price)
                    VALUES %s
                    ON CONFLICT (ts) DO UPDATE SET price = EXCLUDED.price
                    """,
                    rows,
                )
    except Exception:
        pass
    finally:
        conn.close()


def db_load_brti_ticks(lookback_secs: int = 3600) -> pd.DataFrame:
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(seconds=lookback_secs)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ts, price FROM brti_ticks WHERE ts >= %s ORDER BY ts ASC",
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "price"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["price"] = df["price"].astype(float)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_save_bobby_brti(ticks: list):
    if not ticks or not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO bobby_brti_ticks (ts, price, v_t, c_t, n_exchanges)
                    VALUES %s
                    ON CONFLICT (ts) DO UPDATE SET
                        price = EXCLUDED.price, v_t = EXCLUDED.v_t,
                        c_t = EXCLUDED.c_t, n_exchanges = EXCLUDED.n_exchanges
                    """,
                    [(t["ts"].isoformat(), t["price"], t.get("v_t"), t.get("c_t"), t.get("n_exchanges")) for t in ticks],
                )
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


def db_load_bobby_brti(lookback_secs: int = 3600) -> pd.DataFrame:
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(seconds=lookback_secs)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ts, price, v_t, c_t, n_exchanges FROM bobby_brti_ticks WHERE ts >= %s ORDER BY ts ASC",
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "price", "v_t", "c_t", "n_exchanges"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["price"] = df["price"].astype(float)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_save_ensemble_predictions(ticks: list):
    if not ticks or not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO ensemble_predictions (ts, brti, direction, confidence, model,
                        prob_up, prob_neutral, prob_down, v_t, c_t, hawkes, n_exchanges, brti_return)
                    VALUES %s
                    ON CONFLICT (ts) DO NOTHING
                    """,
                    [(t["ts"].isoformat(), t["brti"], t["direction"], t["confidence"],
                      t["model"], t["prob_up"], t["prob_neutral"], t["prob_down"],
                      t["v_T"], t["C_T"], t["hawkes"], t["n_exchanges"], t["brti_return"]) for t in ticks],
                )
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


_MTF_DIR_MAP = {"DOWN": 0, "NEUTRAL": 1, "UP": 2}

def _db_log_mtf_prediction(price: float | None, pred_15s: dict | None, pred_60s: dict | None):
    """Insert one row into xgb_mtf_predictions for accuracy tracking."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        p15_dir  = _MTF_DIR_MAP.get(pred_15s["direction"]) if pred_15s else None
        p15_conf = pred_15s["confidence"] if pred_15s else None
        p60_dir  = _MTF_DIR_MAP.get(pred_60s["direction"]) if pred_60s else None
        p60_conf = pred_60s["confidence"] if pred_60s else None
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO xgb_mtf_predictions
                       (ts, price_at_capture,
                        pred_15s_dir, pred_15s_conf,
                        pred_60s_dir, pred_60s_conf)
                       VALUES (NOW(), %s, %s, %s, %s, %s)""",
                    (price, p15_dir, p15_conf, p60_dir, p60_conf),
                )
    except Exception:
        pass
    finally:
        conn.close()


def _db_resolve_mtf_outcomes():
    """Background: find rows older than 15s/60s with no outcome and fill them in."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        bobby_ticks = get_bobby_brti_ticks()
        if not bobby_ticks:
            return
        tick_ts_list = []
        for t in bobby_ticks:
            t_ts = t["ts"].timestamp() if hasattr(t["ts"], "timestamp") else float(t["ts"])
            tick_ts_list.append((t_ts, t["price"]))
        if not tick_ts_list:
            return

        import bisect
        tick_times = [x[0] for x in tick_ts_list]

        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, EXTRACT(EPOCH FROM ts)::double precision, price_at_capture,
                          resolved_15s, resolved_60s
                   FROM xgb_mtf_predictions
                   WHERE resolved_15s = FALSE OR resolved_60s = FALSE
                   ORDER BY ts ASC LIMIT 200"""
            )
            rows = cur.fetchall()

        if not rows:
            return

        now_ts = time.time()
        updates = []
        for row_id, row_ts, price_cap, res15, res60 in rows:
            if price_cap is None:
                continue
            upd = {}
            def _resolve_horizon(horizon, res_flag):
                if res_flag:
                    return None
                if now_ts - row_ts < horizon:
                    return None
                target = row_ts + horizon
                idx = bisect.bisect_left(tick_times, target)
                best_dist = float("inf")
                fp = None
                for j in range(max(0, idx - 1), min(len(tick_ts_list), idx + 2)):
                    d = abs(tick_ts_list[j][0] - target)
                    if d < best_dist:
                        best_dist = d
                        fp = tick_ts_list[j][1]
                if fp is not None and best_dist < horizon * 0.5:
                    return _MTF_DIR_MAP.get(
                        ["DOWN", "NEUTRAL", "UP"][_label_from_returns(float(price_cap), fp)]
                    )
                if now_ts - row_ts > horizon + 120:
                    return -1   # sentinel: too old, mark resolved with NULL actual
                return None

            a15 = _resolve_horizon(_MTF_HORIZON_15S, res15)
            a60 = _resolve_horizon(_MTF_HORIZON_60S, res60)
            if a15 is not None or a60 is not None:
                updates.append((row_id, a15, a60))

        if updates:
            with conn:
                with conn.cursor() as cur:
                    for row_id, a15, a60 in updates:
                        actual_15 = None if a15 == -1 else a15
                        actual_60 = None if a60 == -1 else a60
                        cur.execute(
                            """UPDATE xgb_mtf_predictions SET
                               actual_15s_dir  = COALESCE(%s, actual_15s_dir),
                               resolved_15s    = CASE WHEN %s IS NOT NULL THEN TRUE ELSE resolved_15s END,
                               actual_60s_dir  = COALESCE(%s, actual_60s_dir),
                               resolved_60s    = CASE WHEN %s IS NOT NULL THEN TRUE ELSE resolved_60s END
                               WHERE id = %s""",
                            (actual_15, a15, actual_60, a60, row_id),
                        )
    except Exception:
        pass
    finally:
        conn.close()


def db_save_book_image_snapshot(ts_unix: float, price: float, image_np):
    """Persist a (1,1,500,2) float32 book image to the DB.
    Rounds ts to the nearest 30-second bucket — ON CONFLICT discards all
    duplicate writes from any process within the same window, so the DB
    receives at most 2 rows/minute regardless of how many writers exist."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        # Snap to nearest 30-second boundary — the unique index on ts handles dedup
        bucket = int(ts_unix // 30) * 30
        ts_dt = datetime.fromtimestamp(bucket, tz=timezone.utc)
        img_bytes = image_np.tobytes()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO book_image_snapshots (ts, price, image_bytes)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (ts) DO NOTHING
                    """,
                    (ts_dt.isoformat(), float(price), psycopg2.Binary(img_bytes)),
                )
    except Exception:
        pass
    finally:
        conn.close()


def db_load_book_image_snapshots() -> list:
    """Load all book image snapshots from DB as list of {ts, price, image_np}."""
    if not DATABASE_URL:
        return []
    conn = _db_conn()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ts, price, image_bytes FROM book_image_snapshots ORDER BY ts ASC"
            )
            rows = cur.fetchall()
        result = []
        for ts_val, price, img_bytes in rows:
            t = ts_val
            if hasattr(t, 'timestamp'):
                t = t.timestamp()
            img_np = np.frombuffer(bytes(img_bytes), dtype=np.float32).reshape(1, 1, 500, 2)
            result.append({"ts": float(t), "price": float(price), "image_np": img_np})
        return result
    except Exception:
        return []
    finally:
        conn.close()


def db_prune_book_image_snapshots(keep_hours: int = 48):
    """Delete book image snapshots older than keep_hours."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=keep_hours)).isoformat()
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM book_image_snapshots WHERE ts < %s", (cutoff,))
    except Exception:
        pass
    finally:
        conn.close()


def db_save_orderbook_snapshot(ts: datetime, ticker: str, yes_bids: list, yes_asks: list):
    """Save a full order-book snapshot. yes_bids/yes_asks are [[price_cents, qty], ...]."""
    if not DATABASE_URL:
        return
    rows = []
    for p, q in yes_bids[:10]:
        rows.append((ts.isoformat(), ticker, "yes_bid", int(p), int(q)))
    for p, q in yes_asks[:10]:
        rows.append((ts.isoformat(), ticker, "yes_ask", int(p), int(q)))
    if not rows:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO kalshi_orderbook (ts, ticker, side, price_cents, quantity)
                    VALUES %s
                    ON CONFLICT (ts, ticker, side, price_cents) DO UPDATE SET
                        quantity = EXCLUDED.quantity
                    """,
                    rows,
                )
    except Exception:
        pass
    finally:
        conn.close()


def db_ensure_depth_signal_table():
    """Create kalshi_depth_signal table if it doesn't exist yet."""
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS kalshi_depth_signal (
                        id              SERIAL PRIMARY KEY,
                        ts              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        ticker          TEXT,
                        best_bid_cents  FLOAT,
                        best_ask_cents  FLOAT,
                        bid_depth       BIGINT,
                        ask_depth       BIGINT,
                        ask_to_bid_ratio FLOAT,
                        signal          TEXT,
                        brti_at_capture FLOAT,
                        future_brti_5m  FLOAT,
                        future_brti_10m FLOAT,
                        resolved        BOOLEAN DEFAULT FALSE
                    )
                """)
    except Exception:
        pass
    finally:
        conn.close()


def db_save_depth_signal(ts: datetime, ticker: str, best_bid: float, best_ask: float,
                         bid_depth: int, ask_depth: int, ask_to_bid_ratio: float,
                         signal: str, brti: float):
    """Persist one kalshi_depth_signal snapshot."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO kalshi_depth_signal
                        (ts, ticker, best_bid_cents, best_ask_cents,
                         bid_depth, ask_depth, ask_to_bid_ratio, signal, brti_at_capture)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (ts.isoformat(), ticker, best_bid, best_ask,
                     int(bid_depth), int(ask_depth), float(ask_to_bid_ratio),
                     signal, float(brti)),
                )
    except Exception:
        pass
    finally:
        conn.close()


def db_resolve_depth_signals():
    """Fill future_brti_5m / future_brti_10m for rows old enough to be resolved."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE kalshi_depth_signal ds
                    SET
                        future_brti_5m = (
                            SELECT price FROM bobby_brti_ticks
                            WHERE ts BETWEEN ds.ts + INTERVAL '4 minutes'
                                         AND ds.ts + INTERVAL '6 minutes'
                            ORDER BY ABS(EXTRACT(EPOCH FROM (ts - (ds.ts + INTERVAL '5 minutes'))))
                            LIMIT 1
                        ),
                        future_brti_10m = (
                            SELECT price FROM bobby_brti_ticks
                            WHERE ts BETWEEN ds.ts + INTERVAL '9 minutes'
                                         AND ds.ts + INTERVAL '11 minutes'
                            ORDER BY ABS(EXTRACT(EPOCH FROM (ts - (ds.ts + INTERVAL '10 minutes'))))
                            LIMIT 1
                        ),
                        resolved = TRUE
                    WHERE NOT resolved
                      AND ts < NOW() - INTERVAL '11 minutes'
                """)
    except Exception:
        pass
    finally:
        conn.close()


def db_load_depth_signal_history(lookback_mins: int = 120) -> pd.DataFrame:
    """Return recent depth signal history for the UI chart + accuracy table."""
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ts, ticker, best_bid_cents, best_ask_cents,
                       bid_depth, ask_depth, ask_to_bid_ratio, signal,
                       brti_at_capture, future_brti_5m, future_brti_10m, resolved
                FROM kalshi_depth_signal
                WHERE ts >= %s
                ORDER BY ts DESC
                LIMIT 500
            """, (cutoff,))
            rows = cur.fetchall()
            if not rows:
                return pd.DataFrame()
            cols = ["ts", "ticker", "best_bid_cents", "best_ask_cents",
                    "bid_depth", "ask_depth", "ask_to_bid_ratio", "signal",
                    "brti_at_capture", "future_brti_5m", "future_brti_10m", "resolved"]
            return pd.DataFrame(rows, columns=cols)
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def _classify_depth_signal(ask_to_bid: float) -> str:
    """Map ask:bid ratio to a signal label."""
    if ask_to_bid > 3.0:
        return "HEAVY_ASK"
    if ask_to_bid > 1.5:
        return "ASK_LEAN"
    if ask_to_bid > 0.67:
        return "BALANCED"
    if ask_to_bid > 0.33:
        return "BID_LEAN"
    return "HEAVY_BID"


def db_load_multi_window_book_values(lookback_mins: int = 240) -> pd.DataFrame:
    """Return YES/NO book values across ALL stored tickers (market windows) for history chart."""
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ts,
                    ticker,
                    SUM(CASE WHEN side='yes_bid'
                        THEN price_cents::numeric / 100.0 * quantity ELSE 0 END) AS yes_value,
                    SUM(CASE WHEN side='yes_ask'
                        THEN (100 - price_cents)::numeric / 100.0 * quantity ELSE 0 END) AS no_value
                FROM kalshi_orderbook
                WHERE ts >= %s
                GROUP BY ts, ticker
                ORDER BY ts ASC
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "ticker", "yes_value", "no_value"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["yes_value"] = pd.to_numeric(df["yes_value"], errors="coerce")
        df["no_value"] = pd.to_numeric(df["no_value"], errors="coerce")
        # Derive window key (everything before the last hyphen-separated strike segment)
        df["window"] = df["ticker"].apply(
            lambda t: "-".join(t.split("-")[:2]) if t.count("-") >= 2 else t
        )
        return df.dropna()
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_load_window_sessions(lookback_mins: int = 1440) -> pd.DataFrame:
    """Return distinct windows (ticker prefixes) seen in stored order book data."""
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ticker,
                    MIN(ts) AS first_seen,
                    MAX(ts) AS last_seen,
                    COUNT(DISTINCT ts) AS snapshots
                FROM kalshi_orderbook
                WHERE ts >= %s
                GROUP BY ticker
                ORDER BY MIN(ts) ASC
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ticker", "first_seen", "last_seen", "snapshots"])
        df["first_seen"] = pd.to_datetime(df["first_seen"], utc=True)
        df["last_seen"] = pd.to_datetime(df["last_seen"], utc=True)
        df["window"] = df["ticker"].apply(
            lambda t: "-".join(t.split("-")[:2]) if t.count("-") >= 2 else t
        )
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_load_book_values(ticker: str, lookback_mins: int = 60) -> pd.DataFrame:
    """Return YES and NO dollar values per snapshot from stored order book data."""
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ts,
                    SUM(CASE WHEN side='yes_bid'
                        THEN price_cents::numeric / 100.0 * quantity ELSE 0 END) AS yes_value,
                    SUM(CASE WHEN side='yes_ask'
                        THEN (100 - price_cents)::numeric / 100.0 * quantity ELSE 0 END) AS no_value
                FROM kalshi_orderbook
                WHERE ticker = %s AND ts >= %s
                GROUP BY ts
                ORDER BY ts ASC
                """,
                (ticker, cutoff),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "yes_value", "no_value"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["yes_value"] = pd.to_numeric(df["yes_value"], errors="coerce")
        df["no_value"] = pd.to_numeric(df["no_value"], errors="coerce")
        return df.dropna()
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_load_orderbook_history(ticker: str, lookback_mins: int = 60) -> pd.DataFrame:
    """Return mid-price, spread, and depth time-series from stored snapshots."""
    if not DATABASE_URL:
        return pd.DataFrame()
    conn = _db_conn()
    if not conn:
        return pd.DataFrame()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=lookback_mins)).isoformat()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ts,
                    MAX(CASE WHEN side='yes_bid' THEN price_cents END) AS best_bid,
                    MIN(CASE WHEN side='yes_ask' THEN price_cents END) AS best_ask,
                    SUM(CASE WHEN side='yes_bid' THEN quantity ELSE 0 END) AS total_bid_qty,
                    SUM(CASE WHEN side='yes_ask' THEN quantity ELSE 0 END) AS total_ask_qty
                FROM kalshi_orderbook
                WHERE ticker = %s AND ts >= %s
                GROUP BY ts
                ORDER BY ts ASC
                """,
                (ticker, cutoff),
            )
            rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=["ts", "best_bid", "best_ask", "total_bid_qty", "total_ask_qty"])
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        for col in ["best_bid", "best_ask", "total_bid_qty", "total_ask_qty"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["mid_price"] = (df["best_bid"] + df["best_ask"]) / 2.0
        df["spread_cents"] = df["best_ask"] - df["best_bid"]
        return df.dropna(subset=["mid_price"])
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


def db_load_orderbook_latest(ticker: str) -> dict:
    """Return the most recent order-book snapshot as {'yes_bids': [...], 'yes_asks': [...]}."""
    if not DATABASE_URL:
        return {}
    conn = _db_conn()
    if not conn:
        return {}
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT side, price_cents, quantity
                FROM kalshi_orderbook
                WHERE ticker = %s
                  AND ts = (
                      SELECT MAX(ts) FROM kalshi_orderbook WHERE ticker = %s
                  )
                ORDER BY side, price_cents
                """,
                (ticker, ticker),
            )
            rows = cur.fetchall()
        if not rows:
            return {}
        yes_bids = sorted(
            [[r[1], r[2]] for r in rows if r[0] == "yes_bid"], key=lambda x: -x[0]
        )
        yes_asks = sorted(
            [[r[1], r[2]] for r in rows if r[0] == "yes_ask"], key=lambda x: x[0]
        )
        return {"yes_bids": yes_bids, "yes_asks": yes_asks}
    except Exception:
        return {}
    finally:
        conn.close()

def db_init_auto_trades():
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS auto_trades (
                        id SERIAL PRIMARY KEY,
                        ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        ticker TEXT NOT NULL,
                        direction TEXT NOT NULL,
                        signal_confidence DOUBLE PRECISION,
                        action TEXT NOT NULL,
                        contracts INTEGER NOT NULL,
                        price_cents INTEGER,
                        order_id TEXT,
                        pnl_cents INTEGER
                    )
                """)
                cur.execute("""
                    ALTER TABLE auto_trades ADD COLUMN IF NOT EXISTS fee_cents INTEGER DEFAULT 0
                """)
                cur.execute("""
                    ALTER TABLE auto_trades ADD COLUMN IF NOT EXISTS is_paper BOOLEAN DEFAULT FALSE
                """)
    except Exception:
        pass
    finally:
        conn.close()


def db_insert_auto_trade(ticker, direction, signal_confidence, action, contracts, price_cents=None, order_id=None, pnl_cents=None, fee_cents=0, is_paper=False):
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO auto_trades (ts, ticker, direction, signal_confidence, action, contracts, price_cents, order_id, pnl_cents, fee_cents, is_paper)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (datetime.now(timezone.utc).isoformat(), ticker, direction, signal_confidence, action, contracts, price_cents, order_id, pnl_cents, fee_cents or 0, bool(is_paper)),
                )
    except Exception:
        pass
    finally:
        conn.close()


def db_update_auto_trade_price(order_id, price_cents, contracts=None):
    if not DATABASE_URL or not order_id:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                if contracts is not None:
                    cur.execute(
                        "UPDATE auto_trades SET price_cents = %s, contracts = %s WHERE order_id = %s AND action = 'buy'",
                        (price_cents, contracts, order_id),
                    )
                else:
                    cur.execute(
                        "UPDATE auto_trades SET price_cents = %s WHERE order_id = %s AND action = 'buy'",
                        (price_cents, order_id),
                    )
    except Exception:
        pass
    finally:
        conn.close()


def db_load_auto_trades(limit=50):
    if not DATABASE_URL:
        return []
    conn = _db_conn()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ts, ticker, direction, signal_confidence, action, contracts, price_cents, order_id, pnl_cents, COALESCE(fee_cents, 0) as fee_cents
                FROM auto_trades
                ORDER BY ts DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
        return [
            {
                "ts": r[0], "ticker": r[1], "direction": r[2], "signal_confidence": r[3],
                "action": r[4], "contracts": r[5], "price_cents": r[6], "order_id": r[7], "pnl_cents": r[8], "fee_cents": r[9],
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        conn.close()


db_init_auto_trades()


def db_init_training_samples():
    """Create training_samples table and add label column to book_image_snapshots."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS training_samples (
                        id        SERIAL PRIMARY KEY,
                        ts        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        label     SMALLINT NOT NULL,
                        v_t       DOUBLE PRECISION,
                        c_t       DOUBLE PRECISION,
                        exchanges SMALLINT,
                        hawkes    DOUBLE PRECISION,
                        brti_return   DOUBLE PRECISION,
                        bid_ask_spread DOUBLE PRECISION,
                        bid_depth_10   DOUBLE PRECISION,
                        ask_depth_10   DOUBLE PRECISION,
                        imbalance      DOUBLE PRECISION
                    )
                """)
                # Add all extended feature columns (safe: ADD COLUMN IF NOT EXISTS is idempotent)
                for _col in [
                    "brti_ret_5 DOUBLE PRECISION",
                    "brti_ret_10 DOUBLE PRECISION",
                    "brti_ret_30 DOUBLE PRECISION",
                    "vt_velocity DOUBLE PRECISION",
                    "microprice DOUBLE PRECISION",
                    "spread_pct DOUBLE PRECISION",
                    "bid1_vol DOUBLE PRECISION",
                    "ask1_vol DOUBLE PRECISION",
                    "bid5_vol DOUBLE PRECISION",
                    "ask5_vol DOUBLE PRECISION",
                    "bid20_vol DOUBLE PRECISION",
                    "ask20_vol DOUBLE PRECISION",
                    "depth_ratio_1 DOUBLE PRECISION",
                    "depth_ratio_5 DOUBLE PRECISION",
                    "vol_30 DOUBLE PRECISION",
                    "vol_60 DOUBLE PRECISION",
                    "rsi_7 DOUBLE PRECISION",
                    "rsi_14 DOUBLE PRECISION",
                    "rsi_21 DOUBLE PRECISION",
                    "vwap_dev DOUBLE PRECISION",
                    "imbalance_velocity DOUBLE PRECISION",
                ]:
                    cur.execute(f"ALTER TABLE training_samples ADD COLUMN IF NOT EXISTS {_col}")
                cur.execute("""
                    ALTER TABLE book_image_snapshots
                    ADD COLUMN IF NOT EXISTS label SMALLINT
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS xgb_mtf_predictions (
                        id              SERIAL PRIMARY KEY,
                        ts              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        price_at_capture DOUBLE PRECISION,
                        pred_15s_dir    SMALLINT,
                        pred_15s_conf   DOUBLE PRECISION,
                        pred_60s_dir    SMALLINT,
                        pred_60s_conf   DOUBLE PRECISION,
                        actual_15s_dir  SMALLINT,
                        actual_60s_dir  SMALLINT,
                        resolved_15s    BOOLEAN DEFAULT FALSE,
                        resolved_60s    BOOLEAN DEFAULT FALSE
                    )
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS xgb_mtf_predictions_ts_idx
                    ON xgb_mtf_predictions (ts DESC)
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS xgb_mtf_predictions_unresolved_idx
                    ON xgb_mtf_predictions (ts) WHERE resolved_15s = FALSE OR resolved_60s = FALSE
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS training_samples_ts_idx
                    ON training_samples (ts DESC)
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS ensemble_predictions_ts_brin
                    ON ensemble_predictions (ts DESC)
                """)
    except Exception:
        pass
    finally:
        conn.close()


db_init_training_samples()


def _db_persist_labeled_batch(tab_rows: list, img_updates: list):
    """Background: INSERT new tabular labeled rows + UPDATE image labels.
    tab_rows: list of dicts with keys matching training_samples columns + 'label'.
    img_updates: list of (ts_unix_float, label) tuples."""
    if not DATABASE_URL or (not tab_rows and not img_updates):
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                if tab_rows:
                    def _to_py(v):
                        """Coerce numpy/other scalar to native Python type."""
                        if v is None:
                            return None
                        try:
                            return float(v)
                        except (TypeError, ValueError):
                            return v
                    execute_values(
                        cur,
                        """INSERT INTO training_samples
                           (ts, label, v_t, c_t, exchanges, hawkes, brti_return,
                            bid_ask_spread, bid_depth_10, ask_depth_10, imbalance,
                            brti_ret_5, brti_ret_10, brti_ret_30, vt_velocity,
                            microprice, spread_pct,
                            bid1_vol, ask1_vol, bid5_vol, ask5_vol, bid20_vol, ask20_vol,
                            depth_ratio_1, depth_ratio_5,
                            vol_30, vol_60, rsi_7, rsi_14, rsi_21,
                            vwap_dev, imbalance_velocity)
                           VALUES %s""",
                        [(
                            datetime.fromtimestamp(
                                float(r.get("_sample_ts") or time.time()), tz=timezone.utc
                            ).isoformat(),
                            int(r["label"]),
                            _to_py(r.get("v_T")), _to_py(r.get("C_T")),
                            int(r["exchanges"]) if r.get("exchanges") is not None else None,
                            _to_py(r.get("hawkes")), _to_py(r.get("brti_return")),
                            _to_py(r.get("bid_ask_spread")),
                            _to_py(r.get("bid_depth_10")), _to_py(r.get("ask_depth_10")),
                            _to_py(r.get("imbalance")),
                            _to_py(r.get("brti_ret_5")), _to_py(r.get("brti_ret_10")),
                            _to_py(r.get("brti_ret_30")), _to_py(r.get("vt_velocity")),
                            _to_py(r.get("microprice")), _to_py(r.get("spread_pct")),
                            _to_py(r.get("bid1_vol")), _to_py(r.get("ask1_vol")),
                            _to_py(r.get("bid5_vol")), _to_py(r.get("ask5_vol")),
                            _to_py(r.get("bid20_vol")), _to_py(r.get("ask20_vol")),
                            _to_py(r.get("depth_ratio_1")), _to_py(r.get("depth_ratio_5")),
                            _to_py(r.get("vol_30")), _to_py(r.get("vol_60")),
                            _to_py(r.get("rsi_7")), _to_py(r.get("rsi_14")),
                            _to_py(r.get("rsi_21")), _to_py(r.get("vwap_dev")),
                            _to_py(r.get("imbalance_velocity")),
                        ) for r in tab_rows],
                    )
                if img_updates:
                    execute_values(
                        cur,
                        """UPDATE book_image_snapshots SET label = _d.label
                           FROM (VALUES %s) AS _d(ts_unix, label)
                           WHERE ABS(EXTRACT(EPOCH FROM book_image_snapshots.ts)
                                     - _d.ts_unix::DOUBLE PRECISION) < 0.05""",
                        [(float(ts_unix), int(lbl)) for ts_unix, lbl in img_updates],
                        template="(%s::DOUBLE PRECISION, %s::SMALLINT)",
                    )
    except Exception as _pe:
        try:
            with open("/tmp/bobby_debug.log", "a") as _f:
                _f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] "
                    f"[PERSIST ERROR] tab={len(tab_rows)} img={len(img_updates)}: {_pe}\n"
                )
        except Exception:
            pass
    finally:
        conn.close()


def db_prune_old_data():
    """Prune tables that grow without bound. Keeps data needed for training
    and analysis while preventing disk exhaustion."""
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                # kalshi_orderbook: keep 48 hours of snapshot history
                cur.execute(
                    "DELETE FROM kalshi_orderbook WHERE ts < NOW() - INTERVAL '48 hours'"
                )
                # bobby_brti_ticks: keep 14 days (training window)
                cur.execute(
                    "DELETE FROM bobby_brti_ticks WHERE ts < NOW() - INTERVAL '14 days'"
                )
                # brti_ticks: keep 14 days
                cur.execute(
                    "DELETE FROM brti_ticks WHERE ts < NOW() - INTERVAL '14 days'"
                )
                # ensemble_predictions: keep 7 days (analysis + calibration)
                cur.execute(
                    "DELETE FROM ensemble_predictions WHERE ts < NOW() - INTERVAL '7 days'"
                )
                # book_image_snapshots: keep 48 hours (CNN only needs recent images)
                cur.execute(
                    "DELETE FROM book_image_snapshots WHERE ts < NOW() - INTERVAL '48 hours'"
                )
                # training_samples: NEUTRAL samples (label=1) older than 14 days are
                # unused by either model (XGBoost trains on UP/DOWN only, CNN filters
                # NEUTRAL) — prune them to control table growth. Keep all directional.
                cur.execute(
                    "DELETE FROM training_samples WHERE label = 1 "
                    "AND ts < NOW() - INTERVAL '14 days'"
                )
                # btc_prices: keep 30 days for analysis
                cur.execute(
                    "DELETE FROM btc_prices WHERE ts < NOW() - INTERVAL '30 days'"
                )
                # auto_trades: keep 90 days for performance review
                cur.execute(
                    "DELETE FROM auto_trades WHERE ts < NOW() - INTERVAL '90 days'"
                )
    except Exception as _prune_err:
        try:
            with open("/tmp/bobby_debug.log", "a") as _f:
                _f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] "
                    f"[PRUNE ERROR] {_prune_err}\n"
                )
        except Exception:
            pass
    finally:
        conn.close()


with st.sidebar:
    st.title("⚙️ Settings")

    st.subheader("API Status")
    if KALSHI_AUTH_READY:
        st.success("Kalshi API: Authenticated (RSA-PSS)")
    elif KALSHI_API_KEY:
        st.warning("Kalshi API: Key found, private key missing")
    else:
        st.error("Kalshi API Key: Not found")
    if POLYGON_API_KEY:
        st.success("Polygon API Key: Connected")
    else:
        st.error("Polygon API Key: Not found")
    if DATABASE_URL:
        st.success("Database: Connected")
    else:
        st.warning("Database: Not configured")

    st.divider()
    st.subheader("Chart Settings")
    timeframe_opts = {
        "1 Hour": 60,
        "4 Hours": 240,
        "12 Hours": 720,
        "1 Day": 1440,
        "3 Days": 4320,
        "7 Days": 10080,
    }
    selected_tf = st.selectbox("Lookback Window", list(timeframe_opts.keys()), index=2)
    lookback_mins = timeframe_opts[selected_tf]

    candle_opts = {"1m": (1, "minute"), "5m": (5, "minute"), "15m": (15, "minute")}
    candle_size = st.selectbox("BTC Candle Size", list(candle_opts.keys()), index=0)
    candle_mult, candle_span = candle_opts[candle_size]

    divergence_threshold = st.slider(
        "Divergence Threshold (%)",
        min_value=1, max_value=20, value=5,
        help="Flag periods where Kalshi yes% and BTC price diverge by more than this amount (normalised)."
    )

    auto_refresh = st.checkbox("Auto-refresh every 30s", value=False)

    st.divider()
    if st.button("🔄 Refresh Now", width="stretch"):
        st.cache_data.clear()


def _sign_kalshi_request(method: str, path: str) -> dict:
    if not KALSHI_AUTH_READY:
        return {"Content-Type": "application/json", "Accept": "application/json"}
    timestamp_ms = str(int(datetime.now(timezone.utc).timestamp() * 1000))
    msg = timestamp_ms + method.upper() + path
    signature = _kalshi_private_key.sign(
        msg.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    sig_b64 = base64.b64encode(signature).decode("utf-8")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "KALSHI-ACCESS-KEY": KALSHI_API_KEY,
        "KALSHI-ACCESS-SIGNATURE": sig_b64,
        "KALSHI-ACCESS-TIMESTAMP": timestamp_ms,
    }


def _kalshi_get(api_path, params, timeout=10):
    full_path = KALSHI_BASE_PATH + api_path
    return _kalshi_get_core(full_path, params, timeout, report_ui=True)


def _kalshi_get_bg(api_path, params, timeout=10):
    """Kalshi GET safe for background threads (no Streamlit UI calls)."""
    full_path = KALSHI_BASE_PATH + api_path
    return _kalshi_get_core(full_path, params, timeout, report_ui=False)


def _kalshi_post(api_path, body, timeout=10):
    if not KALSHI_AUTH_READY:
        return None, "Kalshi auth not configured"
    full_path = KALSHI_BASE_PATH + api_path
    last_error = None
    for host in KALSHI_HOSTS:
        url = host + full_path
        try:
            headers = _sign_kalshi_request("POST", full_path)
            resp = requests.post(url, json=body, headers=headers, timeout=timeout)
            if resp.status_code in (401, 403):
                last_error = f"{host}: {resp.status_code} {resp.text[:300]}"
                break
            if not resp.ok:
                last_error = f"{host}: {resp.status_code} {resp.text[:300]}"
                break
            return resp.json(), None
        except requests.exceptions.HTTPError as e:
            body_text = getattr(getattr(e, "response", None), "text", "")
            last_error = f"{str(e)} — {body_text[:300]}"
            break
        except requests.exceptions.ConnectionError:
            last_error = f"{host}: connection error"
            continue
    return None, last_error


def _kalshi_delete(api_path, timeout=10):
    if not KALSHI_AUTH_READY:
        return None, "Kalshi auth not configured"
    full_path = KALSHI_BASE_PATH + api_path
    last_error = None
    for host in KALSHI_HOSTS:
        url = host + full_path
        try:
            headers = _sign_kalshi_request("DELETE", full_path)
            resp = requests.delete(url, headers=headers, timeout=timeout)
            if resp.status_code in (401, 403):
                last_error = f"{host}: {resp.status_code} {resp.text[:200]}"
                break
            resp.raise_for_status()
            return resp.json(), None
        except requests.exceptions.HTTPError as e:
            last_error = str(e)
            break
        except requests.exceptions.ConnectionError:
            last_error = f"{host}: connection error"
            continue
    return None, last_error


def kalshi_get_balance():
    data = _kalshi_get_bg("/portfolio/balance", {}, timeout=10)
    if data and "balance" in data:
        return data["balance"]
    return None


def kalshi_place_order(ticker, action, side, count, price_cents=None, client_order_id=None):
    """Place a limit order on Kalshi.
    price_cents: the limit price in cents for the given side.
                 If None, falls back to aggressive defaults (99 buy / 1 sell).
    """
    import uuid as _uuid
    if price_cents is None:
        price_cents = 99 if action == "buy" else 1
    price_key = "yes_price" if side == "yes" else "no_price"
    body = {
        "ticker": ticker,
        "action": action,
        "side": side,
        "count": count,
        "type": "limit",
        price_key: int(price_cents),
        "client_order_id": client_order_id or str(_uuid.uuid4()),
    }
    return _kalshi_post("/portfolio/orders", body, timeout=15)


def kalshi_cancel_order(order_id):
    return _kalshi_delete(f"/portfolio/orders/{order_id}", timeout=10)


def _kalshi_get_core(full_path, params, timeout, report_ui=False):
    last_error = None
    for host in KALSHI_HOSTS:
        url = host + full_path
        for use_auth in [False, True]:
            try:
                if use_auth and KALSHI_AUTH_READY:
                    headers = _sign_kalshi_request("GET", full_path)
                else:
                    headers = {"Content-Type": "application/json", "Accept": "application/json"}
                resp = requests.get(url, params=params, headers=headers, timeout=timeout)
                if resp.status_code in (401, 403) and not use_auth:
                    continue
                if resp.status_code in (401, 403) and use_auth:
                    last_error = f"{host}: {resp.status_code} {resp.text[:200]}"
                    break
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.HTTPError as e:
                last_error = str(e)
                if not use_auth:
                    continue
                break
            except requests.exceptions.ConnectionError:
                break
    if last_error and report_ui:
        st.sidebar.caption(f"Kalshi API: {last_error[:120]}")
    return {}


_KALSHI_WS_URL = "wss://api.elections.kalshi.com/trade-api/ws/v2"


def _sign_kalshi_ws_headers() -> list:
    """Return RSA-PSS signed headers for the Kalshi WebSocket handshake."""
    if not KALSHI_AUTH_READY:
        return []
    path = "/trade-api/ws/v2"
    ts = str(int(datetime.now(timezone.utc).timestamp() * 1000))
    msg = ts + "GET" + path
    sig = _kalshi_private_key.sign(
        msg.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return [
        f"KALSHI-ACCESS-KEY: {KALSHI_API_KEY}",
        f"KALSHI-ACCESS-SIGNATURE: {base64.b64encode(sig).decode()}",
        f"KALSHI-ACCESS-TIMESTAMP: {ts}",
    ]


@st.cache_resource
def _kalshi_ws_state():
    """Live order book state — maintained by delta messages, persists across reruns."""
    return {
        "yes_book": {},
        "no_book": {},
        "ticker_data": {},
        "snapshot_deque": collections.deque(maxlen=3600),
        "lock": threading.Lock(),
        "ws_obj": [None],
        "ws_thread": [None],
        "snap_thread": [None],
        "connected": [False],
        "ticker": [None],
        "msg_count": [0],
        "last_msg_ts": [None],
        "stop_snap": [False],
    }


def _kalshi_ws_snapshot_loop():
    """Runs every second: snapshot the live book state, append to deque, save to DB every 5s."""
    state = _kalshi_ws_state()
    last_db_save = 0.0
    last_msg_seen = 0
    while not state["stop_snap"][0]:
        time.sleep(1)
        if state["stop_snap"][0]:
            break
        if not state["connected"][0]:
            continue
        now = datetime.now(timezone.utc)
        with state["lock"]:
            cur_msg_count = state["msg_count"][0]
            raw_yes_list = list(state["yes_book"].items())
            raw_no_list = list(state["no_book"].items())
            ticker = state["ticker"][0]
            ticker_data = dict(state["ticker_data"])
        if not ticker or not (raw_yes_list or raw_no_list):
            continue
        if cur_msg_count == last_msg_seen:
            continue
        last_msg_seen = cur_msg_count
        processed = _process_raw_orderbook(raw_yes_list, raw_no_list)
        snapshot = {"ts": now, "ticker": ticker, "ticker_data": ticker_data, **processed}
        with state["lock"]:
            state["snapshot_deque"].append(snapshot)
        now_ts = time.time()
        if now_ts - last_db_save >= 5.0:
            last_db_save = now_ts
            threading.Thread(
                target=db_save_orderbook_snapshot,
                args=(now, ticker, processed["yes_bids"], processed["yes_asks"]),
                daemon=True,
            ).start()


def start_kalshi_ws(ticker: str):
    state = _kalshi_ws_state()
    need_full_reset = state["ticker"][0] != ticker
    if need_full_reset:
        state["stop_snap"][0] = True
        ws = state["ws_obj"][0]
        if ws:
            try:
                ws.keep_running = False
                ws.close()
            except Exception:
                pass
        old_t = state["ws_thread"][0]
        if old_t is not None:
            old_t.join(timeout=2)
        old_s = state["snap_thread"][0]
        if old_s is not None:
            old_s.join(timeout=2)
        with state["lock"]:
            state["yes_book"].clear()
            state["no_book"].clear()
            state["ticker_data"].clear()
            state["msg_count"][0] = 0
            state["last_msg_ts"][0] = None
            state["snapshot_deque"].clear()
        state["ticker"][0] = ticker
        state["connected"][0] = False
        state["ws_obj"][0] = None
        state["ws_thread"][0] = None
        state["snap_thread"][0] = None
    t = state["ws_thread"][0]
    if t is not None and t.is_alive():
        s = state["snap_thread"][0]
        if s is None or not s.is_alive():
            state["stop_snap"][0] = False
            snap_thread = threading.Thread(target=_kalshi_ws_snapshot_loop, daemon=True)
            snap_thread.start()
            state["snap_thread"][0] = snap_thread
        return

    old_snap = state["snap_thread"][0]
    if old_snap is not None and old_snap.is_alive():
        state["stop_snap"][0] = True
        old_snap.join(timeout=2)

    def _on_message(ws, raw):
        try:
            d = json.loads(raw)
            msg_type = d.get("type")
            msg = d.get("msg", {})
            with state["lock"]:
                state["msg_count"][0] += 1
                state["last_msg_ts"][0] = datetime.now(timezone.utc)
                if msg_type == "orderbook_snapshot":
                    state["yes_book"].clear()
                    state["no_book"].clear()
                    yes_fp = msg.get("yes_dollars_fp", [])
                    no_fp = msg.get("no_dollars_fp", [])
                    if yes_fp or no_fp:
                        for pair in yes_fp:
                            state["yes_book"][round(float(pair[0]) * 100)] = round(float(pair[1]))
                        for pair in no_fp:
                            state["no_book"][round(float(pair[0]) * 100)] = round(float(pair[1]))
                    else:
                        for price, qty in msg.get("yes", []):
                            state["yes_book"][int(price)] = int(qty)
                        for price, qty in msg.get("no", []):
                            state["no_book"][int(price)] = int(qty)
                elif msg_type == "orderbook_delta":
                    side = msg.get("side", "yes")
                    book = state["yes_book"] if side == "yes" else state["no_book"]
                    price_d = msg.get("price_dollars")
                    delta_d = msg.get("delta_fp")
                    if price_d is not None and delta_d is not None:
                        price_cents = round(float(price_d) * 100)
                        delta_val = round(float(delta_d))
                        new_qty = book.get(price_cents, 0) + delta_val
                        if new_qty <= 0:
                            book.pop(price_cents, None)
                        else:
                            book[price_cents] = new_qty
                    else:
                        price = msg.get("price")
                        delta = msg.get("delta", 0)
                        if isinstance(price, str):
                            price = round(float(price) * 100)
                        if isinstance(delta, str):
                            delta = round(float(delta))
                        if delta == 0:
                            book.pop(price, None)
                        else:
                            book[int(price)] = int(delta)
                elif msg_type == "ticker":
                    state["ticker_data"].update(msg)
        except Exception:
            pass

    def _on_open(ws):
        with state["lock"]:
            state["yes_book"].clear()
            state["no_book"].clear()
        state["connected"][0] = True
        ws.send(json.dumps({
            "id": 1,
            "cmd": "subscribe",
            "params": {
                "channels": ["orderbook_delta", "ticker"],
                "market_tickers": [state["ticker"][0]],
            },
        }))

    def _on_close(ws, code, reason):
        state["connected"][0] = False

    def _on_error(ws, err):
        state["connected"][0] = False

    ws_obj = _WebSocketApp(
        _KALSHI_WS_URL,
        header=_sign_kalshi_ws_headers,
        on_message=_on_message,
        on_open=_on_open,
        on_error=_on_error,
        on_close=_on_close,
    )
    state["ws_obj"][0] = ws_obj
    ws_thread = threading.Thread(
        target=ws_obj.run_forever, kwargs={"reconnect": 5}, daemon=True
    )
    ws_thread.start()
    state["ws_thread"][0] = ws_thread

    state["stop_snap"][0] = False
    snap_thread = threading.Thread(target=_kalshi_ws_snapshot_loop, daemon=True)
    snap_thread.start()
    state["snap_thread"][0] = snap_thread


def stop_kalshi_ws():
    state = _kalshi_ws_state()
    state["stop_snap"][0] = True
    ws = state["ws_obj"][0]
    if ws:
        try:
            ws.keep_running = False
            ws.close()
        except Exception:
            pass
    old_t = state["ws_thread"][0]
    if old_t is not None:
        old_t.join(timeout=3)
    old_s = state["snap_thread"][0]
    if old_s is not None:
        old_s.join(timeout=2)
    state["ws_obj"][0] = None
    state["connected"][0] = False
    state["ws_thread"][0] = None
    state["snap_thread"][0] = None


def kalshi_ws_is_running() -> bool:
    state = _kalshi_ws_state()
    t = state["ws_thread"][0]
    return t is not None and t.is_alive()


def kalshi_ws_is_connected() -> bool:
    return _kalshi_ws_state()["connected"][0]


def get_live_book() -> dict:
    state = _kalshi_ws_state()
    with state["lock"]:
        yes_bids = sorted([[p, q] for p, q in state["yes_book"].items()], key=lambda x: -x[0])[:10]
        yes_asks = sorted([[100 - p, q] for p, q in state["no_book"].items()], key=lambda x: x[0])[:10]
        return {
            "yes_bids": yes_bids,
            "yes_asks": yes_asks,
            "ticker_data": dict(state["ticker_data"]),
            "msg_count": state["msg_count"][0],
            "last_msg_ts": state["last_msg_ts"][0],
            "connected": state["connected"][0],
        }


def get_live_snapshots() -> list:
    state = _kalshi_ws_state()
    with state["lock"]:
        return list(state["snapshot_deque"])


@st.cache_resource
def _ob_state():
    """Shared state for background orderbook polling — persists across reruns."""
    return {
        "deque": collections.deque(maxlen=720),
        "lock": threading.Lock(),
        "thread": [None],
        "stop": [False],
        "ticker": [None],
        "last_snapshot": [None],
    }


@st.cache_resource
def _depth_signal_state():
    """In-memory ring buffer of the last 240 depth signal snapshots (~4 hours at 1/min)."""
    return {
        "deque": collections.deque(maxlen=240),
        "lock": threading.Lock(),
        "latest": [None],
    }


def get_depth_signal_latest() -> dict:
    s = _depth_signal_state()
    with s["lock"]:
        return s["latest"][0] or {}


def get_depth_signal_history() -> list:
    s = _depth_signal_state()
    with s["lock"]:
        return list(s["deque"])


def _ob_poll_loop():
    state = _ob_state()
    while not state["stop"][0]:
        ticker = state["ticker"][0]
        if ticker:
            try:
                data = _kalshi_get_bg(f"/markets/{ticker}/orderbook", {})
                raw_yes, raw_no = _extract_ob_from_response(data)
                if raw_yes or raw_no:
                    now = datetime.now(timezone.utc)
                    processed = _process_raw_orderbook(raw_yes, raw_no)
                    snapshot = {"ts": now, "ticker": ticker, **processed}
                    with state["lock"]:
                        state["deque"].append(snapshot)
                        state["last_snapshot"][0] = snapshot
                    db_save_orderbook_snapshot(now, ticker, processed["yes_bids"], processed["yes_asks"])
            except Exception:
                pass
        time.sleep(5)


def start_ob_polling(ticker: str):
    state = _ob_state()
    state["ticker"][0] = ticker
    t = state["thread"][0]
    if t is not None and t.is_alive():
        return
    state["stop"][0] = False
    thread = threading.Thread(target=_ob_poll_loop, daemon=True)
    thread.start()
    state["thread"][0] = thread


def stop_ob_polling():
    state = _ob_state()
    state["stop"][0] = True
    state["thread"][0] = None


def ob_is_running() -> bool:
    t = _ob_state()["thread"][0]
    return t is not None and t.is_alive()


def get_ob_latest() -> dict:
    state = _ob_state()
    with state["lock"]:
        return state["last_snapshot"][0] or {}


def get_ob_history() -> list:
    state = _ob_state()
    with state["lock"]:
        return list(state["deque"])


@st.cache_resource
def _bg_data_state():
    return {
        "thread": [None],
        "stop": [False],
        "last_btc_ts": [None],
        "last_kalshi_ts": [None],
        "lock": threading.Lock(),
    }


def _bg_data_loop():
    """Background thread: fetches BTC prices + Kalshi candlesticks every 60 s
    and saves to the database, independent of UI reruns."""
    state = _bg_data_state()
    _prune_counter = [0]
    _depth_table_ensured = [False]
    while not state["stop"][0]:
        try:
            if POLYGON_API_KEY:
                now = datetime.now(timezone.utc)
                from_dt = now - timedelta(minutes=120)
                from_ms = int(from_dt.timestamp() * 1000)
                to_ms = int(now.timestamp() * 1000)
                resp = requests.get(
                    f"{POLYGON_BASE}/aggs/ticker/X:BTCUSD/range/1/minute/{from_ms}/{to_ms}",
                    params={"apiKey": POLYGON_API_KEY, "adjusted": "true",
                            "sort": "asc", "limit": 50000},
                    timeout=15,
                )
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        btc_df_bg = _parse_polygon_results(results)
                        if not btc_df_bg.empty:
                            db_save_btc_prices(btc_df_bg)
                        with state["lock"]:
                            state["last_btc_ts"][0] = datetime.now(timezone.utc)
        except Exception:
            pass

        try:
            if KALSHI_AUTH_READY:
                data = _kalshi_get_bg("/markets",
                    {"series_ticker": SERIES_TICKER, "status": "open", "limit": 20})
                bg_markets = data.get("markets", [])
                now_k = datetime.now(timezone.utc)
                bg_active = None
                for m in bg_markets:
                    ct = m.get("close_time") or m.get("expected_expiration_time")
                    if ct:
                        exp = pd.to_datetime(ct, utc=True)
                        if exp > now_k:
                            bg_active = m
                            break
                if bg_active:
                    bg_ticker = bg_active["ticker"]
                    end_ts = int(now_k.timestamp())
                    start_ts = end_ts - 7200
                    cdata = _kalshi_get_bg(
                        f"/series/{SERIES_TICKER}/markets/{bg_ticker}/candlesticks",
                        {"start_ts": start_ts, "end_ts": end_ts, "period_interval": 1},
                    )
                    candles = cdata.get("candlesticks", [])
                    rows = [r for c in candles if (r := _parse_candle_yes_price(c)) is not None]
                    if rows:
                        kdf = pd.DataFrame(rows).sort_values("ts").reset_index(drop=True)
                        db_save_kalshi_candlesticks(kdf, bg_ticker)
                        with state["lock"]:
                            state["last_kalshi_ts"][0] = datetime.now(timezone.utc)

                    # ── Depth signal: fetch OB for active ticker ──────────────
                    try:
                        if not _depth_table_ensured[0]:
                            db_ensure_depth_signal_table()
                            _depth_table_ensured[0] = True
                        ob_data = _kalshi_get_bg(f"/markets/{bg_ticker}/orderbook", {})
                        raw_yes, raw_no = _extract_ob_from_response(ob_data)
                        if raw_yes is not None and raw_no is not None:
                            bid_depth = sum(q for _p, q in raw_yes)
                            ask_depth = sum(q for _p, q in raw_no)
                            if bid_depth > 0 and ask_depth > 0:
                                processed_ob = _process_raw_orderbook(raw_yes, raw_no)
                                best_bid = processed_ob.get("best_bid") or 0.0
                                best_ask = processed_ob.get("best_ask") or 0.0
                                ratio = ask_depth / bid_depth
                                sig = _classify_depth_signal(ratio)
                                # grab current BRTI price
                                try:
                                    brti_now = _bobby_brti_state()["last_price"][0] or 0.0
                                except Exception:
                                    brti_now = 0.0
                                snap = {
                                    "ts": now_k,
                                    "ticker": bg_ticker,
                                    "best_bid_cents": best_bid,
                                    "best_ask_cents": best_ask,
                                    "bid_depth": bid_depth,
                                    "ask_depth": ask_depth,
                                    "ask_to_bid_ratio": ratio,
                                    "signal": sig,
                                    "brti_at_capture": brti_now,
                                }
                                ds = _depth_signal_state()
                                with ds["lock"]:
                                    ds["deque"].append(snap)
                                    ds["latest"][0] = snap
                                threading.Thread(
                                    target=db_save_depth_signal,
                                    args=(now_k, bg_ticker, best_bid, best_ask,
                                          bid_depth, ask_depth, ratio, sig, brti_now),
                                    daemon=True,
                                ).start()
                    except Exception:
                        pass
        except Exception:
            pass

        # Resolve future prices every 5 minutes
        _prune_counter[0] += 1
        if _prune_counter[0] % 5 == 0:
            threading.Thread(target=db_resolve_depth_signals, daemon=True,
                             name="depth-resolve").start()
        # Prune old data once per hour (every 60 iterations × 60s = 1hr)
        if _prune_counter[0] % 60 == 1:
            threading.Thread(target=db_prune_old_data, daemon=True, name="db-prune").start()

        for _ in range(60):
            if state["stop"][0]:
                return
            time.sleep(1)


def start_bg_data_collector():
    state = _bg_data_state()
    t = state["thread"][0]
    if t is not None and t.is_alive():
        return
    state["stop"][0] = False
    thread = threading.Thread(target=_bg_data_loop, daemon=True)
    thread.start()
    state["thread"][0] = thread


def bg_data_is_running() -> bool:
    t = _bg_data_state()["thread"][0]
    return t is not None and t.is_alive()


@st.cache_data(ttl=20)
def fetch_kalshi_markets():
    try:
        data = _kalshi_get(
            "/markets",
            params={"series_ticker": SERIES_TICKER, "status": "open", "limit": 20},
        )
        return data.get("markets", [])
    except Exception as e:
        st.sidebar.warning(f"Kalshi markets error: {e}")
        return []


_MONTH_MAP_15M = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
                  "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}


def build_15m_ticker(dt_utc: datetime) -> str:
    """Build the KXBTC15M market ticker for the 15-min window containing *dt_utc*.
    Real Kalshi format: KXBTC15M-26MAR120200-00
    (uppercase, window END time in ET, dash-minute suffix)."""
    dt_et = dt_utc.astimezone(_ET)
    minute_start = (dt_et.minute // 15) * 15
    window_start_et = dt_et.replace(minute=minute_start, second=0, microsecond=0)
    window_end_et   = window_start_et + timedelta(minutes=15)
    end_minute = f"{window_end_et.minute:02d}"
    base = (f"KXBTC15M-{window_end_et.strftime('%y')}"
            f"{window_end_et.strftime('%b').upper()}"
            f"{window_end_et.strftime('%d%H%M')}")
    return f"{base}-{end_minute}"


def build_15m_event_ticker(dt_utc: datetime) -> str:
    """Build the KXBTC15M event ticker (no dash-minute suffix).
    Real Kalshi format: KXBTC15M-26MAR120200."""
    dt_et = dt_utc.astimezone(_ET)
    minute_start = (dt_et.minute // 15) * 15
    window_start_et = dt_et.replace(minute=minute_start, second=0, microsecond=0)
    window_end_et   = window_start_et + timedelta(minutes=15)
    return (f"KXBTC15M-{window_end_et.strftime('%y')}"
            f"{window_end_et.strftime('%b').upper()}"
            f"{window_end_et.strftime('%d%H%M')}")


def parse_15m_ticker(ticker: str) -> datetime:
    """Return the window END time as UTC from a ticker string."""
    s = re.sub(r"(?i)^kxbtc15m-", "", ticker)
    s = re.sub(r"-\d+$", "", s)
    m = re.fullmatch(r"(\d{2})([a-zA-Z]{3})(\d{2})(\d{2})(\d{2})", s)
    if not m:
        raise ValueError(f"Unrecognised ticker: {ticker}")
    yy, mon, dd, hh, mm = m.groups()
    dt_et = datetime(2000 + int(yy), _MONTH_MAP_15M[mon.lower()], int(dd),
                     int(hh), int(mm), tzinfo=_ET)
    return dt_et.astimezone(timezone.utc)


@st.cache_data(ttl=5)
def fetch_kalshi_15m_markets(status: str = "active") -> list:
    """Fetch KXBTC15M markets with the given status filter."""
    try:
        data = _kalshi_get(
            "/markets",
            params={"series_ticker": SERIES_TICKER_15M, "status": status, "limit": 100},
        )
        return data.get("markets", [])
    except Exception:
        return []


@st.cache_data(ttl=30)
def _find_next_15m_event(now_utc: datetime):
    """Find the next upcoming 15m market/event with open_time > now."""
    try:
        data = _kalshi_get("/events", params={
            "series_ticker": SERIES_TICKER_15M, "limit": 20,
        })
        events = data.get("events", [])
        candidates = []
        for e in events:
            sub_markets = e.get("markets", [])
            for m in sub_markets:
                ot = m.get("open_time")
                if not ot:
                    continue
                open_dt = pd.to_datetime(ot, utc=True)
                if open_dt > now_utc:
                    candidates.append((open_dt, m))
        if candidates:
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]
    except Exception:
        pass
    return None


def _find_active_15m_3strategy(now_utc: datetime) -> dict | None:
    """3-strategy fallback to discover the active 15-minute market.
    Strategy 1: series search (open/active status).
    Strategy 2: direct computed ticker lookup (builds ticker from clock).
    Strategy 3: broad scan for BTC 15-min markets among all open markets.
    """
    _active_statuses = {"open", "active", "trading"}

    # ── Strategy 1: series search ────────────────────────────────────────
    for status_q in ("open", "active"):
        try:
            markets = fetch_kalshi_15m_markets(status_q)
            for m in markets:
                st_status = (m.get("status") or "").lower()
                ticker    = m.get("ticker", "")
                if st_status in _active_statuses:
                    ct = m.get("close_time") or m.get("expected_expiration_time")
                    if ct:
                        exp = pd.to_datetime(ct, utc=True)
                        if exp <= now_utc:
                            continue
                    return m
        except Exception:
            pass

    # ── Strategy 2: direct computed ticker lookup ────────────────────────
    for offset_min in (0, 15, -15):
        ticker = build_15m_ticker(now_utc + timedelta(minutes=offset_min))
        try:
            data = _kalshi_get(f"/markets/{ticker}", params={})
            if "error" not in data and "market" in data:
                market = data.get("market", data)
                if (market.get("status") or "").lower() not in _active_statuses:
                    continue
                ct = market.get("close_time") or market.get("expected_expiration_time")
                if ct:
                    exp = pd.to_datetime(ct, utc=True)
                    if exp <= now_utc:
                        continue
                return market
        except Exception:
            pass

    # ── Strategy 3: broad scan for BTC 15-min among all open markets ─────
    try:
        data = _kalshi_get("/markets", params={"limit": 200, "status": "open"})
        for m in data.get("markets", []):
            ticker = m.get("ticker", "")
            st_status = (m.get("status") or "").lower()
            if "kxbtc15m" in ticker.lower() and st_status in _active_statuses:
                return m
    except Exception:
        pass

    return None


def _find_next_15m_windows(markets: list, now: datetime, n: int = 6) -> list:
    """Return up to *n* upcoming initialized markets sorted by open time."""
    upcoming = []
    for m in markets:
        ot = m.get("open_time")
        if not ot:
            continue
        open_dt = pd.to_datetime(ot, utc=True)
        if open_dt > now:
            upcoming.append((open_dt, m))
    upcoming.sort(key=lambda x: x[0])
    return [m for _, m in upcoming[:n]]


@st.cache_data(ttl=5)
def fetch_kalshi_15m_orderbook(ticker: str) -> dict:
    """Fetch the order book for a specific KXBTC15M market (refreshes every 5 s)."""
    try:
        data = _kalshi_get(f"/markets/{ticker}/orderbook", params={})
        raw_yes, raw_no = _extract_ob_from_response(data)
        result = _process_raw_orderbook(raw_yes, raw_no)
        result["ts"] = datetime.now(timezone.utc)
        return result
    except Exception:
        return {}


@st.cache_data(ttl=20)
def fetch_kalshi_trades(ticker: str, limit: int = 500):
    endpoint_paths = [
        ("/markets/trades", {"ticker": ticker, "limit": limit}),
        (f"/markets/{ticker}/trades", {"limit": limit}),
    ]
    trades = []
    for api_path, params in endpoint_paths:
        try:
            data = _kalshi_get(api_path, params)
            trades = data.get("trades", [])
            if trades:
                break
        except Exception:
            continue
    if not trades:
        return pd.DataFrame()
    df = pd.DataFrame(trades)
    ts_col = next((c for c in ["created_time", "ts", "timestamp"] if c in df.columns), None)
    if ts_col:
        df["ts"] = pd.to_datetime(df[ts_col], utc=True)
    else:
        return pd.DataFrame()
    df = df.sort_values("ts")
    if "yes_price" in df.columns:
        df["yes_price_pct"] = df["yes_price"].astype(float) / 100.0
    elif "price" in df.columns:
        df["yes_price_pct"] = df.apply(
            lambda r: float(r["price"]) / 100.0
            if str(r.get("taker_side", "")).lower() == "yes"
            else 1 - float(r["price"]) / 100.0,
            axis=1,
        )
    else:
        return pd.DataFrame()
    return df[["ts", "yes_price_pct"]].dropna()


@st.cache_data(ttl=30)
def fetch_kalshi_candlesticks(ticker: str, lookback_mins: int):
    if not KALSHI_AUTH_READY:
        return pd.DataFrame()
    end_ts = int(datetime.now(timezone.utc).timestamp())
    start_ts = end_ts - lookback_mins * 60
    try:
        data = _kalshi_get(
            f"/series/{SERIES_TICKER}/markets/{ticker}/candlesticks",
            params={"start_ts": start_ts, "end_ts": end_ts, "period_interval": 1},
        )
        candles = data.get("candlesticks", [])
        if not candles:
            return pd.DataFrame()
        rows = [r for c in candles if (r := _parse_candle_yes_price(c)) is not None]
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows).sort_values("ts").reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=20)
def fetch_kalshi_orderbook(ticker: str):
    try:
        data = _kalshi_get(f"/markets/{ticker}/orderbook", params={})
        raw_yes, raw_no = _extract_ob_from_response(data)
        return {"yes": raw_yes, "no": raw_no}
    except Exception:
        return {}


@st.cache_data(ttl=30)
def fetch_btc_polygon(multiplier: int, timespan: str, lookback_mins: int):
    if not POLYGON_API_KEY:
        return pd.DataFrame()
    now = datetime.now(timezone.utc)
    from_dt = now - timedelta(minutes=lookback_mins)
    from_ms = int(from_dt.timestamp() * 1000)
    to_ms = int(now.timestamp() * 1000)
    try:
        resp = requests.get(
            f"{POLYGON_BASE}/aggs/ticker/X:BTCUSD/range/{multiplier}/{timespan}/{from_ms}/{to_ms}",
            params={
                "apiKey": POLYGON_API_KEY,
                "adjusted": "true",
                "sort": "asc",
                "limit": 50000,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        return _parse_polygon_results(results)
    except Exception as e:
        st.sidebar.warning(f"Polygon BTC error: {e}")
        return pd.DataFrame()


_ET = ZoneInfo("America/New_York")

TIMESCALE_BUTTONS = [
    dict(count=1, label="1H", step="hour", stepmode="backward"),
    dict(count=4, label="4H", step="hour", stepmode="backward"),
    dict(count=12, label="12H", step="hour", stepmode="backward"),
    dict(count=1, label="1D", step="day", stepmode="backward"),
    dict(count=3, label="3D", step="day", stepmode="backward"),
    dict(count=7, label="1W", step="day", stepmode="backward"),
    dict(step="all", label="All"),
]

TIMESCALE_BUTTONS_SHORT = [
    dict(count=1, label="1H", step="hour", stepmode="backward"),
    dict(count=4, label="4H", step="hour", stepmode="backward"),
    dict(count=12, label="12H", step="hour", stepmode="backward"),
    dict(count=1, label="1D", step="day", stepmode="backward"),
    dict(step="all", label="All"),
]


def _parse_candle_yes_price(c: dict):
    ts_raw = c.get("end_period_ts") or c.get("t")
    if ts_raw is None:
        return None
    ts_val = pd.to_datetime(ts_raw, unit="s", utc=True)
    yes_price_dollars = None
    price_obj = c.get("price")
    if isinstance(price_obj, dict):
        if price_obj.get("close_dollars") is not None:
            yes_price_dollars = float(price_obj["close_dollars"])
        elif price_obj.get("close") is not None:
            yes_price_dollars = float(price_obj["close"]) / 100.0
    if yes_price_dollars is None:
        ask_obj = c.get("yes_ask") or {}
        bid_obj = c.get("yes_bid") or {}
        ask_d = ask_obj.get("close_dollars")
        bid_d = bid_obj.get("close_dollars")
        ask_c = ask_obj.get("close")
        bid_c = bid_obj.get("close")
        if ask_d is not None and bid_d is not None:
            a, b = float(ask_d), float(bid_d)
            yes_price_dollars = (a + b) / 2.0 if b > 0 else a
        elif ask_d is not None:
            yes_price_dollars = float(ask_d)
        elif ask_c is not None and bid_c is not None:
            yes_price_dollars = (float(ask_c) + float(bid_c)) / 200.0
        elif ask_c is not None:
            yes_price_dollars = float(ask_c) / 100.0
        elif c.get("yes_price") is not None:
            yes_price_dollars = float(c["yes_price"]) / 100.0
    if yes_price_dollars is not None:
        return {"ts": ts_val, "yes_price_pct": yes_price_dollars}
    return None


def _parse_polygon_results(results: list) -> pd.DataFrame:
    if not results:
        return pd.DataFrame()
    df = pd.DataFrame(results)
    df = df.rename(columns={
        "o": "open", "h": "high", "l": "low",
        "c": "close", "v": "volume", "t": "ts_ms",
        "vw": "vwap", "n": "num_trades",
    })
    df["ts"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    return df[["ts", "open", "high", "low", "close", "volume"]].reset_index(drop=True)


def _extract_ob_from_response(data: dict) -> tuple[list, list]:
    """Extract raw [price_cents, qty] lists from either API format.
    New format: orderbook_fp.yes_dollars / no_dollars (string dollar pairs).
    Old format: orderbook.yes / no (integer cents pairs).
    Returns (raw_yes, raw_no) as [[cents_int, qty_int], ...]."""
    ob_fp = data.get("orderbook_fp")
    if ob_fp:
        raw_yes = []
        for pair in ob_fp.get("yes_dollars", []):
            try:
                price_cents = round(float(pair[0]) * 100)
                qty = round(float(pair[1]))
                raw_yes.append([price_cents, qty])
            except (ValueError, IndexError, TypeError):
                continue
        raw_no = []
        for pair in ob_fp.get("no_dollars", []):
            try:
                price_cents = round(float(pair[0]) * 100)
                qty = round(float(pair[1]))
                raw_no.append([price_cents, qty])
            except (ValueError, IndexError, TypeError):
                continue
        return raw_yes, raw_no
    ob = data.get("orderbook", {})
    return ob.get("yes", []), ob.get("no", [])


def _process_raw_orderbook(raw_yes: list, raw_no: list, top_n: int = 10) -> dict:
    yes_bids = sorted([[p, q] for p, q in raw_yes], key=lambda x: -x[0])[:top_n]
    yes_asks = sorted([[100 - p, q] for p, q in raw_no], key=lambda x: x[0])[:top_n]
    best_bid = yes_bids[0][0] if yes_bids else None
    best_ask = yes_asks[0][0] if yes_asks else None
    mid = (best_bid + best_ask) / 2.0 if (best_bid is not None and best_ask is not None) else None
    spread = (best_ask - best_bid) if (best_bid is not None and best_ask is not None) else None
    yes_value = sum(p / 100.0 * q for p, q in raw_yes)
    no_value = sum(p / 100.0 * q for p, q in raw_no)
    return {
        "yes_bids": yes_bids, "yes_asks": yes_asks,
        "best_bid": best_bid, "best_ask": best_ask,
        "mid": mid, "spread": spread,
        "yes_value": yes_value, "no_value": no_value,
    }


def divergence_color(val, max_abs):
    if max_abs == 0:
        return "rgba(0,230,118,0.8)"
    ratio = min(abs(val) / max_abs, 1.0)
    if ratio < 0.33:
        r = int(ratio * 3 * 255)
        g = int(230 - ratio * 3 * 100)
        return f"rgba({r},{g},50,0.85)"
    elif ratio < 0.66:
        t = (ratio - 0.33) * 3
        g = int(130 - t * 80)
        return f"rgba(255,{g},30,0.85)"
    else:
        t = (ratio - 0.66) * 3
        g = int(50 - t * 50)
        return f"rgba(255,{max(g, 0)},20,0.9)"


def _window_key(ticker: str) -> str:
    parts = ticker.split("-")
    return "-".join(parts[:2]) if len(parts) >= 3 else ticker


def _render_book_ladder(yes_bids: list, yes_asks: list, mid=None, title_prefix: str = ""):
    lad_c1, lad_c2 = st.columns(2)
    with lad_c1:
        st.markdown("#### 🟢 YES Bids (Buyers)")
        if yes_bids:
            cum = 0
            rows = []
            for p, q in yes_bids:
                cum += q
                rows.append({"Price (¢)": p, "YES %": f"{p:.0f}%", "Qty": q, "Cumulative": cum})
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        else:
            st.info("No YES bid levels available")
    with lad_c2:
        st.markdown("#### 🔴 YES Asks (Sellers)")
        if yes_asks:
            cum = 0
            rows = []
            for p, q in yes_asks:
                cum += q
                rows.append({"Price (¢)": p, "YES %": f"{p:.0f}%", "Qty": q, "Cumulative": cum})
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        else:
            st.info("No YES ask levels available")

    if yes_bids or yes_asks:
        fig_depth = go.Figure()
        if yes_bids:
            fig_depth.add_trace(go.Bar(
                x=[-q for _, q in yes_bids], y=[p for p, _ in yes_bids],
                orientation="h", name="YES Bids", marker_color="#00E676",
                hovertemplate="Price: %{y}¢<br>Qty: %{x:.0f}<extra>YES Bid</extra>",
            ))
        if yes_asks:
            fig_depth.add_trace(go.Bar(
                x=[q for _, q in yes_asks], y=[p for p, _ in yes_asks],
                orientation="h", name="YES Asks", marker_color="#FF5252",
                hovertemplate="Price: %{y}¢<br>Qty: %{x:.0f}<extra>YES Ask</extra>",
            ))
        if mid:
            fig_depth.add_hline(
                y=mid, line_color="white", line_dash="dot", line_width=1,
                annotation_text=f"Mid {mid:.1f}¢", annotation_position="right",
            )
        fig_depth.update_layout(
            title=f"{title_prefix}Order Book Depth (bids left, asks right)",
            template="plotly_dark",
            paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
            height=360,
            margin=dict(l=10, r=10, t=50, b=30),
            xaxis_title="Quantity (negative = bids)",
            yaxis_title="Price (cents)",
            barmode="overlay",
            legend=dict(orientation="h", y=1.1),
        )
        _show_chart(fig_depth, width="stretch")


_BRTI_WS_URL = "wss://www.cfbenchmarks.com/ws/v4"
_BRTI_CREDS_B64 = base64.b64encode(b"cfbenchmarksws2:e3709a02-9876-45ea-ac46-e9020e06d7c6").decode()


@st.cache_resource
def _brti_state():
    """Single shared state object persisted across all Streamlit reruns."""
    return {
        "deque": collections.deque(maxlen=7200),
        "lock": threading.Lock(),
        "ws_obj": [None],
        "ws_thread": [None],
        "flush_buf": [],
        "flush_lock": threading.Lock(),
        "flush_counter": [0],
    }


def brti_ws_is_running() -> bool:
    t = _brti_state()["ws_thread"][0]
    return t is not None and t.is_alive()


def start_brti_ws():
    if brti_ws_is_running():
        return
    state = _brti_state()

    def _on_message(ws, raw):
        try:
            d = json.loads(raw)
            if d.get("type") == "value" and d.get("id") == "BRTI":
                ts = datetime.fromtimestamp(d["time"] / 1000.0, tz=timezone.utc)
                price = float(d["value"])
                tick = {"ts": ts, "price": price}
                with state["lock"]:
                    state["deque"].append(tick)
                with state["flush_lock"]:
                    state["flush_buf"].append(tick)
                    state["flush_counter"][0] += 1
                    if state["flush_counter"][0] >= 60:
                        to_flush = list(state["flush_buf"])
                        state["flush_buf"].clear()
                        state["flush_counter"][0] = 0
                        threading.Thread(
                            target=db_save_brti_ticks, args=(to_flush,), daemon=True
                        ).start()
        except Exception:
            pass

    def _on_open(ws):
        ws.send(json.dumps({"type": "subscribe", "id": "BRTI", "stream": "value"}))

    ws_obj = _WebSocketApp(
        _BRTI_WS_URL,
        header=[f"Authorization: Basic {_BRTI_CREDS_B64}", "Origin: https://www.cfbenchmarks.com"],
        on_message=_on_message,
        on_open=_on_open,
        on_error=lambda ws, e: None,
        on_close=lambda ws, c, r: None,
    )
    state["ws_obj"][0] = ws_obj
    t = threading.Thread(target=ws_obj.run_forever, kwargs={"reconnect": 5}, daemon=True)
    t.start()
    state["ws_thread"][0] = t


def stop_brti_ws():
    state = _brti_state()
    ws = state["ws_obj"][0]
    if ws:
        try:
            ws.close()
        except Exception:
            pass
        state["ws_obj"][0] = None
    state["ws_thread"][0] = None


def get_brti_ticks() -> list:
    state = _brti_state()
    with state["lock"]:
        return list(state["deque"])


_BOBBY_SYMBOL = "BTC/USD"
_BOBBY_SPACING = 1.0
_BOBBY_D = 0.005
_BOBBY_LAMBDA = 1.0
_BOBBY_MIN_EXCHANGES = 2   # CF BRTI requires ≥2 constituent exchanges
_BOBBY_MAX_V = 10000
# CF BRTI constituent exchanges available in ccxt.pro
# (itBit/LMAX are in CF's published methodology but unavailable in ccxt.pro)
_BOBBY_CF_EXCHANGES = ["bitstamp", "coinbase", "kraken", "gemini"]


@st.cache_resource
def _bobby_brti_state():
    return {
        "deque": collections.deque(maxlen=36000),
        "lock": threading.Lock(),
        "thread": [None],
        "live_books": {},
        "books_lock": threading.Lock(),
        "flush_buf": [],
        "flush_lock": threading.Lock(),
        "flush_counter": [0],
        "status": ["off"],
        "n_exchanges": [0],
        "last_price": [None],
        "last_ts": [None],
        "error": [None],
        "stop_flag": [False],
        "cached_bids": [None],
        "cached_asks": [None],
        "cached_v_T": [None],
        "cached_C_T": [None],
        "cached_n_ex": [0],
    }


def _bobby_aggregate_order_book(books_dict):
    from collections import defaultdict
    bid_dict = defaultdict(float)
    ask_dict = defaultdict(float)
    active_count = 0
    now = time.time()
    for book in books_dict.values():
        age = now - book.get("timestamp", 0)
        if age > 30:
            continue
        b = book["bids"]
        a = book["asks"]
        if len(b) > 10 and len(a) > 10:
            active_count += 1
            for row in b:
                bid_dict[float(row[0])] += float(row[1])
            for row in a:
                ask_dict[float(row[0])] += float(row[1])
    bids = np.array(sorted([[p, s] for p, s in bid_dict.items() if s > 1e-8], reverse=True)) if bid_dict else np.array([])
    asks = np.array(sorted([[p, s] for p, s in ask_dict.items() if s > 1e-8])) if ask_dict else np.array([])
    return bids, asks, active_count


def _bobby_calculate_dynamic_cap(uncapped_bids, uncapped_asks):
    if len(uncapped_asks) == 0 or len(uncapped_bids) == 0:
        return 50.0
    best_ask = uncapped_asks[0, 0]
    best_bid = uncapped_bids[0, 0]
    ask_mask = uncapped_asks[:, 0] <= best_ask * 1.05
    ask_sizes = uncapped_asks[ask_mask, 1][:50]
    bid_mask = uncapped_bids[:, 0] >= best_bid * 0.95
    bid_sizes = uncapped_bids[bid_mask, 1][:50]
    sample = np.concatenate([ask_sizes, bid_sizes])
    if len(sample) < 5:
        return 50.0
    sorted_s = np.sort(sample)
    n = len(sorted_s)
    k = max(1, int(0.01 * n))
    trimmed_mean = np.mean(sorted_s[k: n - k]) if n > 2 * k else np.mean(sorted_s)
    lower = sorted_s[k]
    upper = sorted_s[n - k - 1] if n > k else sorted_s[-1]
    winsor = np.clip(sorted_s, lower, upper)
    sigma = np.std(winsor, ddof=1) if n > 1 else 0.0
    return max(trimmed_mean + 5 * sigma, 10.0)


def _bobby_build_pv_curves(bids, asks, C_T):
    bids_c = bids.copy()
    asks_c = asks.copy()
    bids_c[:, 1] = np.minimum(bids_c[:, 1], C_T)
    asks_c[:, 1] = np.minimum(asks_c[:, 1], C_T)
    ask_prices, ask_sizes = asks_c[:, 0], asks_c[:, 1]
    bid_prices, bid_sizes = bids_c[:, 0], bids_c[:, 1]
    ask_cum = np.cumsum(ask_sizes)
    bid_cum = np.cumsum(bid_sizes)

    def askPV(v):
        if v <= 0:
            return ask_prices[0]
        idx = np.searchsorted(ask_cum, v, side="right")
        return ask_prices[idx] if idx < len(ask_prices) else ask_prices[-1]

    def bidPV(v):
        if v <= 0:
            return bid_prices[0]
        idx = np.searchsorted(bid_cum, v, side="right")
        return bid_prices[idx] if idx < len(bid_prices) else bid_prices[-1]

    return askPV, bidPV


def _bobby_calculate_brti(books_dict):
    """
    CF-aligned BRTI replica:
      Price = arithmetic mean of per-exchange (best_bid + best_ask) / 2
      across all constituent exchanges with fresh, valid data.
    v_T and C_T are still derived from the aggregated order book and
    kept as auxiliary depth metrics for the ensemble feature set.
    """
    # ── Step 1: CF price — per-exchange best-mid average ─────────────────────
    now = time.time()
    mids = []
    for book in books_dict.values():
        if now - book.get("timestamp", 0) > 30:
            continue
        b, a = book["bids"], book["asks"]
        if len(b) == 0 or len(a) == 0:
            continue
        best_bid = float(b[0, 0])
        best_ask = float(a[0, 0])
        if best_bid > 0 and best_ask > best_bid:
            mids.append((best_bid + best_ask) / 2.0)
    n_ex = len(mids)
    if n_ex < _BOBBY_MIN_EXCHANGES:
        return None, None, None, n_ex, np.array([]), np.array([])
    brti_value = round(float(np.mean(mids)), 2)

    # ── Step 2: aggregate book for v_T / C_T (ensemble depth features) ───────
    uncapped_bids, uncapped_asks, _ = _bobby_aggregate_order_book(books_dict)
    if len(uncapped_bids) == 0 or len(uncapped_asks) == 0:
        return brti_value, None, None, n_ex, uncapped_bids, uncapped_asks
    C_T = _bobby_calculate_dynamic_cap(uncapped_bids, uncapped_asks)
    askPV, bidPV = _bobby_build_pv_curves(uncapped_bids, uncapped_asks, C_T)

    def midSV(v):
        ask_p, bid_p = askPV(v), bidPV(v)
        m = (ask_p + bid_p) / 2
        return (ask_p - m) / m if m > 0 else 1.0

    v = _BOBBY_SPACING
    v_T = _BOBBY_SPACING
    while v < _BOBBY_MAX_V:
        if midSV(v) > _BOBBY_D:
            break
        v_T = v
        v += _BOBBY_SPACING
    return brti_value, round(v_T, 1), round(C_T, 2), n_ex, uncapped_bids, uncapped_asks


_BOBBY_OB_LIMITS = {}  # no per-exchange depth limits needed for CF constituents

async def _bobby_watch_order_book(exchange, symbol, state_ref, book_event):
    ex_id = exchange.id
    live_books = state_ref["live_books"]
    books_lock = state_ref["books_lock"]
    _first_update = True
    _limit = _BOBBY_OB_LIMITS.get(ex_id, 500)
    while True:
        try:
            ob = await exchange.watch_order_book(symbol, limit=_limit)
            bids_arr = np.array(ob["bids"] or [], dtype=float)
            asks_arr = np.array(ob["asks"] or [], dtype=float)
            ts = time.time()
            with books_lock:
                live_books[ex_id] = {"bids": bids_arr, "asks": asks_arr, "timestamp": ts}
            book_event.set()
            if _first_update:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    _f.write(f"[{datetime.now(timezone.utc).isoformat()}] {ex_id} connected — {len(bids_arr)} bids, {len(asks_arr)} asks\n")
                _first_update = False
        except asyncio.CancelledError:
            raise
        except Exception as e:
            with open("/tmp/bobby_debug.log", "a") as _f:
                _f.write(f"[{datetime.now(timezone.utc).isoformat()}] {ex_id} error: {e}\n")
            with books_lock:
                live_books.pop(ex_id, None)
            await asyncio.sleep(5)


_BOBBY_DEBOUNCE_MS = 50

async def _bobby_async_main(state):
    from ccxt.pro import bitstamp, coinbase, kraken, gemini
    exchange_classes = [bitstamp, coinbase, kraken, gemini]
    exchanges = [cls({"enableRateLimit": True}) for cls in exchange_classes]
    books_lock = state["books_lock"]
    live_books = state["live_books"]
    state["status"][0] = "connecting"
    loop = asyncio.get_event_loop()

    _orig_handler = loop.get_exception_handler()

    def _quiet_ccxt_handler(loop, context):
        msg = context.get("message", "")
        exc = context.get("exception")
        if exc and "ccxt" in type(exc).__module__:
            return
        if "Client.receive_loop" in msg:
            return
        if _orig_handler:
            _orig_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(_quiet_ccxt_handler)

    book_event = asyncio.Event()

    watcher_tasks = [
        asyncio.create_task(_bobby_watch_order_book(ex, _BOBBY_SYMBOL, state, book_event))
        for ex in exchanges
    ]

    try:
        while not state["stop_flag"][0]:
            try:
                await asyncio.wait_for(book_event.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            book_event.clear()
            await asyncio.sleep(_BOBBY_DEBOUNCE_MS / 1000.0)
            if book_event.is_set():
                book_event.clear()

            ts = datetime.now(timezone.utc)

            try:
                with books_lock:
                    current_books = {k: v for k, v in live_books.items()}
                brti_value, v_T, C_T, n_ex, agg_bids, agg_asks = _bobby_calculate_brti(current_books)
            except Exception as calc_err:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    import traceback
                    _f.write(f"[{datetime.now(timezone.utc).isoformat()}] calc error: {calc_err}\n{traceback.format_exc()}\n")
                continue
            state["n_exchanges"][0] = n_ex

            if brti_value is not None:
                state["status"][0] = "live"
                state["last_price"][0] = brti_value
                state["last_ts"][0] = ts
                state["error"][0] = None
                state["cached_bids"][0] = agg_bids
                state["cached_asks"][0] = agg_asks
                state["cached_v_T"][0] = v_T
                state["cached_C_T"][0] = C_T
                state["cached_n_ex"][0] = n_ex
                tick = {"ts": ts, "price": float(brti_value), "v_t": float(v_T) if v_T is not None else None, "c_t": float(C_T) if C_T is not None else None, "n_exchanges": int(n_ex)}
                with state["lock"]:
                    state["deque"].append(tick)
                with state["flush_lock"]:
                    state["flush_buf"].append(tick)
                    state["flush_counter"][0] += 1
                    fc = state["flush_counter"][0]
                    if fc in (1, 10, 30, 60) or fc % 60 == 0:
                        with open("/tmp/bobby_debug.log", "a") as _f:
                            _f.write(f"[{datetime.now(timezone.utc).isoformat()}] tick #{fc} price={brti_value:.2f} n_ex={n_ex}\n")
                    if state["flush_counter"][0] >= 60:
                        to_flush = list(state["flush_buf"])
                        state["flush_buf"].clear()
                        state["flush_counter"][0] = 0
                        threading.Thread(
                            target=db_save_bobby_brti, args=(to_flush,), daemon=True
                        ).start()

    except asyncio.CancelledError:
        with open("/tmp/bobby_debug.log", "a") as _f:
            _f.write(f"[{datetime.now(timezone.utc).isoformat()}] async_main CancelledError\n")
    except Exception as e:
        state["error"][0] = str(e)
        state["status"][0] = "error"
        with open("/tmp/bobby_debug.log", "a") as _f:
            import traceback
            _f.write(f"[{datetime.now(timezone.utc).isoformat()}] async_main error: {e}\n{traceback.format_exc()}\n")
    finally:
        for task in watcher_tasks:
            task.cancel()
        await asyncio.gather(*watcher_tasks, return_exceptions=True)
        for ex in exchanges:
            try:
                await ex.close()
            except Exception:
                pass


def _bobby_thread_target():
    state = _bobby_brti_state()
    with open("/tmp/bobby_debug.log", "a") as _f:
        _f.write(f"[{datetime.now(timezone.utc).isoformat()}] Bobby thread starting\n")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_bobby_async_main(state))
    except Exception as e:
        state["error"][0] = str(e)
        state["status"][0] = "error"
        with open("/tmp/bobby_debug.log", "a") as _f:
            import traceback
            _f.write(f"[{datetime.now(timezone.utc).isoformat()}] Bobby thread fatal: {e}\n{traceback.format_exc()}\n")
    finally:
        loop.close()


def start_bobby_brti():
    state = _bobby_brti_state()
    t = state["thread"][0]
    if t is not None and t.is_alive():
        return
    state["stop_flag"][0] = False
    state["status"][0] = "starting"
    t = threading.Thread(target=_bobby_thread_target, daemon=True)
    t.start()
    state["thread"][0] = t


def stop_bobby_brti():
    state = _bobby_brti_state()
    state["stop_flag"][0] = True
    state["status"][0] = "off"
    t = state["thread"][0]
    if t is not None:
        t.join(timeout=5)
    state["thread"][0] = None


def bobby_brti_is_running() -> bool:
    state = _bobby_brti_state()
    t = state["thread"][0]
    return t is not None and t.is_alive()


def get_bobby_brti_ticks() -> list:
    state = _bobby_brti_state()
    with state["lock"]:
        return list(state["deque"])


def get_bobby_brti_latest() -> dict:
    state = _bobby_brti_state()
    return {
        "price": state["last_price"][0],
        "ts": state["last_ts"][0],
        "status": state["status"][0],
        "n_exchanges": state["n_exchanges"][0],
        "error": state["error"][0],
    }


_ENSEMBLE_MAX_LEVELS = 500
_ENSEMBLE_SNAPSHOT_INTERVAL = 30
_CNN_SEQ_LEN = 10          # temporal frames fed to CNN-LSTM (10 × ~1s = ~10s window)
_TRAIN_HORIZON_SECS = 10
_CNN_TRAIN_HORIZON_SECS = 600   # CNN-LSTM trains on 10-minute forward label (matches empirical edge horizon)
_TRAIN_NEUTRAL_THRESHOLD = 0.0005  # 5bps — filters bid-ask noise for 10s/15s/60s XGBoost windows (~10% directional)
_CNN_NEUTRAL_THRESHOLD  = 0.002   # 20bps — minimum move meaningful for 15-min contract economics (CNN-LSTM 10-min only)
_CNN_CONFIDENCE_THRESHOLD = 0.45
_TRAIN_MIN_SAMPLES = 50
_TRAIN_XGB_INTERVAL = 120
_TRAIN_CNN_INTERVAL = 180
_TRAIN_CNN_LR = 1e-4
_TRAIN_MAGNITUDE_INTERVAL = 300  # retrain magnitude regressor every 5 min

# Multi-timeframe XGBoost horizons (seconds ahead to label)
_MTF_HORIZON_15S = 15
_MTF_HORIZON_60S = 60
_TRAIN_MTF_INTERVAL = 180   # retrain MTF models every 3 min


def _create_raw_book_image(bids, asks):
    import torch
    bid_vol = np.zeros(_ENSEMBLE_MAX_LEVELS)
    ask_vol = np.zeros(_ENSEMBLE_MAX_LEVELS)
    if len(bids) > 0:
        bid_vol[:min(_ENSEMBLE_MAX_LEVELS, len(bids))] = bids[:_ENSEMBLE_MAX_LEVELS, 1]
    if len(asks) > 0:
        ask_vol[:min(_ENSEMBLE_MAX_LEVELS, len(asks))] = asks[:_ENSEMBLE_MAX_LEVELS, 1]
    image = np.stack([np.log1p(bid_vol), np.log1p(ask_vol)], axis=1)
    image = image.reshape(1, 1, _ENSEMBLE_MAX_LEVELS, 2).astype(np.float32)
    return torch.from_numpy(image)


@st.cache_resource
def _training_state():
    return {
        "pending": collections.deque(maxlen=30000),
        "labeled_tabular": collections.deque(maxlen=500000),
        "labeled_images": collections.deque(maxlen=10000),
        "lock": threading.Lock(),
        "xgb_train_count": [0],
        "cnn_train_count": [0],
        "xgb_accuracy": [None],
        "cnn_loss": [None],
        "last_xgb_train": [None],
        "last_cnn_train": [None],
        "total_samples": [0],
        # Multi-timeframe XGBoost buffers
        "pending_15s": collections.deque(maxlen=30000),
        "pending_60s": collections.deque(maxlen=30000),
        "labeled_tabular_15s": collections.deque(maxlen=500000),
        "labeled_tabular_60s": collections.deque(maxlen=500000),
        "mtf_lock": threading.Lock(),
        "xgb_15s_train_count": [0],
        "xgb_60s_train_count": [0],
        "xgb_15s_accuracy": [None],
        "xgb_60s_accuracy": [None],
        "last_xgb_15s_train": [None],
        "last_xgb_60s_train": [None],
        # CNN-LSTM 10-minute horizon buffers + training stats
        "pending_cnn_10m": collections.deque(maxlen=30000),
        "labeled_images_10m": collections.deque(maxlen=10000),
        "cnn_10m_train_count": [0],
        "cnn_10m_loss": [None],
        "last_cnn_10m_train": [None],
        # Magnitude regression (continuous 10-min return prediction)
        "labeled_magnitude_10m": collections.deque(maxlen=500000),
        "magnitude_train_count": [0],
        "magnitude_accuracy": [None],   # stored as MAE (% return)
        "last_magnitude_train": [None],
    }


def _label_from_returns(price_before, price_after):
    ret = (price_after - price_before) / price_before if price_before > 0 else 0.0
    if ret > _TRAIN_NEUTRAL_THRESHOLD:
        return 2
    elif ret < -_TRAIN_NEUTRAL_THRESHOLD:
        return 0
    return 1


def _seed_training_from_db():
    """Load labeled training samples into memory on startup.

    Fast path (seconds): reads directly from training_samples + labeled book_image_snapshots
    when pre-labeled rows are available (i.e. after the first session that generated labels).

    Slow path (minutes): reconstructs labels from raw bobby_brti_ticks + ensemble_predictions.
    Only used the very first time, before training_samples is populated.
    """
    ts = _training_state()
    with ts["lock"]:
        if ts["total_samples"][0] > 0:
            return
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        # ── Fast path: load pre-labeled rows directly ───────────────────────
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM training_samples")
            n_cached = cur.fetchone()[0]

        if n_cached >= 100:
            seeded = 0
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT label, v_t, c_t, exchanges, hawkes, brti_return,
                              bid_ask_spread, bid_depth_10, ask_depth_10, imbalance,
                              brti_ret_5, brti_ret_10, brti_ret_30, vt_velocity,
                              microprice, spread_pct,
                              bid1_vol, ask1_vol, bid5_vol, ask5_vol, bid20_vol, ask20_vol,
                              depth_ratio_1, depth_ratio_5,
                              vol_30, vol_60, rsi_7, rsi_14, rsi_21,
                              vwap_dev, imbalance_velocity
                       FROM training_samples
                       ORDER BY id ASC"""
                )
                for row in cur.fetchall():
                    tab_row = {
                        "label": int(row[0]),
                        "v_T": row[1] or 0.0,
                        "C_T": row[2] or 0.0,
                        "exchanges": row[3] or 0,
                        "hawkes": row[4] or 0.0,
                        "brti_return": row[5] or 0.0,
                        "bid_ask_spread": row[6] or 0.0,
                        "bid_depth_10": row[7] or 0.0,
                        "ask_depth_10": row[8] or 0.0,
                        "imbalance": row[9] or 0.0,
                        "brti_ret_5": row[10] or 0.0,
                        "brti_ret_10": row[11] or 0.0,
                        "brti_ret_30": row[12] or 0.0,
                        "vt_velocity": row[13] or 0.0,
                        "microprice": row[14] or 0.0,
                        "spread_pct": row[15] or 0.0,
                        "bid1_vol": row[16] or 0.0,
                        "ask1_vol": row[17] or 0.0,
                        "bid5_vol": row[18] or 0.0,
                        "ask5_vol": row[19] or 0.0,
                        "bid20_vol": row[20] or 0.0,
                        "ask20_vol": row[21] or 0.0,
                        "depth_ratio_1": row[22] or 0.0,
                        "depth_ratio_5": row[23] or 0.0,
                        "vol_30": row[24] or 0.0,
                        "vol_60": row[25] or 0.0,
                        "rsi_7": row[26] or 0.0,
                        "rsi_14": row[27] or 0.0,
                        "rsi_21": row[28] or 0.0,
                        "vwap_dev": row[29] or 0.0,
                        "imbalance_velocity": row[30] or 0.0,
                    }
                    with ts["lock"]:
                        ts["labeled_tabular"].append(tab_row)
                        ts["total_samples"][0] += 1
                    seeded += 1

            img_seeded = 0
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT image_bytes, label, EXTRACT(EPOCH FROM ts)::double precision
                           FROM book_image_snapshots
                           WHERE label IS NOT NULL
                           ORDER BY ts ASC LIMIT 10000"""
                    )
                    for img_bytes, lbl, img_ts_f in cur.fetchall():
                        frame_np = np.frombuffer(bytes(img_bytes), dtype=np.float32).reshape(500, 2)
                        with ts["lock"]:
                            ts["labeled_images"].append({
                                "image": frame_np,
                                "label": int(lbl),
                                "ts": float(img_ts_f),
                            })
                        img_seeded += 1
            except Exception:
                pass

            try:
                with open("/tmp/bobby_debug.log", "a") as f:
                    f.write(
                        f"[{datetime.now(timezone.utc).isoformat()}] "
                        f"[FAST SEED] loaded {seeded} tabular + {img_seeded} image samples from training_samples cache\n"
                    )
            except Exception:
                pass
            return  # fast path done — skip slow reconstruction below

        # ── Slow path: reconstruct labels from raw tick data ─────────────────
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ts, price, v_t, c_t, n_exchanges FROM bobby_brti_ticks ORDER BY ts ASC"
            )
            bobby_rows = cur.fetchall()
        if len(bobby_rows) < 100:
            return

        ep_features = {}
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT ts, v_t, c_t, hawkes, n_exchanges, brti_return FROM ensemble_predictions ORDER BY ts ASC"
                )
                ep_rows = cur.fetchall()
            for row in ep_rows:
                ep_ts = row[0]
                if hasattr(ep_ts, 'timestamp'):
                    ep_ts = ep_ts.timestamp()
                ep_features[int(ep_ts)] = {
                    "hawkes": float(row[3]) if row[3] is not None else 0.0,
                    "brti_return": float(row[5]) if row[5] is not None else 0.0,
                }
        except Exception:
            pass

        prices = []
        for row in bobby_rows:
            t = row[0]
            if hasattr(t, 'timestamp'):
                t = t.timestamp()
            prices.append({
                "ts": float(t),
                "price": float(row[1]),
                "v_t": float(row[2]) if row[2] is not None else 0.0,
                "c_t": float(row[3]) if row[3] is not None else 0.0,
                "n_ex": int(row[4]) if row[4] is not None else 0,
            })

        seeded = 0
        slow_tab_batch = []
        for i in range(0, len(prices) - 1):
            p = prices[i]
            target_ts = p["ts"] + _TRAIN_HORIZON_SECS
            best_j = None
            best_dist = float("inf")
            for j in range(i + 1, min(i + 200, len(prices))):
                dist = abs(prices[j]["ts"] - target_ts)
                if dist < best_dist:
                    best_dist = dist
                    best_j = j
                if prices[j]["ts"] > target_ts + 5:
                    break
            if best_j is None or best_dist > 5.0:
                continue
            label = _label_from_returns(p["price"], prices[best_j]["price"])
            prev_price = prices[max(0, i - 1)]["price"]
            brti_return = (p["price"] - prev_price) / prev_price if prev_price > 0 else 0.0
            hawkes = 0.0
            ep_key = int(p["ts"])
            if ep_key in ep_features:
                hawkes = ep_features[ep_key].get("hawkes", 0.0)
                brti_return = ep_features[ep_key].get("brti_return", brti_return)
            features = {
                "v_T": p["v_t"], "C_T": p["c_t"], "exchanges": p["n_ex"],
                "hawkes": hawkes, "brti_return": brti_return,
                "bid_ask_spread": 0.0, "bid_depth_10": 0.0,
                "ask_depth_10": 0.0, "imbalance": 0.0,
            }
            tab_row = dict(features)
            tab_row["label"] = label
            with ts["lock"]:
                ts["labeled_tabular"].append(tab_row)
                ts["total_samples"][0] += 1
            slow_tab_batch.append(tab_row)
            seeded += 1

        # Persist the slow-path results so next restart uses the fast path
        if slow_tab_batch:
            threading.Thread(
                target=_db_persist_labeled_batch,
                args=(slow_tab_batch, []),
                daemon=True, name="slow-seed-persist",
            ).start()

        img_seeded = 0
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT ts, price, image_bytes FROM book_image_snapshots ORDER BY ts DESC LIMIT 10000"
                )
                img_rows = cur.fetchall()[::-1]

            price_ts_list = [(p["ts"], p["price"]) for p in prices]
            img_updates = []
            for img_ts_val, img_price, img_bytes in img_rows:
                img_ts = img_ts_val
                if hasattr(img_ts, 'timestamp'):
                    img_ts = img_ts.timestamp()
                img_ts = float(img_ts)
                target_ts = img_ts + _TRAIN_HORIZON_SECS
                best_price = None
                best_dist = float("inf")
                lo, hi = 0, len(price_ts_list) - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if price_ts_list[mid][0] < target_ts:
                        lo = mid + 1
                    else:
                        hi = mid - 1
                for idx in range(max(0, lo - 3), min(len(price_ts_list), lo + 3)):
                    d = abs(price_ts_list[idx][0] - target_ts)
                    if d < best_dist:
                        best_dist = d
                        best_price = price_ts_list[idx][1]
                if best_price is None or best_dist > 5.0:
                    continue
                label = _label_from_returns(float(img_price), best_price)
                frame_np = np.frombuffer(bytes(img_bytes), dtype=np.float32).reshape(500, 2)
                with ts["lock"]:
                    ts["labeled_images"].append({"image": frame_np, "label": label, "ts": float(img_ts)})
                img_updates.append((img_ts, label))
                img_seeded += 1

            if img_updates:
                threading.Thread(
                    target=_db_persist_labeled_batch,
                    args=([], img_updates),
                    daemon=True, name="slow-img-persist",
                ).start()
        except Exception:
            pass

        try:
            with open("/tmp/bobby_debug.log", "a") as f:
                f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] "
                    f"[SLOW SEED] seeded {seeded} tabular + {img_seeded} image training samples from DB\n"
                )
        except Exception:
            pass
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


def _seed_cnn_10m_from_db():
    """Seed labeled_images_10m by cross-referencing book_image_snapshots against
    brti_ticks to compute 10-minute forward-price labels.

    Runs once on startup. Lets the 10m CNN-LSTM begin training immediately using
    historical order-book snapshots rather than waiting ~10 hours for live labels.
    """
    ts = _training_state()
    with ts["lock"]:
        already = len(ts["labeled_images_10m"])
    if already >= 500:
        return   # already seeded (e.g. from a previous call this session)
    if not DATABASE_URL:
        return
    conn = _db_conn()
    if not conn:
        return
    try:
        # For each snapshot, find the nearest brti_tick between 9m30s and 10m30s later.
        # Use a LATERAL join for efficiency — one pass, no Python loop against the DB.
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    s.image_bytes,
                    EXTRACT(EPOCH FROM s.ts)::double precision AS snap_ts,
                    s.price                                      AS price_before,
                    b.price                                      AS price_after
                FROM book_image_snapshots s
                JOIN LATERAL (
                    SELECT price
                    FROM brti_ticks
                    WHERE ts BETWEEN s.ts + INTERVAL '9 minutes 30 seconds'
                                 AND s.ts + INTERVAL '10 minutes 30 seconds'
                    ORDER BY ABS(EXTRACT(EPOCH FROM (ts - (s.ts + INTERVAL '10 minutes'))))
                    LIMIT 1
                ) b ON true
                ORDER BY s.ts ASC
                LIMIT 10000
                """
            )
            rows = cur.fetchall()

        threshold = _CNN_NEUTRAL_THRESHOLD  # 20bps — correct scale for 10-minute contract moves

        loaded = 0
        for img_bytes, snap_ts_f, price_before, price_after in rows:
            if price_before is None or price_after is None or float(price_before) <= 0:
                continue
            ret = (float(price_after) - float(price_before)) / float(price_before)
            if ret > threshold:
                label = 2   # UP
            elif ret < -threshold:
                label = 0   # DOWN
            else:
                label = 1   # NEUTRAL
            frame_np = np.frombuffer(bytes(img_bytes), dtype=np.float32).reshape(500, 2)
            with ts["lock"]:
                ts["labeled_images_10m"].append({
                    "image": frame_np,
                    "label": label,
                    "ts": float(snap_ts_f),
                })
            loaded += 1

        try:
            with open("/tmp/bobby_debug.log", "a") as f:
                f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] "
                    f"[10M SEED] loaded {loaded} labeled images into labeled_images_10m\n"
                )
        except Exception:
            pass
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


@st.cache_resource
def _book_image_save_state():
    return {"last_save": [0.0]}


def _collect_training_sample(features_dict, book_image_np, brti_price):
    ts = _training_state()
    now = time.time()
    sample = {
        "ts": now,
        "features": features_dict,
        "book_image": book_image_np,
        "price_at_capture": brti_price,
        "label": None,
    }
    with ts["lock"]:
        ts["pending"].append(sample)
        # Queue for CNN-LSTM 10-min horizon (needs book image + features + price)
        if book_image_np is not None:
            ts["pending_cnn_10m"].append({
                "ts": now,
                "book_image": book_image_np,
                "features": features_dict,
                "price_at_capture": float(brti_price),
            })
    # Also queue for multi-timeframe label resolution
    mtf_sample = {
        "ts": now,
        "features": features_dict,
        "price_at_capture": float(brti_price),
    }
    with ts["mtf_lock"]:
        ts["pending_15s"].append(dict(mtf_sample))
        ts["pending_60s"].append(dict(mtf_sample))
    if book_image_np is not None:
        save_st = _book_image_save_state()
        if now - save_st["last_save"][0] >= _ENSEMBLE_SNAPSHOT_INTERVAL:
            save_st["last_save"][0] = now
            threading.Thread(
                target=db_save_book_image_snapshot,
                args=(now, float(brti_price), book_image_np),
                daemon=True,
            ).start()


_resolve_call_count = [0]


def _resolve_pending_labels():
    ts = _training_state()
    now = time.time()
    bobby_ticks = get_bobby_brti_ticks()
    _resolve_call_count[0] += 1
    if not bobby_ticks:
        if _resolve_call_count[0] % 60 == 1:
            try:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    _f.write(
                        f"[{datetime.now(timezone.utc).isoformat()}] "
                        f"[RESOLVE] no bobby_ticks, pending={len(ts['pending'])}\n"
                    )
            except Exception:
                pass
        return
    latest_price = bobby_ticks[-1]["price"]
    latest_ts = bobby_ticks[-1]["ts"].timestamp() if hasattr(bobby_ticks[-1]["ts"], "timestamp") else bobby_ticks[-1]["ts"]

    tick_ts_list = []
    for t in bobby_ticks:
        t_ts = t["ts"].timestamp() if hasattr(t["ts"], "timestamp") else t["ts"]
        tick_ts_list.append((float(t_ts), t["price"]))

    import bisect
    tick_times = [x[0] for x in tick_ts_list]

    resolved = []
    still_pending = []
    with ts["lock"]:
        for s in ts["pending"]:
            age = now - s["ts"]
            if age >= _TRAIN_HORIZON_SECS:
                target_ts = s["ts"] + _TRAIN_HORIZON_SECS
                idx = bisect.bisect_left(tick_times, target_ts)
                best_dist = float("inf")
                future_price = None
                for j in range(max(0, idx - 1), min(len(tick_ts_list), idx + 2)):
                    d = abs(tick_ts_list[j][0] - target_ts)
                    if d < best_dist:
                        best_dist = d
                        future_price = tick_ts_list[j][1]
                if future_price is not None and best_dist < 5.0:
                    label = _label_from_returns(s["price_at_capture"], future_price)
                    s["label"] = label
                    resolved.append(s)
                elif age > _TRAIN_HORIZON_SECS + 15:
                    pass
                else:
                    still_pending.append(s)
            else:
                still_pending.append(s)
        ts["pending"].clear()
        ts["pending"].extend(still_pending)

    # Periodic diagnostic (every 60 calls ≈ every 60s)
    if _resolve_call_count[0] % 60 == 0:
        try:
            with open("/tmp/bobby_debug.log", "a") as _f:
                _f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] "
                    f"[RESOLVE] ticks={len(bobby_ticks)} pending={len(still_pending)} "
                    f"resolved={len(resolved)} total={ts.get('total_samples', [0])[0]}\n"
                )
        except Exception:
            pass

    tab_to_persist = []
    img_to_persist = []
    for s in resolved:
        tab_row = dict(s["features"])
        tab_row["label"] = s["label"]
        tab_row["_sample_ts"] = s["ts"]
        with ts["lock"]:
            ts["labeled_tabular"].append(tab_row)
            if s["book_image"] is not None:
                # Store single frame as (500, 2) + timestamp for sequence building
                raw_img = s["book_image"]  # currently (1, 1, 500, 2) numpy
                frame_np = raw_img.reshape(500, 2) if hasattr(raw_img, "reshape") else np.array(raw_img).reshape(500, 2)
                ts["labeled_images"].append({
                    "image": frame_np,
                    "label": s["label"],
                    "ts": s["ts"],
                })
            ts["total_samples"][0] += 1
        tab_to_persist.append(tab_row)
        if s["book_image"] is not None:
            img_to_persist.append((s["ts"], s["label"]))

    if tab_to_persist or img_to_persist:
        threading.Thread(
            target=_db_persist_labeled_batch,
            args=(tab_to_persist, img_to_persist),
            daemon=True, name="persist-labels",
        ).start()


_EXCLUDED_FEATURE_COLS = {"label", "_sample_ts"}


def _resolve_mtf_labels():
    """Resolve 15s and 60s pending samples against future BRTI ticks."""
    import bisect
    ts = _training_state()
    now = time.time()
    bobby_ticks = get_bobby_brti_ticks()
    if not bobby_ticks:
        return

    tick_ts_list = []
    for t in bobby_ticks:
        t_ts = t["ts"].timestamp() if hasattr(t["ts"], "timestamp") else float(t["ts"])
        tick_ts_list.append((t_ts, t["price"]))
    tick_times = [x[0] for x in tick_ts_list]

    def _resolve_deque(pending_key, labeled_key, horizon, count_key, stats_fn):
        resolved = []
        still_pending = []
        with ts["mtf_lock"]:
            for s in ts[pending_key]:
                age = now - s["ts"]
                if age >= horizon:
                    target_ts = s["ts"] + horizon
                    idx = bisect.bisect_left(tick_times, target_ts)
                    best_dist = float("inf")
                    future_price = None
                    for j in range(max(0, idx - 1), min(len(tick_ts_list), idx + 2)):
                        d = abs(tick_ts_list[j][0] - target_ts)
                        if d < best_dist:
                            best_dist = d
                            future_price = tick_ts_list[j][1]
                    if future_price is not None and best_dist < horizon * 0.5:
                        label = _label_from_returns(s["price_at_capture"], future_price)
                        tab_row = dict(s["features"])
                        tab_row["label"] = label
                        tab_row["_sample_ts"] = s["ts"]
                        ts[labeled_key].append(tab_row)
                        resolved.append((s, label))
                    elif age > horizon + 30:
                        pass   # too old, drop
                    else:
                        still_pending.append(s)
                else:
                    still_pending.append(s)
            ts[pending_key].clear()
            ts[pending_key].extend(still_pending)
        return resolved

    _resolve_deque("pending_15s", "labeled_tabular_15s", _MTF_HORIZON_15S, None, None)
    _resolve_deque("pending_60s", "labeled_tabular_60s", _MTF_HORIZON_60S, None, None)


def _resolve_cnn_10m_labels():
    """Resolve CNN-LSTM 10-minute pending samples.
    Populates labeled_images_10m (for CNN direction training) and
    labeled_magnitude_10m (for the XGBoost magnitude regressor).
    """
    import bisect
    ts = _training_state()
    now = time.time()
    bobby_ticks = get_bobby_brti_ticks()
    if not bobby_ticks:
        return

    tick_ts_list = []
    for t in bobby_ticks:
        t_ts = t["ts"].timestamp() if hasattr(t["ts"], "timestamp") else float(t["ts"])
        tick_ts_list.append((t_ts, t["price"]))
    tick_times = [x[0] for x in tick_ts_list]

    resolved_img = []
    resolved_mag = []
    still_pending = []

    with ts["lock"]:
        for s in ts["pending_cnn_10m"]:
            age = now - s["ts"]
            if age >= _CNN_TRAIN_HORIZON_SECS:
                target_ts = s["ts"] + _CNN_TRAIN_HORIZON_SECS
                idx = bisect.bisect_left(tick_times, target_ts)
                best_dist = float("inf")
                future_price = None
                for j in range(max(0, idx - 2), min(len(tick_ts_list), idx + 3)):
                    d = abs(tick_ts_list[j][0] - target_ts)
                    if d < best_dist:
                        best_dist = d
                        future_price = tick_ts_list[j][1]
                if future_price is not None and best_dist < 30.0:
                    p_now = s["price_at_capture"]
                    ret_10m = (future_price - p_now) / p_now if p_now > 0 else 0.0
                    # Use CNN-specific 20bps threshold — 10-minute moves need meaningful magnitude
                    label = 2 if ret_10m > _CNN_NEUTRAL_THRESHOLD else (0 if ret_10m < -_CNN_NEUTRAL_THRESHOLD else 1)
                    # Image entry for CNN-LSTM direction training
                    raw_img = s["book_image"]
                    frame_np = raw_img.reshape(500, 2) if hasattr(raw_img, "reshape") else np.array(raw_img).reshape(500, 2)
                    resolved_img.append({"image": frame_np, "label": label, "ts": s["ts"]})
                    # Tabular entry for magnitude regression (any direction useful)
                    tab_row = dict(s.get("features", {}))
                    tab_row["ret_10m"] = float(ret_10m)
                    tab_row["_sample_ts"] = s["ts"]
                    resolved_mag.append(tab_row)
                elif age > _CNN_TRAIN_HORIZON_SECS + 60:
                    pass   # too stale to match, drop
                else:
                    still_pending.append(s)
            else:
                still_pending.append(s)
        ts["pending_cnn_10m"].clear()
        ts["pending_cnn_10m"].extend(still_pending)
        ts["labeled_images_10m"].extend(resolved_img)
        ts["labeled_magnitude_10m"].extend(resolved_mag)


def _train_xgboost_magnitude():
    """Train XGBRegressor to predict continuous 10-minute return magnitude.
    Output is a signed percentage return — positive = expected UP, negative = expected DOWN.
    MAE (in basis-points) is tracked as the accuracy proxy.
    """
    import xgboost as xgb
    import joblib

    ts = _training_state()
    with ts["lock"]:
        mag_data = list(ts["labeled_magnitude_10m"])
    if len(mag_data) < _TRAIN_MIN_SAMPLES:
        return

    df = pd.DataFrame(mag_data)
    feature_cols = [c for c in df.columns if c not in {"ret_10m", "_sample_ts"}]
    if not feature_cols:
        return
    X = df[feature_cols].values.astype(np.float32)
    y = df["ret_10m"].values.astype(np.float32)

    model = xgb.XGBRegressor(
        n_estimators=150, max_depth=5, learning_rate=0.08,
        subsample=0.8, colsample_bytree=0.8,
        objective="reg:squarederror", verbosity=0, n_jobs=1,
    )
    model.fit(X, y)

    preds = model.predict(X)
    mae_bps = float(np.mean(np.abs(preds - y)) * 10000)   # basis points

    ens = _ensemble_state()
    ens["xgb_magnitude_model"][0] = model
    ens["magnitude_feature_cols"][0] = feature_cols
    try:
        joblib.dump(model, "brti_xgboost_magnitude.pkl")
    except Exception:
        pass

    ts["magnitude_train_count"][0] += 1
    ts["magnitude_accuracy"][0] = mae_bps
    ts["last_magnitude_train"][0] = datetime.now(timezone.utc)


def _train_xgboost_mtf(horizon_key: str, labeled_key: str, count_key: str,
                       acc_key: str, time_key: str, model_key: str, pkl_path: str):
    """Generic MTF XGBoost trainer shared by 15s and 60s models."""
    import xgboost as xgb
    import joblib
    ts = _training_state()
    ens = _ensemble_state()
    _MAX_DIR = 15_000
    with ts["mtf_lock"]:
        all_data = list(ts[labeled_key])
    if len(all_data) < _TRAIN_MIN_SAMPLES:
        return
    down_rows = [r for r in all_data if int(r.get("label", 1)) == 0]
    up_rows   = [r for r in all_data if int(r.get("label", 1)) == 2]
    if not down_rows or not up_rows:
        return
    def _sample(rows, n):
        idx = np.random.choice(len(rows), min(n, len(rows)), replace=False)
        return [rows[i] for i in idx]
    balanced = _sample(down_rows, _MAX_DIR) + _sample(up_rows, _MAX_DIR)
    np.random.shuffle(balanced)
    df = pd.DataFrame(balanced)
    feature_cols = [c for c in df.columns if c not in _EXCLUDED_FEATURE_COLS]
    X = df[feature_cols].values.astype(np.float32)
    y_raw = df["label"].values.astype(int)
    y = np.where(y_raw == 2, 1, 0)
    model = xgb.XGBClassifier(
        n_estimators=150, max_depth=5, learning_rate=0.08,
        subsample=0.8, colsample_bytree=0.8,
        objective="binary:logistic", eval_metric="logloss",
        use_label_encoder=False, verbosity=0, n_jobs=1,
    )
    model.fit(X, y)
    acc = None
    try:
        if len(balanced) >= 200:
            acc = float((model.predict(X) == y).mean())
    except Exception:
        pass
    ens[model_key][0] = model
    try:
        joblib.dump(model, pkl_path)
    except Exception:
        pass
    with ts["mtf_lock"]:
        ts[count_key][0] += 1
        ts[acc_key][0] = acc
        ts[time_key][0] = datetime.now(timezone.utc)


def _train_xgboost_online():
    import xgboost as xgb
    from sklearn.model_selection import TimeSeriesSplit
    import joblib

    ts = _training_state()
    _XGB_MAX_PER_CLASS = 20_000
    with ts["lock"]:
        all_data = list(ts["labeled_tabular"])
    if len(all_data) < _TRAIN_MIN_SAMPLES:
        return

    # 3-class model: DOWN=0, NEUTRAL=1, UP=2
    # Include NEUTRAL so the model learns to output genuine neutral probability
    # instead of always splitting confidence between UP and DOWN (binary inflation bug).
    down_rows    = [r for r in all_data if int(r.get("label", 1)) == 0]
    neutral_rows = [r for r in all_data if int(r.get("label", 1)) == 1]
    up_rows      = [r for r in all_data if int(r.get("label", 1)) == 2]
    if not down_rows or not up_rows:
        return

    def _sample(rows, n):
        # Time-ordered sample: prefer recent rows, cap at n
        return rows[-n:] if len(rows) > n else rows

    # Balance: cap each class, keep time order for walk-forward split
    balanced = (
        _sample(down_rows, _XGB_MAX_PER_CLASS) +
        _sample(neutral_rows, _XGB_MAX_PER_CLASS) +
        _sample(up_rows, _XGB_MAX_PER_CLASS)
    )
    # Sort by sample timestamp so walk-forward split is meaningful
    balanced.sort(key=lambda r: r.get("_sample_ts", 0.0))

    df = pd.DataFrame(balanced)
    feature_cols = [c for c in df.columns if c not in _EXCLUDED_FEATURE_COLS]
    X = df[feature_cols].fillna(0.0).values.astype(np.float32)
    y = df["label"].values.astype(int)   # 0=DOWN, 1=NEUTRAL, 2=UP

    model = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softprob",
        num_class=3,
        eval_metric="mlogloss",
        use_label_encoder=False,
        verbosity=0,
        n_jobs=1,
    )
    model.fit(X, y)

    # Walk-forward validation: train on first 80%, test on last 20%
    # This gives an honest out-of-sample accuracy estimate without leaking future data.
    acc = None
    try:
        n = len(X)
        if n >= 200:
            split = int(n * 0.8)
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]
            wf_model = xgb.XGBClassifier(
                n_estimators=150, max_depth=5, learning_rate=0.08,
                subsample=0.8, colsample_bytree=0.8,
                objective="multi:softprob", num_class=3,
                eval_metric="mlogloss", use_label_encoder=False,
                verbosity=0, n_jobs=1,
            )
            wf_model.fit(X_train, y_train)
            acc = float((wf_model.predict(X_test) == y_test).mean())
    except Exception:
        pass

    ens = _ensemble_state()
    ens["xgb_model"][0] = model

    try:
        joblib.dump(model, "brti_xgboost.pkl")
    except Exception:
        pass

    with ts["lock"]:
        ts["xgb_train_count"][0] += 1
        ts["xgb_accuracy"][0] = acc
        ts["last_xgb_train"][0] = datetime.now(timezone.utc)


_TRAIN_CNN_WINDOW = 8192
_TRAIN_CNN_10M_WINDOW = 4000     # use full 48h snapshot history for 10-min model
_TRAIN_CNN_BATCH = 32


def _train_cnn_lstm_online():
    """Train the 10-second CNN-LSTM on the fast-seed / tick-level label pool."""
    import torch
    import torch.nn as nn

    ts = _training_state()
    with ts["lock"]:
        all_data = list(ts["labeled_images"])   # 10-second label pool only
    if len(all_data) < _TRAIN_MIN_SAMPLES + _CNN_SEQ_LEN:
        return

    ens = _ensemble_state()
    model = ens["deep_model"][0]
    optimizer = ens["deep_optimizer"][0]
    device = ens["device"][0]
    if model is None or device is None:
        return

    if optimizer is None:
        optimizer = torch.optim.Adam(model.parameters(), lr=_TRAIN_CNN_LR)
        ens["deep_optimizer"][0] = optimizer

    # Sort by timestamp so sliding windows are temporally consistent
    all_data.sort(key=lambda d: d.get("ts", 0.0))
    # Keep only recent _TRAIN_CNN_WINDOW frames before windowing
    data = all_data[-(_TRAIN_CNN_WINDOW + _CNN_SEQ_LEN):]

    # ── Build sliding-window sequences ────────────────────────────────────
    # Each sequence covers T consecutive frames; label = label of last frame.
    # Skip sequences whose last frame is NEUTRAL (uninformative for trading).
    T = _CNN_SEQ_LEN
    sequences = []   # list of (frames_list, label)
    for end in range(T, len(data) + 1):
        window = data[end - T:end]
        label = window[-1]["label"]
        frames = [np.asarray(w["image"], dtype=np.float32) for w in window]  # T × (500,2)
        sequences.append((frames, label))

    # Directional filter: prefer UP/DOWN sequences; fall back to all if too few
    directional_seqs = [s for s in sequences if s[1] in (0, 2)]
    train_seqs = directional_seqs if len(directional_seqs) >= _TRAIN_MIN_SAMPLES else sequences
    n = len(train_seqs)
    if n < 2:
        return

    model.train()
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    batches = 0

    for _epoch in range(3):
        idx_list = list(range(n))
        np.random.shuffle(idx_list)
        for start in range(0, n, _TRAIN_CNN_BATCH):
            batch_idx = idx_list[start:start + _TRAIN_CNN_BATCH]
            if len(batch_idx) < 2:
                continue

            # Stack frames → (batch, T, 500, 2)
            batch_seqs = []
            batch_labels = []
            for i in batch_idx:
                frames, label = train_seqs[i]
                seq_np = np.stack(frames, axis=0)   # (T, 500, 2)
                batch_seqs.append(seq_np)
                batch_labels.append(label)

            seqs_t = torch.from_numpy(np.stack(batch_seqs, axis=0)).to(device)  # (B, T, 500, 2)
            labels_t = torch.tensor(batch_labels, dtype=torch.long, device=device)

            optimizer.zero_grad()
            outputs = model(seqs_t)
            loss = criterion(outputs, labels_t)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            total_loss += loss.item()
            batches += 1

    model.eval()
    avg_loss = total_loss / max(batches, 1)

    try:
        torch.save(model.state_dict(), "brti_cnn_lstm.pth")
    except Exception:
        pass

    with ts["lock"]:
        ts["cnn_train_count"][0] += 1
        ts["cnn_loss"][0] = avg_loss
        ts["last_cnn_train"][0] = datetime.now(timezone.utc)


def _train_cnn_lstm_10m_online():
    """Train the dedicated 10-minute CNN-LSTM. Only runs once labeled_images_10m is big enough.
    Uses deep_model_10m weights (saved to brti_cnn_lstm_10m.pth). Never touches 10s labels."""
    import torch
    import torch.nn as nn

    ts = _training_state()
    with ts["lock"]:
        all_data = list(ts["labeled_images_10m"])   # 10-minute label pool only
    if len(all_data) < _TRAIN_MIN_SAMPLES + _CNN_SEQ_LEN:
        return

    ens = _ensemble_state()
    model = ens["deep_model_10m"][0]
    optimizer = ens["deep_optimizer_10m"][0]
    device = ens["device"][0]
    if model is None or device is None:
        return

    if optimizer is None:
        import torch as _torch
        optimizer = _torch.optim.Adam(model.parameters(), lr=_TRAIN_CNN_LR)
        ens["deep_optimizer_10m"][0] = optimizer

    all_data.sort(key=lambda d: d.get("ts", 0.0))
    data = all_data[-(_TRAIN_CNN_10M_WINDOW + _CNN_SEQ_LEN):]
    T = _CNN_SEQ_LEN
    sequences = []
    for end in range(T, len(data) + 1):
        window = data[end - T:end]
        label = window[-1]["label"]
        frames = [np.asarray(w["image"], dtype=np.float32) for w in window]
        sequences.append((frames, label))

    # Train on ALL sequences — model must learn NEUTRAL as a real class.
    # Class-weighted loss compensates for the 75% NEUTRAL / 25% directional imbalance.
    train_seqs = sequences
    n = len(train_seqs)
    if n < 2:
        return

    # Compute inverse-frequency class weights
    _lbl_counts = [0, 0, 0]
    for _, _lbl in train_seqs:
        _lbl_counts[_lbl] += 1
    _total_seqs = max(sum(_lbl_counts), 1)
    _weights = [
        _total_seqs / max(_lbl_counts[0] * 3, 1),
        _total_seqs / max(_lbl_counts[1] * 3, 1),
        _total_seqs / max(_lbl_counts[2] * 3, 1),
    ]
    _weight_t = torch.tensor(_weights, dtype=torch.float32, device=device)

    model.train()
    criterion = nn.CrossEntropyLoss(weight=_weight_t)
    total_loss = 0.0
    batches = 0

    for _epoch in range(5):
        idx_list = list(range(n))
        np.random.shuffle(idx_list)
        for start in range(0, n, _TRAIN_CNN_BATCH):
            batch_idx = idx_list[start:start + _TRAIN_CNN_BATCH]
            if len(batch_idx) < 2:
                continue
            batch_seqs, batch_labels = [], []
            for i in batch_idx:
                frames, label = train_seqs[i]
                batch_seqs.append(np.stack(frames, axis=0))
                batch_labels.append(label)
            seqs_t = torch.from_numpy(np.stack(batch_seqs, axis=0)).to(device)
            labels_t = torch.tensor(batch_labels, dtype=torch.long, device=device)
            optimizer.zero_grad()
            outputs = model(seqs_t)
            loss = criterion(outputs, labels_t)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()
            batches += 1

    model.eval()
    avg_loss = total_loss / max(batches, 1)
    try:
        torch.save(model.state_dict(), "brti_cnn_lstm_10m.pth")
    except Exception:
        pass
    with ts["lock"]:
        ts["cnn_10m_train_count"][0] += 1
        ts["cnn_10m_loss"][0] = avg_loss
        ts["last_cnn_10m_train"][0] = datetime.now(timezone.utc)


def _training_loop():
    last_xgb = 0
    last_cnn = 0
    last_mtf = 0
    last_magnitude = 0
    last_resolve_outcomes = 0
    db_seeded = False
    time.sleep(5)   # short wait for exchanges to connect, then seed immediately
    while True:
        try:
            if not db_seeded:
                _seed_training_from_db()
                _seed_cnn_10m_from_db()   # fast-seed 10m labels from historical snapshots
                db_seeded = True
            _resolve_pending_labels()
            _resolve_mtf_labels()
            _resolve_cnn_10m_labels()
            now = time.time()
            if now - last_xgb >= _TRAIN_XGB_INTERVAL:
                _train_xgboost_online()
                last_xgb = now
            if now - last_cnn >= _TRAIN_CNN_INTERVAL:
                _train_cnn_lstm_online()       # 10-second model
                _train_cnn_lstm_10m_online()   # 10-minute model (no-op until pool fills)
                last_cnn = now
            if now - last_mtf >= _TRAIN_MTF_INTERVAL:
                _train_xgboost_mtf(
                    "pending_15s", "labeled_tabular_15s",
                    "xgb_15s_train_count", "xgb_15s_accuracy", "last_xgb_15s_train",
                    "xgb_15s_model", "brti_xgboost_15s.pkl",
                )
                _train_xgboost_mtf(
                    "pending_60s", "labeled_tabular_60s",
                    "xgb_60s_train_count", "xgb_60s_accuracy", "last_xgb_60s_train",
                    "xgb_60s_model", "brti_xgboost_60s.pkl",
                )
                last_mtf = now
            if now - last_magnitude >= _TRAIN_MAGNITUDE_INTERVAL:
                _train_xgboost_magnitude()
                last_magnitude = now
            # Resolve DB outcome rows every 30s
            if now - last_resolve_outcomes >= 30:
                threading.Thread(
                    target=_db_resolve_mtf_outcomes, daemon=True, name="mtf-resolve-outcomes"
                ).start()
                last_resolve_outcomes = now
        except Exception as _train_exc:
            try:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    _f.write(f"[{datetime.now(timezone.utc).isoformat()}] [TRAIN ERROR] {_train_exc}\n")
            except Exception:
                pass
        time.sleep(1)


def _start_training_loop():
    t = threading.Thread(target=_training_loop, daemon=True, name="ensemble-trainer")
    t.start()


def _build_book_image_cnn_lstm_class():
    import torch.nn as nn
    class BookImageCNNLSTM(nn.Module):
        """Temporal CNN-LSTM: processes a sequence of T order-book snapshots.

        Input:  (batch, T, 500, 2)  — T consecutive bid/ask depth images
        Output: (batch, 3)          — softmax over [DOWN, NEUTRAL, UP]

        Architecture:
          - Shared Conv2d feature extractor applied to each frame independently
          - FC projects each frame's features to a 32-d embedding
          - 2-layer LSTM over the T embeddings captures temporal dynamics
          - Final hidden state → 3-class output
        """
        def __init__(self, n_levels=_ENSEMBLE_MAX_LEVELS, seq_len=_CNN_SEQ_LEN):
            super().__init__()
            self.seq_len = seq_len
            self.conv = nn.Sequential(
                nn.Conv2d(1, 32, kernel_size=(3, 2), padding=(1, 0)),
                nn.ReLU(),
                nn.MaxPool2d((2, 1)),
                nn.Conv2d(32, 64, kernel_size=(3, 1), padding=(1, 0)),
                nn.ReLU(),
            )
            self.flatten_dim = 64 * (n_levels // 2) * 1
            self.fc = nn.Linear(self.flatten_dim, 32)
            self.dropout = nn.Dropout(0.2)
            self.lstm = nn.LSTM(32, 64, num_layers=2, batch_first=True, dropout=0.2)
            self.out = nn.Linear(64, 3)

        def forward(self, x):
            import torch
            # x: (batch, T, H, W) = (batch, T, 500, 2)
            batch, T, H, W = x.shape
            # Reshape to process all frames through Conv simultaneously
            x_flat = x.contiguous().view(batch * T, 1, H, W)   # (batch*T, 1, 500, 2)
            cnn_out = self.conv(x_flat)                          # (batch*T, 64, 250, 1)
            cnn_out = cnn_out.view(batch * T, -1)                # (batch*T, flatten_dim)
            emb = torch.relu(self.fc(cnn_out))                   # (batch*T, 32)
            emb = self.dropout(emb)
            seq = emb.view(batch, T, -1)                         # (batch, T, 32)
            lstm_out, _ = self.lstm(seq)                         # (batch, T, 64)
            last = lstm_out[:, -1, :]                            # (batch, 64)
            return torch.softmax(self.out(last), dim=1)

    return BookImageCNNLSTM


class OnlineHawkes:
    def __init__(self, mu=0.1, alpha=0.5, beta=1.0):
        self.mu = mu
        self.alpha = alpha
        self.beta = beta
        self.last_event_time = time.time()
        self.intensity = mu

    def update(self, event_occurred=True):
        now = time.time()
        dt = now - self.last_event_time
        self.intensity = self.mu + self.intensity * np.exp(-self.beta * dt)
        if event_occurred:
            self.intensity += self.alpha
        self.last_event_time = now
        return self.intensity


def _apply_temperature(probs: np.ndarray, temp: float) -> np.ndarray:
    """Soften overconfident probabilities via temperature scaling.
    temp > 1 → flatter (less certain); temp = 1 → unchanged; temp < 1 → sharper."""
    if abs(temp - 1.0) < 1e-6:
        return probs
    log_p = np.log(np.clip(probs, 1e-10, 1.0)) / temp
    log_p -= log_p.max()
    exp_p = np.exp(log_p)
    return exp_p / exp_p.sum()


def _fit_temperature(model_label: str) -> float:
    """Fit temperature T that minimises NLL on recent predictions for model_label.
    Uses brti_return sign as ground truth (DOWN / NEUTRAL / UP).
    Falls back to T=1.5 when fewer than 200 labelled rows are available."""
    try:
        from scipy.optimize import minimize_scalar
        conn = _db_conn()
        if not conn:
            return 1.5
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT prob_down, prob_neutral, prob_up, brti_return
                       FROM ensemble_predictions
                       WHERE model = %s
                         AND brti_return IS NOT NULL
                         AND prob_down   IS NOT NULL
                       ORDER BY ts DESC LIMIT 10000""",
                    (model_label,)
                )
                rows = cur.fetchall()
        finally:
            conn.close()

        if len(rows) < 200:
            return 1.5

        probs_arr = np.array([[r[0], r[1], r[2]] for r in rows], dtype=np.float64)
        returns   = np.array([r[3] for r in rows],               dtype=np.float64)

        # Ground-truth label: DOWN=0, NEUTRAL=1, UP=2
        thr    = 1e-5
        labels = np.where(returns < -thr, 0, np.where(returns > thr, 2, 1))

        def nll(log_t: float) -> float:
            t     = np.exp(log_t)
            log_p = np.log(np.clip(probs_arr, 1e-10, 1.0)) / t
            log_p -= log_p.max(axis=1, keepdims=True)
            exp_p = np.exp(log_p)
            cal   = exp_p / exp_p.sum(axis=1, keepdims=True)
            return float(-np.log(np.clip(cal[np.arange(len(labels)), labels], 1e-10, 1.0)).mean())

        res = minimize_scalar(nll, bounds=(np.log(0.3), np.log(8.0)), method="bounded")
        return float(np.exp(res.x))
    except Exception:
        return 1.5


@st.cache_resource
def _ensemble_state():
    return {
        "deque": collections.deque(maxlen=7200),
        "lock": threading.Lock(),
        "thread": [None],
        "stop_flag": [False],
        "status": ["off"],
        "hawkes": [OnlineHawkes()],
        "deep_prediction": [np.array([0.33, 0.34, 0.33])],
        "deep_lock": threading.Lock(),
        # 10-minute CNN-LSTM — separate model, separate weights, never sees 10s labels
        "deep_model_10m": [None],
        "deep_optimizer_10m": [None],
        "deep_prediction_10m": [np.array([0.33, 0.34, 0.33])],
        "deep_lock_10m": threading.Lock(),
        "cnn_10m_run_direction": [""],
        "cnn_10m_run_count": [0],
        "model_mode": ["auto"],
        "last_prediction": [None],
        "xgb_last_prediction": [None],
        "error": [None],
        "xgb_model": [None],
        "deep_model": [None],
        "deep_optimizer": [None],
        "device": [None],
        "flush_buf": [],
        "flush_lock": threading.Lock(),
        "flush_counter": [0],
        "temp_cnn": [1.5],
        "temp_xgb": [1.5],
        "temp_last_fit": [0.0],
        # Rolling buffers for XGBoost feature engineering
        "brti_history":     collections.deque(maxlen=120),  # 120s of BRTI prices
        "vt_history":       collections.deque(maxlen=10),
        "return_history":   collections.deque(maxlen=120),  # 1s returns for RSI + realized vol
        "imbalance_history":collections.deque(maxlen=60),   # depth imbalance for velocity
        "vwap_num":         [0.0],   # running VWAP numerator (price × vol)
        "vwap_den":         [0.0],   # running VWAP denominator (vol)
        # Temporal image buffer for CNN-LSTM sequence input
        "image_seq_buf": collections.deque(maxlen=_CNN_SEQ_LEN),
        # Latest indicator values — written by main loop, read by UI
        "indicator_cache": [{}],
        # Consecutive-run tracker (local to ensemble — not dependent on auto-trader process)
        "run_direction": [""],
        "run_count": [0],
        # Multi-timeframe XGBoost models
        "xgb_15s_model": [None],
        "xgb_60s_model": [None],
        "xgb_15s_last_prediction": [None],
        "xgb_60s_last_prediction": [None],
        # Magnitude regression (10-min signed return predictor)
        "xgb_magnitude_model": [None],
        "magnitude_feature_cols": [None],
        "magnitude_last_prediction": [None],
    }


def _ensemble_init_models():
    import torch
    state = _ensemble_state()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    state["device"][0] = device

    BookImageCNNLSTM = _build_book_image_cnn_lstm_class()
    deep_model = BookImageCNNLSTM().to(device)
    try:
        deep_model.load_state_dict(torch.load("brti_cnn_lstm.pth", map_location=device, weights_only=True))
        deep_model.eval()
    except Exception:
        deep_model.eval()
    state["deep_optimizer"][0] = torch.optim.Adam(deep_model.parameters(), lr=_TRAIN_CNN_LR)
    # torch.compile skipped: adds ~90s startup + 400 MB peak RAM with no
    # meaningful benefit at 2-second inference intervals on CPU
    state["deep_model"][0] = deep_model

    # 10-minute CNN-LSTM — separate weights, loads from brti_cnn_lstm_10m.pth
    deep_model_10m = BookImageCNNLSTM().to(device)
    try:
        deep_model_10m.load_state_dict(
            torch.load("brti_cnn_lstm_10m.pth", map_location=device, weights_only=True))
        deep_model_10m.eval()
    except Exception:
        deep_model_10m.eval()
    state["deep_optimizer_10m"][0] = torch.optim.Adam(deep_model_10m.parameters(), lr=_TRAIN_CNN_LR)
    state["deep_model_10m"][0] = deep_model_10m

    try:
        import joblib
        state["xgb_model"][0] = joblib.load("brti_xgboost.pkl")
    except Exception:
        state["xgb_model"][0] = None

    try:
        import joblib
        state["xgb_15s_model"][0] = joblib.load("brti_xgboost_15s.pkl")
    except Exception:
        state["xgb_15s_model"][0] = None

    try:
        import joblib
        state["xgb_60s_model"][0] = joblib.load("brti_xgboost_60s.pkl")
    except Exception:
        state["xgb_60s_model"][0] = None

    try:
        import joblib
        state["xgb_magnitude_model"][0] = joblib.load("brti_xgboost_magnitude.pkl")
    except Exception:
        state["xgb_magnitude_model"][0] = None


def _ensemble_deep_inference_loop(state):
    import torch
    while not state["stop_flag"][0]:
        time.sleep(1)
        try:
            bobby_state = _bobby_brti_state()
            bids = bobby_state["cached_bids"][0]
            asks = bobby_state["cached_asks"][0]
            if bids is None or asks is None or len(bids) == 0 or len(asks) == 0:
                continue
            n_ex = bobby_state["cached_n_ex"][0]
            if n_ex < _BOBBY_MIN_EXCHANGES:
                continue

            # Build (500, 2) frame and push into temporal buffer
            frame_tensor = _create_raw_book_image(bids, asks)   # (1, 1, 500, 2)
            frame_np = frame_tensor.numpy()[0, 0]               # (500, 2)
            state["image_seq_buf"].append(frame_np)

            if len(state["image_seq_buf"]) < _CNN_SEQ_LEN:
                continue   # wait until buffer is full

            device = state["device"][0]
            deep_model = state["deep_model"][0]

            # Stack T frames → (1, T, 500, 2)
            seq_np = np.stack(list(state["image_seq_buf"]), axis=0)  # (T, 500, 2)
            seq_t = torch.from_numpy(seq_np).unsqueeze(0).to(device)  # (1, T, 500, 2)

            with torch.no_grad():
                probs = deep_model(seq_t).cpu().numpy()[0]
            with state["deep_lock"]:
                state["deep_prediction"][0] = probs

            # 10-minute model — same input sequence, separate weights
            deep_model_10m = state["deep_model_10m"][0]
            if deep_model_10m is not None:
                try:
                    with torch.no_grad():
                        probs_10m = deep_model_10m(seq_t).cpu().numpy()[0]
                    with state["deep_lock_10m"]:
                        state["deep_prediction_10m"][0] = probs_10m
                except Exception:
                    pass
        except Exception as _deep_exc:
            try:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    _f.write(f"[{datetime.now(timezone.utc).isoformat()}] [DEEP INFER ERROR] {_deep_exc}\n")
            except Exception:
                pass


def _ensemble_main_loop(state):
    import torch
    import pandas as _pd
    previous_brti = None
    hawkes = state["hawkes"][0]
    _default_probs = np.array([0.33, 0.34, 0.33])

    while not state["stop_flag"][0]:
        try:
            bobby_state = _bobby_brti_state()
            brti_value = bobby_state["last_price"][0]
            if brti_value is None:
                time.sleep(0.5)
                continue

            bids = bobby_state["cached_bids"][0]
            asks = bobby_state["cached_asks"][0]
            v_T = bobby_state["cached_v_T"][0] or 0.0
            C_T = bobby_state["cached_C_T"][0] or 0.0
            n_ex = bobby_state["cached_n_ex"][0]

            if bids is None or asks is None:
                time.sleep(0.5)
                continue

            event = abs(brti_value - (previous_brti or brti_value)) > 0.1
            hawkes_intensity = hawkes.update(event)

            brti_return = 0.0 if previous_brti is None else (brti_value - previous_brti) / previous_brti

            # ── Update rolling history buffers ──────────────────────────────
            state["brti_history"].append(float(brti_value))
            state["vt_history"].append(float(v_T))
            state["return_history"].append(float(brti_return))
            bh = list(state["brti_history"])
            vh = list(state["vt_history"])
            rh = list(state["return_history"])

            def _ret(hist, n):
                if len(hist) > n and hist[-n - 1] > 0:
                    return (hist[-1] - hist[-n - 1]) / hist[-n - 1]
                return 0.0

            brti_ret_5  = _ret(bh, 5)
            brti_ret_10 = _ret(bh, 10)
            brti_ret_30 = _ret(bh, 30)
            vt_velocity = (vh[-1] - vh[-5]) if len(vh) >= 5 else 0.0

            # ── Realized volatility ─────────────────────────────────────────
            def _rvol(rets, n):
                if len(rets) >= n:
                    return float(np.std(rets[-n:]))
                return 0.0

            vol_30 = _rvol(rh, 30)
            vol_60 = _rvol(rh, 60)

            # ── RSI on 1-second BRTI returns ────────────────────────────────
            def _rsi(rets, n):
                if len(rets) < n:
                    return 50.0
                window = rets[-n:]
                gains  = [r for r in window if r > 0]
                losses = [-r for r in window if r < 0]
                avg_g  = sum(gains) / n
                avg_l  = sum(losses) / n
                if avg_l == 0:
                    return 100.0
                return 100.0 - 100.0 / (1.0 + avg_g / avg_l)

            rsi_7  = _rsi(rh, 7)
            rsi_14 = _rsi(rh, 14)
            rsi_21 = _rsi(rh, 21)

            # ── VWAP deviation (running, decayed every 3600 iters ~1 hr) ────
            state["vwap_num"][0] += float(brti_value) * float(v_T)
            state["vwap_den"][0] += float(v_T)
            flush_cnt = state["flush_counter"][0]
            if flush_cnt % 3600 == 0 and flush_cnt > 0:
                state["vwap_num"][0] = 0.0
                state["vwap_den"][0] = 0.0
            vwap = (state["vwap_num"][0] / state["vwap_den"][0]
                    if state["vwap_den"][0] > 0 else brti_value)
            vwap_dev = (brti_value - vwap) / vwap if vwap > 0 else 0.0

            # ── Order-book derived features ─────────────────────────────────
            bid_ask_spread = 0.0
            spread_pct     = 0.0
            microprice     = 0.0
            bid1_vol = ask1_vol = 0.0
            bid5_vol = ask5_vol = 0.0
            bid10_vol = ask10_vol = 0.0
            bid20_vol = ask20_vol = 0.0
            depth_ratio_1 = depth_ratio_5 = 0.0
            imbalance = 0.0

            if len(bids) > 0 and len(asks) > 0:
                best_bid = float(bids[0, 0]);  best_ask = float(asks[0, 0])
                mid = (best_bid + best_ask) / 2.0
                bid_ask_spread = best_ask - best_bid
                spread_pct     = bid_ask_spread / mid if mid > 0 else 0.0

                bid1_vol = float(bids[0, 1])
                ask1_vol = float(asks[0, 1])
                microprice = ((bid1_vol * best_ask + ask1_vol * best_bid)
                              / (bid1_vol + ask1_vol)) if (bid1_vol + ask1_vol) > 0 else mid

                def _depth(arr, n):
                    return float(arr[:min(n, len(arr)), 1].sum())

                bid5_vol  = _depth(bids, 5);   ask5_vol  = _depth(asks, 5)
                bid10_vol = _depth(bids, 10);  ask10_vol = _depth(asks, 10)
                bid20_vol = _depth(bids, 20);  ask20_vol = _depth(asks, 20)

                depth_ratio_1 = (bid1_vol / ask1_vol)   if ask1_vol > 0 else 1.0
                depth_ratio_5 = (bid5_vol / ask5_vol)   if ask5_vol > 0 else 1.0
                total10 = bid10_vol + ask10_vol
                imbalance = (bid10_vol - ask10_vol) / total10 if total10 > 0 else 0.0

            # ── Imbalance velocity (rate of change over 10 ticks) ───────────
            state["imbalance_history"].append(float(imbalance))
            ih = list(state["imbalance_history"])
            imbalance_velocity = (ih[-1] - ih[-10]) if len(ih) >= 10 else 0.0

            features_dict = {
                # Original features
                "v_T": v_T, "C_T": C_T, "exchanges": n_ex,
                "hawkes": hawkes_intensity, "brti_return": brti_return,
                "bid_ask_spread": bid_ask_spread,
                "bid_depth_10": bid10_vol,
                "ask_depth_10": ask10_vol,
                "imbalance": imbalance,
                # Rolling-return features
                "brti_ret_5": brti_ret_5, "brti_ret_10": brti_ret_10, "brti_ret_30": brti_ret_30,
                "vt_velocity": vt_velocity,
                # Order-book microstructure features
                "microprice": microprice,
                "spread_pct": spread_pct,
                "bid1_vol": bid1_vol, "ask1_vol": ask1_vol,
                "bid5_vol": bid5_vol, "ask5_vol": ask5_vol,
                "bid20_vol": bid20_vol, "ask20_vol": ask20_vol,
                "depth_ratio_1": depth_ratio_1, "depth_ratio_5": depth_ratio_5,
                # New: volatility regime
                "vol_30": vol_30, "vol_60": vol_60,
                # New: RSI momentum
                "rsi_7": rsi_7, "rsi_14": rsi_14, "rsi_21": rsi_21,
                # New: VWAP deviation
                "vwap_dev": vwap_dev,
                # New: imbalance velocity
                "imbalance_velocity": imbalance_velocity,
            }

            # ── Update indicator cache for UI ────────────────────────────────
            _rd = state["run_direction"][0]
            _rc = state["run_count"][0]
            state["indicator_cache"][0] = {
                "vol_30": vol_30, "vol_60": vol_60,
                "rsi_7": rsi_7, "rsi_14": rsi_14, "rsi_21": rsi_21,
                "vwap": vwap, "vwap_dev": vwap_dev,
                "imbalance": imbalance, "imbalance_velocity": imbalance_velocity,
                "brti_ret_5": brti_ret_5, "brti_ret_10": brti_ret_10,
                "hawkes": hawkes_intensity,
                "depth_ratio_1": depth_ratio_1, "depth_ratio_5": depth_ratio_5,
                "run_count": _rc,
                "run_dir": _rd,
            }

            book_img_np = None
            if len(bids) > 0 and len(asks) > 0:
                bid_vol = np.zeros(_ENSEMBLE_MAX_LEVELS)
                ask_vol = np.zeros(_ENSEMBLE_MAX_LEVELS)
                n_b = min(_ENSEMBLE_MAX_LEVELS, len(bids))
                n_a = min(_ENSEMBLE_MAX_LEVELS, len(asks))
                bid_vol[:n_b] = bids[:n_b, 1]
                ask_vol[:n_a] = asks[:n_a, 1]
                book_img_np = np.stack([np.log1p(bid_vol), np.log1p(ask_vol)], axis=1)
                book_img_np = book_img_np.reshape(1, 1, _ENSEMBLE_MAX_LEVELS, 2).astype(np.float32)

            _collect_training_sample(features_dict, book_img_np, brti_value)

            model_mode = state["model_mode"][0]
            xgb_model = state["xgb_model"][0]

            # ── Periodic temperature recalibration (every 30 min) ──────────
            _now_ts = time.time()
            if _now_ts - state["temp_last_fit"][0] > 1800:
                state["temp_last_fit"][0] = _now_ts
                def _recalibrate():
                    t_cnn = _fit_temperature("CNN-LSTM")
                    t_xgb = _fit_temperature("XGBoost")
                    state["temp_cnn"][0] = t_cnn
                    state["temp_xgb"][0] = t_xgb
                threading.Thread(target=_recalibrate, daemon=True, name="temp-cal").start()

            xgb_probs = _default_probs.copy()
            if xgb_model is not None:
                try:
                    _features_df = _pd.DataFrame([features_dict])
                    _proba = xgb_model.predict_proba(_features_df)[0]
                    if len(_proba) == 3:
                        xgb_probs = np.array(_proba)
                    elif len(_proba) == 2:
                        xgb_probs = np.array([_proba[0], 0.0, _proba[1]])
                    # Apply temperature scaling to XGBoost
                    xgb_probs = _apply_temperature(xgb_probs, state["temp_xgb"][0])
                except Exception:
                    pass

            if model_mode == "xgboost" or (model_mode == "auto" and v_T <= 30):
                active_model = "XGBoost"
                final_probs = xgb_probs.copy()
            elif model_mode == "deep":
                active_model = "CNN-LSTM"
                with state["deep_lock"]:
                    deep_probs = _apply_temperature(
                        state["deep_prediction"][0].copy(), state["temp_cnn"][0])
                final_probs = deep_probs
            else:
                # Auto blend: XGBoost always gets at least 30% weight
                # so the ensemble never fully ignores 356k tabular training samples
                active_model = "Ensemble"
                with state["deep_lock"]:
                    deep_probs = _apply_temperature(
                        state["deep_prediction"][0].copy(), state["temp_cnn"][0])
                cnn_weight = min(0.70, v_T / 100)  # caps at 70% CNN-LSTM; XGBoost ≥ 30%
                final_probs = cnn_weight * deep_probs + (1 - cnn_weight) * xgb_probs

            pred_idx = int(np.argmax(final_probs))
            direction = ["DOWN", "NEUTRAL", "UP"][pred_idx]
            confidence = float(final_probs[pred_idx])

            if active_model in ("CNN-LSTM", "Ensemble") and confidence < _CNN_CONFIDENCE_THRESHOLD:
                direction = "NEUTRAL"

            if direction == "NEUTRAL" or direction != state["run_direction"][0]:
                state["run_direction"][0] = direction
                state["run_count"][0] = 0 if direction == "NEUTRAL" else 1
            else:
                state["run_count"][0] += 1

            # ── 10-minute CNN-LSTM signal (independent run tracker) ─────────
            _cnn10m_dir = "NEUTRAL"
            _cnn10m_conf = 0.33
            _cnn10m_p_up = 0.33
            _cnn10m_p_dn = 0.33
            _cnn10m_trained = _training_state()["cnn_10m_train_count"][0] > 0
            if _cnn10m_trained:
                with state["deep_lock_10m"]:
                    _p10m = _apply_temperature(
                        state["deep_prediction_10m"][0].copy(), state["temp_cnn"][0])
                _idx10m = int(np.argmax(_p10m))
                _cnn10m_dir = ["DOWN", "NEUTRAL", "UP"][_idx10m]
                _cnn10m_conf = float(_p10m[_idx10m])
                _cnn10m_p_dn = float(_p10m[0])
                _cnn10m_p_up = float(_p10m[2])
                if _cnn10m_conf < _CNN_CONFIDENCE_THRESHOLD:
                    _cnn10m_dir = "NEUTRAL"
            # Track 10m run length
            if _cnn10m_dir == "NEUTRAL" or _cnn10m_dir != state["cnn_10m_run_direction"][0]:
                state["cnn_10m_run_direction"][0] = _cnn10m_dir
                state["cnn_10m_run_count"][0] = 0 if _cnn10m_dir == "NEUTRAL" else 1
            else:
                state["cnn_10m_run_count"][0] += 1

            ts = datetime.now(timezone.utc)
            tick = {
                "ts": ts,
                "brti": float(brti_value) if brti_value is not None else None,
                "v_T": float(v_T) if v_T is not None else None,
                "C_T": float(C_T) if C_T is not None else None,
                "hawkes": float(hawkes_intensity) if hawkes_intensity is not None else None,
                "direction": direction,
                "confidence": confidence,
                "model": active_model,
                "prob_down": float(final_probs[0]),
                "prob_neutral": float(final_probs[1]),
                "prob_up": float(final_probs[2]),
                "n_exchanges": int(n_ex) if n_ex is not None else None,
                "brti_return": float(brti_return) if brti_return is not None else None,
                "xgb_prob_up": float(xgb_probs[2]),
                "xgb_prob_down": float(xgb_probs[0]),
                "xgb_conf": float(xgb_probs[int(np.argmax(xgb_probs))]),
                "cnn_10m_direction": _cnn10m_dir,
                "cnn_10m_confidence": _cnn10m_conf,
                "cnn_10m_prob_up": _cnn10m_p_up,
                "cnn_10m_prob_dn": _cnn10m_p_dn,
                "cnn_10m_run_count": state["cnn_10m_run_count"][0],
                "cnn_10m_trained": _cnn10m_trained,
            }

            xgb_pred_idx = int(np.argmax(xgb_probs))
            state["xgb_last_prediction"][0] = {
                "direction": ["DOWN", "NEUTRAL", "UP"][xgb_pred_idx],
                "confidence": float(xgb_probs[xgb_pred_idx]),
                "prob_down": float(xgb_probs[0]),
                "prob_neutral": float(xgb_probs[1]),
                "prob_up": float(xgb_probs[2]),
                "brti": float(brti_value) if brti_value is not None else None,
                "ts": datetime.now(timezone.utc),
            }

            # ── Multi-timeframe XGBoost inference ──────────────────────────
            _mtf_labels = ["DOWN", "NEUTRAL", "UP"]
            _default_mtf = np.array([0.33, 0.34, 0.33])

            def _run_mtf_model(model_key, pred_key):
                mdl = state[model_key][0]
                if mdl is None:
                    state[pred_key][0] = None
                    return None
                try:
                    _fdf = _pd.DataFrame([features_dict])
                    _p = mdl.predict_proba(_fdf)[0]
                    if len(_p) == 2:
                        _p = np.array([_p[0], 0.0, _p[1]])
                    else:
                        _p = np.array(_p)
                    _idx = int(np.argmax(_p))
                    state[pred_key][0] = {
                        "direction": _mtf_labels[_idx],
                        "confidence": float(_p[_idx]),
                        "prob_down": float(_p[0]),
                        "prob_neutral": float(_p[1]),
                        "prob_up": float(_p[2]),
                        "ts": datetime.now(timezone.utc),
                    }
                    return state[pred_key][0]
                except Exception:
                    state[pred_key][0] = None
                    return None

            _p15 = _run_mtf_model("xgb_15s_model", "xgb_15s_last_prediction")
            _p60 = _run_mtf_model("xgb_60s_model", "xgb_60s_last_prediction")

            # ── Magnitude regression inference ─────────────────────────────
            mag_mdl = state["xgb_magnitude_model"][0]
            if mag_mdl is not None:
                try:
                    _mag_feat_cols = state["magnitude_feature_cols"][0]
                    if _mag_feat_cols:
                        _fdf = _pd.DataFrame([{k: features_dict.get(k, 0.0) for k in _mag_feat_cols}])
                    else:
                        _fdf = _pd.DataFrame([features_dict])
                    _mag_ret = float(mag_mdl.predict(_fdf)[0])
                    state["magnitude_last_prediction"][0] = {
                        "return_10m": _mag_ret,
                        "pct": round(_mag_ret * 100, 4),
                        "bps": round(_mag_ret * 10000, 1),
                        "ts": datetime.now(timezone.utc),
                    }
                except Exception:
                    pass

            # Log predictions + queue outcome resolution every ~10s (every 20 ticks at 0.5s)
            if int(time.time()) % 10 == 0 and (_p15 is not None or _p60 is not None):
                threading.Thread(
                    target=_db_log_mtf_prediction,
                    args=(float(brti_value) if brti_value is not None else None, _p15, _p60),
                    daemon=True, name="mtf-log",
                ).start()

            with state["lock"]:
                state["deque"].append(tick)
            state["last_prediction"][0] = tick
            state["status"][0] = "live"
            state["error"][0] = None

            with state["flush_lock"]:
                state["flush_buf"].append(tick)
                state["flush_counter"][0] += 1
                if state["flush_counter"][0] >= 60:
                    to_flush = list(state["flush_buf"])
                    state["flush_buf"].clear()
                    state["flush_counter"][0] = 0
                    threading.Thread(
                        target=db_save_ensemble_predictions, args=(to_flush,), daemon=True
                    ).start()

            try:
                _write_shared_ui_state(state, _training_state())
            except Exception:
                pass

            previous_brti = brti_value
            time.sleep(0.5)

        except Exception as e:
            state["error"][0] = str(e)
            try:
                with open("/tmp/bobby_debug.log", "a") as _f:
                    _f.write(f"[{datetime.now(timezone.utc).isoformat()}] [ENSEMBLE ERROR] {e}\n")
            except Exception:
                pass
            time.sleep(1)


def _ensemble_thread_target():
    state = _ensemble_state()
    try:
        _ensemble_init_models()
        state["status"][0] = "running"

        deep_t = threading.Thread(target=_ensemble_deep_inference_loop, args=(state,), daemon=True)
        deep_t.start()

        _start_training_loop()

        _ensemble_main_loop(state)
    except Exception as e:
        state["error"][0] = str(e)
        state["status"][0] = "error"


def start_ensemble_predictor():
    state = _ensemble_state()
    t = state["thread"][0]
    if t is not None and t.is_alive():
        return
    state["stop_flag"][0] = False
    state["status"][0] = "starting"
    t = threading.Thread(target=_ensemble_thread_target, daemon=True)
    t.start()
    state["thread"][0] = t


def stop_ensemble_predictor():
    state = _ensemble_state()
    state["stop_flag"][0] = True
    state["status"][0] = "off"
    t = state["thread"][0]
    if t is not None:
        t.join(timeout=5)
    state["thread"][0] = None


def ensemble_is_running() -> bool:
    state = _ensemble_state()
    t = state["thread"][0]
    return t is not None and t.is_alive()


_SHARED_UI_STATE_FILE = "/tmp/ensemble_ui_state.json"


def _write_shared_ui_state(state, training_state):
    """Write UI-visible state from background_runner to a shared file so Streamlit can read it."""
    try:
        pred = state["last_prediction"][0]
        xgb = state["xgb_last_prediction"][0]
        ind = state["indicator_cache"][0] or {}
        ts = training_state
        data = {
            "prediction": None,
            "xgb_prediction": None,
            "status": state["status"][0],
            "error": state["error"][0],
            "model_mode": state["model_mode"][0],
            "indicators": ind,
            "temp_cnn": state["temp_cnn"][0],
            "temp_xgb": state["temp_xgb"][0],
            "temp_last_fit": state["temp_last_fit"][0],
            "run_count": state["run_count"][0],
            "run_direction": state["run_direction"][0],
            "training": {
                "xgb_train_count": ts["xgb_train_count"][0],
                "cnn_train_count": ts["cnn_train_count"][0],
                "cnn_10m_train_count": ts["cnn_10m_train_count"][0],
                "xgb_accuracy": ts["xgb_accuracy"][0],
                "cnn_loss": ts["cnn_loss"][0],
                "cnn_10m_loss": ts["cnn_10m_loss"][0],
                "last_xgb_train": ts["last_xgb_train"][0].isoformat() if ts["last_xgb_train"][0] else None,
                "last_cnn_train": ts["last_cnn_train"][0].isoformat() if ts["last_cnn_train"][0] else None,
                "last_cnn_10m_train": ts["last_cnn_10m_train"][0].isoformat() if ts["last_cnn_10m_train"][0] else None,
                "total_samples": ts["total_samples"][0],
                "labeled_tabular": len(ts["labeled_tabular"]),
                "labeled_images": len(ts["labeled_images"]),
                "labeled_images_10m": len(ts["labeled_images_10m"]),
                "pending_count": len(ts["pending"]),
            },
            "cnn_10m_run_count": state["cnn_10m_run_count"][0],
            "cnn_10m_run_direction": state["cnn_10m_run_direction"][0],
        }
        if pred and isinstance(pred, dict):
            safe_pred = {}
            for k, v in pred.items():
                if k == "ts" and hasattr(v, "isoformat"):
                    safe_pred[k] = v.isoformat()
                else:
                    safe_pred[k] = v
            data["prediction"] = safe_pred
        if xgb and isinstance(xgb, dict):
            safe_xgb = {}
            for k, v in xgb.items():
                if k == "ts" and hasattr(v, "isoformat"):
                    safe_xgb[k] = v.isoformat()
                else:
                    safe_xgb[k] = v
            data["xgb_prediction"] = safe_xgb

        # MTF predictions
        for _mtf_key, _out_key in [
            ("xgb_15s_last_prediction", "xgb_15s_prediction"),
            ("xgb_60s_last_prediction", "xgb_60s_prediction"),
        ]:
            _mtf_pred = state.get(_mtf_key, [None])[0]
            if _mtf_pred and isinstance(_mtf_pred, dict):
                _safe = {}
                for k, v in _mtf_pred.items():
                    _safe[k] = v.isoformat() if k == "ts" and hasattr(v, "isoformat") else v
                data[_out_key] = _safe
            else:
                data[_out_key] = None

        # Magnitude prediction
        _mag = state.get("magnitude_last_prediction", [None])[0]
        if _mag and isinstance(_mag, dict):
            _safe_mag = {}
            for k, v in _mag.items():
                _safe_mag[k] = v.isoformat() if k == "ts" and hasattr(v, "isoformat") else v
            data["magnitude_prediction"] = _safe_mag
        else:
            data["magnitude_prediction"] = None

        # MTF training stats
        _ts_obj = training_state
        data["training"]["xgb_15s_train_count"] = _ts_obj["xgb_15s_train_count"][0]
        data["training"]["xgb_60s_train_count"] = _ts_obj["xgb_60s_train_count"][0]
        data["training"]["xgb_15s_accuracy"]    = _ts_obj["xgb_15s_accuracy"][0]
        data["training"]["xgb_60s_accuracy"]    = _ts_obj["xgb_60s_accuracy"][0]
        data["training"]["labeled_tabular_15s"] = len(_ts_obj["labeled_tabular_15s"])
        data["training"]["labeled_tabular_60s"] = len(_ts_obj["labeled_tabular_60s"])
        data["training"]["labeled_images_10m"]   = len(_ts_obj["labeled_images_10m"])
        data["training"]["labeled_magnitude_10m"] = len(_ts_obj["labeled_magnitude_10m"])
        data["training"]["magnitude_train_count"] = _ts_obj["magnitude_train_count"][0]
        data["training"]["magnitude_accuracy"]    = _ts_obj["magnitude_accuracy"][0]

        try:
            _ats = _auto_trader_state()
            data["auto_trader_status"] = _ats["status"][0]
        except Exception:
            pass
        data["written_at"] = time.time()
        tmp = _SHARED_UI_STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, _SHARED_UI_STATE_FILE)
    except Exception as exc:
        try:
            with open("/tmp/bobby_debug.log", "a") as _f:
                _f.write(f"[{datetime.now(timezone.utc).isoformat()}] [SHARED_STATE_WRITE] {exc}\n")
        except Exception:
            pass


def _read_shared_ui_state() -> dict:
    """Read shared UI state written by background_runner."""
    try:
        with open(_SHARED_UI_STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


@st.cache_data(ttl=5)
def _db_ensemble_ticks(limit=300) -> list:
    if not DATABASE_URL:
        return []
    conn = _db_conn()
    if not conn:
        return []
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT ts, brti, direction, confidence, model, "
                    "prob_up, prob_neutral, prob_down, v_t, c_t, hawkes, n_exchanges, brti_return "
                    "FROM ensemble_predictions ORDER BY ts DESC LIMIT %s",
                    (limit,),
                )
                rows = cur.fetchall()
        ticks = []
        for r in reversed(rows):
            ticks.append({
                "ts": r[0], "brti": float(r[1]), "direction": r[2],
                "confidence": float(r[3]), "model": r[4],
                "prob_up": float(r[5]), "prob_neutral": float(r[6]),
                "prob_down": float(r[7]), "v_T": float(r[8]),
                "C_T": float(r[9]), "hawkes": float(r[10]),
                "n_exchanges": int(r[11]), "brti_return": float(r[12]),
            })
        return ticks
    except Exception:
        return []
    finally:
        conn.close()


def _db_run_count() -> tuple:
    if not DATABASE_URL:
        return 0, "NONE"
    conn = _db_conn()
    if not conn:
        return 0, "NONE"
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT direction FROM ensemble_predictions ORDER BY ts DESC LIMIT 30"
                )
                rows = cur.fetchall()
        if not rows:
            return 0, "NONE"
        first_dir = rows[0][0]
        count = 0
        for r in rows:
            if r[0] == first_dir:
                count += 1
            else:
                break
        return count, first_dir
    except Exception:
        return 0, "NONE"
    finally:
        conn.close()


def _db_ensemble_latest() -> dict:
    ticks = _db_ensemble_ticks(limit=1)
    if ticks:
        t = ticks[0]
        rc, rd = _db_run_count()
        return {
            "prediction": t,
            "xgb_prediction": None,
            "status": "live",
            "error": None,
            "model_mode": t.get("model", "Ensemble"),
            "indicators": {"run_count": rc, "run_dir": rd},
        }
    return {
        "prediction": None, "xgb_prediction": None,
        "status": "off", "error": None, "model_mode": None, "indicators": None,
    }


def get_ensemble_ticks() -> list:
    state = _ensemble_state()
    with state["lock"]:
        ticks = list(state["deque"])
    if len(ticks) >= 5:
        return ticks
    db_ticks = _db_ensemble_ticks(300)
    return db_ticks if db_ticks else ticks


def get_ensemble_latest() -> dict:
    state = _ensemble_state()
    if state["last_prediction"][0] is not None and state["status"][0] == "live":
        return {
            "prediction": state["last_prediction"][0],
            "xgb_prediction": state["xgb_last_prediction"][0],
            "xgb_15s_prediction": state["xgb_15s_last_prediction"][0],
            "xgb_60s_prediction": state["xgb_60s_last_prediction"][0],
            "magnitude_prediction": state["magnitude_last_prediction"][0],
            "status": state["status"][0],
            "error": state["error"][0],
            "model_mode": state["model_mode"][0],
            "indicators": state["indicator_cache"][0],
        }
    shared = _read_shared_ui_state()
    if shared and shared.get("status") == "live" and shared.get("prediction"):
        return {
            "prediction": shared["prediction"],
            "xgb_prediction": shared.get("xgb_prediction"),
            "xgb_15s_prediction": shared.get("xgb_15s_prediction"),
            "xgb_60s_prediction": shared.get("xgb_60s_prediction"),
            "magnitude_prediction": shared.get("magnitude_prediction"),
            "status": shared["status"],
            "error": shared.get("error"),
            "model_mode": shared.get("model_mode"),
            "indicators": shared.get("indicators"),
        }
    return _db_ensemble_latest()


@st.cache_data(ttl=10)
def fetch_brti_seconds(lookback_secs: int = 300):
    """Fetch 1-second BTC/USD aggregates from Polygon for the rolling window."""
    if not POLYGON_API_KEY:
        return pd.DataFrame()
    now = datetime.now(timezone.utc)
    from_ms = int((now - timedelta(seconds=lookback_secs + 30)).timestamp() * 1000)
    to_ms = int(now.timestamp() * 1000)
    try:
        r = requests.get(
            f"{POLYGON_BASE}/aggs/ticker/X:BTCUSD/range/1/second/{from_ms}/{to_ms}",
            params={"apiKey": POLYGON_API_KEY, "limit": min(lookback_secs + 60, 50000), "sort": "asc"},
            timeout=15,
        )
        if r.status_code != 200:
            return pd.DataFrame()
        results = r.json().get("results", [])
        if not results:
            return pd.DataFrame()
        df = pd.DataFrame(results)
        df["ts"] = pd.to_datetime(df["t"], unit="ms", utc=True)
        df["price"] = df["c"].astype(float)
        return df[["ts", "price"]].sort_values("ts").reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def compute_divergence(btc_df: pd.DataFrame, kalshi_df: pd.DataFrame, threshold_pct: float):
    if btc_df.empty or kalshi_df.empty:
        return pd.DataFrame()

    btc = btc_df[["ts", "close"]].copy().rename(columns={"close": "btc_close"})
    btc = btc.set_index("ts").resample("1min").last().ffill().reset_index()

    kal = kalshi_df[["ts", "close"]].copy().rename(columns={"close": "kalshi_yes"})
    kal = kal.set_index("ts").resample("1min").last().ffill().reset_index()

    merged = pd.merge_asof(btc.sort_values("ts"), kal.sort_values("ts"), on="ts", direction="nearest", tolerance=pd.Timedelta("5min"))
    merged = merged.dropna()

    if merged.empty:
        return merged

    btc_z = (merged["btc_close"] - merged["btc_close"].mean()) / (merged["btc_close"].std() + 1e-8)
    kal_z = (merged["kalshi_yes"] - merged["kalshi_yes"].mean()) / (merged["kalshi_yes"].std() + 1e-8)

    merged["btc_norm"] = btc_z
    merged["kalshi_norm"] = kal_z
    merged["divergence"] = btc_z - kal_z
    merged["divergence_abs"] = merged["divergence"].abs()

    z_threshold = threshold_pct / 5.0
    merged["is_divergence"] = merged["divergence_abs"] > z_threshold

    return merged


def compute_stats(div_df: pd.DataFrame):
    stats = {}
    if div_df.empty:
        return stats

    stats["total_candles"] = len(div_df)
    stats["divergence_count"] = int(div_df["is_divergence"].sum())
    stats["divergence_pct"] = stats["divergence_count"] / max(stats["total_candles"], 1) * 100
    stats["avg_divergence"] = float(div_df["divergence"].mean())
    stats["max_divergence"] = float(div_df["divergence"].abs().max())
    stats["btc_kalshi_corr"] = float(div_df["btc_close"].corr(div_df["kalshi_yes"]))

    btc_ret = div_df["btc_close"].pct_change().dropna()
    kal_ret = div_df["kalshi_yes"].pct_change().dropna()
    if len(btc_ret) > 0 and len(kal_ret) > 0:
        min_len = min(len(btc_ret), len(kal_ret))
        agreement = (np.sign(btc_ret.iloc[-min_len:].values) == np.sign(kal_ret.iloc[-min_len:].values)).mean()
        stats["directional_agreement"] = float(agreement) * 100
    else:
        stats["directional_agreement"] = 0.0

    return stats


_AT_SETTINGS_FILE = "auto_trade_settings.json"
_AT_POSITION_FILE = "/tmp/auto_trade_position.json"
_AT_MANUAL_EXIT_FILE = "/tmp/auto_trade_manual_exit"
_AT_BUY_MORE_FILE = "/tmp/auto_trade_buy_more"
_AT_FREEZE_FILE = "/tmp/auto_trade_freeze_exit"


def _signal_manual_exit():
    try:
        with open(_AT_MANUAL_EXIT_FILE, "w") as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception:
        pass


def _check_manual_exit() -> bool:
    try:
        if os.path.exists(_AT_MANUAL_EXIT_FILE):
            os.remove(_AT_MANUAL_EXIT_FILE)
            return True
    except Exception:
        pass
    return False


def _signal_buy_more():
    try:
        with open(_AT_BUY_MORE_FILE, "w") as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception:
        pass


def _check_buy_more() -> bool:
    try:
        if os.path.exists(_AT_BUY_MORE_FILE):
            os.remove(_AT_BUY_MORE_FILE)
            return True
    except Exception:
        pass
    return False


def _freeze_exit_active() -> bool:
    """Return True when the user has frozen all automatic exit criteria."""
    return os.path.exists(_AT_FREEZE_FILE)


def _set_freeze_exit():
    try:
        with open(_AT_FREEZE_FILE, "w") as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception:
        pass


def _clear_freeze_exit():
    try:
        if os.path.exists(_AT_FREEZE_FILE):
            os.remove(_AT_FREEZE_FILE)
    except Exception:
        pass


def _write_position(data: dict | None):
    try:
        if data is None:
            payload = {}
        else:
            data["updated"] = datetime.now(timezone.utc).isoformat()
            payload = data
        import tempfile
        _fd, _tmp = tempfile.mkstemp(dir="/tmp", prefix="at_pos_", suffix=".json")
        with os.fdopen(_fd, "w") as f:
            json.dump(payload, f)
        os.replace(_tmp, _AT_POSITION_FILE)
    except Exception:
        pass


def _read_position() -> dict:
    try:
        with open(_AT_POSITION_FILE, "r") as f:
            pos = json.load(f)
        if not pos or not pos.get("status"):
            return {}
        mc = pos.get("market_close")
        if mc:
            try:
                mc_dt = pd.to_datetime(mc, utc=True)
                if datetime.now(timezone.utc) > mc_dt:
                    try:
                        os.remove(_AT_POSITION_FILE)
                    except OSError:
                        pass
                    return {}
            except Exception:
                pass
        upd = pos.get("updated")
        if upd:
            try:
                upd_dt = datetime.fromisoformat(upd)
                age = (datetime.now(timezone.utc) - upd_dt).total_seconds()
                if age > 120:
                    try:
                        os.remove(_AT_POSITION_FILE)
                    except OSError:
                        pass
                    return {}
            except Exception:
                pass
        return pos
    except Exception:
        return {}


def _read_at_settings() -> dict:
    """Read auto-trader settings from disk. Safe default: disabled."""
    try:
        with open(_AT_SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"enabled": False, "contracts": 1,
                "confidence_threshold": 0.80, "cooldown": 120}


def _write_at_settings(state: dict):
    """Persist auto-trader settings to disk so both processes stay in sync."""
    try:
        data = {
            "enabled": bool(state["enabled"][0]),
            "contracts": int(state["contracts"][0]),
            "confidence_threshold": float(state["confidence_threshold"][0]),
            "cooldown": int(state["cooldown"][0]),
            "min_edge": int(state["min_edge"][0]),
            "min_profit_margin": int(state["min_profit_margin"][0]),
            "paper_mode": bool(state["paper_mode"][0]),
            "allowed_hours": list(state["allowed_hours"][0]),
            "overnight_skip_enabled": bool(state["overnight_skip_enabled"][0]),
            "max_dd_percent": float(state["max_dd_percent"][0]),
            "kelly_fraction": float(state["kelly_fraction"][0]),
        }
        with open(_AT_SETTINGS_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


@st.cache_resource
def _auto_trader_state():
    _s = _read_at_settings()   # load from disk so UI shows current persisted state
    return {
        "enabled": [_s.get("enabled", False)],   # safe default: OFF
        "contracts": [_s.get("contracts", 1)],
        "confidence_threshold": [_s.get("confidence_threshold", 0.82)],
        "cooldown": [_s.get("cooldown", 120)],
        "min_edge": [_s.get("min_edge", 32)],
        "min_profit_margin": [_s.get("min_profit_margin", 10)],
        "paper_mode": [_s.get("paper_mode", False)],
        "allowed_hours": [_s.get("allowed_hours", [0, 1, 2, 3, 4, 22])],
        "overnight_skip_enabled": [_s.get("overnight_skip_enabled", True)],
        "max_dd_percent": [_s.get("max_dd_percent", 5.0)],
        "kelly_fraction": [_s.get("kelly_fraction", 0.65)],
        "dd_paused": [False],
        "session_pnl_cents": [0],
        "last_trade_ts": [0.0],
        "thread": [None],
        "stop_flag": [False],
        "log": collections.deque(maxlen=200),
        "lock": threading.Lock(),
        "balance_cents": [None],
        "balance_ts": [0.0],
        "status": ["idle"],
        "position_open": [False],
    }


def _time_remaining_s_for_ticker(ticker_str):
    try:
        _mr = _kalshi_get_bg(f"/markets/{ticker_str}", params={})
        if _mr and "market" in _mr:
            ct = _mr["market"].get("close_time") or _mr["market"].get("expected_expiration_time")
            if ct:
                exp = pd.to_datetime(ct, utc=True)
                return max((exp - datetime.now(timezone.utc)).total_seconds(), 0)
    except Exception:
        pass
    return 9999


def _auto_trader_loop():
    state = _auto_trader_state()
    state["status"][0] = "running"
    _loop_itr = 0
    _FAST_SLEEP = 0.25
    while not state["stop_flag"][0]:
        try:
            _loop_itr += 1
            if _loop_itr % 8 == 0:
                _s = _read_at_settings()
                with state["lock"]:
                    state["enabled"][0] = _s.get("enabled", False)
                    state["contracts"][0] = _s.get("contracts", state["contracts"][0])
                    state["confidence_threshold"][0] = _s.get("confidence_threshold", state["confidence_threshold"][0])
                    state["cooldown"][0] = _s.get("cooldown", state["cooldown"][0])
                    state["paper_mode"][0] = _s.get("paper_mode", state["paper_mode"][0])
                    state["allowed_hours"][0] = _s.get("allowed_hours", state["allowed_hours"][0])
                    state["overnight_skip_enabled"][0] = _s.get("overnight_skip_enabled", state["overnight_skip_enabled"][0])
                    state["max_dd_percent"][0] = _s.get("max_dd_percent", state["max_dd_percent"][0])
                    state["kelly_fraction"][0] = _s.get("kelly_fraction", state["kelly_fraction"][0])

            ens = get_ensemble_latest()
            pred = ens.get("prediction")
            if not pred or ens.get("status") != "live":
                time.sleep(_FAST_SLEEP)
                continue

            direction = pred.get("direction", "NEUTRAL")
            confidence = pred.get("confidence", 0.0)

            if direction == "NEUTRAL":
                time.sleep(_FAST_SLEEP)
                continue

            ens_state = _ensemble_state()
            run_count = ens_state["run_count"][0]

            if not state["enabled"][0]:
                time.sleep(_FAST_SLEEP)
                continue

            # ── Hour gate ────────────────────────────────────────────────────
            # Only trade during statistically profitable UTC hours.
            _overnight_skip_on = state["overnight_skip_enabled"][0]
            _allowed_hours = state["allowed_hours"][0]
            if _overnight_skip_on and _allowed_hours:
                _cur_hour = datetime.now(timezone.utc).hour
                if _cur_hour not in _allowed_hours:
                    _next_allowed = min(
                        (h for h in _allowed_hours if h > _cur_hour), default=min(_allowed_hours) + 24
                    )
                    state["log"].appendleft({
                        "ts": datetime.now(timezone.utc),
                        "msg": f"Hour gate: {_cur_hour:02d}:xx UTC not in allowed hours {_allowed_hours} — next at {_next_allowed % 24:02d}:00",
                        "type": "info"
                    })
                    time.sleep(30)
                    continue

            # ── Drawdown circuit breaker ─────────────────────────────────────
            if state["dd_paused"][0]:
                state["log"].appendleft({
                    "ts": datetime.now(timezone.utc),
                    "msg": "DD circuit breaker ACTIVE — auto-trader paused. Re-enable manually to reset.",
                    "type": "error"
                })
                time.sleep(10)
                continue

            now = time.time()
            if now - state["balance_ts"][0] > 30:
                bal = kalshi_get_balance()
                if bal is not None:
                    state["balance_cents"][0] = bal
                    state["balance_ts"][0] = now

            with state["lock"]:
                threshold = state["confidence_threshold"][0]
                cooldown = state["cooldown"][0]
                contracts = state["contracts"][0]

            if confidence < threshold:
                time.sleep(_FAST_SLEEP)
                continue

            _MIN_RUN = 11
            if run_count < _MIN_RUN:
                time.sleep(_FAST_SLEEP)
                continue

            if now - state["last_trade_ts"][0] < cooldown:
                time.sleep(_FAST_SLEEP)
                continue

            _open_pos = _read_position()
            _open_ticker = _open_pos.get("ticker") if _open_pos and _open_pos.get("status") else None

            dt_now = datetime.now(timezone.utc)

            bal = state["balance_cents"][0]
            if bal is not None and bal < 100 * contracts:
                entry = {"ts": datetime.now(timezone.utc), "msg": f"Insufficient balance: {bal}c", "type": "error"}
                state["log"].appendleft(entry)
                time.sleep(2)
                continue

            # Find a tradeable market: must be active and show real bid/ask prices.
            ticker = None
            yes_bid_mkt = None
            yes_ask_mkt = None

            def _mkt_cents(mkt_dict, key):
                """Read a market price field as integer cents.
                Handles both 'yes_bid' (int cents) and 'yes_bid_dollars' (str/float dollars)."""
                v = mkt_dict.get(key) or mkt_dict.get(key + "_dollars")
                if v is None:
                    return None
                try:
                    fv = float(v)
                    # ≤ 1.0 means the value is in dollars; convert to cents
                    return round(fv * 100) if fv <= 1.0 else round(fv)
                except (ValueError, TypeError):
                    return None

            for offset_min in (0, 15, 30, 45):
                candidate = build_15m_ticker(dt_now + timedelta(minutes=offset_min))
                try:
                    data = _kalshi_get_bg(f"/markets/{candidate}", params={})
                    if data and "market" in data:
                        mkt = data["market"]
                        mkt_status = (mkt.get("status") or "").lower()
                        if mkt_status not in ("open", "active", "trading"):
                            continue
                        ct = mkt.get("close_time") or mkt.get("expected_expiration_time")
                        if ct:
                            exp = pd.to_datetime(ct, utc=True)
                            if exp <= dt_now:
                                continue
                            # Require ≥5 minutes remaining — contracts near expiry
                            # have compressed delta and widen spreads
                            mins_left = (exp - dt_now).total_seconds() / 60.0
                            if mins_left < 5.0:
                                continue
                        yb = _mkt_cents(mkt, "yes_bid")
                        ya = _mkt_cents(mkt, "yes_ask")
                        if yb is None or ya is None:
                            continue   # no displayed liquidity — skip
                        if (ya - yb) > 20:
                            continue   # spread too wide (>20c) — illiquid
                        if _open_ticker and candidate == _open_ticker:
                            continue
                        ticker = candidate
                        yes_bid_mkt = int(yb)
                        yes_ask_mkt = int(ya)
                        break
                except Exception:
                    pass
            if not ticker:
                state["log"].appendleft({"ts": datetime.now(timezone.utc),
                    "msg": "No liquid market found (need bid/ask)", "type": "warn"})
                time.sleep(3)
                continue

            side = "yes" if direction == "UP" else "no"

            _is_paper_now = state["paper_mode"][0]
            if bal is None:
                if not _is_paper_now:
                    entry = {"ts": datetime.now(timezone.utc), "msg": "Balance unavailable — skipping trade", "type": "error"}
                    state["log"].appendleft(entry)
                    time.sleep(2)
                    continue
                else:
                    # Paper mode: simulate $1,000 paper balance so missing API creds don't block trading
                    bal = 100_000  # 100,000 cents = $1,000

            # ── Fresh quote right before order placement ──────────────────
            try:
                _fresh = _kalshi_get_bg(f"/markets/{ticker}", params={})
                if _fresh and "market" in _fresh:
                    _fm = _fresh["market"]
                    _fyb = _mkt_cents(_fm, "yes_bid")
                    _fya = _mkt_cents(_fm, "yes_ask")
                    if _fyb is not None and _fya is not None:
                        yes_bid_mkt = int(_fyb)
                        yes_ask_mkt = int(_fya)
            except Exception:
                pass

            spread = yes_ask_mkt - yes_bid_mkt

            if side == "yes":
                _ask_for_side = yes_ask_mkt
                _bid_for_side = yes_bid_mkt
            else:
                _ask_for_side = 100 - yes_bid_mkt
                _bid_for_side = 100 - yes_ask_mkt

            # ── Rule #0: Contrarian time-premium filter ──────────────────────
            # When the market has strong conviction (YES > 70c or YES < 30c),
            # we need more runway for a reversal to materialize.
            # Deep-value contrarian trades need ≥8 min remaining.
            # Normal uncertain trades (30-70c) only need the standard ≥5 min.
            _yes_mid = (yes_bid_mkt + yes_ask_mkt) / 2
            _is_contrarian = (side == "no" and _yes_mid > 70) or (side == "yes" and _yes_mid < 30)
            if _is_contrarian:
                try:
                    _ct_resp = _kalshi_get_bg(f"/markets/{ticker}", params={})
                    if _ct_resp and "market" in _ct_resp:
                        _ct_val = _ct_resp["market"].get("close_time") or _ct_resp["market"].get("expected_expiration_time")
                        if _ct_val:
                            _mins_left = (pd.to_datetime(_ct_val, utc=True) - datetime.now(timezone.utc)).total_seconds() / 60.0
                            if _mins_left < 8.0:
                                state["log"].appendleft({
                                    "ts": datetime.now(timezone.utc),
                                    "msg": f"Contrarian trade needs ≥8 min, only {_mins_left:.1f} left — YES={_yes_mid:.0f}c, skipping",
                                    "type": "warn"})
                                time.sleep(1)
                                continue
                except Exception:
                    pass

            # ── Rule #1: Hard cap — never pay more than 35c for any contract ──
            if _ask_for_side > 35:
                state["log"].appendleft({
                    "ts": datetime.now(timezone.utc),
                    "msg": f"Entry {_ask_for_side}c > 35c cap — skipping ({direction} on {ticker})",
                    "type": "warn"})
                time.sleep(1)
                continue

            # ── Rule #1b: Edge filter — model vs market disagreement ──────
            # Only enter when model confidence exceeds market implied
            # probability by at least min_edge points.
            # edge = (model_conf * 100) - entry_price
            _settings_now = _read_at_settings()
            _min_edge = _settings_now.get("min_edge", 55)
            _model_edge = (confidence * 100) - _ask_for_side
            if _model_edge < _min_edge:
                state["log"].appendleft({
                    "ts": datetime.now(timezone.utc),
                    "msg": f"Edge {_model_edge:.0f}c < {_min_edge}c min — model {confidence:.0%} vs mkt {_ask_for_side}c ({direction} on {ticker})",
                    "type": "warn"})
                time.sleep(1)
                continue

            # ── Rule #1c: Minimum upside filter ──────────────────────
            # Round-trip fees ~6¢/contract. For a winning prediction the
            # contract pays out 100¢, so max upside = 100 − entry − fees.
            # Skip when there isn't enough room to comfortably clear fees,
            # e.g. high entry prices where even a correct call barely profits.
            _min_profit_margin = _settings_now.get("min_profit_margin", 10)
            _rt_fee = 6
            _net_upside = (100 - _ask_for_side) - _rt_fee
            if _net_upside < _min_profit_margin:
                state["log"].appendleft({
                    "ts": datetime.now(timezone.utc),
                    "msg": f"Upside {_net_upside}c < {_min_profit_margin}c min — entry {_ask_for_side}c ({direction} on {ticker})",
                    "type": "warn"})
                time.sleep(1)
                continue

            # ── Adaptive buy pricing based on spread width ────────────────
            # Tight spread (≤5c): cross ask by 2c — fills instantly
            # Medium spread (6-12c): cross ask by 3c — need aggression to fill
            # Wide spread (13-20c): cross ask by 4c — illiquid, be aggressive
            if spread <= 5:
                _cross = 2
            elif spread <= 12:
                _cross = 3
            else:
                _cross = 4
            if side == "yes":
                buy_limit = min(yes_ask_mkt + _cross, 99)
                sell_limit = max(yes_bid_mkt - 1, 1)
            else:
                no_ask_mkt = 100 - yes_bid_mkt
                no_bid_mkt = 100 - yes_ask_mkt
                buy_limit = min(no_ask_mkt + _cross, 99)
                sell_limit = max(no_bid_mkt - 1, 1)

            # ── Rule #3: Scale contracts — 3× at ≤20c entry, 1× at 21–35c ──
            _scale = 3 if _ask_for_side <= 20 else 1
            _base_contracts = contracts * _scale

            # ── Kelly fraction position sizing ───────────────────────────────
            # Kelly f = (p*b - (1-p)) / b  where b = net_upside / entry_price
            # Size = kelly_fraction * f * bankroll / entry_price (in contracts)
            _kelly_fraction = state["kelly_fraction"][0]
            _bal_for_kelly = state["balance_cents"][0]
            if _kelly_fraction > 0 and _bal_for_kelly and _bal_for_kelly > 0 and _ask_for_side > 0:
                _b_ratio = _net_upside / _ask_for_side
                _kelly_f = (confidence * _b_ratio - (1 - confidence)) / _b_ratio if _b_ratio > 0 else 0
                _kelly_f = max(0.0, _kelly_f)
                _kelly_contracts = max(1, round(_kelly_f * _kelly_fraction * _bal_for_kelly / _ask_for_side))
                _trade_contracts = max(1, min(_base_contracts, _kelly_contracts))
            else:
                _trade_contracts = _base_contracts

            state["position_open"][0] = True
            state["last_trade_ts"][0] = time.time()
            _entry_ts = datetime.now(timezone.utc)
            _write_position({
                "status": "entering", "ticker": ticker, "direction": direction,
                "side": side, "contracts": _trade_contracts, "entry_ts": _entry_ts.isoformat(),
                "confidence": round(confidence, 3), "spread": spread,
            })

            try:
                with open("/tmp/bobby_debug.log", "a") as _lf:
                    _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] AUTO-TRADE: {direction} conf={confidence:.2f} "
                              f"run={run_count} edge={_model_edge:.0f}c "
                              f"ticker={ticker} side={side} buy_limit={buy_limit}c sell_limit={sell_limit}c "
                              f"mkt_bid={yes_bid_mkt} mkt_ask={yes_ask_mkt} spread={spread}c cross={_cross}c "
                              f"entry={_ask_for_side}c scale={_scale}x contracts={_trade_contracts}\n")
            except Exception:
                pass

            try:  # buy + launch exit thread
                _is_paper = state["paper_mode"][0]
                if _is_paper:
                    # ── Paper mode: simulate fill, no real order ─────────────
                    buy_result = None
                    buy_err = None
                    buy_order_id = f"PAPER-{int(time.time() * 1000)}"
                    buy_price = buy_limit
                    _filled_contracts = _trade_contracts
                    _buy_fee = 0
                else:
                    buy_result, buy_err = kalshi_place_order(ticker, "buy", side, _trade_contracts, price_cents=buy_limit)
                buy_order_id = None if not _is_paper else buy_order_id
                buy_price = None if not _is_paper else buy_price
                _filled_contracts = 0 if not _is_paper else _filled_contracts

                def _parse_order_fill(order_dict):
                    """Return (avg_price_cents, filled_count, fee_cents) from order response.
                    Uses the side-specific price field for accuracy, falling back to fill_cost."""
                    _fn_raw = order_dict.get("fill_count_fp") or order_dict.get("fill_count")
                    _fn = int(float(_fn_raw)) if _fn_raw else 0
                    _tf = float(order_dict.get("taker_fees_dollars") or 0)
                    _mf = float(order_dict.get("maker_fees_dollars") or 0)
                    _fee = round((_tf + _mf) * 100)
                    if _fn <= 0:
                        return None, _fn, _fee
                    _order_side = (order_dict.get("side") or "").lower()
                    _price_key = "no_price_dollars" if _order_side == "no" else "yes_price_dollars"
                    _pd = order_dict.get(_price_key)
                    if _pd is not None:
                        try:
                            return round(float(_pd) * 100), _fn, _fee
                        except (ValueError, TypeError):
                            pass
                    _fc = order_dict.get("taker_fill_cost_dollars") or order_dict.get("maker_fill_cost_dollars")
                    if _fc is not None:
                        return round(float(_fc) / _fn * 100), _fn, _fee
                    return None, _fn, _fee

                _buy_fee = 0
                if buy_result and "order" in buy_result:
                    _o = buy_result["order"]
                    buy_order_id = _o.get("order_id", "")
                    buy_price, _filled_contracts, _buy_fee = _parse_order_fill(_o)

                db_insert_auto_trade(
                    ticker=ticker, direction=direction, signal_confidence=confidence,
                    action="buy", contracts=_trade_contracts, price_cents=buy_price, order_id=buy_order_id,
                    fee_cents=_buy_fee, is_paper=_is_paper,
                )
                _paper_tag = " [PAPER]" if _is_paper else ""
                log_entry = {
                    "ts": datetime.now(timezone.utc), "ticker": ticker, "direction": direction,
                    "confidence": confidence, "action": f"buy{_paper_tag}", "contracts": _trade_contracts,
                    "price_cents": buy_price, "order_id": buy_order_id, "error": buy_err,
                    "filled": _filled_contracts,
                }
                state["log"].appendleft(log_entry)

                if not _is_paper and (buy_err or buy_order_id is None):
                    try:
                        with open("/tmp/bobby_debug.log", "a") as _f:
                            _f.write(f"[{datetime.now(timezone.utc).isoformat()}] AUTO-TRADE BUY FAILED: {buy_err}\n")
                    except Exception:
                        pass
                    state["position_open"][0] = False
                    _write_position(None)
                    time.sleep(1)
                    continue

                if _filled_contracts < _trade_contracts and buy_order_id:
                    _buy_deadline = time.time() + 6
                    while time.time() < _buy_deadline:
                        time.sleep(0.5)
                        try:
                            _bo = _kalshi_get_bg(f"/portfolio/orders/{buy_order_id}", params={})
                            if _bo and "order" in _bo:
                                _bo2 = _bo["order"]
                                _bst = (_bo2.get("status") or "").lower()
                                buy_price, _filled_contracts, _buy_fee = _parse_order_fill(_bo2)
                                if _bst in ("filled", "executed"):
                                    break
                                if _bst in ("cancelled", "expired", "closed"):
                                    break
                                if _filled_contracts >= _trade_contracts:
                                    break
                        except Exception:
                            pass
                    if _filled_contracts == 0:
                        try:
                            kalshi_cancel_order(buy_order_id)
                        except Exception:
                            pass
                        try:
                            with open("/tmp/bobby_debug.log", "a") as _f:
                                _f.write(f"[{datetime.now(timezone.utc).isoformat()}] AUTO-TRADE BUY NOT FILLED — cancelled {buy_order_id}\n")
                        except Exception:
                            pass
                        state["position_open"][0] = False
                        _write_position(None)
                        time.sleep(1)
                        continue
                    if _filled_contracts < _trade_contracts:
                        try:
                            kalshi_cancel_order(buy_order_id)
                        except Exception:
                            pass
                        try:
                            with open("/tmp/bobby_debug.log", "a") as _f:
                                _f.write(f"[{datetime.now(timezone.utc).isoformat()}] AUTO-TRADE PARTIAL FILL: {_filled_contracts}/{_trade_contracts} — proceeding with {_filled_contracts}\n")
                        except Exception:
                            pass
                        _trade_contracts = _filled_contracts

                db_update_auto_trade_price(buy_order_id, buy_price, _trade_contracts)

                _entry = buy_price or yes_ask_mkt

                _write_position({
                    "status": "filled", "ticker": ticker, "direction": direction,
                    "side": side, "contracts": _trade_contracts,
                    "entry_ts": _entry_ts.isoformat(), "entry_price": _entry,
                    "confidence": round(confidence, 3),
                })

                def _cancel_silent(order_id):
                    if order_id:
                        try:
                            kalshi_cancel_order(order_id)
                        except Exception:
                            pass

                _bound_ticker = ticker
                _bound_side = side
                _bound_contracts = _trade_contracts

                def _get_live_bid(_tk=_bound_ticker, _sd=_bound_side):
                    """Get current bid for our side in cents."""
                    try:
                        _mr = _kalshi_get_bg(f"/markets/{_tk}", params={})
                        if _mr and "market" in _mr:
                            _m = _mr["market"]
                            if _sd == "yes":
                                _b = _mkt_cents(_m, "yes_bid")
                                return _b if _b is not None else 0
                            else:
                                _ya = _mkt_cents(_m, "yes_ask")
                                return (100 - _ya) if _ya is not None else 0
                    except Exception:
                        pass
                    return 0

                def _market_buy_one(price_cents, _tk=_bound_ticker, _sd=_bound_side, _paper=_is_paper):
                    """Buy 1 extra contract. Returns (fill_price, fee_cents) or (None, 0)."""
                    if _paper:
                        # Paper mode: simulate fill at requested price, no real order
                        return price_cents, 0
                    _result, _err = kalshi_place_order(
                        _tk, "buy", _sd, 1, price_cents=price_cents)
                    if _result and "order" in _result:
                        _o = _result["order"]
                        _oid = _o.get("order_id", "")
                        _fp, _, _fe = _parse_order_fill(_o)
                        if _fp:
                            return _fp, _fe
                        if _oid:
                            _deadline = time.time() + 4
                            while time.time() < _deadline:
                                time.sleep(0.5)
                                try:
                                    _od = _kalshi_get_bg(f"/portfolio/orders/{_oid}", params={})
                                    if _od and "order" in _od:
                                        _o2 = _od["order"]
                                        _st = (_o2.get("status") or "").lower()
                                        if _st in ("filled", "executed"):
                                            _fp2, _, _fe2 = _parse_order_fill(_o2)
                                            return _fp2, _fe2
                                        if _st in ("cancelled", "expired", "closed"):
                                            break
                                except Exception:
                                    pass
                            _cancel_silent(_oid)
                    return None, 0

                def _time_remaining_s(_tk=_bound_ticker):
                    """Seconds until market close."""
                    try:
                        _mr = _kalshi_get_bg(f"/markets/{_tk}", params={})
                        if _mr and "market" in _mr:
                            ct = _mr["market"].get("close_time") or _mr["market"].get("expected_expiration_time")
                            if ct:
                                exp = pd.to_datetime(ct, utc=True)
                                return max((exp - datetime.now(timezone.utc)).total_seconds(), 0)
                    except Exception:
                        pass
                    return 9999

                def _market_sell(price_cents, count=None, _tk=_bound_ticker, _sd=_bound_side, _ct=_bound_contracts):
                    """Place an aggressive sell and poll briefly. Returns (fill_price, order_id, fee)."""
                    _use_ct = count if count is not None else _ct
                    _result, _err = kalshi_place_order(
                        _tk, "sell", _sd, _use_ct, price_cents=max(price_cents, 1))
                    if _result and "order" in _result:
                        _o = _result["order"]
                        _oid = _o.get("order_id", "")
                        _fp, _, _fe = _parse_order_fill(_o)
                        if _fp:
                            return _fp, _oid, _fe
                        if _oid:
                            _deadline = time.time() + 4
                            while time.time() < _deadline:
                                time.sleep(0.5)
                                try:
                                    _od = _kalshi_get_bg(f"/portfolio/orders/{_oid}", params={})
                                    if _od and "order" in _od:
                                        _o2 = _od["order"]
                                        _st = (_o2.get("status") or "").lower()
                                        if _st in ("filled", "executed"):
                                            _fp2, _, _fe2 = _parse_order_fill(_o2)
                                            return _fp2, _oid, _fe2
                                        if _st in ("cancelled", "expired", "closed"):
                                            break
                                except Exception:
                                    pass
                            _cancel_silent(_oid)
                            try:
                                _od2 = _kalshi_get_bg(f"/portfolio/orders/{_oid}", params={})
                                if _od2 and "order" in _od2:
                                    _o3 = _od2["order"]
                                    if (_o3.get("status") or "").lower() in ("filled", "executed"):
                                        _fp3, _, _fe3 = _parse_order_fill(_o3)
                                        return _fp3, _oid, _fe3
                            except Exception:
                                pass
                    return None, None, 0

                # ── Trailing-bid exit — runs in a daemon thread so the
                #    main loop stays free to fire on new signals ──────────
                _check_manual_exit()

                def _trailing_exit_thread(
                    _t_ticker, _t_direction, _t_side, _t_contracts, _t_entry,
                    _t_entry_ts, _t_buy_price, _t_buy_fee, _t_confidence,
                    _t_state, _t_time_remaining_fn, _t_get_live_bid_fn,
                    _t_market_sell_fn, _t_market_buy_one_fn,
                    _t_is_paper=False,
                ):
                    sell_order_id = None
                    sell_price = None
                    sell_err = None
                    _sell_fee = 0

                    _remaining = _t_time_remaining_fn()
                    _mkt_close_iso = (datetime.now(timezone.utc) + timedelta(seconds=_remaining)).isoformat() if _remaining < 9999 else None

                    _bid_high = _t_entry
                    _min_profit = 3
                    _hold_start = time.time()
                    _poll_interval = 1
                    _STALE_TIMEOUT_BASE = 60
                    _LOSING_EXIT_SECS_BASE = 90
                    _STALE_TIMEOUT = _STALE_TIMEOUT_BASE
                    _LOSING_EXIT_SECS = _LOSING_EXIT_SECS_BASE
                    _SIGNAL_CONF_HOLD = 0.65   # min confidence to keep holding
                    _SIGNAL_RUN_HOLD  = 5      # min consecutive run to extend hold
                    _signal_support   = False  # currently has model backing

                    # Clear any stale freeze flag from a previous trade
                    _clear_freeze_exit()

                    try:
                        with open("/tmp/bobby_debug.log", "a") as _lf:
                            _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] TRAIL-START: "
                                      f"entry={_t_entry}c side={_t_side} remaining={_remaining:.0f}s "
                                      f"(async thread)\n")
                    except Exception:
                        pass

                    _sell_fail_count = 0
                    _MAX_SELL_FAILS = 5
                    _ever_profitable = False

                    try:
                        while sell_price is None:
                            time.sleep(_poll_interval)

                            _remaining = _t_time_remaining_fn()
                            _held = time.time() - _hold_start
                            _bid = _t_get_live_bid_fn()

                            if _bid > _bid_high:
                                _bid_high = _bid

                            _profit = _bid - _t_entry
                            if _profit > 0:
                                _ever_profitable = True

                            # ── Live signal monitoring ────────────────────────
                            # Read the latest ensemble prediction and check
                            # whether it still supports holding this trade.
                            _live_conf = 0.0
                            _live_run  = 0
                            try:
                                _live = _read_shared_ui_state()
                                _live_pred = _live.get("prediction") or {}
                                _live_dir  = _live_pred.get("direction", "NEUTRAL")
                                _live_conf = float(_live_pred.get("confidence", 0.0))
                                _live_run  = int(_live.get("run_count", 0))
                                _live_rdir = _live.get("run_direction", "")
                                # Signal supports trade when direction + run still aligned
                                _trade_dir = _t_direction  # "UP" or "DOWN"
                                _signal_support = (
                                    _live_dir == _trade_dir
                                    and _live_conf >= _SIGNAL_CONF_HOLD
                                    and _live_rdir == _trade_dir
                                    and _live_run >= _SIGNAL_RUN_HOLD
                                )
                            except Exception:
                                _signal_support = False

                            # Extend timeouts dynamically when signal still backing us
                            if _signal_support:
                                _STALE_TIMEOUT   = min(_STALE_TIMEOUT_BASE * 3, 180)
                                _LOSING_EXIT_SECS = min(_LOSING_EXIT_SECS_BASE * 2, 180)
                            else:
                                _STALE_TIMEOUT   = _STALE_TIMEOUT_BASE
                                _LOSING_EXIT_SECS = _LOSING_EXIT_SECS_BASE

                            if _remaining < 120:
                                _trail = 2
                            elif _remaining < 300:
                                _trail = 3
                            else:
                                _trail = 5

                            _trigger = False
                            _reason = ""
                            _frozen = _freeze_exit_active()

                            if _remaining < 90:
                                # Time expiry always fires — contract about to close
                                _trigger = True
                                _reason = f"time_expiry({_remaining:.0f}s left)"
                            elif _frozen:
                                # Manual override active — skip all auto-exit criteria
                                pass
                            elif _profit >= _min_profit and _bid <= (_bid_high - _trail):
                                _trigger = True
                                _reason = f"trail(bid={_bid} peak={_bid_high} drop={_bid_high - _bid} trail={_trail})"
                            elif _profit >= 15 and _bid <= (_bid_high - 2):
                                _trigger = True
                                _reason = f"lock_big(bid={_bid} peak={_bid_high} profit={_profit})"
                            elif _held > 120 and _profit >= _min_profit and _bid <= (_bid_high - 2):
                                _trigger = True
                                _reason = f"time_pressure(held={_held:.0f}s bid={_bid} peak={_bid_high})"
                            elif _profit <= 0 and _held > _STALE_TIMEOUT and not _ever_profitable:
                                _trigger = True
                                _reason = f"stale(held={_held:.0f}s profit={_profit} never_profitable signal_support={_signal_support})"
                            elif _profit < -2 and _held > _LOSING_EXIT_SECS:
                                _trigger = True
                                _reason = f"stop_loss(held={_held:.0f}s profit={_profit} bid={_bid} signal_support={_signal_support})"

                            _write_position({
                                "status": "trailing", "ticker": _t_ticker, "direction": _t_direction,
                                "side": _t_side, "contracts": _t_contracts,
                                "entry_ts": _t_entry_ts.isoformat(), "entry_price": _t_entry,
                                "bid": _bid, "bid_high": _bid_high, "trail": _trail,
                                "profit": _profit, "remaining": round(_remaining),
                                "market_close": _mkt_close_iso,
                                "signal_support": _signal_support,
                                "signal_conf": round(_live_conf, 3) if _signal_support else None,
                                "signal_run": _live_run if _signal_support else None,
                                "exit_frozen": _frozen,
                            })

                            if _check_manual_exit():
                                _trigger = True
                                _reason = "manual_exit(user)"

                            if _check_buy_more() and not _trigger:
                                _buy_at = _bid + 2
                                _bm_price, _bm_fee = _t_market_buy_one_fn(_buy_at)
                                if _bm_price is not None:
                                    _old_total = _t_entry * _t_contracts
                                    _t_contracts += 1
                                    _t_entry = round((_old_total + _bm_price) / _t_contracts)
                                    _t_buy_price = _t_entry
                                    _t_buy_fee = (_t_buy_fee or 0) + (_bm_fee or 0)
                                    _bid_high = max(_bid_high, _bid)
                                    _ever_profitable = False
                                    _t_state["log"].appendleft({
                                        "ts": datetime.now(timezone.utc),
                                        "msg": f"Buy more +1 @ {_bm_price}¢ → avg {_t_entry}¢ x{_t_contracts}",
                                        "type": "info",
                                    })
                                    _write_position({
                                        "status": "trailing", "ticker": _t_ticker, "direction": _t_direction,
                                        "side": _t_side, "contracts": _t_contracts,
                                        "entry_ts": _t_entry_ts.isoformat(), "entry_price": _t_entry,
                                        "bid": _bid, "bid_high": _bid_high, "trail": _trail,
                                        "profit": _bid - _t_entry, "remaining": round(_remaining),
                                        "market_close": _mkt_close_iso,
                                    })
                                    try:
                                        with open("/tmp/bobby_debug.log", "a") as _lf:
                                            _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] BUY-MORE: "
                                                      f"+1 @ {_bm_price}c → avg={_t_entry}c x{_t_contracts} fee={_bm_fee}\n")
                                    except Exception:
                                        pass
                                else:
                                    _t_state["log"].appendleft({
                                        "ts": datetime.now(timezone.utc),
                                        "msg": "Buy more failed — order did not fill",
                                        "type": "warn",
                                    })

                            if not _trigger:
                                if _remaining < 60:
                                    _poll_interval = 1
                                continue

                            _sell_at = max(_bid - 1, 1)

                            try:
                                with open("/tmp/bobby_debug.log", "a") as _lf:
                                    _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] TRAIL-EXIT: "
                                              f"{_reason} sell_at={_sell_at}c entry={_t_entry}c "
                                              f"bid={_bid} peak={_bid_high} remaining={_remaining:.0f}s\n")
                            except Exception:
                                pass

                            if _t_is_paper:
                                # Paper mode: simulate sell at live bid — no real order
                                sell_price = max(_bid, 1)
                                sell_order_id = f"PAPER-SELL-{int(time.time() * 1000)}"
                                _sell_fee = 0
                            else:
                                sell_price, sell_order_id, _sell_fee = _t_market_sell_fn(_sell_at, count=_t_contracts)

                            if not _t_is_paper and sell_price is None:
                                _sell_at2 = max(_bid - 3, 1)
                                sell_price, sell_order_id, _sell_fee = _t_market_sell_fn(_sell_at2, count=_t_contracts)

                            if not _t_is_paper and sell_price is None and _remaining < 90:
                                sell_price, sell_order_id, _sell_fee = _t_market_sell_fn(1, count=_t_contracts)

                            if sell_price is None:
                                _sell_fail_count += 1
                                _bid_high = max(_bid_high - 2, _t_entry)
                                try:
                                    with open("/tmp/bobby_debug.log", "a") as _lf:
                                        _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] TRAIL-RETRY: "
                                                  f"sell failed ({_sell_fail_count}/{_MAX_SELL_FAILS}), reset peak to {_bid_high}, continuing\n")
                                except Exception:
                                    pass
                                if _sell_fail_count >= _MAX_SELL_FAILS:
                                    try:
                                        with open("/tmp/bobby_debug.log", "a") as _lf:
                                            _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] TRAIL-ABORT: "
                                                      f"max sell failures reached, market likely expired. Abandoning position.\n")
                                    except Exception:
                                        pass
                                    sell_price = 0
                                    sell_order_id = None
                                    _sell_fee = 0

                        # Always clear the freeze flag when the position closes
                        # so it cannot carry over into the next trade.
                        _clear_freeze_exit()

                        _total_fee = (_t_buy_fee or 0) + (_sell_fee or 0)
                        pnl = None
                        if _t_buy_price is not None and sell_price is not None:
                            pnl = (sell_price - _t_buy_price) * _t_contracts - _total_fee

                        try:
                            with open("/tmp/bobby_debug.log", "a") as _lf:
                                _lf.write(f"[{datetime.now(timezone.utc).isoformat()}] EXIT: "
                                          f"buy={_t_buy_price}c sell={sell_price}c pnl={pnl} "
                                          f"fee={_total_fee}c side={_t_side} x{_t_contracts} "
                                          f"sell_oid={str(sell_order_id)[:12] if sell_order_id else 'None'}\n")
                        except Exception:
                            pass

                        _sell_action = "sell [PAPER]" if _t_is_paper else "sell"
                        db_insert_auto_trade(
                            ticker=_t_ticker, direction=_t_direction, signal_confidence=_t_confidence,
                            action=_sell_action, contracts=_t_contracts, price_cents=sell_price,
                            order_id=sell_order_id, pnl_cents=pnl, fee_cents=_total_fee,
                            is_paper=_t_is_paper,
                        )
                        sell_log = {
                            "ts": datetime.now(timezone.utc), "ticker": _t_ticker, "direction": _t_direction,
                            "confidence": _t_confidence, "action": _sell_action, "contracts": _t_contracts,
                            "price_cents": sell_price, "order_id": sell_order_id, "pnl_cents": pnl, "fee_cents": _total_fee, "error": sell_err,
                        }
                        _t_state["log"].appendleft(sell_log)

                        # ── Session PnL & drawdown circuit breaker ────────────
                        if pnl is not None:
                            _t_state["session_pnl_cents"][0] = _t_state["session_pnl_cents"][0] + pnl
                            _max_dd_pct = _t_state["max_dd_percent"][0]
                            _bal_now = _t_state["balance_cents"][0]
                            if _bal_now and _bal_now > 0 and _max_dd_pct > 0:
                                _dd_threshold = -(_max_dd_pct / 100.0) * _bal_now
                                if _t_state["session_pnl_cents"][0] < _dd_threshold:
                                    _t_state["dd_paused"][0] = True
                                    _t_state["log"].appendleft({
                                        "ts": datetime.now(timezone.utc),
                                        "msg": f"DRAWDOWN CIRCUIT BREAKER: session PnL {_t_state['session_pnl_cents'][0]}c breached "
                                               f"{_max_dd_pct:.1f}% DD limit ({_dd_threshold:.0f}c). Auto-trader PAUSED.",
                                        "type": "error",
                                    })

                        _t_state["last_trade_ts"][0] = time.time()

                        if not _t_is_paper:
                            bal = kalshi_get_balance()
                            if bal is not None:
                                _t_state["balance_cents"][0] = bal
                                _t_state["balance_ts"][0] = time.time()
                    finally:
                        _t_state["position_open"][0] = False
                        _write_position(None)

                _exit_thread = threading.Thread(
                    target=_trailing_exit_thread,
                    args=(
                        ticker, direction, side, _trade_contracts, _entry,
                        _entry_ts, buy_price, _buy_fee, confidence,
                        state, _time_remaining_s, _get_live_bid,
                        _market_sell, _market_buy_one,
                        _is_paper,
                    ),
                    daemon=True,
                )
                _exit_thread.start()

            except Exception as e:
                state["position_open"][0] = False
                _write_position(None)
                state["log"].appendleft({"ts": datetime.now(timezone.utc), "msg": f"Trade error: {e}", "type": "error"})
                time.sleep(2)

        except Exception as e:
            state["log"].appendleft({"ts": datetime.now(timezone.utc), "msg": f"Error: {e}", "type": "error"})
            time.sleep(2)

        time.sleep(_FAST_SLEEP)

    state["status"][0] = "stopped"


def start_auto_trader():
    if not os.environ.get("_BG_RUNNER"):
        return
    state = _auto_trader_state()
    t = state["thread"][0]
    if t is not None and t.is_alive():
        return
    state["stop_flag"][0] = False
    t = threading.Thread(target=_auto_trader_loop, daemon=True, name="auto-trader")
    t.start()
    state["thread"][0] = t


def _staggered_startup():
    start_bg_data_collector()
    time.sleep(5)
    start_brti_ws()
    time.sleep(5)
    start_bobby_brti()
    time.sleep(5)
    start_ensemble_predictor()
    time.sleep(2)
    start_auto_trader()

if os.environ.get("_BG_RUNNER"):
    threading.Thread(target=_staggered_startup, daemon=True, name="staggered-startup").start()
    raise SystemExit(0)
else:
    def _streamlit_lightweight_startup():
        start_bg_data_collector()
        time.sleep(5)
        start_brti_ws()
    threading.Thread(target=_streamlit_lightweight_startup, daemon=True, name="streamlit-startup").start()

st.title("📊 Kalshi KXBTC vs Spot BTC — Divergence Analyzer")
st.caption(
    "Overlaying Kalshi 15-min Bitcoin YES% prices against Polygon.io spot BTC/USD to surface convergences & divergences."
)

markets = fetch_kalshi_markets()
btc_df = pd.DataFrame()

active_market = None
if markets:
    now_utc = datetime.now(timezone.utc)
    live = []
    for i, m in enumerate(markets):
        ct = m.get("close_time") or m.get("expected_expiration_time")
        if ct:
            exp = pd.to_datetime(ct, utc=True)
            if exp > now_utc:
                live.append(m)
    if not live:
        live = markets[:1]
    if live:
        best = None
        best_score = -1
        for m in live:
            vol = int(float(m.get("volume_fp", "0") or m.get("volume", 0) or "0"))
            oi = int(float(m.get("open_interest_fp", "0") or m.get("open_interest", 0) or "0"))
            try:
                yes_ask = float(m.get("yes_ask_dollars", "0") or "0")
                yes_bid = float(m.get("yes_bid_dollars", "0") or "0")
                last_p = float(m.get("last_price_dollars", "0") or "0")
                yes_p = (yes_ask + yes_bid) / 2.0 if yes_bid > 0 else (last_p if last_p > 0 else yes_ask)
                cents = int(yes_p * 100)
                atm_score = 50 - abs(50 - cents)
            except (TypeError, ValueError):
                atm_score = 0
            score = atm_score * 1000 + vol + oi
            if score > best_score:
                best_score = score
                best = m
        active_market = best or live[0]
k_count, b_count, br_count, ob_count, bb_count = db_row_counts()

col1, col2, col3, col4 = st.columns(4)
def _market_yes_pct(m):
    ask = float(m.get("yes_ask_dollars", "0") or "0")
    bid = float(m.get("yes_bid_dollars", "0") or "0")
    last = float(m.get("last_price_dollars", "0") or "0")
    if bid > 0:
        return (ask + bid) / 2.0
    return last if last > 0 else ask

if active_market:
    _yes_d = _market_yes_pct(active_market)
    _no_d = 1.0 - _yes_d
    col1.metric("Current YES %", f"{_yes_d:.1%}")
    col2.metric("Current NO %", f"{_no_d:.1%}")
    close_time = active_market.get("close_time") or active_market.get("expected_expiration_time")
    col3.metric(
        "Next Expiry",
        pd.to_datetime(close_time, utc=True).strftime("%H:%M UTC") if close_time else "—"
    )
else:
    col1.metric("Current YES %", "—")
    col2.metric("Current NO %", "—")
    col3.metric("Next Expiry", "—")
col4.metric(
    "Stored Data",
    f"{k_count:,}K · {b_count:,}B · {br_count:,}BRTI · {ob_count:,}OB",
    help="K = Kalshi candles · B = BTC candles · BRTI = live tick records · OB = order book snapshots"
)

if active_market:
    start_ob_polling(active_market["ticker"])

st.markdown(
    """
    <style>
    [data-stale] { opacity: 1 !important; transition: none !important; }
    [data-stale="true"] { opacity: 1 !important; }
    div[data-stale] > * { opacity: 1 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.fragment(run_every=3)
def _render_ensemble_tab():
    ens_info = get_ensemble_latest()
    _all_ticks = get_ensemble_ticks()
    ens_ticks = _all_ticks[-300:] if len(_all_ticks) > 300 else _all_ticks

    st.subheader("Ensemble Predictor — CNN-LSTM + Hawkes + XGBoost")

    e_status = ens_info["status"]
    e_error = ens_info["error"]
    e_pred = ens_info["prediction"]
    xgb_pred = ens_info["xgb_prediction"]

    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    if e_status == "live" and e_pred:
        dir_label = e_pred["direction"]
        dir_color = {"UP": "🟢", "DOWN": "🔴", "NEUTRAL": "🟡"}.get(dir_label, "⚪")
        sc1.metric(f"{dir_color} Prediction", dir_label,
                   delta=f"{e_pred['confidence']:.1%} confidence")
        sc2.metric("Model", e_pred["model"])
        sc3.metric("BobbyBRTI", f"${e_pred['brti']:,.2f}")
        sc4.metric("Hawkes λ", f"{e_pred['hawkes']:.3f}")
        sc5.metric("v_T", f"{e_pred['v_T']:.0f}")
        sc6.metric("Exchanges", f"{e_pred['n_exchanges']}")
    else:
        sc1.metric("Prediction", "—")
        sc2.metric("Status", e_status)
        if e_error:
            sc3.metric("Error", e_error[:30])
        else:
            sc3.metric("BobbyBRTI", "Waiting…")
        sc4.metric("Hawkes λ", "—")
        sc5.metric("v_T", "—")
        sc6.metric("Exchanges", "—")

    if e_pred:
        pc1, pc2, pc3 = st.columns(3)
        pc1.metric("P(UP)", f"{e_pred['prob_up']:.1%}" if e_pred else "—")
        pc2.metric("P(NEUTRAL)", f"{e_pred['prob_neutral']:.1%}" if e_pred else "—")
        pc3.metric("P(DOWN)", f"{e_pred['prob_down']:.1%}" if e_pred else "—")

    _es = _ensemble_state()
    _shared = _read_shared_ui_state()
    _is_local_live = _es['status'][0] == 'live'
    _t_cnn = _es['temp_cnn'][0] if _is_local_live else _shared.get('temp_cnn', 1.5)
    _t_xgb = _es['temp_xgb'][0] if _is_local_live else _shared.get('temp_xgb', 1.5)
    _last_cal = _es["temp_last_fit"][0] if _is_local_live else _shared.get('temp_last_fit', 0)
    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Temp (CNN-LSTM)", f"{_t_cnn:.3f}",
               help="Temperature T > 1 softens overconfident predictions. Recalibrated every 30 min from historical NLL.")
    tc2.metric("Temp (XGBoost)",  f"{_t_xgb:.3f}",
               help="Temperature T > 1 softens overconfident predictions. Recalibrated every 30 min from historical NLL.")
    tc3.metric("Last Calibration",
               f"{int((time.time()-_last_cal)//60)}m ago" if _last_cal else "—",
               help="How long ago the temperature was last fitted on historical predictions.")

    st.subheader("XGBoost Prediction")
    xc1, xc2, xc3, xc4 = st.columns(4)
    if xgb_pred:
        xgb_dir = xgb_pred["direction"]
        xgb_color = {"UP": "🟢", "DOWN": "🔴", "NEUTRAL": "🟡"}.get(xgb_dir, "⚪")
        xc1.metric(f"{xgb_color} Direction", xgb_dir,
                   delta=f"{xgb_pred['confidence']:.1%} confidence")
        xc2.metric("P(UP)", f"{xgb_pred['prob_up']:.1%}")
        xc3.metric("P(NEUTRAL)", f"{xgb_pred['prob_neutral']:.1%}")
        xc4.metric("P(DOWN)", f"{xgb_pred['prob_down']:.1%}")
    else:
        xc1.metric("Direction", "—")
        xc2.metric("P(UP)", "—")
        xc3.metric("P(NEUTRAL)", "—")
        xc4.metric("P(DOWN)", "—")

    # ── CNN-LSTM 10m Directional Signal ─────────────────────────────────
    st.subheader("CNN-LSTM 10-Minute Directional Signal")
    _p10m_tick = e_pred if e_pred else {}
    # DB-fallback predictions don't carry cnn_10m_* fields — patch from shared state
    if not _p10m_tick.get("cnn_10m_trained") and _shared.get("prediction"):
        _sp = _shared["prediction"]
        _p10m_tick = {**_p10m_tick, **{k: v for k, v in _sp.items() if k.startswith("cnn_10m")}}
    _cnn10m_dir   = _p10m_tick.get("cnn_10m_direction", "NEUTRAL")
    _cnn10m_conf  = _p10m_tick.get("cnn_10m_confidence", 0.0)
    _cnn10m_p_up  = _p10m_tick.get("cnn_10m_prob_up", 0.33)
    _cnn10m_p_dn  = _p10m_tick.get("cnn_10m_prob_dn", 0.33)
    _cnn10m_run   = _p10m_tick.get("cnn_10m_run_count", 0)
    _cnn10m_ready = _p10m_tick.get("cnn_10m_trained", False)
    # Fall back to shared state run count when no tick yet
    if not _cnn10m_ready:
        _cnn10m_run = _shared.get("cnn_10m_run_count", 0)
        _cnn10m_dir = _shared.get("cnn_10m_run_direction", "NEUTRAL")
    _tr_10m = _shared.get("training", {})
    _cnn10m_trains = (
        _training_state()["cnn_10m_train_count"][0] if _is_local_live
        else _tr_10m.get("cnn_10m_train_count", 0)
    )
    _cnn10m_imgs = (
        len(_training_state()["labeled_images_10m"]) if _is_local_live
        else _tr_10m.get("labeled_images_10m", 0)
    )
    c10a, c10b, c10c, c10d = st.columns(4)
    if _cnn10m_ready and _cnn10m_dir != "NEUTRAL":
        _c10_icon = "🟢" if _cnn10m_dir == "UP" else "🔴"
        c10a.metric(f"{_c10_icon} 10m Direction", _cnn10m_dir,
                    delta=f"{_cnn10m_conf:.1%} confidence")
    elif _cnn10m_ready:
        c10a.metric("🟡 10m Direction", "NEUTRAL",
                    delta=f"{_cnn10m_conf:.1%} confidence")
    else:
        c10a.metric("⏳ 10m Direction", "Warming up…",
                    delta=f"{_cnn10m_imgs}/{_TRAIN_MIN_SAMPLES + _CNN_SEQ_LEN} labels")
    c10b.metric("P(UP)", f"{_cnn10m_p_up:.1%}" if _cnn10m_ready else "—")
    c10c.metric("P(DOWN)", f"{_cnn10m_p_dn:.1%}" if _cnn10m_ready else "—")
    c10d.metric("Run Length", str(_cnn10m_run) if _cnn10m_ready else "—",
                help="Consecutive ticks with same 10m directional signal")
    st.caption(
        f"Separate CNN-LSTM trained exclusively on 10-minute forward-price labels. "
        f"Trains: **{_cnn10m_trains}** · Image samples: **{_cnn10m_imgs:,}** · "
        f"Same DeepLOB architecture as 10s model but optimised for longer-horizon trend detection. "
        f"Begins training once {_TRAIN_MIN_SAMPLES + _CNN_SEQ_LEN} labeled images accumulate (~10 hours)."
    )

    # ── Magnitude Predictor ──────────────────────────────────────────────
    st.subheader("10-Minute Move Magnitude")
    _mag_pred = ens_info.get("magnitude_prediction")
    _mag_tr   = _shared.get("training", {}) if not _is_local_live else {}
    _mag_train_count = (
        _training_state()["magnitude_train_count"][0] if _is_local_live
        else _mag_tr.get("magnitude_train_count", 0)
    )
    _mag_samples_10m = (
        len(_training_state()["labeled_magnitude_10m"]) if _is_local_live
        else _mag_tr.get("labeled_magnitude_10m", 0)
    )
    _mag_mae = (
        _training_state()["magnitude_accuracy"][0] if _is_local_live
        else _mag_tr.get("magnitude_accuracy")
    )
    _mag_10m_imgs = (
        len(_training_state()["labeled_images_10m"]) if _is_local_live
        else _mag_tr.get("labeled_images_10m", 0)
    )
    st.caption(
        "XGBRegressor predicting the signed 10-minute forward return. "
        "Positive = expected price increase; negative = expected decrease. "
        f"Magnitude model trains every 5 min once ≥50 samples resolve. "
        f"10m CNN images: **{_mag_10m_imgs:,}** · Magnitude samples: **{_mag_samples_10m:,}** · "
        f"Trains: **{_mag_train_count}** · "
        + (f"MAE: **{_mag_mae:.1f} bps**" if _mag_mae else "MAE: **pending**")
    )
    if _mag_pred:
        _mag_ret = _mag_pred.get("return_10m", 0.0)
        _mag_pct = _mag_pred.get("pct", 0.0)
        _mag_bps = _mag_pred.get("bps", 0.0)
        _mag_arrow = "📈" if _mag_ret > 0 else ("📉" if _mag_ret < 0 else "➡️")
        _mag_sign  = "+" if _mag_ret > 0 else ""
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric(
            f"{_mag_arrow} Predicted Move",
            f"{_mag_sign}{_mag_pct:.4f}%",
            delta=f"{_mag_sign}{_mag_bps:.1f} bps",
            delta_color="normal",
        )
        mc2.metric("In $ (at BRTI)", f"{_mag_sign}${abs(_mag_ret) * e_pred['brti']:,.0f}" if e_pred else "—")
        mc3.metric("Direction", "UP" if _mag_ret > 0 else ("DOWN" if _mag_ret < 0 else "FLAT"))
        mc4.metric("Magnitude Trains", _mag_train_count if _mag_train_count > 0 else "⏳ building")
        if abs(_mag_bps) < 1.0:
            st.caption("⚠️ Move too small to be meaningful — model still accumulating 10-min labeled data.")
    else:
        st.info(
            "Magnitude predictor warming up — needs ≥50 samples resolved at the 10-minute horizon "
            "(approximately 10 minutes of live runtime). Check back soon.",
            icon=None
        )

    # ── Multi-Timeframe XGBoost ─────────────────────────────────────────
    st.subheader("Multi-Timeframe XGBoost (15s · 1 min)")
    st.caption(
        "Two separate XGBoost models trained on 15s and 60s forward price labels. "
        "Predictions are display-only — not wired to the auto-trader. "
        "Outcomes are logged to the DB for accuracy analysis."
    )

    _p15_pred = ens_info.get("xgb_15s_prediction")
    _p60_pred = ens_info.get("xgb_60s_prediction")

    _mtf_col_a, _mtf_col_b = st.columns(2)

    def _render_mtf_card(col, label, pred):
        with col:
            st.markdown(f"**{label}**")
            if pred:
                _dir = pred.get("direction", "?")
                _conf = pred.get("confidence", 0.0)
                _pu = pred.get("prob_up", 0.0)
                _pn = pred.get("prob_neutral", 0.0)
                _pd_ = pred.get("prob_down", 0.0)
                _clr = {"UP": "🟢", "DOWN": "🔴", "NEUTRAL": "🟡"}.get(_dir, "⚪")
                mc1, mc2, mc3, mc4 = st.columns(4)
                mc1.metric(f"{_clr} Direction", _dir, delta=f"{_conf:.1%} conf")
                mc2.metric("P(UP)",     f"{_pu:.1%}")
                mc3.metric("P(NEUTRAL)",f"{_pn:.1%}")
                mc4.metric("P(DOWN)",   f"{_pd_:.1%}")
            else:
                st.info("Waiting for first training cycle — need ≥50 labeled samples at this horizon.", icon=None)

    _render_mtf_card(_mtf_col_a, "🕐 15-second horizon", _p15_pred)
    _render_mtf_card(_mtf_col_b, "🕐 1-minute horizon",  _p60_pred)

    # MTF training stats
    _shared_for_mtf = _read_shared_ui_state() if not _is_local_live else {}
    _mtf_tr = _shared_for_mtf.get("training", {}) if not _is_local_live else {}
    if _is_local_live:
        _tr_live2 = _training_state()
        _mtf_15s_count = _tr_live2["xgb_15s_train_count"][0]
        _mtf_60s_count = _tr_live2["xgb_60s_train_count"][0]
        _mtf_15s_acc   = _tr_live2["xgb_15s_accuracy"][0]
        _mtf_60s_acc   = _tr_live2["xgb_60s_accuracy"][0]
        _mtf_15s_rows  = len(_tr_live2["labeled_tabular_15s"])
        _mtf_60s_rows  = len(_tr_live2["labeled_tabular_60s"])
    else:
        _mtf_15s_count = _mtf_tr.get("xgb_15s_train_count", 0)
        _mtf_60s_count = _mtf_tr.get("xgb_60s_train_count", 0)
        _mtf_15s_acc   = _mtf_tr.get("xgb_15s_accuracy")
        _mtf_60s_acc   = _mtf_tr.get("xgb_60s_accuracy")
        _mtf_15s_rows  = _mtf_tr.get("labeled_tabular_15s", 0)
        _mtf_60s_rows  = _mtf_tr.get("labeled_tabular_60s", 0)

    _ms1, _ms2, _ms3, _ms4 = st.columns(4)
    _ms1.metric("15s Trains",   _mtf_15s_count,
                delta=f"acc {_mtf_15s_acc:.1%}" if _mtf_15s_acc else "pending")
    _ms2.metric("15s Samples",  _mtf_15s_rows)
    _ms3.metric("1m Trains",    _mtf_60s_count,
                delta=f"acc {_mtf_60s_acc:.1%}" if _mtf_60s_acc else "pending")
    _ms4.metric("1m Samples",   _mtf_60s_rows)

    # Live accuracy from DB
    if DATABASE_URL:
        @st.cache_data(ttl=60)
        def _fetch_mtf_accuracy():
            conn = _db_conn()
            if not conn:
                return None
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT
                            COUNT(*) FILTER (WHERE resolved_15s AND pred_15s_dir = actual_15s_dir) AS c15_correct,
                            COUNT(*) FILTER (WHERE resolved_15s) AS c15_total,
                            COUNT(*) FILTER (WHERE resolved_60s AND pred_60s_dir = actual_60s_dir) AS c60_correct,
                            COUNT(*) FILTER (WHERE resolved_60s) AS c60_total
                           FROM xgb_mtf_predictions"""
                    )
                    row = cur.fetchone()
                return row
            except Exception:
                return None
            finally:
                conn.close()

        _acc_row = _fetch_mtf_accuracy()
        if _acc_row:
            _c15_corr, _c15_tot, _c60_corr, _c60_tot = _acc_row
            _acc_a, _acc_b = st.columns(2)
            with _acc_a:
                if _c15_tot and _c15_tot > 0:
                    _acc15 = _c15_corr / _c15_tot
                    st.metric("DB Accuracy — 15s",
                              f"{_acc15:.1%}",
                              delta=f"{_c15_corr}/{_c15_tot} resolved",
                              delta_color="normal")
                else:
                    st.metric("DB Accuracy — 15s", "—", delta="no resolved rows yet")
            with _acc_b:
                if _c60_tot and _c60_tot > 0:
                    _acc60 = _c60_corr / _c60_tot
                    st.metric("DB Accuracy — 1m",
                              f"{_acc60:.1%}",
                              delta=f"{_c60_corr}/{_c60_tot} resolved",
                              delta_color="normal")
                else:
                    st.metric("DB Accuracy — 1m", "—", delta="no resolved rows yet")

    st.divider()

    # ── Signal Monitor ─────────────────────────────────────────────────
    ind = ens_info.get("indicators") or {}
    run_count = int(ind.get("run_count", 0))
    run_dir   = ind.get("run_dir", "NONE")
    rsi14     = float(ind.get("rsi_14", 50.0))
    rsi7      = float(ind.get("rsi_7",  50.0))
    rsi21     = float(ind.get("rsi_21", 50.0))
    vol30     = float(ind.get("vol_30", 0.0))
    vol60     = float(ind.get("vol_60", 0.0))
    vwap_d    = float(ind.get("vwap_dev", 0.0))
    imb       = float(ind.get("imbalance", 0.0))
    imb_vel   = float(ind.get("imbalance_velocity", 0.0))
    dr1       = float(ind.get("depth_ratio_1", 1.0))

    st.subheader("Signal Monitor")

    g1, g2, g3 = st.columns(3)

    run_pct  = min(run_count / 11, 1.0)
    dir_clr  = {"UP": "#4CAF50", "DOWN": "#F44336"}.get(run_dir, "#FFC107")
    run_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=run_count,
        title={"text": f"Signal Run ({run_dir})", "font": {"size": 13}},
        number={"suffix": "/11", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 11], "tickcolor": "#666"},
            "bar": {"color": dir_clr},
            "bgcolor": "#1E2130",
            "steps": [
                {"range": [0, 7],  "color": "#1E2130"},
                {"range": [7, 10], "color": "#2a2d3e"},
                {"range": [10, 11],"color": "#2d3548"},
            ],
            "threshold": {"line": {"color": dir_clr, "width": 3}, "thickness": 0.85, "value": 11},
        },
    ))
    run_fig.update_layout(height=230, margin=dict(l=20, r=20, t=50, b=10),
                          paper_bgcolor="#0E1117", font_color="#FAFAFA")
    with g1:
        _show_chart(run_fig)

    rsi_clr = "#4CAF50" if 40 < rsi14 < 65 else ("#FF9800" if rsi14 >= 65 else "#F44336")
    rsi_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rsi14,
        title={"text": "RSI-14 (1s BRTI)", "font": {"size": 13}},
        number={"font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#666"},
            "bar": {"color": rsi_clr},
            "bgcolor": "#1E2130",
            "steps": [
                {"range": [0,  30],  "color": "#3d1f1f"},
                {"range": [30, 70],  "color": "#1E2130"},
                {"range": [70, 100], "color": "#3d2e1f"},
            ],
            "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.8, "value": rsi14},
        },
    ))
    rsi_fig.update_layout(height=230, margin=dict(l=20, r=20, t=50, b=10),
                          paper_bgcolor="#0E1117", font_color="#FAFAFA")
    with g2:
        _show_chart(rsi_fig)

    vol_bps   = vol30 * 10000
    if vol_bps < 0.5:
        vol_label, vol_clr = "FLAT", "#F44336"
    elif vol_bps < 3.0:
        vol_label, vol_clr = "TRENDING", "#4CAF50"
    else:
        vol_label, vol_clr = "CHOPPY", "#FF9800"
    vol_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(vol_bps, 2),
        title={"text": f"Vol-30s ({vol_label})", "font": {"size": 13}},
        number={"suffix": " bps", "font": {"size": 18}},
        gauge={
            "axis": {"range": [0, 6], "tickcolor": "#666"},
            "bar": {"color": vol_clr},
            "bgcolor": "#1E2130",
            "steps": [
                {"range": [0,   0.5], "color": "#3d1f1f"},
                {"range": [0.5, 3.0], "color": "#1E2130"},
                {"range": [3.0, 6.0], "color": "#3d2e1f"},
            ],
        },
    ))
    vol_fig.update_layout(height=230, margin=dict(l=20, r=20, t=50, b=10),
                          paper_bgcolor="#0E1117", font_color="#FAFAFA")
    with g3:
        _show_chart(vol_fig)

    # ── Indicator tiles ─────────────────────────────────────────────────
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    t1.metric("RSI-7",  f"{rsi7:.1f}",
              delta="overbought" if rsi7 > 70 else ("oversold" if rsi7 < 30 else "neutral"),
              delta_color="inverse" if rsi7 > 70 else ("inverse" if rsi7 < 30 else "off"))
    t2.metric("RSI-21", f"{rsi21:.1f}",
              delta="overbought" if rsi21 > 70 else ("oversold" if rsi21 < 30 else "neutral"),
              delta_color="inverse" if rsi21 > 70 else ("inverse" if rsi21 < 30 else "off"))
    t3.metric("Vol-60s", f"{vol60*10000:.2f} bps")
    t4.metric("VWAP Dev", f"{vwap_d*100:+.3f}%",
              delta="above" if vwap_d > 0 else "below",
              delta_color="normal" if vwap_d > 0 else "inverse")
    t5.metric("Imbalance", f"{imb:+.3f}",
              delta=f"Δvel {imb_vel:+.3f}",
              delta_color="normal" if imb_vel > 0 else "inverse")
    t6.metric("Depth Ratio", f"{dr1:.2f}x",
              delta="bid-heavy" if dr1 > 1.1 else ("ask-heavy" if dr1 < 0.9 else "balanced"),
              delta_color="normal" if dr1 > 1.1 else ("inverse" if dr1 < 0.9 else "off"))

    # ── Entry Gate Checklist ────────────────────────────────────────────
    st.markdown("**Entry Gate Status**")
    conf_val = e_pred["confidence"] if e_pred else 0.0
    auto_cfg = {}
    try:
        with open("auto_trade_settings.json") as _f:
            auto_cfg = json.load(_f)
    except Exception:
        pass
    conf_thresh = float(auto_cfg.get("confidence_threshold", 0.80))

    gates = [
        ("Run ≥11 consecutive",  run_count >= 11,   f"{run_count}/11 {run_dir}"),
        (f"Conf ≥{conf_thresh:.0%}",  conf_val >= conf_thresh, f"{conf_val:.1%}" if e_pred else "—"),
        ("Imbalance building",    abs(imb) > 0.05,  f"{imb:+.3f}"),
        ("Imbalance accelerating",abs(imb_vel) > 0.01, f"Δ{imb_vel:+.3f}"),
    ]
    gc = st.columns(len(gates))
    for col, (label, passing, detail) in zip(gc, gates):
        icon  = "✅" if passing else "❌"
        color = "#1a3a1a" if passing else "#3a1a1a"
        col.markdown(
            f'<div style="background:{color};border-radius:6px;padding:6px 8px;'
            f'font-size:0.75rem;text-align:center;">'
            f'<b>{icon} {label}</b><br><span style="color:#aaa;">{detail}</span></div>',
            unsafe_allow_html=True,
        )

    # ── Feature contribution bar chart ──────────────────────────────────
    with st.expander("Feature Contribution Breakdown", expanded=False):
        feat_names = [
            "RSI-7", "RSI-14", "RSI-21",
            "Vol-30s (bps)", "Vol-60s (bps)",
            "VWAP Dev (%)", "Imbalance",
            "Imbal Velocity", "Depth Ratio",
            "Hawkes λ", "BRTI Ret-5s", "BRTI Ret-10s",
        ]
        feat_vals = [
            rsi7 - 50, rsi14 - 50, rsi21 - 50,
            vol30 * 10000, vol60 * 10000,
            vwap_d * 100,
            imb * 100, imb_vel * 100,
            (dr1 - 1.0) * 10,
            float(ind.get("hawkes", 0.0)) * 10,
            float(ind.get("brti_ret_5", 0.0)) * 10000,
            float(ind.get("brti_ret_10", 0.0)) * 10000,
        ]
        bar_clrs = ["#4CAF50" if v > 0 else "#F44336" for v in feat_vals]
        feat_fig = go.Figure(go.Bar(
            x=feat_vals, y=feat_names,
            orientation="h",
            marker_color=bar_clrs,
            text=[f"{v:+.3f}" for v in feat_vals],
            textposition="outside",
        ))
        feat_fig.add_vline(x=0, line=dict(color="white", width=1, dash="dash"), opacity=0.5)
        feat_fig.update_layout(
            height=380,
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            margin=dict(l=120, r=60, t=20, b=20),
            xaxis_title="Scaled contribution (positive = bullish bias)",
            showlegend=False,
        )
        _show_chart(feat_fig, width="stretch")

    st.divider()

    if len(ens_ticks) > 1:
        edf = pd.DataFrame(ens_ticks)
        edf["ts"] = pd.to_datetime(edf["ts"])

        efig = go.Figure()

        efig.add_trace(go.Scatter(
            x=edf["ts"], y=edf["brti"], name="BobbyBRTI",
            line=dict(color="#00BCD4", width=2),
            hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>",
        ))

        up_mask = edf["direction"] == "UP"
        down_mask = edf["direction"] == "DOWN"
        neutral_mask = edf["direction"] == "NEUTRAL"

        if up_mask.any():
            efig.add_trace(go.Scatter(
                x=edf.loc[up_mask, "ts"], y=edf.loc[up_mask, "brti"],
                mode="markers", name="UP",
                marker=dict(color="#4CAF50", size=6, symbol="triangle-up"),
                hovertemplate="%{x}<br>UP %{y:,.2f}<extra></extra>",
            ))
        if down_mask.any():
            efig.add_trace(go.Scatter(
                x=edf.loc[down_mask, "ts"], y=edf.loc[down_mask, "brti"],
                mode="markers", name="DOWN",
                marker=dict(color="#F44336", size=6, symbol="triangle-down"),
                hovertemplate="%{x}<br>DOWN %{y:,.2f}<extra></extra>",
            ))
        if neutral_mask.any():
            efig.add_trace(go.Scatter(
                x=edf.loc[neutral_mask, "ts"], y=edf.loc[neutral_mask, "brti"],
                mode="markers", name="NEUTRAL",
                marker=dict(color="#FFC107", size=4, symbol="diamond"),
                hovertemplate="%{x}<br>NEUTRAL %{y:,.2f}<extra></extra>",
            ))

        efig.update_layout(
            height=450,
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=60, r=30, t=40, b=30),
            title="BobbyBRTI + Prediction Direction",
        )
        efig.update_yaxes(title_text="USD", gridcolor="#1E2130")
        efig.update_xaxes(gridcolor="#1E2130")

        _show_chart(efig, width="stretch")

        st.divider()

        st.subheader("Prediction History")
        show_df = edf[["ts", "brti", "direction", "confidence", "model", "hawkes",
                       "prob_up", "prob_neutral", "prob_down", "v_T", "n_exchanges"]].copy()
        show_df["ts"] = show_df["ts"].apply(
            lambda x: x.strftime("%H:%M:%S UTC") if hasattr(x, "strftime") else str(x))
        show_df["brti"] = show_df["brti"].apply(
            lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
        show_df["confidence"] = show_df["confidence"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "—")
        show_df["hawkes"] = show_df["hawkes"].apply(
            lambda x: f"{x:.3f}" if pd.notna(x) else "—")
        show_df["prob_up"] = show_df["prob_up"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "—")
        show_df["prob_neutral"] = show_df["prob_neutral"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "—")
        show_df["prob_down"] = show_df["prob_down"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "—")
        show_df.columns = ["Time", "BobbyBRTI", "Direction", "Confidence", "Model",
                           "Hawkes λ", "P(UP)", "P(NEUTRAL)", "P(DOWN)", "v_T", "Exchanges"]
        st.dataframe(show_df.tail(100).iloc[::-1], width="stretch", hide_index=True)
    else:
        _tick_shared_status = _read_shared_ui_state().get("status")
        if _tick_shared_status == "live":
            st.info("Loading prediction history…")
        else:
            st.info("Ensemble predictor is starting up — waiting for BobbyBRTI data from 3+ exchanges. "
                    "Predictions will appear here every second once live.")

    st.divider()

    st.subheader("Online Training Status")
    tr = _training_state()
    _shared_tr = _read_shared_ui_state().get("training", {})
    _is_display_only = not os.environ.get("_BG_RUNNER")
    _use_shared = _is_display_only and bool(_shared_tr)
    if _use_shared:
        total_samples = _shared_tr.get("total_samples", 0)
        pending_count = _shared_tr.get("pending_count", 0)
        labeled_tab = _shared_tr.get("labeled_tabular", 0)
        labeled_img = _shared_tr.get("labeled_images", 0)
        labeled_img_10m = _shared_tr.get("labeled_images_10m", 0)
        xgb_trains = _shared_tr.get("xgb_train_count", 0)
        cnn_trains = _shared_tr.get("cnn_train_count", 0)
        cnn_10m_trains = _shared_tr.get("cnn_10m_train_count", 0)
        xgb_acc = _shared_tr.get("xgb_accuracy")
        cnn_loss_val = _shared_tr.get("cnn_loss")
        cnn_10m_loss_val = _shared_tr.get("cnn_10m_loss")
        last_xgb_str = _shared_tr.get("last_xgb_train")
        last_cnn_str = _shared_tr.get("last_cnn_train")
        last_cnn_10m_str = _shared_tr.get("last_cnn_10m_train")
        last_xgb = datetime.fromisoformat(last_xgb_str) if last_xgb_str else None
        last_cnn = datetime.fromisoformat(last_cnn_str) if last_cnn_str else None
        last_cnn_10m = datetime.fromisoformat(last_cnn_10m_str) if last_cnn_10m_str else None
    else:
        with tr["lock"]:
            total_samples = tr["total_samples"][0]
            pending_count = len(tr["pending"])
            labeled_tab = len(tr["labeled_tabular"])
            labeled_img = len(tr["labeled_images"])
            labeled_img_10m = len(tr["labeled_images_10m"])
            xgb_trains = tr["xgb_train_count"][0]
            cnn_trains = tr["cnn_train_count"][0]
            cnn_10m_trains = tr["cnn_10m_train_count"][0]
            xgb_acc = tr["xgb_accuracy"][0]
            cnn_loss_val = tr["cnn_loss"][0]
            cnn_10m_loss_val = tr["cnn_10m_loss"][0]
            last_xgb = tr["last_xgb_train"][0]
            last_cnn = tr["last_cnn_train"][0]
            last_cnn_10m = tr["last_cnn_10m_train"][0]

    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Labeled Samples", f"{total_samples:,}",
               delta=f"{pending_count} pending",
               help=f"Tabular: {labeled_tab:,} · Image (10s): {labeled_img:,} · Image (10m): {labeled_img_10m:,}")
    tc2.metric("XGBoost Trains", f"{xgb_trains}",
               delta=f"acc: {xgb_acc:.1%}" if xgb_acc is not None else "waiting for data")
    tc3.metric("CNN-LSTM 10s Trains", f"{cnn_trains}",
               delta=f"loss: {cnn_loss_val:.4f}" if cnn_loss_val is not None else "waiting for data")
    tc4.metric("CNN-LSTM 10m Trains", f"{cnn_10m_trains}",
               delta=f"loss: {cnn_10m_loss_val:.4f}" if cnn_10m_loss_val is not None else f"need {labeled_img_10m}/{_TRAIN_MIN_SAMPLES + _CNN_SEQ_LEN} img")

    if last_xgb:
        age_xgb = (datetime.now(timezone.utc) - last_xgb).total_seconds()
        t_col1, t_col2, t_col3 = st.columns(3)
        t_col1.caption(f"XGB last train: {age_xgb:.0f}s ago")
        if last_cnn:
            age_cnn = (datetime.now(timezone.utc) - last_cnn).total_seconds()
            t_col2.caption(f"CNN-10s last train: {age_cnn:.0f}s ago")
        if last_cnn_10m:
            age_cnn_10m = (datetime.now(timezone.utc) - last_cnn_10m).total_seconds()
            t_col3.caption(f"CNN-10m last train: {age_cnn_10m:.0f}s ago")
        else:
            t_col3.caption(f"CNN-10m: collecting labels ({labeled_img_10m} so far)…")
    else:
        st.caption(f"Need {_TRAIN_MIN_SAMPLES}+ samples to begin training")

    if total_samples > 0:
        st.progress(min(total_samples / _TRAIN_MIN_SAMPLES, 1.0),
                   text=f"Training data: {total_samples}/{_TRAIN_MIN_SAMPLES} samples"
                   if total_samples < _TRAIN_MIN_SAMPLES
                   else f"Training active — {total_samples:,} tabular · {labeled_img:,} image (10s) · {labeled_img_10m:,} image (10m)")

    st.divider()
    st.caption(
        "**Architecture**: Dual CNN-LSTM — 10s horizon (fast) + 10m horizon (slow) run in parallel · "
        "XGBoost (fast path for low v_T) · Hawkes process (event intensity) · "
        "Auto-switch: XGBoost when v_T ≤ 30, CNN-LSTM blend when v_T > 30 · "
        "Deep inference every 1s · **Online training**: 10s model uses tick labels; 10m model uses 10-min labels · "
        f"XGBoost retrains every {_TRAIN_XGB_INTERVAL}s · CNN-LSTM retrains every {_TRAIN_CNN_INTERVAL}s · "
        "Models: brti_xgboost.pkl / brti_cnn_lstm.pth (10s) / brti_cnn_lstm_10m.pth (10m)"
    )

    st.divider()
    st.subheader("🤖 Auto-Trading")

    at_state = _auto_trader_state()

    _disk_settings = _read_at_settings()
    _disk_enabled = _disk_settings.get("enabled", False)
    at_state["enabled"][0] = _disk_enabled

    if not KALSHI_AUTH_READY:
        st.warning("Kalshi API credentials not configured — auto-trading unavailable.")
    else:
        at_col1, at_col2, at_col3 = st.columns([1, 1, 2])
        with at_col1:
            at_enabled = st.toggle("Enable Auto-Trading", value=_disk_enabled, key="at_enable_toggle")
            at_state["enabled"][0] = at_enabled
        with at_col2:
            _paper_default = bool(_disk_settings.get("paper_mode", True))
            at_paper = st.toggle("Paper Mode (no real orders)", value=_paper_default, key="at_paper_toggle")
            at_state["paper_mode"][0] = at_paper

        with at_col3:
            at_status = at_state["status"][0]
            if at_status == "idle":
                _sh_status = _read_shared_ui_state().get("auto_trader_status")
                if _sh_status and _sh_status != "idle":
                    at_status = _sh_status
            at_status = at_status or "monitoring"
            _ens_s = _ensemble_state()
            _run_cnt = _ens_s["run_count"][0]
            _run_dir = _ens_s["run_direction"][0]
            if _run_cnt == 0 and not _run_dir:
                _sh = _read_shared_ui_state()
                _run_cnt = _sh.get("run_count", 0)
                _run_dir = _sh.get("run_direction", "")
            if _run_cnt == 0 and not _run_dir:
                _run_cnt, _run_dir = _db_run_count()
            _run_str = f" · Run: **{_run_cnt}/11** {_run_dir}" if _run_dir and _run_dir != "NEUTRAL" else ""
            _pos_headline = _read_position()
            _paper_tag = " · **PAPER MODE**" if at_paper else " · **LIVE MODE**"
            # Check if hour gate is currently blocking
            _oh_on = _disk_settings.get("overnight_skip_enabled", True)
            _ah_now = _disk_settings.get("allowed_hours", [0, 1, 2, 3, 4, 22])
            _cur_utc_hr = datetime.now(timezone.utc).hour
            _hour_blocked = _oh_on and _ah_now and (_cur_utc_hr not in _ah_now)
            _hour_tag = f" · ⏱ Hour gate blocking ({_cur_utc_hr:02d}:xx UTC — allowed: {_ah_now})" if _hour_blocked else ""
            if at_enabled:
                if _pos_headline and _pos_headline.get("status"):
                    _pha = _pos_headline["status"]
                    _pha_short = {"entering": "Entering", "filled": "Filled", "trailing": "Trailing"}.get(_pha, _pha)
                    st.info(f"Status: **{at_status}** · Position **{_pha_short}**{_run_str}{_paper_tag}")
                elif _hour_blocked:
                    st.warning(f"Status: **{at_status}** · Monitoring signals{_run_str}{_paper_tag}{_hour_tag}")
                else:
                    st.success(f"Status: **{at_status}** · Monitoring signals{_run_str}{_paper_tag}")
            else:
                st.caption(f"Status: **{at_status}** · Disabled{_paper_tag}")

        # ── Drawdown circuit breaker status ──────────────────────────────
        _dd_paused = at_state.get("dd_paused", [False])[0]
        _sess_pnl = at_state.get("session_pnl_cents", [0])[0]
        if _dd_paused:
            _dd_col1, _dd_col2 = st.columns([3, 1])
            with _dd_col1:
                st.error(f"⛔ DRAWDOWN CIRCUIT BREAKER ACTIVE — Session PnL: {_sess_pnl:+d}¢. Re-enable to reset and resume.")
            with _dd_col2:
                if st.button("Reset DD & Resume", key="at_dd_reset"):
                    at_state["dd_paused"][0] = False
                    at_state["session_pnl_cents"][0] = 0
        elif _sess_pnl != 0:
            st.caption(f"Session PnL: {_sess_pnl:+d}¢ · DD limit: {_disk_settings.get('max_dd_percent', 5.0):.1f}%")

        ac1, ac2, ac3, ac4, ac5 = st.columns(5)
        with ac1:
            at_contracts = st.slider("Contracts per trade", 1, 10, int(_disk_settings.get("contracts", 1)), key="at_contracts")
            at_state["contracts"][0] = at_contracts
        with ac2:
            at_conf = st.slider("Confidence threshold", 50, 99,
                                int(_disk_settings.get("confidence_threshold", 0.82) * 100), key="at_confidence")
            at_state["confidence_threshold"][0] = at_conf / 100.0
        with ac3:
            at_cd = st.slider("Cooldown (sec)", 1, 300, int(_disk_settings.get("cooldown", 30)), key="at_cooldown")
            at_state["cooldown"][0] = at_cd
        with ac4:
            at_edge = st.slider("Min edge (model−market)", 0, 80, int(_disk_settings.get("min_edge", 32)), key="at_edge")
            at_state["min_edge"][0] = at_edge
        with ac5:
            at_margin = st.slider("Min margin (bid−ask)", 0, 30, int(_disk_settings.get("min_profit_margin", 10)), key="at_margin")
            at_state["min_profit_margin"][0] = at_margin

        ac6, ac7, ac8 = st.columns(3)
        with ac6:
            at_kelly = st.slider("Kelly fraction", 10, 100,
                                 int(_disk_settings.get("kelly_fraction", 0.65) * 100), key="at_kelly")
            at_state["kelly_fraction"][0] = at_kelly / 100.0
        with ac7:
            at_max_dd = st.slider("Max drawdown %", 1, 20,
                                  int(_disk_settings.get("max_dd_percent", 5.0)), key="at_max_dd")
            at_state["max_dd_percent"][0] = float(at_max_dd)
        with ac8:
            _oh_default = bool(_disk_settings.get("overnight_skip_enabled", True))
            at_hour_gate = st.toggle("Hour gate", value=_oh_default, key="at_hour_gate")
            at_state["overnight_skip_enabled"][0] = at_hour_gate
            _ah = _disk_settings.get("allowed_hours", [0, 1, 2, 3, 4, 22])
            at_state["allowed_hours"][0] = _ah
            if at_hour_gate:
                st.caption(f"Allowed UTC hours: {_ah}")

        st.caption(
            "Entry rules: ≥11 consecutive signals · conf ≥ threshold · edge ≥ min · "
            "upside ≥ min margin (100−entry−6¢ fees) · "
            "entry ≤ 35¢ · spread ≤ 20¢ · ≥5 min remaining · 3× scale if ≤20¢ · "
            "Kelly fraction sizes contracts by bankroll · "
            "Hour gate blocks trades outside allowed UTC hours · "
            "DD circuit breaker pauses after session loss exceeds max% · "
            "contrarian trades (YES >70¢ or <30¢) need ≥8 min remaining · "
            "Exit: trailing bid (5¢/3¢/2¢ trail tightens near close)"
        )

        _write_at_settings(at_state)

        bal_age = time.time() - at_state["balance_ts"][0]
        if bal_age > 30 or at_state["balance_cents"][0] is None:
            fresh_bal = kalshi_get_balance()
            if fresh_bal is not None:
                at_state["balance_cents"][0] = fresh_bal
                at_state["balance_ts"][0] = time.time()

        bal_cents = at_state["balance_cents"][0]
        if bal_cents is not None:
            st.metric("Kalshi Balance", f"${bal_cents / 100:.2f}")
        else:
            st.caption("Balance: fetching…")

        # ── OB Depth Signal panel ─────────────────────────────────────────
        st.subheader("📊 OB Depth Signal (Market Maker Positioning)")

        _ds_latest = get_depth_signal_latest()
        _ds_history = get_depth_signal_history()

        # Fall back to DB if in-memory is empty (fresh restart)
        if not _ds_history:
            _ds_df_fb = db_load_depth_signal_history(lookback_mins=120)
            if not _ds_df_fb.empty:
                _ds_history = _ds_df_fb.to_dict("records")
                if not _ds_latest and _ds_history:
                    _ds_latest = _ds_history[0]

        _sig_colors = {
            "HEAVY_ASK":  ("#14532d", "🟢"),  # dark green — market heavily short YES
            "ASK_LEAN":   ("#166534", "🟩"),
            "BALANCED":   ("#374151", "⬜"),
            "BID_LEAN":   ("#7c2d12", "🟧"),
            "HEAVY_BID":  ("#7f1d1d", "🔴"),
        }
        _sig_labels = {
            "HEAVY_ASK": "HEAVY ASK — Market makers flooding YES supply",
            "ASK_LEAN":  "ASK LEAN — Moderate excess supply on YES",
            "BALANCED":  "BALANCED — Even depth on both sides",
            "BID_LEAN":  "BID LEAN — Moderate excess demand for YES",
            "HEAVY_BID": "HEAVY BID — Strong demand pressure on YES",
        }

        if _ds_latest:
            _ratio  = _ds_latest.get("ask_to_bid_ratio") or 0.0
            _sig    = _ds_latest.get("signal", "BALANCED")
            _bid_d  = _ds_latest.get("bid_depth", 0)
            _ask_d  = _ds_latest.get("ask_depth", 0)
            _bb     = _ds_latest.get("best_bid_cents") or 0.0
            _ba     = _ds_latest.get("best_ask_cents") or 0.0
            _ts_ds  = _ds_latest.get("ts")

            _col_hex, _col_emoji = _sig_colors.get(_sig, ("#374151", "⬜"))
            _sig_lbl = _sig_labels.get(_sig, _sig)

            ds_c1, ds_c2, ds_c3, ds_c4 = st.columns(4)
            with ds_c1:
                st.metric("Ask:Bid Depth Ratio", f"{_ratio:.2f}×",
                          delta=_sig.replace("_", " "),
                          delta_color="off")
            with ds_c2:
                st.metric("YES Bid Depth", f"{int(_bid_d):,}")
            with ds_c3:
                st.metric("YES Ask Depth", f"{int(_ask_d):,}")
            with ds_c4:
                st.metric("Mid (¢)", f"{(_bb + _ba) / 2:.1f}¢" if _bb and _ba else "—")

            st.markdown(
                f"<div style='background:{_col_hex};padding:6px 12px;border-radius:6px;"
                f"color:white;font-weight:600;font-size:0.9rem'>"
                f"{_col_emoji} {_sig_lbl}</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Interpretation: HIGH ask:bid ratio means market makers are heavily supplying YES "
                "(net short). When the ensemble model also signals the same direction as a net-long "
                "YES position, the depth imbalance adds confirmation of potential mispricing."
            )
        else:
            st.caption("Depth signal: warming up — first snapshot in ~60s after restart.")

        # Mini chart of ratio history
        if _ds_history:
            _ds_chart_rows = []
            for _r in reversed(_ds_history):
                _rts = _r.get("ts")
                _rrat = _r.get("ask_to_bid_ratio")
                if _rts is not None and _rrat is not None:
                    _rts_dt = pd.to_datetime(_rts, utc=True) if not isinstance(_rts, datetime) else _rts
                    _ds_chart_rows.append({"Time": _rts_dt, "Ask:Bid Ratio": float(_rrat),
                                           "Signal": _r.get("signal", "BALANCED")})
            if _ds_chart_rows:
                _ds_chart_df = pd.DataFrame(_ds_chart_rows).set_index("Time").sort_index()
                _ds_chart_df = _ds_chart_df.tail(120)
                st.line_chart(_ds_chart_df[["Ask:Bid Ratio"]], height=140,
                              use_container_width=True)
                # Threshold reference caption
                st.caption(
                    "Thresholds: >3.0 = HEAVY ASK · 1.5–3.0 = ASK LEAN · "
                    "0.67–1.5 = BALANCED · 0.33–0.67 = BID LEAN · <0.33 = HEAVY BID"
                )

        # Accuracy table (from resolved DB rows)
        with st.expander("Signal Accuracy (resolved outcomes)", expanded=False):
            _acc_df = db_load_depth_signal_history(lookback_mins=14400)  # last 10 days
            if not _acc_df.empty:
                _resolved = _acc_df[_acc_df["resolved"] == True].copy()
                if not _resolved.empty and "future_brti_5m" in _resolved.columns:
                    _resolved = _resolved.dropna(subset=["brti_at_capture", "future_brti_5m"])
                    if not _resolved.empty:
                        _resolved["move_5m"] = (
                            (_resolved["future_brti_5m"] - _resolved["brti_at_capture"])
                            / _resolved["brti_at_capture"] * 100
                        )
                        _resolved["move_10m"] = (
                            (_resolved["future_brti_10m"] - _resolved["brti_at_capture"])
                            / _resolved["brti_at_capture"] * 100
                        ).where(_resolved["future_brti_10m"].notna())
                        _acc_tbl = (
                            _resolved.groupby("signal")
                            .agg(
                                n=("signal", "count"),
                                avg_move_5m=("move_5m", "mean"),
                                pct_up_5m=("move_5m", lambda x: (x > 0).mean() * 100),
                                avg_move_10m=("move_10m", "mean"),
                                pct_up_10m=("move_10m", lambda x: (x > 0).mean() * 100),
                            )
                            .reset_index()
                        )
                        _acc_tbl.columns = [
                            "Signal", "N", "Avg Move 5m (%)", "% BTC Up 5m",
                            "Avg Move 10m (%)", "% BTC Up 10m",
                        ]
                        for _col in ["Avg Move 5m (%)", "% BTC Up 5m",
                                     "Avg Move 10m (%)", "% BTC Up 10m"]:
                            _acc_tbl[_col] = _acc_tbl[_col].round(2)
                        st.dataframe(_acc_tbl, hide_index=True, use_container_width=True)
                        st.caption(
                            "HEAVY_ASK = market makers net short YES. "
                            "If 'Avg Move 5m' is positive when HEAVY_ASK, "
                            "it means YES historically moves up after heavy ask supply — "
                            "the market overshot the ask side."
                        )
                    else:
                        st.caption("No resolved rows yet — needs 11+ minutes of history.")
                else:
                    st.caption("Resolving future prices… check back in ~15 minutes.")
            else:
                st.caption("No history in DB yet — logging started.")

        _pos = _read_position()
        if _pos and _pos.get("status"):
            st.subheader("📍 Active Position")
            _ps = _pos["status"]
            _phase_labels = {
                "entering": "🟡 Placing buy order…",
                "filled": "🟢 Buy filled — starting trail",
                "trailing": "📈 Trailing bid",
            }
            _phase_text = _phase_labels.get(_ps, _ps)

            _live_bid_now = None
            _live_ask_now = None
            _pos_ticker = _pos.get("ticker")
            _pos_side = _pos.get("side")
            if _pos_ticker and _pos_side:
                try:
                    _lm = _kalshi_get(f"/markets/{_pos_ticker}", params={})
                    if _lm and "market" in _lm:
                        _lmkt = _lm["market"]
                        _lyb = _lmkt.get("yes_bid")
                        _lya = _lmkt.get("yes_ask")
                        if _lyb is not None and _lya is not None:
                            _lyb = int(float(_lyb) * 100) if float(_lyb) <= 1.0 else int(_lyb)
                            _lya = int(float(_lya) * 100) if float(_lya) <= 1.0 else int(_lya)
                            if _pos_side == "yes":
                                _live_bid_now = _lyb
                                _live_ask_now = _lya
                            else:
                                _live_bid_now = 100 - _lya
                                _live_ask_now = 100 - _lyb
                except Exception:
                    pass

            _entry_p = _pos.get("entry_price")
            _pnl_now = None
            _n_contracts = _pos.get("contracts", 1)
            if _live_bid_now is not None and _entry_p is not None:
                _pnl_now = (_live_bid_now - _entry_p) * _n_contracts

            _pc1, _pc2, _pc3, _pc4, _pc5 = st.columns(5)
            with _pc1:
                st.metric("Direction", f"{_pos.get('direction', '?')} ({_pos_side or '?'})")
            with _pc2:
                st.metric("Entry Price", f"{_entry_p}¢" if _entry_p is not None else "?")
            with _pc3:
                if _live_bid_now is not None and _entry_p is not None:
                    _delta = _live_bid_now - _entry_p
                    st.metric("Live Bid", f"{_live_bid_now}¢", delta=f"{_delta:+d}¢")
                else:
                    st.metric("Live Bid", "—")
            with _pc4:
                st.metric("Contracts", _n_contracts)
            with _pc5:
                if _pnl_now is not None:
                    st.metric("Unrealized PnL", f"{_pnl_now:+d}¢", delta=f"${_pnl_now/100:+.2f}")
                else:
                    st.metric("Unrealized PnL", "—")

            _pc6, _pc7, _pc8, _pc9 = st.columns(4)
            with _pc6:
                _ets = _pos.get("entry_ts")
                if _ets:
                    try:
                        _et = datetime.fromisoformat(_ets)
                        _held = (datetime.now(timezone.utc) - _et).total_seconds()
                        st.metric("Held", f"{_held:.0f}s")
                    except Exception:
                        st.metric("Held", "—")
                else:
                    st.metric("Held", "—")
            with _pc7:
                st.metric("Exit Phase", _phase_text)
            with _pc8:
                _bh = _pos.get("bid_high")
                _tr = _pos.get("trail")
                if _bh is not None and _tr is not None:
                    st.metric("Peak / Trail", f"{_bh}¢ / -{_tr}¢")
                else:
                    st.metric("Peak / Trail", "—")
            with _pc9:
                _mc = _pos.get("market_close")
                if _mc:
                    try:
                        _mct = pd.to_datetime(_mc, utc=True)
                        _tr_live = max((_mct - datetime.now(timezone.utc)).total_seconds(), 0)
                        _m, _s = divmod(int(_tr_live), 60)
                        st.metric("Mkt Closes In", f"{_m}m {_s}s")
                    except Exception:
                        st.metric("Mkt Closes In", "—")
                else:
                    st.metric("Mkt Closes In", "—")

            if _ps == "trailing":
                _pb = _pos.get("bid", 0)
                _pbh = _pos.get("bid_high", 0)
                _ptr = _pos.get("trail", 5)
                _pprofit = _pos.get("profit", 0)
                _trigger_at = max(_pbh - _ptr, 0)
                st.caption(f"Bid: {_pb}¢ · Peak: {_pbh}¢ · Sells at ≤{_trigger_at}¢ · Profit: {_pprofit:+d}¢/contract")

                # Freeze / signal-support status banners
                _exit_frozen_now = _pos.get("exit_frozen", False)
                if _exit_frozen_now:
                    st.warning(
                        "⛔ **Manual override active** — all auto-exit rules are suspended "
                        "(trail, stop-loss, stale). Only contract expiry (<90s) or "
                        "**Exit Now** will close the position.",
                        icon=None
                    )
                else:
                    _ssup = _pos.get("signal_support", False)
                    _sconf = _pos.get("signal_conf")
                    _srun  = _pos.get("signal_run")
                    if _ssup and _sconf is not None:
                        st.success(
                            f"🟢 **Signal holding:** model still {_pos.get('direction','?')} · "
                            f"conf {_sconf:.0%} · run {_srun} — stale/stop-loss timeouts extended",
                            icon=None
                        )
                    else:
                        st.info("⚪ No active signal support — standard exit timeouts apply", icon=None)

            _exit_frozen_now = _pos.get("exit_frozen", False) if _ps == "trailing" else False
            _exit_col1, _exit_col2, _exit_col3, _exit_col4 = st.columns([1, 1, 1, 2])
            with _exit_col1:
                if st.button("🚪 Exit Now", type="primary", key="manual_exit_btn"):
                    _signal_manual_exit()
                    st.toast("Manual exit signal sent — will sell within seconds.", icon="🚪")
            with _exit_col2:
                _buy_label = f"➕ Buy +1 @ {_live_ask_now}¢" if _live_ask_now is not None else "➕ Buy +1"
                if st.button(_buy_label, key="buy_more_btn"):
                    _signal_buy_more()
                    st.toast("Buy-more signal sent — 1 contract will be added on next poll cycle (~2s).", icon="➕")
            with _exit_col3:
                if _exit_frozen_now:
                    if st.button("▶ Resume Auto-Exit", key="unfreeze_exit_btn"):
                        _clear_freeze_exit()
                        st.toast("Auto-exit rules resumed.", icon="▶")
                        st.rerun()
                else:
                    if st.button("⛔ Freeze Auto-Exit", key="freeze_exit_btn"):
                        _set_freeze_exit()
                        st.toast("Auto-exit frozen — only you or expiry will close this trade.", icon="⛔")
                        st.rerun()
            with _exit_col4:
                _ask_txt = f"Ask: {_live_ask_now}¢" if _live_ask_now is not None else ""
                _bid_txt = f"Bid: {_live_bid_now}¢" if _live_bid_now is not None else ""
                st.caption(f"Exit sells at bid · Buy More buys 1 at ask · Freeze suspends all auto-exit rules · {_bid_txt} / {_ask_txt}")

            st.caption(f"Ticker: {_pos.get('ticker', '?')} · Updated: {_pos.get('updated', '?')}")

        st.subheader("Trade Log")

        recent_errors = [e for e in list(at_state["log"])[:10] if e.get("type") == "error"]
        if recent_errors:
            for err in recent_errors[:3]:
                ts_str = err["ts"].strftime("%H:%M:%S") if hasattr(err.get("ts"), "strftime") else ""
                st.warning(f"{ts_str} — {err.get('msg', 'Unknown error')}")

        db_trades = db_load_auto_trades(50)
        if db_trades:
            tdf = pd.DataFrame(db_trades)
            tdf["ts"] = pd.to_datetime(tdf["ts"]).dt.strftime("%H:%M:%S")
            tdf["signal_confidence"] = tdf["signal_confidence"].apply(lambda x: f"{x:.1%}" if x else "—")
            tdf["price_cents"] = tdf["price_cents"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "—")
            tdf["pnl_cents"] = tdf["pnl_cents"].apply(lambda x: f"{int(x):+d}" if pd.notna(x) else "—")
            tdf["fee_cents"] = tdf["fee_cents"].apply(lambda x: f"{int(x)}" if pd.notna(x) and x else "—")
            tdf["order_id"] = tdf["order_id"].apply(lambda x: str(x)[:8] if pd.notna(x) else "—")
            tdf.columns = ["Time", "Ticker", "Direction", "Confidence", "Action", "Contracts", "Price (¢)", "Order ID", "PnL (¢)", "Fee (¢)"]
            st.dataframe(tdf[["Time", "Ticker", "Direction", "Confidence", "Action", "Contracts", "Price (¢)", "PnL (¢)", "Fee (¢)", "Order ID"]], hide_index=True, width="stretch")
        else:
            st.caption("No trades yet.")

_render_ensemble_tab()



@st.fragment(run_every=30)
def _auto_refresh_data():
    """Periodic cache-clear + status indicator — clears cached REST data so
    the UI picks up fresh rows written by the background data collector."""
    if auto_refresh:
        st.cache_data.clear()
    bg_state = _bg_data_state()
    with bg_state["lock"]:
        btc_ts = bg_state["last_btc_ts"][0]
        kal_ts = bg_state["last_kalshi_ts"][0]
    parts = []
    if bg_data_is_running():
        parts.append("BG collector: ✅ running")
    else:
        parts.append("BG collector: ❌ stopped")
    if btc_ts:
        age = (datetime.now(timezone.utc) - btc_ts).total_seconds()
        parts.append(f"BTC last saved: {age:.0f}s ago")
    if kal_ts:
        age = (datetime.now(timezone.utc) - kal_ts).total_seconds()
        parts.append(f"Kalshi last saved: {age:.0f}s ago")
    st.caption(" · ".join(parts))

_auto_refresh_data()
