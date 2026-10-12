"""PayGap Navigator — Slice 3: thin, local three-screen journey.

Only the current-year ratio is active. Historical data, optional statistics,
scenario calculations, complete precision checks and dirty-state warnings
are deliberately reserved for later approved slices.
"""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from typing import Any

import streamlit as st

from calculations import calculate_current_year


st.set_page_config(page_title="PayGap Navigator", page_icon="🧭", layout="centered")

# The approved seven-field record shape, even though only three fields are
# editable in this initial skeleton.
RECORD_FIELDS = (
    "year",
    "top_5_total",
    "bottom_5_total",
    "highest_total",
    "lowest_total",
    "average_total",
    "median_total",
)
SCREENS = ("calculate", "understand", "explore")


def blank_record() -> dict[str, Any]:
    """Return a fresh current-year draft with genuinely blank numeric fields."""
    return {field: None for field in RECORD_FIELDS}


def init_session() -> None:
    """Initialise only the state used by Slice 3."""
    defaults = {
        "pn_screen": "calculate",
        "pn_started": False,
        "pn_draft_current": blank_record(),
        "pn_draft_history": [],
        "pn_confirmed_current": None,
        "pn_confirmed_history": [],
        "pn_confirmed_result": None,
        "pn_errors": [],
        "pn_technical_error": None,
    }
    for name, value in defaults.items():
        if name not in st.session_state:
            st.session_state[name] = value


def navigate(screen: str) -> None:
    """Allow results screens only after a successful confirmation."""
    if screen not in SCREENS:
        return
    if screen != "calculate" and st.session_state["pn_confirmed_result"] is None:
        return
    st.session_state["pn_screen"] = screen
    st.rerun()


def render_navigation() -> None:
    """The same three-stage navigation appears on every screen."""
    current = st.session_state["pn_screen"]
    has_results = st.session_state["pn_confirmed_result"] is not None
    columns = st.columns([1, 1.5, 1])
    stages = (
        ("calculate", "1 · CALCULATE"),
        ("understand", "2 · UNDERSTAND & TRACK"),
        ("explore", "3 · EXPLORE"),
    )
    for column, (screen, label) in zip(columns, stages):
        with column:
            if st.button(
                label,
                key=f"pn_nav_{screen}",
                use_container_width=True,
                disabled=(screen == current or (screen != "calculate" and not has_results)),
                type="primary" if screen == current else "secondary",
            ):
                navigate(screen)
    st.divider()


def capture_input(field: str) -> None:
    """Copy the widget's value into a draft independent of widget lifetime."""
    st.session_state["pn_draft_current"][field] = st.session_state[f"pn_input_{field}"]
    # Previously displayed validation errors must not look like a fresh check.
    st.session_state["pn_errors"] = []
    st.session_state["pn_technical_error"] = None


def money_label(value: Any) -> str:
    """Simple current-year rand display; advanced adaptive formatting is later."""
    amount = Decimal(str(value))
    displayed = format(amount, ",.2f")
    if "." in displayed:
        displayed = displayed.rstrip("0").rstrip(".")
    return f"R{displayed}"


def show_field_errors(field: str) -> None:
    for item in st.session_state["pn_errors"]:
        if item.get("field") == field:
            st.error(item["message"])


def confirm_draft() -> None:
    """Validate a deep copy and replace confirmed data only on success."""
    proposed = deepcopy(st.session_state["pn_draft_current"])
    try:
        outcome = calculate_current_year(proposed)
    except Exception:
        # No remuneration amounts or traceback are intentionally logged.
        st.session_state["pn_technical_error"] = (
            "Something unexpected prevented this calculation. Your previously "
            "confirmed results have not been changed. Please try again."
        )
        st.session_state["pn_errors"] = []
        st.rerun()
        return

    if not outcome["success"]:
        st.session_state["pn_errors"] = outcome["errors"]
        st.session_state["pn_technical_error"] = None
        st.rerun()
        return

    st.session_state["pn_confirmed_current"] = deepcopy(proposed)
    st.session_state["pn_confirmed_result"] = deepcopy(outcome["results"])
    st.session_state["pn_errors"] = []
    st.session_state["pn_technical_error"] = None
    st.session_state["pn_screen"] = "understand"
    st.rerun()


def render_calculate() -> None:
    if not st.session_state["pn_started"]:
        st.title("Understand your vertical pay gap")
        st.caption("PAYGAP NAVIGATOR · From disclosure to understanding and action")
        st.write(
            "South African public and state-owned companies disclose the ratio "
            "between aggregate remuneration of their highest-paid and "
            "lowest-paid 5% of employees. The ratio alone does not determine "
            "whether the gap is fair or what should be done about it."
        )
        st.write("**CALCULATE → UNDERSTAND & TRACK → EXPLORE**")
        st.caption("This tool explains and explores your own figures. It does not assign a fairness score.")
        if st.button("Start navigating your pay gap →", type="primary"):
            st.session_state["pn_started"] = True
            st.rerun()
        return

    st.title("Calculate your vertical remuneration gap")
    with st.expander("About PayGap Navigator"):
        st.write(
            "Enter your organisation's aggregate remuneration figures to "
            "calculate the descriptive vertical gap. A ratio on its own is not "
            "a judgement of fairness or legal compliance."
        )

    st.info(
        "**Before entering remuneration data**\n\n"
        "This is a publicly hosted prototype. Please use synthetic or publicly "
        "available aggregate remuneration figures only. Do not enter "
        "confidential organisational information.\n\n"
        "PayGap Navigator does not include a database or application feature "
        "designed to permanently store your remuneration inputs. However, "
        "information entered into the application is processed through the "
        "hosting environment while you use the tool."
    )
    st.caption(
        "Aggregate figures only. No individual employee records, employee "
        "identifiers or payroll files are required."
    )
    st.markdown(
        "**Enter amounts in full rand (ZAR).** If your source reports remuneration "
        "in thousands or millions of rand, convert the figures to full rand "
        "before entering them. For example, R25,000 reported in R'000 = "
        "enter 25,000,000."
    )
    st.caption(
        "Use **total remuneration**, not basic salary alone. Total remuneration "
        "includes salary, benefits, employer contributions to benefit funds, "
        "short- and long-term incentives, share options and incentive awards."
    )

    # Temporary widget keys can disappear when Screen 1 is not rendered.
    # Restore them from persistent draft records when returning to this screen.
    fields = (
        (
            "year",
            "Financial year ending",
            {"step": 1, "format": "%d", "help": (
                "Enter the calendar year in which the financial year covered "
                "by these figures ended, e.g. 2026 for a financial year "
                "ending in March 2026."
            )},
        ),
        (
            "top_5_total",
            "Top-5% aggregate remuneration (R)",
            {"step": 0.01, "format": "%.2f", "help": (
                "Combined total remuneration of the highest-paid 5% of employees."
            )},
        ),
        (
            "bottom_5_total",
            "Bottom-5% aggregate remuneration (R)",
            {"step": 0.01, "format": "%.2f", "help": (
                "Combined total remuneration of the lowest-paid 5% of employees."
            )},
        ),
    )
    for field, label, options in fields:
        widget_key = f"pn_input_{field}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = st.session_state["pn_draft_current"][field]
        st.number_input(
            label,
            value=None,
            key=widget_key,
            placeholder="Enter an amount" if field != "year" else "Enter the year",
            on_change=capture_input,
            args=(field,),
            **options,
        )
        show_field_errors(field)

    if st.session_state["pn_technical_error"]:
        st.error("**Unable to complete the calculation**\n\n" + st.session_state["pn_technical_error"])
    for item in st.session_state["pn_errors"]:
        if item.get("field") not in {"year", "top_5_total", "bottom_5_total"}:
            st.error(item["message"])

    if st.button("Calculate my pay gap →", type="primary"):
        confirm_draft()


def render_understand() -> None:
    results = st.session_state["pn_confirmed_result"]
    st.title("Understand your pay gap")
    st.write("Your ratio is only the starting point. It describes the remuneration difference, not whether the difference is fair.")
    st.subheader("Your vertical remuneration gap")
    st.metric("Confirmed ratio", f'{results["ratio"]:.1f} : 1')
    st.write(results["interpretation"])
    top_column, bottom_column = st.columns(2)
    top_column.metric("Top 5% total remuneration", money_label(results["top_5_total"]))
    bottom_column.metric("Bottom 5% total remuneration", money_label(results["bottom_5_total"]))
    st.caption("These results use the last confirmed figures. Recalculate on Screen 1 to apply new edits.")
    st.info("Historical tracking will be added in a later build stage. No historical results are currently calculated.")
    st.caption("This descriptive ratio is not a determination that remuneration is fair, unfair, lawful or unlawful.")
    back, next_screen = st.columns(2)
    with back:
        if st.button("← Edit remuneration data", use_container_width=True):
            navigate("calculate")
    with next_screen:
        if st.button("Explore scenarios →", type="primary", use_container_width=True):
            navigate("explore")


def render_explore() -> None:
    results = st.session_state["pn_confirmed_result"]
    st.title("Explore what could change the gap")
    st.write("Your currently confirmed baseline is shown below.")
    st.metric("Current confirmed gap", f'{results["ratio"]:.1f} : 1')
    top_column, bottom_column = st.columns(2)
    top_column.metric("Top 5% aggregate remuneration", money_label(results["top_5_total"]))
    bottom_column.metric("Bottom 5% aggregate remuneration", money_label(results["bottom_5_total"]))
    st.info(
        "**Development placeholder:** Scenario controls have not yet been "
        "implemented. No hypothetical changes or scenario results are calculated here."
    )
    st.caption("The baseline uses last confirmed data only. Edits on Screen 1 require a new calculation.")
    if st.button("← Back to Understand & Track"):
        navigate("understand")


def main() -> None:
    init_session()
    # Defensive navigation gate even if a stale session key names a result screen.
    if st.session_state["pn_screen"] not in SCREENS or (
        st.session_state["pn_screen"] != "calculate"
        and st.session_state["pn_confirmed_result"] is None
    ):
        st.session_state["pn_screen"] = "calculate"
    render_navigation()
    screen = st.session_state["pn_screen"]
    if screen == "calculate":
        render_calculate()
    elif screen == "understand":
        render_understand()
    else:
        render_explore()


if __name__ == "__main__":
    main()
