"""Slice 1 ONLY: experimental Streamlit number-input behaviour.

No PayGap Navigator business calculations or production validation live here.
All numbers must be synthetic. This spike tests whether the UI preserves raw
precision before any downstream validation can reject an over-precise entry.
"""

from decimal import Decimal

import streamlit as st

st.set_page_config(page_title="Numeric input feasibility spike")
st.title("Slice 1 — Numeric input feasibility")
st.caption("Isolated Streamlit experiment. NOT the PayGap Navigator application.")
st.write(
    "Use only synthetic amounts. Test blank, 0, 1, 1.2, 1.23, and 1.234. "
    "After each entry, press Tab or Enter to commit the widget edit. "
    "Then hide and restore each input to check draft persistence."
)


def capture_to_draft(name: str) -> None:
    """Preserve the widget value in a non-widget session-state key."""
    st.session_state[f"draft_{name}"] = st.session_state[f"widget_{name}"]


def describe(value: float | None) -> str:
    """Inspect numeric precision *received from the widget* (not the raw keystrokes)."""
    if value is None:
        return "BLANK (None)"
    try:
        significant_cents = Decimal(str(value)) * 100
        if significant_cents != significant_cents.to_integral_value():
            return "OVER-PRECISE VALUE OBSERVED BY PYTHON — can reject"
    except (ValueError, ArithmeticError):
        return "UNUSABLE VALUE"
    return "Within two-decimal precision (as received by Python)"


for name, display_format in (("two", "%.2f"), ("four", "%.4f")):
    st.divider()
    st.subheader(f"Candidate {name}: format={display_format}")
    st.session_state.setdefault(f"draft_{name}", None)
    st.session_state.setdefault(f"show_{name}", True)
    st.checkbox("Show numeric input", key=f"show_{name}")
    widget_key = f"widget_{name}"

    if st.session_state[f"show_{name}"]:
        # The draft is independent of the temporary widget, which Streamlit
        # may remove when the widget disappears from a conditional screen.
        if widget_key not in st.session_state:
            st.session_state[widget_key] = st.session_state[f"draft_{name}"]

        st.number_input(
            f"Synthetic remuneration (R) — {name}",
            value=None,
            step=0.01,
            format=display_format,
            key=widget_key,
            on_change=capture_to_draft,
            args=(name,),
            placeholder="Leave blank to test None",
        )
        st.write(f"Server widget value: `{st.session_state[widget_key]!r}`")
        st.write(f"Widget precision check: **{describe(st.session_state[widget_key])}**")
    else:
        st.info("Widget hidden. Toggle Show to recreate it from the saved draft.")

    st.write(f"Persistent draft value: `{st.session_state[f'draft_{name}']!r}`")

st.divider()
st.warning(
    "Important: the server cannot reject 1.234 if the browser/widget has "
    "already rounded it to 1.23 before sending the value. Seeing 'valid' "
    "after typing 1.234 is therefore a FAILURE, not evidence of success."
)
