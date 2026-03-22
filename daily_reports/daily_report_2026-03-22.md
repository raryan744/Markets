# Daily Evidence Report — 2026-03-22

**Generated:** 2026-03-22 00:18:33 UTC
**Repository:** https://github.com/raryan744/Markets

---

## Auto-Trade Settings

```json
{
  "enabled": false,
  "contracts": 1,
  "confidence_threshold": 0.82,
  "cooldown": 30,
  "min_edge": 32,
  "min_profit_margin": 1,
  "paper_mode": true,
  "allowed_hours": [
    0,
    1,
    2,
    3,
    4,
    22
  ],
  "overnight_skip_enabled": true,
  "max_dd_percent": 5.0,
  "kelly_fraction": 0.65
}
```

---

## Active Threads

```
  - MainThread (daemon=False, alive=True)
  - keep-alive (daemon=True, alive=True)
  - staggered-startup (daemon=True, alive=True)
  - Thread-1 (_bg_data_loop) (daemon=True, alive=True)
  - github-auto-push (daemon=True, alive=True)
```

---

## Running Processes

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
runner       1  5.8  0.1 1269844 41344 ?       Ssl  00:18   0:00 /usr/local/bin/pid1
runner      27  0.0  0.0   7640  3840 ?        S    00:18   0:00 bash -c python3 background_runner.py & streamlit run app.py --server.port 5000 --server.enableCORS false --server.enableXsrfProtection false
runner      28 52.2  0.4 974008 142144 ?       Sl   00:18   0:03 python3 background_runner.py
runner      29 58.0  0.2 475608 96476 ?        Sl   00:18   0:04 /nix/store/flbj8bq2vznkcwss7sm0ky8rd0k6kar7-python-wrapped-0.1.0/bin/python3 /home/runner/workspace/.pythonlibs/bin/streamlit run app.py --server.port 5000 --server.enableCORS false --server.enableXsrfProtection false
runner      55 25.0  0.0  11172  4736 ?        R    00:18   0:00 ps aux

```

---

## Database State

```
Tables: auto_trades, bobby_brti_ticks, book_image_snapshots, brti_ticks, btc_prices, ensemble_predictions, kalshi_candlesticks, kalshi_depth_signal, kalshi_orderbook, paper_trader_log, training_samples, xgb_mtf_predictions

  auto_trades: 419 rows
  bobby_brti_ticks: 587759 rows
  book_image_snapshots: 3552 rows
  brti_ticks: 344817 rows
  btc_prices: 10944 rows
  ensemble_predictions: 307259 rows
  kalshi_candlesticks: 2141 rows
  kalshi_depth_signal: 0 rows
  kalshi_orderbook: 52930 rows
  paper_trader_log: 690 rows
  training_samples: 199197 rows
  xgb_mtf_predictions: 3664 rows

```

---

## Environment Variables (safe subset)

```
  DATABASE_URL=ep-young-boat-ak2ta5v2.c-3.us-west-2.aws.neon.tech/neondb?sslmode=require
  HOME=/home/runner
  PATH=/nix/store/4a6vvmvfm41qkpv5vwl0n6ac1af22qnc-ztoc-0.1.0/bin:/nix/store/6d497pvkcidpdicsy0srpsmx48l3144p-gobject-introspection-wrapped-1.84.0-dev/bin:/nix/store/d667kdfbfn17905f7kmdl33r9gvwzaji-pkg-config-wrapper-0.29.2/bin:/nix/store/zbydgvn9gypb3vg88mzydn88ky6cibaz-dbus-1.14.10/bin:/nix/store/6bymzja2kc2kvpx8r8vhmgmj8g47p8ss-gdk-pixbuf-2.42.12-dev/bin:/nix/store/88zx26jgcxgl6abfvakbv3phrywkl339-gdk-pixbuf-2.42.12/bin:/nix/store/flpfkdzbac7071xlydh8f4qqq6dvnzx9-gettext-0.22.5/bin:/nix/store/ygri5mmqmril5ll9lhawa01faa2qhdvd-cargo-1.86.0/bin:/nix/store/w9qijf113qkgqcv54ydhbjh0rlslysbr-freetype-2.13.3-dev/bin:/nix/store/y0n9h3hcv2wfp2rv03ii862lhycx5wij-glib-2.84.3-dev/bin:/nix/store/9sjxbq6k58fcrxrjdi6wwdbxa2ivs4fg-gtk+3-3.24.49-dev/bin:/nix/store/ddap6dm3fjdm0zmw4m3rls73a0gml3xd-zstd-1.5.7-bin/bin:/nix/store/cmv326slnswzsjm2sqgbz16hzzqvkfjy-xz-5.8.1-bin/bin:/nix/store/gzlgwyd3n4r17yyx7hrrlpkmplqianbl-openssl-3.4.1-bin/bin:/nix/store/ynlnyy6rn70kvzamy3b40bp3qlz70mn0-ffmpeg-full-7.1.1-bin/bin:/nix/store/28z6bx9sg0lsr7wra22pbjsk6fzfphy4-bzip2-1.0.8-bin/bin:/nix/store/jl5pd089fd6ciars6gpsg48hh2h97nqd-git-with-svn-2.49.0/bin:/nix/store/wbv7b4dc17n1azxan5m5mm07fifai44a-zstd-1.5.7/bin:/nix/store/zgfr10jz12gpfxn5n4mlblxxknv8f19v-libtiff-4.7.0-bin/bin:/nix/store/3d1gd74i76bhlxr249lmm9cv5bq30aqd-fribidi-1.0.16/bin:/nix/store/jrmf65p7pn32f0hxlg2qxj99s8sw2038-cups-2.4.11-dev/bin:/nix/store/m9rqkx8s9a45wivak202kiw7p11xp6n5-libwebp-1.5.0/bin:/nix/store/i2c4lj0hirk7i27xgib08zy0rdrkfi70-libpng-apng-1.6.46-dev/bin:/nix/store/f9zdz15l2zd408yq7a3bgrj593kpwjqx-rustc-wrapper-1.86.0/bin:/nix/store/llqrkvzn5f08iwlq4xqy5av5mppgp7yp-brotli-1.1.0/bin:/nix/store/8xj3g825qwj894bxafa8h98scxxyvxps-libdeflate-1.23/bin:/nix/store/jfpaxm9dvrrv3xsdbz5y3myj7sxkp7hj-pango-1.56.3-bin/bin:/nix/store/shh4106z91l7cx93zk1m8mrwkb5ykwhd-qhull-2020.2/bin:/nix/store/i8ls8rz7c56ipdqwkr3c1lcpr30kh77m-fontconfig-2.16.0-bin/bin:/nix/store/p4c8g2fhfabnkx8rm4ng8radkh83h7ba-cairo-1.18.2-dev/bin:/nix/store/yfrv3rw3w96wxvgfga55dpb291v2x7cl-harfbuzz-10.2.0-dev/bin:/nix/store/dll7gaqkvw597jim01q7rpbsx2dzhsr0-graphite2-1.3.14/bin:/nix/store/6x7s7vfydrik42pk4599sm1jcqxmi1qp-gtk+3-3.24.49/bin:/nix/store/231d6mmkylzr80pf30dbywa9x9aryjgy-dbus-1.14.10-lib/bin:/nix/store/si92b84j9mqr3zshc8l78b7liq98sldc-cups-2.4.11/bin:/nix/store/bqppwwi9g8nzbk0b6hq6fwkqnwd06y63-tcl-8.6.15/bin:/nix/store/75qdpfrkxkj0c64qnjjn51cawi84xr30-ghostscript-with-X-10.05.1/bin:/nix/store/lrrj9h7h1ifbdv82rrbddxracm5jjxwx-libjpeg-turbo-3.0.4-bin/bin:/nix/store/bd7z19f32ww73wlrkpqdcma7ra67hs82-expat-2.7.1-dev/bin:/nix/store/3ybnl9nq86s7jz0i8pzqlrabjgdxzrjz-glib-2.84.3-bin/bin:/nix/store/lpspyskfibz1b27c4914p2qipgpm1rva-tk-8.6.15/bin:/home/runner/workspace/.pythonlibs/bin:/nix/store/flbj8bq2vznkcwss7sm0ky8rd0k6kar7-python-wrapped-0.1.0/bin:/nix/store/xwg0ddq9mjf6ibwdvp93jsp0cf51z3xr-pip-wrapper/bin:/nix/store/ypy3l3k428kc1kmcw090wlbxi8vj1m8l-poetry-wrapper/bin:/nix/store/6m2322jq0rkfdnv6cm3dq8437djbfv1l-uv-0.9.5/bin:/nix/store/bgwr5i8jf8jpg75rr53rz3fqv5k8yrwp-postgresql-16.10/bin:/nix/store/gi3n1mvycj13x8bs2x90fj9p0wr2z11f-pid1/bin:/nix/store/6h39ipxhzp4r5in5g4rhdjz7p7fkicd0-replit-runtime-path/bin:/home/runner/.nix-profile/bin:/home/runner/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  PGDATABASE=neondb
  PGHOST=ep-young-boat-ak2ta5v2.c-3.us-west-2.aws.neon.tech
  PGPORT=5432
  PYTHONPATH=/nix/store/y50fwh2sha400s38m12psfxpvk2c8w39-sitecustomize/lib/python/site-packages:/nix/store/sqs1z4grvym0nv6r3ksdc990m8sr5wgx-python3.11-pip-25.0.1/lib/python3.11/site-packages
  REPLIT_DB_URL=NOT SET
  REPLIT_DEV_DOMAIN=35f20cd7-3230-421e-88f9-3a48005150d4-00-b62fgqjp8ckw.kirk.replit.dev
  REPLIT_DOMAINS=market-divergence-analysis.replit.app
  REPL_ID=35f20cd7-3230-421e-88f9-3a48005150d4
  REPL_OWNER=PsyBob
  REPL_SLUG=workspace
```

---

## Workspace File Inventory

```
  .gitignore: 273 bytes, modified 2026-03-20 00:07:42
  .replit: 1,195 bytes, modified 2026-03-19 17:21:23
  ALL_SKILL_DOCUMENTS.md: 633,206 bytes, modified 2026-03-20 07:31:18
  APPLICATION_LOGS.log: 12,754 bytes, modified 2026-03-20 07:31:44
  CONVERSATION_RECORD.md: 15,054 bytes, modified 2026-03-20 07:37:42
  EVIDENCE_PACKAGE.md: 15,359 bytes, modified 2026-03-20 07:30:09
  SKILLS_PRIMARY.md: 257,193 bytes, modified 2026-03-20 07:31:26
  SKILLS_SECONDARY.md: 376,275 bytes, modified 2026-03-20 07:31:26
  SYSTEM_FAILURE_REPORT.md: 117,931 bytes, modified 2026-03-20 07:22:37
  app.py: 332,855 bytes, modified 2026-03-20 20:25:48
  auto_trade_settings.json: 257 bytes, modified 2026-03-20 20:27:40
  auto_trading_sliders.png: 4,016 bytes, modified 2026-03-18 23:47:58
  background_runner.py: 7,567 bytes, modified 2026-03-20 07:38:39
  brti_cnn_lstm.pth: 2,314,039 bytes, modified 2026-03-20 20:26:49
  brti_cnn_lstm_10m.pth: 2,314,127 bytes, modified 2026-03-20 20:24:38
  brti_xgboost.pkl: 1,070,788 bytes, modified 2026-03-20 20:26:46
  brti_xgboost_15s.pkl: 111,303 bytes, modified 2026-03-20 20:24:38
  brti_xgboost_60s.pkl: 126,812 bytes, modified 2026-03-20 20:24:39
  brti_xgboost_magnitude.pkl: 109,550 bytes, modified 2026-03-20 20:24:48
  daily_report_2026-03-20.md: 18,350 bytes, modified 2026-03-20 20:26:00
  github_auto_push.py: 10,138 bytes, modified 2026-03-20 07:38:33
  github_push_log.json: 28,671 bytes, modified 2026-03-20 20:26:19
  main.py: 96 bytes, modified 2026-03-07 00:48:06
  pyproject.toml: 90,964 bytes, modified 2026-03-13 00:56:26
  replit.md: 9,301 bytes, modified 2026-03-20 16:33:43
  start.py: 3,766 bytes, modified 2026-03-13 05:58:41
  uv.lock: 621,704 bytes, modified 2026-03-13 00:56:26
  .streamlit/config.toml: 105 bytes, modified 2026-03-13 07:12:55
  attached_assets/IMG_1773_1773973264862.jpeg: 296,832 bytes, modified 2026-03-20 02:21:05
  attached_assets/Pasted--export-for-grok-py-Safe-summary-export-for-Grok-run-in_1773973013080.txt: 2,017 bytes, modified 2026-03-20 02:16:53
  attached_assets/Pasted--export-for-grok-py-Safe-summary-export-for-Grok-run-in_1773973284062.txt: 2,017 bytes, modified 2026-03-20 02:21:24
  attached_assets/Pasted--pip-install-ccxt-pro-pandas-numpy-Run-once-ccxt-pro-is_1773355859001.txt: 6,545 bytes, modified 2026-03-12 22:50:59
  attached_assets/Pasted--pip-install-ccxt-pro-pandas-numpy-torch-xgboost-joblib_1773357615585.txt: 8,305 bytes, modified 2026-03-12 23:20:16
  attached_assets/Pasted-2026-03-13-02-26-32-92-af96cfe9-User-For-use-container-_1773384468916.txt: 3,436 bytes, modified 2026-03-13 06:47:49
  attached_assets/Pasted-AGENT-HANDOVER-SCRIPT-START-Hey-Agent-Robert-wants-you-_1773972110880.txt: 7,228 bytes, modified 2026-03-20 02:01:51
  attached_assets/Pasted-Can-you-write-out-the-function-to-scan-and-lock-into-up_1773278756406.txt: 7,711 bytes, modified 2026-03-12 01:25:57
  attached_assets/Pasted-import-requests-import-time-import-ccxt-import-pandas-a_1772844384946.txt: 2,771 bytes, modified 2026-03-07 00:47:51
  attached_assets/Pasted-import-requests-import-time-import-datetime-import-stat_1774037941575.txt: 7,992 bytes, modified 2026-03-20 20:19:02
  attached_assets/image_1773277442314.png: 432,201 bytes, modified 2026-03-12 01:04:03
  attached_assets/image_1773929697578.png: 197,134 bytes, modified 2026-03-19 14:14:58
  db_backup/RESTORE.md: 1,596 bytes, modified 2026-03-20 00:31:32
  scripts/deploy_db_setup.py: 2,734 bytes, modified 2026-03-19 22:13:22
  scripts/post-merge.sh: 730 bytes, modified 2026-03-15 21:14:03
```

---

## Skill Files Available

```
  .local/skills/agent-inbox/SKILL.md: 3,735 bytes, modified 2026-03-20 20:19:39
  .local/skills/artifacts/SKILL.md: 602 bytes, modified 2026-03-20 20:19:40
  .local/skills/canvas/SKILL.md: 11,045 bytes, modified 2026-03-20 20:19:39
  .local/skills/code_review/SKILL.md: 3,102 bytes, modified 2026-03-20 20:19:39
  .local/skills/database/SKILL.md: 6,779 bytes, modified 2026-03-20 20:19:39
  .local/skills/delegation/SKILL.md: 6,999 bytes, modified 2026-03-20 20:19:39
  .local/skills/deployment/SKILL.md: 6,960 bytes, modified 2026-03-20 20:19:39
  .local/skills/design/SKILL.md: 9,814 bytes, modified 2026-03-20 20:19:39
  .local/skills/design-exploration/SKILL.md: 8,150 bytes, modified 2026-03-20 20:19:39
  .local/skills/diagnostics/SKILL.md: 3,667 bytes, modified 2026-03-20 20:19:39
  .local/skills/environment-secrets/SKILL.md: 6,608 bytes, modified 2026-03-20 20:19:39
  .local/skills/external_apis/SKILL.md: 669 bytes, modified 2026-03-20 20:19:39
  .local/skills/integrations/SKILL.md: 11,460 bytes, modified 2026-03-20 20:19:39
  .local/skills/media-generation/SKILL.md: 9,021 bytes, modified 2026-03-20 20:19:39
  .local/skills/mockup-extract/SKILL.md: 9,083 bytes, modified 2026-03-20 20:19:39
  .local/skills/mockup-graduate/SKILL.md: 5,209 bytes, modified 2026-03-20 20:19:39
  .local/skills/mockup-sandbox/SKILL.md: 39,937 bytes, modified 2026-03-20 20:19:39
  .local/skills/package-management/SKILL.md: 7,991 bytes, modified 2026-03-20 20:19:39
  .local/skills/post_merge_setup/SKILL.md: 4,562 bytes, modified 2026-03-20 20:19:39
  .local/skills/project_tasks/SKILL.md: 13,773 bytes, modified 2026-03-20 20:19:39
  .local/skills/query-integration-data/SKILL.md: 14,892 bytes, modified 2026-03-20 20:19:39
  .local/skills/remove-image-background/SKILL.md: 1,856 bytes, modified 2026-03-20 20:19:39
  .local/skills/repl_setup/SKILL.md: 3,575 bytes, modified 2026-03-20 20:19:39
  .local/skills/replit-docs/SKILL.md: 2,565 bytes, modified 2026-03-20 20:19:39
  .local/skills/revenuecat/SKILL.md: 5,993 bytes, modified 2026-03-20 20:19:39
  .local/skills/skill-authoring/SKILL.md: 3,560 bytes, modified 2026-03-20 20:19:39
  .local/skills/streamlit/SKILL.md: 1,341 bytes, modified 2026-03-20 20:19:39
  .local/skills/stripe/SKILL.md: 16,139 bytes, modified 2026-03-20 20:19:39
  .local/skills/suggest-new-project/SKILL.md: 3,907 bytes, modified 2026-03-20 20:19:39
  .local/skills/testing/SKILL.md: 8,869 bytes, modified 2026-03-20 20:19:39
  .local/skills/validation/SKILL.md: 7,356 bytes, modified 2026-03-20 20:19:39
  .local/skills/web-search/SKILL.md: 2,803 bytes, modified 2026-03-20 20:19:39
  .local/skills/workflows/SKILL.md: 7,813 bytes, modified 2026-03-20 20:19:39
  .local/secondary_skills/ad-creative/SKILL.md: 14,893 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/ai-recruiter/SKILL.md: 11,002 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/ai-secretary/SKILL.md: 9,249 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/apartment-finder/SKILL.md: 14,073 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/branding-generator/SKILL.md: 5,631 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/competitive-analysis/SKILL.md: 9,924 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/content-machine/SKILL.md: 5,830 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/deep-research/SKILL.md: 9,409 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/design-thinker/SKILL.md: 10,173 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/excel-generator/SKILL.md: 7,898 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/file-converter/SKILL.md: 6,193 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/find-customers/SKILL.md: 11,632 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/flashcard-generator/SKILL.md: 9,166 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/github-solution-finder/SKILL.md: 7,013 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/insurance-optimizer/SKILL.md: 10,232 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/interview-prep/SKILL.md: 11,034 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/invoice-generator/SKILL.md: 14,638 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/legal-contract/SKILL.md: 9,070 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/meal-planner/SKILL.md: 11,772 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/personal-shopper/SKILL.md: 8,031 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/photo-editor/SKILL.md: 8,945 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/podcast-generator/SKILL.md: 7,169 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/product-manager/SKILL.md: 5,554 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/programmatic-seo/SKILL.md: 11,239 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/real-estate-analyzer/SKILL.md: 9,589 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/recipe-creator/SKILL.md: 7,401 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/repl-seo-optimizer/SKILL.md: 7,473 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/resume-maker/SKILL.md: 19,149 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/seo-auditor/SKILL.md: 8,116 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/stock-analyzer/SKILL.md: 16,312 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/storyboard/SKILL.md: 8,717 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/supplier-research/SKILL.md: 11,596 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/tax-reviewer/SKILL.md: 7,343 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/translation/SKILL.md: 7,206 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/travel-assistant/SKILL.md: 10,026 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/used-car-advisor/SKILL.md: 10,596 bytes, modified 2026-03-20 20:19:40
  .local/secondary_skills/website-cloning/SKILL.md: 18,169 bytes, modified 2026-03-20 20:19:40
```

---

## Application Logs (latest)

```
No logs found
```

---

## Push History

Total pushes to date: 18
Last push: 2026-03-20 20:25:59 UTC

- 2026-03-20 17:11:50 UTC: 10 pushed, 0 failed
- 2026-03-20 18:05:07 UTC: 5 pushed, 1 failed
- 2026-03-20 18:36:24 UTC: 6 pushed, 0 failed
- 2026-03-20 20:12:17 UTC: 6 pushed, 0 failed
- 2026-03-20 20:25:59 UTC: 6 pushed, 0 failed

---

*Auto-generated by github_auto_push.py at 2026-03-22 00:18:33 UTC*
