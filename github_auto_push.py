import os
import time
import base64
import json
import requests
import datetime
import threading
import traceback

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO = 'raryan744/Markets'
BRANCH = 'main'
PUSH_INTERVAL_SECONDS = 86400
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

FILES_TO_TRACK = [
    'app.py',
    'background_runner.py',
    'auto_trade_settings.json',
    'replit.md',
    'SYSTEM_FAILURE_REPORT.md',
    'CONVERSATION_RECORD.md',
    'EVIDENCE_PACKAGE.md',
    'SKILLS_PRIMARY.md',
    'SKILLS_SECONDARY.md',
    'ALL_SKILL_DOCUMENTS.md',
    'APPLICATION_LOGS.log',
    'start.py',
    'main.py',
    'scripts/deploy_db_setup.py',
    'db_backup/RESTORE.md',
    '.streamlit/config.toml',
]

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


def push_file(filepath, message):
    if not os.path.exists(filepath):
        return False, f'{filepath} not found'

    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        encoded = base64.b64encode(raw).decode()

        sha = get_file_sha(filepath)
        data = {
            'message': message,
            'content': encoded,
            'branch': BRANCH
        }
        if sha:
            data['sha'] = sha

        resp = requests.put(
            f'https://api.github.com/repos/{REPO}/contents/{filepath}',
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


def generate_daily_snapshot():
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    snapshot = f"# Daily Snapshot — {now}\n\n"

    snapshot += "## File Status\n\n"
    for fp in FILES_TO_TRACK:
        if os.path.exists(fp):
            stat = os.stat(fp)
            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            snapshot += f"- `{fp}`: {stat.st_size:,} bytes, modified {mod_time}\n"
        else:
            snapshot += f"- `{fp}`: NOT FOUND\n"

    snapshot += "\n## Auto-Trade Settings\n\n"
    if os.path.exists('auto_trade_settings.json'):
        with open('auto_trade_settings.json', 'r') as f:
            settings = json.load(f)
        snapshot += f"```json\n{json.dumps(settings, indent=2)}\n```\n"

    snapshot += f"\n## Environment\n\n"
    snapshot += f"- Snapshot generated: {now}\n"
    snapshot += f"- Repository: https://github.com/{REPO}\n"

    log = load_push_log()
    snapshot += f"- Total auto-pushes to date: {log['total_pushes']}\n"
    snapshot += f"- Last push: {log.get('last_push', 'never')}\n"

    return snapshot


def do_daily_push():
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    date_tag = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    log = load_push_log()

    results = []
    snapshot = generate_daily_snapshot()
    snapshot_file = f'daily_snapshot_{date_tag}.md'
    with open(snapshot_file, 'w') as f:
        f.write(snapshot)

    all_files = FILES_TO_TRACK + [snapshot_file, PUSH_LOG_FILE]

    for filepath in all_files:
        if not os.path.exists(filepath):
            continue
        success, detail = push_file(
            filepath,
            f'Auto-push {date_tag}: {filepath}'
        )
        results.append({
            'file': filepath,
            'success': success,
            'detail': detail,
            'time': now
        })
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
    print("Running immediate push...")
    result = do_daily_push()
    print(f"Result: {result['files_pushed']} pushed, {result['files_failed']} failed")
    print("\nStarting keep-alive loop (pushes every 24 hours)...")
    auto_push_loop()
