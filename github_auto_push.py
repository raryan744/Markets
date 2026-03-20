import os
import time
import base64
import json
import requests
import datetime
import threading
import traceback
import subprocess
import glob

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO = 'raryan744/Markets'
BRANCH = 'main'
PUSH_INTERVAL_SECONDS = 86400
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

PUSH_LOG_FILE = 'github_push_log.json'


def load_push_log():
    if os.path.exists(PUSH_LOG_FILE):
        with open(PUSH_LOG_FILE, 'r') as f:
            return json.load(f)
    return {'pushes': [], 'last_push': None, 'total_pushes': 0}


def save_push_log(log):
    with open(PUSH_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)


def get_file_sha(filepath):
    try:
        resp = requests.get(
            f'https://api.github.com/repos/{REPO}/contents/{filepath}',
            headers=HEADERS,
            timeout=60
        )
        if resp.status_code == 200:
            return resp.json().get('sha')
    except Exception:
        pass
    return None


def push_file(filepath, github_path, message):
    if not os.path.exists(filepath):
        return False, f'{filepath} not found'
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        encoded = base64.b64encode(raw).decode()
        sha = get_file_sha(github_path)
        data = {
            'message': message,
            'content': encoded,
            'branch': BRANCH
        }
        if sha:
            data['sha'] = sha
        resp = requests.put(
            f'https://api.github.com/repos/{REPO}/contents/{github_path}',
            headers=HEADERS,
            json=data,
            timeout=120
        )
        if resp.status_code in (200, 201):
            return True, f'{resp.status_code} OK'
        else:
            return False, f'{resp.status_code}: {resp.text[:200]}'
    except Exception as e:
        return False, f'{type(e).__name__}: {str(e)}'


def collect_application_logs():
    logs = []
    log_dir = '/tmp/logs'
    if os.path.isdir(log_dir):
        for f in sorted(glob.glob(os.path.join(log_dir, '*.log'))):
            try:
                with open(f, 'r') as fh:
                    logs.append(f"=== {os.path.basename(f)} ===\n{fh.read()}\n")
            except Exception:
                pass
    return '\n'.join(logs) if logs else 'No logs found'


def collect_thread_info():
    import threading as _t
    threads = []
    for t in _t.enumerate():
        threads.append(f"  - {t.name} (daemon={t.daemon}, alive={t.is_alive()})")
    return '\n'.join(threads)


def collect_process_info():
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        return f'Error: {e}'


def collect_env_info():
    safe_keys = [
        'REPL_ID', 'REPL_SLUG', 'REPL_OWNER', 'REPLIT_DB_URL',
        'REPLIT_DOMAINS', 'REPLIT_DEV_DOMAIN', 'HOME', 'PATH',
        'PYTHONPATH', 'DATABASE_URL', 'PGDATABASE', 'PGHOST', 'PGPORT',
    ]
    lines = []
    for key in sorted(safe_keys):
        val = os.environ.get(key, 'NOT SET')
        if key == 'DATABASE_URL' and val != 'NOT SET':
            val = val.split('@')[1] if '@' in val else '[redacted]'
        lines.append(f"  {key}={val}")
    return '\n'.join(lines)


def collect_file_inventory():
    lines = []
    for root, dirs, files in os.walk('/home/runner/workspace'):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.cache', 'node_modules', '.local', '.upm', '.pythonlibs')]
        for f in sorted(files):
            fp = os.path.join(root, f)
            try:
                stat = os.stat(fp)
                mod = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                rel = os.path.relpath(fp, '/home/runner/workspace')
                lines.append(f"  {rel}: {stat.st_size:,} bytes, modified {mod}")
            except Exception:
                pass
    return '\n'.join(lines)


def collect_auto_trade_state():
    if os.path.exists('auto_trade_settings.json'):
        with open('auto_trade_settings.json', 'r') as f:
            return json.dumps(json.load(f), indent=2)
    return 'File not found'


def collect_skill_file_list():
    lines = []
    for base in ['.local/skills', '.local/secondary_skills']:
        if os.path.isdir(base):
            for name in sorted(os.listdir(base)):
                skill_path = os.path.join(base, name, 'SKILL.md')
                if os.path.isfile(skill_path):
                    stat = os.stat(skill_path)
                    mod = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    lines.append(f"  {skill_path}: {stat.st_size:,} bytes, modified {mod}")
    return '\n'.join(lines)


def collect_db_info():
    try:
        import psycopg2
        conn = psycopg2.connect(os.environ.get('DATABASE_URL', ''))
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        tables = [r[0] for r in cur.fetchall()]
        info = f"Tables: {', '.join(tables)}\n\n"
        for t in tables:
            cur.execute(f"SELECT count(*) FROM {t}")
            count = cur.fetchone()[0]
            info += f"  {t}: {count} rows\n"
        conn.close()
        return info
    except Exception as e:
        return f'Error: {e}'


def generate_daily_report():
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    date_tag = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    report = f"# Daily Evidence Report — {date_tag}\n\n"
    report += f"**Generated:** {now}\n"
    report += f"**Repository:** https://github.com/{REPO}\n\n"

    report += "---\n\n## Auto-Trade Settings\n\n"
    report += f"```json\n{collect_auto_trade_state()}\n```\n\n"

    report += "---\n\n## Active Threads\n\n"
    report += f"```\n{collect_thread_info()}\n```\n\n"

    report += "---\n\n## Running Processes\n\n"
    report += f"```\n{collect_process_info()}\n```\n\n"

    report += "---\n\n## Database State\n\n"
    report += f"```\n{collect_db_info()}\n```\n\n"

    report += "---\n\n## Environment Variables (safe subset)\n\n"
    report += f"```\n{collect_env_info()}\n```\n\n"

    report += "---\n\n## Workspace File Inventory\n\n"
    report += f"```\n{collect_file_inventory()}\n```\n\n"

    report += "---\n\n## Skill Files Available\n\n"
    report += f"```\n{collect_skill_file_list()}\n```\n\n"

    report += "---\n\n## Application Logs (latest)\n\n"
    report += f"```\n{collect_application_logs()}\n```\n\n"

    report += "---\n\n## Push History\n\n"
    log = load_push_log()
    report += f"Total pushes to date: {log.get('total_pushes', 0)}\n"
    report += f"Last push: {log.get('last_push', 'never')}\n\n"
    for entry in log.get('pushes', [])[-5:]:
        report += f"- {entry.get('date')}: {entry.get('files_pushed')} pushed, {entry.get('files_failed')} failed\n"

    report += f"\n---\n\n*Auto-generated by github_auto_push.py at {now}*\n"
    return report, date_tag


def do_daily_push():
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    date_tag = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    log = load_push_log()
    results = []

    report_content, tag = generate_daily_report()
    report_file = f'daily_report_{tag}.md'
    with open(report_file, 'w') as f:
        f.write(report_content)

    push_list = [
        (report_file, f'daily_reports/{report_file}', f'Daily evidence report {tag}'),
        ('auto_trade_settings.json', 'auto_trade_settings.json', f'Auto-trade state snapshot {tag}'),
        ('app.py', 'app.py', f'Source code snapshot {tag}'),
        ('background_runner.py', 'background_runner.py', f'Background runner snapshot {tag}'),
        ('replit.md', 'replit.md', f'Agent memory snapshot {tag}'),
        ('github_auto_push.py', 'github_auto_push.py', f'Auto-push script snapshot {tag}'),
    ]

    for log_file in sorted(glob.glob('/tmp/logs/*.log')):
        basename = os.path.basename(log_file)
        push_list.append((log_file, f'daily_reports/logs/{tag}_{basename}', f'Log capture {tag}: {basename}'))

    for local_path, github_path, message in push_list:
        if not os.path.exists(local_path):
            continue
        success, detail = push_file(local_path, github_path, message)
        results.append({
            'file': github_path,
            'success': success,
            'detail': detail,
            'time': now
        })
        print(f"  [{now}] {github_path}: {detail}")
        time.sleep(2)

    entry = {
        'date': now,
        'files_pushed': len([r for r in results if r['success']]),
        'files_failed': len([r for r in results if not r['success']]),
        'results': results
    }
    log['pushes'].append(entry)
    log['last_push'] = now
    log['total_pushes'] = log.get('total_pushes', 0) + 1
    save_push_log(log)

    save_result = push_file(PUSH_LOG_FILE, PUSH_LOG_FILE, f'Push log update {tag}')
    print(f"  [{now}] push_log: {save_result[1]}")

    print(f"[{now}] Daily push complete: {entry['files_pushed']} succeeded, {entry['files_failed']} failed")
    return entry


def auto_push_loop():
    print(f"[github_auto_push] Starting daily auto-push loop (interval: {PUSH_INTERVAL_SECONDS}s)")
    while True:
        try:
            do_daily_push()
        except Exception as e:
            print(f"[github_auto_push] Error: {type(e).__name__}: {e}")
            traceback.print_exc()
        time.sleep(PUSH_INTERVAL_SECONDS)


def start_background():
    t = threading.Thread(target=auto_push_loop, daemon=True, name='github-auto-push')
    t.start()
    print(f"[github_auto_push] Background thread started")
    return t


if __name__ == '__main__':
    print("Running immediate push with full evidence collection...")
    result = do_daily_push()
    print(f"\nResult: {result['files_pushed']} pushed, {result['files_failed']} failed")
    print("\nStarting keep-alive loop (pushes every 24 hours)...")
    auto_push_loop()
