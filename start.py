import subprocess
import sys
import os
import time
import threading
import signal
import atexit
import socket

LOG = "/tmp/start_trigger.log"
streamlit_proc = None


def _log(msg):
    try:
        with open(LOG, "a") as f:
            from datetime import datetime, timezone
            f.write(f"[{datetime.now(timezone.utc).isoformat()}] {msg}\n")
    except Exception:
        pass


def _kill_child():
    global streamlit_proc
    if streamlit_proc and streamlit_proc.poll() is None:
        try:
            os.killpg(os.getpgid(streamlit_proc.pid), signal.SIGKILL)
        except Exception:
            try:
                streamlit_proc.kill()
            except Exception:
                pass


def _handle_signal(sig, frame):
    _kill_child()
    os._exit(0)


def _build_rerun_msg():
    from streamlit.proto.BackMsg_pb2 import BackMsg
    msg = BackMsg()
    msg.rerun_script.query_string = ""
    msg.rerun_script.page_script_hash = ""
    return msg.SerializeToString()


def _wait_for_port_free(port, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("0.0.0.0", port))
            s.close()
            return True
        except OSError:
            s.close()
            time.sleep(0.5)
    return False


def self_trigger():
    _log("self_trigger thread started, sleeping 10s")
    time.sleep(10)
    _log("sleep done, attempting WS connection")
    import asyncio
    import websockets

    rerun_msg = _build_rerun_msg()
    triggered = False

    async def _keep_session():
        nonlocal triggered
        while True:
            try:
                async with websockets.connect(
                    "ws://localhost:5000/_stcore/stream",
                    subprotocols=["streamlit"],
                    open_timeout=15,
                    close_timeout=5,
                    ping_interval=20,
                    ping_timeout=10,
                    max_size=16 * 1024 * 1024,
                ) as ws:
                    if not triggered:
                        _log("WS connected, sending initial rerun_script")
                        await ws.send(rerun_msg)
                        triggered = True
                    else:
                        _log("WS reconnected (keepalive only, no rerun)")
                    while True:
                        try:
                            await asyncio.wait_for(ws.recv(), timeout=600)
                        except asyncio.TimeoutError:
                            pass
                        except websockets.exceptions.ConnectionClosed:
                            break
            except Exception as e:
                _log(f"WS error: {type(e).__name__}: {e}")
            await asyncio.sleep(10)

    asyncio.run(_keep_session())


_log("start.py launching, cleaning port 5000")
os.system("pkill -9 -f 'streamlit run app.py' 2>/dev/null")
os.system("lsof -i :5000 -t 2>/dev/null | xargs -r kill -9")
time.sleep(1)
os.system("lsof -i :5000 -t 2>/dev/null | xargs -r kill -9")

if not _wait_for_port_free(5000, timeout=15):
    _log("FATAL: port 5000 still not free after 15s")
    sys.exit(1)

_log("port 5000 is free, starting streamlit")

streamlit_proc = subprocess.Popen(
    [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "5000",
    ],
    env=os.environ.copy(),
    preexec_fn=os.setsid,
)
_log(f"Streamlit started, PID={streamlit_proc.pid}")

atexit.register(_kill_child)
signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)

trigger_thread = threading.Thread(target=self_trigger, daemon=True)
trigger_thread.start()

sys.exit(streamlit_proc.wait())
