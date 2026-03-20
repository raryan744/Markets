#!/usr/bin/env python3
"""
background_runner.py
────────────────────
Standalone background process: data collection, CNN-LSTM/XGBoost training,
Bobby BRTI, Hawkes process, and auto-trading — all without a browser session.

Loads app.py with a mocked streamlit module so every @st.cache_resource
state dict and background thread starts immediately at server launch.
"""

import os
import sys
import time
import types

# ── Mock streamlit ─────────────────────────────────────────────────────────────
_cache_store: dict = {}


def _cache_resource_decorator(fn=None, **kw):
    """Replicate @st.cache_resource: return the same object on every call."""
    def decorator(f):
        def wrapper(*args, **kwargs):
            key = f.__qualname__
            if key not in _cache_store:
                _cache_store[key] = f(*args, **kwargs)
            return _cache_store[key]
        wrapper.__name__ = f.__name__
        wrapper.__qualname__ = f.__qualname__
        return wrapper
    if fn is not None:          # @st.cache_resource  (no parentheses)
        return decorator(fn)
    return decorator            # @st.cache_resource() (with parentheses)


class _CacheData:
    """@st.cache_data — just pass through in background runner (always fresh)."""
    def __call__(self, fn=None, **kw):
        def decorator(f):
            return f
        if fn is not None:
            return fn
        return decorator

    def clear(self):
        pass


class _FakeCtx:
    """Dummy context manager returned by st.sidebar / st.spinner / st.columns."""
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass
    def __getattr__(self, name):
        return _smart_noop
    def __iter__(self):
        return iter([_FakeCtx(), _FakeCtx()])
    def form_submit_button(self, *a, **kw):
        return False


def _noop(*a, **kw):
    return None


class _SmartNoop:
    """
    Callable that can act as:
      - A plain function: st.write("hello") → None
      - A decorator factory: @st.fragment(run_every=1) → passthrough decorator
      - A direct decorator: @st.dialog → passthrough decorator
    """
    def __call__(self, *a, **kw):
        # Single callable arg with no kwargs → direct decorator use (@st.xxx)
        if len(a) == 1 and callable(a[0]) and not kw:
            return a[0]
        # Called with args/kwargs → return a passthrough decorator factory
        def _passthrough(fn):
            return fn
        return _passthrough

    def __getattr__(self, name):
        return _SmartNoop()


_smart_noop = _SmartNoop()


def _selectbox(label, options, index=0, **kw):
    """Return the option at `index` so module-level dict lookups don't crash."""
    try:
        return list(options)[index]
    except Exception:
        return None


def _slider(label, min_value=0, max_value=100, value=None, **kw):
    return value if value is not None else min_value


def _columns(*a, **kw):
    n = a[0] if a else 2
    if isinstance(n, int):
        return [_FakeCtx() for _ in range(n)]
    return [_FakeCtx() for _ in range(len(n))]


class _Sidebar:
    """Fake st.sidebar — supports 'with st.sidebar:' and st.sidebar.xxx()."""
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass
    def __getattr__(self, name):
        return _noop


class _MockSt:
    cache_resource = staticmethod(_cache_resource_decorator)
    cache_data = _CacheData()
    sidebar = _Sidebar()

    selectbox = staticmethod(_selectbox)
    slider = staticmethod(_slider)
    columns = staticmethod(_columns)

    @staticmethod
    def tabs(labels, **kw):
        """Return one FakeCtx per tab so unpacking works."""
        return [_FakeCtx() for _ in labels]

    @staticmethod
    def expander(*a, **kw):
        return _FakeCtx()

    @staticmethod
    def container(*a, **kw):
        return _FakeCtx()

    @staticmethod
    def empty(*a, **kw):
        return _FakeCtx()

    @staticmethod
    def form(*a, **kw):
        return _FakeCtx()

    @staticmethod
    def checkbox(label, value=False, **kw):
        return value

    @staticmethod
    def button(*a, **kw):
        return False

    @staticmethod
    def radio(*a, options=None, index=0, **kw):
        try:
            return list(options)[index]
        except Exception:
            return None

    @staticmethod
    def multiselect(label, options, default=None, **kw):
        return list(default) if default else []

    @staticmethod
    def number_input(label, value=0, **kw):
        return value

    @staticmethod
    def text_input(label, value="", **kw):
        return value

    @staticmethod
    def spinner(*a, **kw):
        return _FakeCtx()

    def __getattr__(self, name):
        # Use smart_noop so this works as a plain call AND as a decorator factory
        return _smart_noop


class _SessionState(dict):
    """st.session_state — behaves as a plain dict with attribute access."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)


_mock_st = _MockSt()
_mock_st.session_state = _SessionState()

# Inject mock before any app.py import
sys.modules["streamlit"] = _mock_st  # type: ignore

# ── Boot ────────────────────────────────────────────────────────────────────────
_LOG = "/tmp/bg_runner.log"


def _log(msg: str):
    from datetime import datetime
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(_LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


_log("background_runner: starting — loading app.py engine")

os.environ["_BG_RUNNER"] = "1"
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

import importlib.util

spec = importlib.util.spec_from_file_location(
    "app_module", os.path.join(app_dir, "app.py")
)
app_mod = importlib.util.module_from_spec(spec)  # type: ignore
sys.modules["app_module"] = app_mod

try:
    spec.loader.exec_module(app_mod)  # type: ignore
    _log("background_runner: app.py loaded — _staggered_startup is now running")
except SystemExit:
    pass
except Exception as exc:
    _log(f"background_runner: ERROR loading app.py: {exc}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Keep the process alive; background threads are daemons but this process must live
_log("background_runner: entering keep-alive loop")
iteration = 0
while True:
    time.sleep(60)
    iteration += 1
    try:
        # Brief health log every 5 minutes
        if iteration % 5 == 0:
            import threading
            names = [t.name for t in threading.enumerate()]
            _log(f"background_runner alive — threads: {names}")
    except Exception:
        pass
