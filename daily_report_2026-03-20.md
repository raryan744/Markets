# Daily Evidence Report — 2026-03-20

**Generated:** 2026-03-20 07:39:36 UTC
**Repository:** https://github.com/raryan744/Markets

---

## Auto-Trade Settings

```json
{
  "enabled": false,
  "contracts": 9,
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
```

---

## Running Processes

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
runner         1  0.3  0.1 2677216 68312 ?       Ssl  Mar19   1:49 /nix/store/f44v4qidsnm4323dwjcq9q0rxahh1pvb-pid1-0.0.1/bin/pid1 --pid2-pooling
runner        14  5.8  1.4 56445156 924548 ?     Sl   Mar19  28:01 pid2 --no-deprecation --disable-warning=ExperimentalWarning --use-openssl-ca /pid2/bundles/0.0.3847/server.cjs --start-timestamp=1773963805231 --socket-listener-fd=3 --pinger-socket-path=/run/replit/socks/pid2ping.0.sock --pooled-fd=4
runner        46  0.0  0.0   3984  2904 ?        S    01:50   0:00 nix-editor --return-output
runner      3306  0.0  0.0   2960  1984 ?        S    02:27   0:00 sh -c /nix/store/775cppcslcvxd4x2v8x4k78xw94zg88a-ty-0.0.21/bin/ty server
runner      3307  0.0  0.4 2137904 317644 ?      Sl   02:27   0:12 /nix/store/775cppcslcvxd4x2v8x4k78xw94zg88a-ty-0.0.21/bin/ty server
runner     13766  0.0  0.0   8252  5072 pts/0    Ss   03:25   0:00 /nix/store/smkzrg2vvp3lng3hq7v9svfni5mnqjh2-bash-interactive-5.2p37/bin/bash -rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc --rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc -ci python3 background_runner.py & streamlit run app.py --server.port 5000 --server.enableCORS false --server.enableXsrfProtection false
runner     13773  106  2.1 4293212 1401088 pts/0 Sl   03:25 271:21 python3 background_runner.py
runner     13774  1.6  0.3 2630332 215092 pts/0  Sl+  03:25   4:05 /nix/store/flbj8bq2vznkcwss7sm0ky8rd0k6kar7-python-wrapped-0.1.0/bin/python3 /home/runner/workspace/.pythonlibs/bin/streamlit run app.py --server.port 5000 --server.enableCORS false --server.enableXsrfProtection false
runner     22438  112  2.0 4188928 1373172 ?     Sl   04:18 225:13 python3 background_runner.py
runner     74428  0.9  0.6 1484864 410436 ?      S    07:38   0:00 pid2 --no-deprecation --disable-warning=ExperimentalWarning --use-openssl-ca /pid2/bundles/0.0.3847/server.cjs --start-timestamp=1773963805231 --socket-listener-fd=3 --pinger-socket-path=/run/replit/socks/pid2ping.0.sock --pooled-fd=4
runner     74429  0.0  0.0   8112  4428 pts/2    Ss+  07:38   0:00 /nix/store/smkzrg2vvp3lng3hq7v9svfni5mnqjh2-bash-interactive-5.2p37/bin/bash -rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc --rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc -c cd /home/runner/workspace && timeout 120 python3 github_auto_push.py 2>&1 | head -50
runner     74432  0.0  0.0   7992  3092 pts/2    S    07:38   0:00 timeout 120 python3 github_auto_push.py
runner     74433  0.0  0.0   7992  3196 pts/2    S+   07:38   0:00 head -50
runner     74434  1.4  0.0  69112 39240 pts/2    S    07:38   0:00 python3 github_auto_push.py
runner     74634 32.4  0.6 1484864 410372 ?      S    07:39   0:00 pid2 --no-deprecation --disable-warning=ExperimentalWarning --use-openssl-ca /pid2/bundles/0.0.3847/server.cjs --start-timestamp=1773963805231 --socket-listener-fd=3 --pinger-socket-path=/run/replit/socks/pid2ping.0.sock --pooled-fd=4
runner     74635  5.7  0.0   8116  4632 pts/3    Ss+  07:39   0:00 /nix/store/smkzrg2vvp3lng3hq7v9svfni5mnqjh2-bash-interactive-5.2p37/bin/bash -rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc --rcfile /nix/store/lsgsb0ar7rdwa09d1z2dnfjh4188pddk-replit-bashrc/bashrc -c cd /home/runner/workspace && python3 << 'PYEOF' import os, json, datetime, glob, subprocess, threading  now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') date_tag = datetime.datetime.utcnow().strftime('%Y-%m-%d')  def collect_threads():     lines = []     for t in threading.enumerate():         lines.append(f"  - {t.name} (daemon={t.daemon}, alive={t.is_alive()})")     return '\n'.join(lines)  def collect_processes():     try:         r = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)         return r.stdout     except: return 'unavailable'  def collect_db():     try:         import psycopg2         conn = psycopg2.connect(os.environ.get('DATABASE_URL',''))         cur = conn.cursor()         cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")         tables = [r[0] for r in cur.fetchall()]         info = f"Tables: {', '.join(tables)}\n"         for t in tables:             cur.execute(f"SELECT count(*) FROM {t}")             info += f"  {t}: {cur.fetchone()[0]} rows\n"         conn.close()         return info     except Exception as e: return str(e)  def collect_files():     lines = []     for root,dirs,files in os.walk('/home/runner/workspace'):         dirs[:] = [d for d in dirs if d not in ('.git','__pycache__','.cache','node_modules','.local','.upm','.pythonlibs')]         for f in sorted(files):             fp = os.path.join(root, f)             try:                 s = os.stat(fp)                 mod = datetime.datetime.fromtimestamp(s.st_mtime).strftime('%Y-%m-%d %H:%M')                 lines.append(f"  {os.path.relpath(fp,'/home/runner/workspace')}: {s.st_size:,}b {mod}")             except: pass     return '\n'.join(lines)  def collect_skills():     lines = []     for base in ['.local/skills','.local/secondary_skills']:         if os.path.isdir(base):             for name in sorted(os.listdir(base)):                 sp = os.path.join(base, name, 'SKILL.md')                 if os.path.isfile(sp):                     s = os.stat(sp)                     lines.append(f"  {sp}: {s.st_size:,}b")     return '\n'.join(lines)  def collect_logs():     parts = []     for f in sorted(glob.glob('/tmp/logs/*.log')):         try:             with open(f) as fh:                 parts.append(f"=== {os.path.basename(f)} ===\n{fh.read()}\n")         except: pass     return '\n'.join(parts) or 'none'  def collect_auto_trade():     if os.path.exists('auto_trade_settings.json'):         with open('auto_trade_settings.json') as f:             return json.dumps(json.load(f), indent=2)     return 'not found'  def collect_env():     keys = ['REPL_ID','REPL_SLUG','REPL_OWNER','REPLIT_DOMAINS','REPLIT_DEV_DOMAIN','PGHOST','PGPORT','PGDATABASE']     return '\n'.join(f"  {k}={os.environ.get(k,'NOT SET')}" for k in sorted(keys))  report = f"""# Daily Evidence Report — {date_tag}  **Generated:** {now} **Repository:** https://github.com/raryan744/Markets  ---  ## Auto-Trade Settings  ```json {collect_auto_trade()} ```  ---  ## Active Threads  ``` {collect_threads()} ```  ---  ## Running Processes  ``` {collect_processes()} ```  ---  ## Database State  ``` {collect_db()} ```  ---  ## Environment Variables  ``` {collect_env()} ```  ---  ## Workspace File Inventory  ``` {collect_files()} ```  ---  ## Skill Files  ``` {collect_skills()} ```  ---  ## Application Logs  ``` {collect_logs()} ```  ---  *Auto-generated by github_auto_push.py at {now}* """  report_file = f'daily_report_{date_tag}.md' with open(report_file, 'w') as f:     f.write(report) print(f"Report written: {len(report)} chars -> {report_file}") PYEOF
runner     74638 17.8  0.0  19208 13916 pts/3    S+   07:39   0:00 python3
runner     74644 26.6  0.0  11696  5456 pts/3    R+   07:39   0:00 ps aux

```

---

## Database State

```
Tables: btc_prices, brti_ticks, kalshi_orderbook, bobby_brti_ticks, book_image_snapshots, auto_trades, training_samples, xgb_mtf_predictions, kalshi_depth_signal, kalshi_candlesticks, ensemble_predictions
  btc_prices: 12573 rows
  brti_ticks: 250788 rows
  kalshi_orderbook: 65209 rows
  bobby_brti_ticks: 1471312 rows
  book_image_snapshots: 9728 rows
  auto_trades: 775 rows
  training_samples: 734597 rows
  xgb_mtf_predictions: 8788 rows
  kalshi_depth_signal: 0 rows
  kalshi_candlesticks: 2553 rows
  ensemble_predictions: 571449 rows

```

---

## Environment Variables

```
  PGDATABASE=heliumdb
  PGHOST=helium
  PGPORT=5432
  REPLIT_DEV_DOMAIN=5f904616-d108-48cb-b7b7-01b6282353bf-00-1t0zvtdbpqc4d.kirk.replit.dev
  REPLIT_DOMAINS=5f904616-d108-48cb-b7b7-01b6282353bf-00-1t0zvtdbpqc4d.kirk.replit.dev
  REPL_ID=5f904616-d108-48cb-b7b7-01b6282353bf
  REPL_OWNER=PsyBob
  REPL_SLUG=workspace
```

---

## Workspace File Inventory

```
  .gitignore: 273b 2026-03-20 00:07
  .replit: 1,195b 2026-03-19 17:21
  ALL_SKILL_DOCUMENTS.md: 633,206b 2026-03-20 07:31
  APPLICATION_LOGS.log: 12,754b 2026-03-20 07:31
  CONVERSATION_RECORD.md: 15,054b 2026-03-20 07:37
  EVIDENCE_PACKAGE.md: 15,359b 2026-03-20 07:30
  SKILLS_PRIMARY.md: 257,193b 2026-03-20 07:31
  SKILLS_SECONDARY.md: 376,275b 2026-03-20 07:31
  SYSTEM_FAILURE_REPORT.md: 117,931b 2026-03-20 07:22
  app.py: 300,794b 2026-03-20 03:25
  auto_trade_settings.json: 257b 2026-03-20 05:48
  auto_trading_sliders.png: 4,016b 2026-03-18 23:47
  background_runner.py: 7,567b 2026-03-20 07:38
  brti_cnn_lstm.pth: 2,314,039b 2026-03-20 07:38
  brti_cnn_lstm_10m.pth: 2,314,127b 2026-03-20 07:39
  brti_xgboost.pkl: 368,087b 2026-03-20 07:39
  brti_xgboost_15s.pkl: 270,371b 2026-03-20 07:39
  brti_xgboost_60s.pkl: 314,027b 2026-03-20 07:39
  brti_xgboost_magnitude.pkl: 376,736b 2026-03-20 07:37
  daily_report_2026-03-20.md: 36,082b 2026-03-20 07:39
  github_auto_push.py: 10,138b 2026-03-20 07:38
  github_push_log.json: 2,484b 2026-03-20 07:39
  main.py: 96b 2026-03-07 00:48
  pyproject.toml: 90,964b 2026-03-13 00:56
  replit.md: 9,288b 2026-03-19 20:05
  start.py: 3,766b 2026-03-13 05:58
  uv.lock: 621,704b 2026-03-13 00:56
  attached_assets/IMG_1773_1773973264862.jpeg: 296,832b 2026-03-20 02:21
  attached_assets/Pasted--export-for-grok-py-Safe-summary-export-for-Grok-run-in_1773973013080.txt: 2,017b 2026-03-20 02:16
  attached_assets/Pasted--export-for-grok-py-Safe-summary-export-for-Grok-run-in_1773973284062.txt: 2,017b 2026-03-20 02:21
  attached_assets/Pasted--pip-install-ccxt-pro-pandas-numpy-Run-once-ccxt-pro-is_1773355859001.txt: 6,545b 2026-03-12 22:50
  attached_assets/Pasted--pip-install-ccxt-pro-pandas-numpy-torch-xgboost-joblib_1773357615585.txt: 8,305b 2026-03-12 23:20
  attached_assets/Pasted-2026-03-13-02-26-32-92-af96cfe9-User-For-use-container-_1773384468916.txt: 3,436b 2026-03-13 06:47
  attached_assets/Pasted-AGENT-HANDOVER-SCRIPT-START-Hey-Agent-Robert-wants-you-_1773972110880.txt: 7,228b 2026-03-20 02:01
  attached_assets/Pasted-Can-you-write-out-the-function-to-scan-and-lock-into-up_1773278756406.txt: 7,711b 2026-03-12 01:25
  attached_assets/Pasted-import-requests-import-time-import-ccxt-import-pandas-a_1772844384946.txt: 2,771b 2026-03-07 00:47
  attached_assets/image_1773277442314.png: 432,201b 2026-03-12 01:04
  attached_assets/image_1773929697578.png: 197,134b 2026-03-19 14:14
  .streamlit/config.toml: 105b 2026-03-13 07:12
  scripts/deploy_db_setup.py: 2,734b 2026-03-19 22:13
  scripts/post-merge.sh: 730b 2026-03-15 21:14
  db_backup/RESTORE.md: 1,596b 2026-03-20 00:31
```

---

## Skill Files

```
  .local/skills/agent-inbox/SKILL.md: 3,735b
  .local/skills/artifacts/SKILL.md: 602b
  .local/skills/canvas/SKILL.md: 11,045b
  .local/skills/code_review/SKILL.md: 3,102b
  .local/skills/database/SKILL.md: 6,779b
  .local/skills/delegation/SKILL.md: 6,999b
  .local/skills/deployment/SKILL.md: 5,804b
  .local/skills/design/SKILL.md: 9,814b
  .local/skills/design-exploration/SKILL.md: 8,150b
  .local/skills/diagnostics/SKILL.md: 3,667b
  .local/skills/environment-secrets/SKILL.md: 6,608b
  .local/skills/external_apis/SKILL.md: 669b
  .local/skills/fetch-deployment-logs/SKILL.md: 4,938b
  .local/skills/integrations/SKILL.md: 11,460b
  .local/skills/media-generation/SKILL.md: 9,021b
  .local/skills/mockup-extract/SKILL.md: 9,083b
  .local/skills/mockup-graduate/SKILL.md: 5,209b
  .local/skills/mockup-sandbox/SKILL.md: 39,937b
  .local/skills/package-management/SKILL.md: 7,991b
  .local/skills/post_merge_setup/SKILL.md: 4,562b
  .local/skills/project_tasks/SKILL.md: 13,773b
  .local/skills/query-integration-data/SKILL.md: 14,903b
  .local/skills/remove-image-background/SKILL.md: 1,856b
  .local/skills/repl_setup/SKILL.md: 3,575b
  .local/skills/replit-docs/SKILL.md: 2,565b
  .local/skills/revenuecat/SKILL.md: 5,993b
  .local/skills/skill-authoring/SKILL.md: 3,560b
  .local/skills/streamlit/SKILL.md: 1,341b
  .local/skills/stripe/SKILL.md: 16,139b
  .local/skills/suggest-new-project/SKILL.md: 3,907b
  .local/skills/testing/SKILL.md: 8,869b
  .local/skills/validation/SKILL.md: 7,356b
  .local/skills/web-search/SKILL.md: 2,803b
  .local/skills/workflows/SKILL.md: 7,813b
  .local/secondary_skills/ad-creative/SKILL.md: 14,893b
  .local/secondary_skills/ai-recruiter/SKILL.md: 11,002b
  .local/secondary_skills/ai-secretary/SKILL.md: 9,249b
  .local/secondary_skills/apartment-finder/SKILL.md: 14,073b
  .local/secondary_skills/branding-generator/SKILL.md: 5,631b
  .local/secondary_skills/competitive-analysis/SKILL.md: 9,924b
  .local/secondary_skills/content-machine/SKILL.md: 5,830b
  .local/secondary_skills/deep-research/SKILL.md: 9,409b
  .local/secondary_skills/design-thinker/SKILL.md: 10,173b
  .local/secondary_skills/excel-generator/SKILL.md: 7,898b
  .local/secondary_skills/file-converter/SKILL.md: 6,193b
  .local/secondary_skills/find-customers/SKILL.md: 11,632b
  .local/secondary_skills/flashcard-generator/SKILL.md: 9,166b
  .local/secondary_skills/github-solution-finder/SKILL.md: 7,013b
  .local/secondary_skills/insurance-optimizer/SKILL.md: 10,232b
  .local/secondary_skills/interview-prep/SKILL.md: 11,034b
  .local/secondary_skills/invoice-generator/SKILL.md: 14,638b
  .local/secondary_skills/legal-contract/SKILL.md: 9,070b
  .local/secondary_skills/meal-planner/SKILL.md: 11,772b
  .local/secondary_skills/personal-shopper/SKILL.md: 8,031b
  .local/secondary_skills/photo-editor/SKILL.md: 8,945b
  .local/secondary_skills/podcast-generator/SKILL.md: 7,169b
  .local/secondary_skills/product-manager/SKILL.md: 5,554b
  .local/secondary_skills/programmatic-seo/SKILL.md: 11,239b
  .local/secondary_skills/real-estate-analyzer/SKILL.md: 9,589b
  .local/secondary_skills/recipe-creator/SKILL.md: 7,401b
  .local/secondary_skills/repl-seo-optimizer/SKILL.md: 7,473b
  .local/secondary_skills/resume-maker/SKILL.md: 19,149b
  .local/secondary_skills/seo-auditor/SKILL.md: 8,116b
  .local/secondary_skills/stock-analyzer/SKILL.md: 16,312b
  .local/secondary_skills/storyboard/SKILL.md: 8,717b
  .local/secondary_skills/supplier-research/SKILL.md: 11,596b
  .local/secondary_skills/tax-reviewer/SKILL.md: 7,343b
  .local/secondary_skills/translation/SKILL.md: 7,206b
  .local/secondary_skills/travel-assistant/SKILL.md: 10,026b
  .local/secondary_skills/used-car-advisor/SKILL.md: 10,596b
  .local/secondary_skills/website-cloning/SKILL.md: 18,169b
```

---

## Application Logs

```
=== Start_application_20260320_023356_902.log ===
<workflow>
<workflow_name>Start application</workflow_name>
<status>RUNNING</status><run_id>Vd_dsKJew_Q1fWm0Xk8oj</run_id><timestamp>2026-03-20T02:33:56.855278+00:00</timestamp>
<logs>[1] 3941
[02:33:44] background_runner: starting — loading app.py engine
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
[02:33:45] background_runner: entering keep-alive loop
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:5000
  Network URL: http://172.31.98.162:5000
  External URL: http://8.229.178.165:5000
2026-03-20 02:33:51.313 Thread 'streamlit-startup': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 02:33:56.317 Thread 'streamlit-startup': missing ScriptRunContext! This warning can be ignored when running in bare mode.</logs>
</workflow>


=== Start_application_20260320_024143_715.log ===
<workflow>
<workflow_name>Start application</workflow_name>
<status>RUNNING</status><run_id>OSsyhryT1PICvVK74rxrU</run_id><timestamp>2026-03-20T02:41:43.667540+00:00</timestamp>
<logs>[1] 4644
[02:39:22] background_runner: starting — loading app.py engine
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
[02:39:22] background_runner: entering keep-alive loop
2026-03-20 02:39:23.039 Port 5000 is not available</logs>
</workflow>


=== Start_application_20260320_025910_786.log ===
<workflow>
<workflow_name>Start application</workflow_name>
<status>RUNNING</status><run_id>MKPC7Gti2arQx2OByrcS2</run_id><timestamp>2026-03-20T02:59:10.745834+00:00</timestamp>
<logs>[1] 5864
[02:45:16] background_runner: starting — loading app.py engine
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
[02:45:17] background_runner: entering keep-alive loop
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:5000
  Network URL: http://172.31.98.162:5000
  External URL: http://8.229.178.165:5000
2026-03-20 02:45:22.420 Thread 'streamlit-startup': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 02:45:27.432 Thread 'streamlit-startup': missing ScriptRunContext! This warning can be ignored when running in bare mode.
[02:50:17] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer', 'persist-labels']
[02:55:18] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer']</logs>
</workflow>


=== Start_application_20260320_031601_563.log ===
<workflow>
<workflow_name>Start application</workflow_name>
<status>RUNNING</status><run_id>MKPC7Gti2arQx2OByrcS2</run_id><timestamp>2026-03-20T03:16:01.521736+00:00</timestamp>
<logs>[03:00:18] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
2026-03-20 03:02:39.288 Session with id 64489082-8bdd-4d75-aad9-21469c975c34 is already connected! Connecting to a new session.
2026-03-20 03:02:39.427 The fragment with id 2f53a65213bd84a6c94ff692b3e310d6 does not exist anymore - it might have been removed during a preceding full-app rerun.
[03:05:18] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[03:10:18] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[03:15:18] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-6 (_ensemble_deep_inference_loop)', 'ensemble-trainer']</logs>
</workflow>


=== Start_application_20260320_073130_655.log ===
<workflow>
<workflow_name>Start application</workflow_name>
<status>RUNNING</status><run_id>890h-x3wBvh8lIx4-5PhD</run_id><timestamp>2026-03-20T07:31:30.616547+00:00</timestamp>
<logs>[1] 22438
[04:18:52] background_runner: starting — loading app.py engine
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
[04:18:52] background_runner: entering keep-alive loop
2026-03-20 04:18:53.139 Port 5000 is not available
[04:23:52] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer', 'persist-labels']
[04:28:53] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:33:53] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:38:53] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:43:53] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:48:53] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:53:54] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[04:58:54] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:03:54] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:08:54] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:13:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:18:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:23:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:28:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:33:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:38:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer', 'Thread-712 (db_save_bobby_brti)']
[05:43:55] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:48:56] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:53:56] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[05:58:56] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:03:56] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:08:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:13:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:18:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:23:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer', 'Thread-1099 (db_save_brti_ticks)']
[06:28:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:33:57] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:38:58] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:43:58] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:48:58] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:53:59] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[06:58:59] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:03:59] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:08:59] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:13:59] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:19:00] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:24:00] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']
[07:29:01] background_runner alive — threads: ['MainThread', 'keep-alive', 'Thread-1 (_bg_data_loop)', 'Thread-2 (run_forever)', 'Thread-3 (_bobby_thread_target)', 'Thread-4 (_run_safe_shutdown_loop)', 'Thread-5 (_ensemble_thread_target)', 'auto-trader', 'Thread-7 (_ensemble_deep_inference_loop)', 'ensemble-trainer']</logs>
</workflow>


=== browser_console_20260320_025910_950.log ===
<browser_console_logs>
Method -warn:
1773974716901.0 - ["WebSocket onclose"]
1773975217908.0 - ["WebSocket onclose"]
<timestamp>2026-03-20T02:59:10.910824+00:00</timestamp>
</browser_console_logs>


```

---

*Auto-generated by github_auto_push.py at 2026-03-20 07:39:36 UTC*
