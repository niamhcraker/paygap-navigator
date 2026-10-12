"""Backend-only safety probes; NOT proof of browser input preservation.

Full Slice 1 feasibility requires a real Streamlit browser session. These tests
are useful preparation but cannot substitute for exercising the rendered widget.
"""

import pytest

streamlit = pytest.importorskip("streamlit", reason="Streamlit not installed in test environment")
from streamlit.testing.v1 import AppTest  # noqa: E402
from pathlib import Path  # noqa: E402

SPIKE = Path(__file__).with_name("numeric_input_spike.py")


def test_blank_and_zero_remain_distinct_on_backend():
    page = AppTest.from_file(str(SPIKE)).run()
    assert len(page.exception) == 0
    assert page.number_input[0].value is None
    page.number_input[0].set_value(0.0).run()
    assert len(page.exception) == 0
    assert page.number_input[0].value == 0.0
    assert page.session_state["draft_two"] == 0.0


@pytest.mark.parametrize("value", [1.0, 1.2, 1.23, 1.234])
def test_back_end_receives_test_number(value):
    """AppTest injects numerical values; browser formatting is NOT exercised."""
    page = AppTest.from_file(str(SPIKE)).run()
    assert len(page.exception) == 0
    page.number_input[0].set_value(value).run()
    assert len(page.exception) == 0
    assert page.session_state["draft_two"] == value


def test_draft_survives_temporary_widget_disappearance():
    page = AppTest.from_file(str(SPIKE)).run()
    page.number_input[0].set_value(1.23).run()
    assert page.session_state["draft_two"] == 1.23
    page.checkbox[0].set_value(False).run()
    assert page.session_state["draft_two"] == 1.23
    page.checkbox[0].set_value(True).run()
    assert page.number_input[0].value == 1.23
