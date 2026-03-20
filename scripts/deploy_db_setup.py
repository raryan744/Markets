#!/usr/bin/env python3
import os, sys

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    print("No DATABASE_URL — skipping DB setup")
    sys.exit(0)

import psycopg2

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

tables = [
    """CREATE TABLE IF NOT EXISTS auto_trades (
        id SERIAL PRIMARY KEY,
        ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        ticker TEXT,
        direction TEXT,
        signal_confidence FLOAT,
        action TEXT,
        contracts INTEGER,
        price_cents INTEGER,
        order_id TEXT,
        client_order_id TEXT,
        pnl_cents INTEGER,
        fee_cents INTEGER
    )""",
    """CREATE TABLE IF NOT EXISTS ensemble_predictions (
        id SERIAL PRIMARY KEY,
        ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        brti DOUBLE PRECISION,
        v_t DOUBLE PRECISION,
        c_t DOUBLE PRECISION,
        hawkes DOUBLE PRECISION,
        direction TEXT,
        confidence DOUBLE PRECISION,
        model TEXT,
        prob_down DOUBLE PRECISION,
        prob_neutral DOUBLE PRECISION,
        prob_up DOUBLE PRECISION,
        n_exchanges INTEGER,
        brti_return DOUBLE PRECISION,
        xgb_prob_up DOUBLE PRECISION,
        xgb_prob_down DOUBLE PRECISION,
        xgb_conf DOUBLE PRECISION
    )""",
    """CREATE TABLE IF NOT EXISTS training_samples (
        id SERIAL PRIMARY KEY,
        ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        features JSONB,
        label INTEGER
    )""",
    """CREATE TABLE IF NOT EXISTS xgb_mtf_predictions (
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
    )""",
    """CREATE TABLE IF NOT EXISTS kalshi_depth_signal (
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
    )""",
]

for ddl in tables:
    try:
        cur.execute(ddl)
    except Exception as e:
        print(f"Warning: {e}")
        conn.rollback()

conn.commit()
conn.close()
print("DB setup complete.")
