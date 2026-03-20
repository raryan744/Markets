# Database Restore Guide

The full PostgreSQL database is stored as a compressed pg_dump split across 4 parts.

## How to restore

### 1. Reassemble the parts
```bash
cat markets_db.part_aa markets_db.part_ab markets_db.part_ac markets_db.part_ad > markets_db.dump
```

### 2. Restore into your PostgreSQL database
```bash
pg_restore --clean --no-owner --no-acl -d "$DATABASE_URL" markets_db.dump
```

Or if you want to restore into a specific database:
```bash
pg_restore --clean --no-owner --no-acl -d "postgresql://user:pass@host/dbname" markets_db.dump
```

## Tables included

| Table | Description |
|---|---|
| `book_image_snapshots` | 51k order-book depth images (500-level bid/ask, float32) used for CNN-LSTM training |
| `bobby_brti_ticks` | BobbyBRTI aggregated price ticks with volatility + correlation metrics |
| `training_samples` | 666k+ labeled tabular training samples for XGBoost |
| `ensemble_predictions` | Historical CNN-LSTM + XGBoost ensemble predictions with confidence scores |
| `kalshi_orderbook` | Kalshi KXBTC contract order book snapshots |
| `brti_ticks` | Raw BTC/USD price ticks (222k+ rows) |
| `btc_prices` | BTC OHLCV candlestick history |
| `auto_trades` | Kalshi auto-trade execution log |
| `kalshi_depth_signal` | Order book depth ratio signal history |
| `xgb_mtf_predictions` | Multi-timeframe XGBoost predictions (15s + 60s horizons) |
| `kalshi_candlesticks` | Kalshi contract candlestick data |

## Notes
- Dump created with `pg_dump --format=custom --compress=9` (PostgreSQL 16)
- Original uncompressed size: ~1.3 GB
- Compressed dump size: ~159 MB
