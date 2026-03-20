# Database Restore Guide

The full PostgreSQL database is stored as a compressed pg_dump split across 7 parts.

## How to restore

### 1. Reassemble the parts
```bash
cat db_chunk_aa db_chunk_ab db_chunk_ac db_chunk_ad db_chunk_ae db_chunk_af db_chunk_ag > markets_db.dump
```

### 2. Restore into your PostgreSQL database
```bash
pg_restore --clean --no-owner --no-acl -d "$DATABASE_URL" markets_db.dump
```

## Tables included

| Table | Description |
|---|---|
| `book_image_snapshots` | 51k order-book depth images (500-level bid/ask) for CNN-LSTM training — 847MB uncompressed |
| `bobby_brti_ticks` | BobbyBRTI aggregated price ticks with volatility + correlation |
| `training_samples` | 666k+ labeled tabular samples for XGBoost |
| `ensemble_predictions` | Historical CNN-LSTM + XGBoost predictions with confidence |
| `kalshi_orderbook` | Kalshi KXBTC contract order book snapshots |
| `brti_ticks` | Raw BTC/USD price ticks (222k+ rows) |
| `btc_prices` | BTC OHLCV candlestick history |
| `auto_trades` | Kalshi auto-trade execution log |
| `kalshi_depth_signal` | Order book depth ratio signal history |
| `xgb_mtf_predictions` | Multi-timeframe XGBoost predictions (15s + 60s) |
| `kalshi_candlesticks` | Kalshi contract candlestick data |

## Notes
- Dump: `pg_dump --format=custom --compress=9` (PostgreSQL 16)
- Uncompressed: ~1.3 GB  |  Compressed: ~159 MB  |  7 chunks x 24MB
