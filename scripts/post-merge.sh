#!/bin/bash
set -e

echo "Running post-merge setup..."

python3 - <<'PYEOF'
import os, psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    print("No DATABASE_URL — skipping DB migrations")
    exit(0)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS auto_trades (
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
    pnl_cents INTEGER
)
""")

conn.commit()
conn.close()
print("DB migrations complete.")
PYEOF

echo "Post-merge setup complete."
