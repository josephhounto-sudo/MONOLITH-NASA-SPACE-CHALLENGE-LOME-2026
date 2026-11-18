"""Open the Streamlit app past the opening hook (the hook has its own tests)."""
from streamlit.testing.v1 import AppTest


def open_app(path, timeout=60):
    at = AppTest.from_file(path, default_timeout=timeout)
    at.session_state["cs-hook-done"] = True
    return at.run()
