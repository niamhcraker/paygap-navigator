"""PayGap Navigator — deterministic calculation layer.

Slice 2 implements only the required CURRENT-YEAR ratio and its blocking
validation. Future slices will add optional-context warnings, historical
analysis, scenario calculations and display-formatting rules.

This module does not import Streamlit or access session state. All example
figures used in tests are synthetic.
"""

from __future__ import annotations

from decimal import Decimal, DecimalException, localcontext
import math
from typing import Any, Mapping


_FIELD_LABELS = {
    "top_5_total": "Top-5% aggregate total remuneration",
    "bottom_5_total": "Bottom-5% aggregate total remuneration",
}


def _error(field: str, code: str, message: str) -> dict[str, str]:
    """A field-addressable, practitioner-friendly validation message."""
    return {"field": field, "code": code, "message": message}


def _outcome(
    *, results: dict[str, Any] | None = None, errors: list[dict[str, str]] | None = None
) -> dict[str, Any]:
    """The small, consistent interface consumed by the future Streamlit app."""
    problems = errors if errors is not None else []
    return {
        "success": not problems,
        "results": None if problems else results,
        "errors": problems,
        # Data-quality warnings intentionally arrive in Slice 6, not Slice 2.
        "warnings": [],
    }


def _validate_money(
    record: Mapping[str, Any], field: str, errors: list[dict[str, str]]
) -> Decimal | None:
    """Validate the basic numeric/safety rules without silently coercing text.

    The >2-decimal *manual-entry* rule is added in Slice 6, after the
    Streamlit draft-persistence implementation is exercised in Slices 3–5.
    """
    value = record.get(field)
    label = _FIELD_LABELS[field]

    if value is None:
        errors.append(_error(field, "missing", f"Enter the {label.lower()} before calculating the ratio."))
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        errors.append(_error(field, "not_numeric", f"Enter a numeric amount for {label.lower()}."))
        return None

    try:
        amount = Decimal(str(value))
    except (DecimalException, ValueError, OverflowError):
        errors.append(_error(field, "not_numeric", f"Enter a usable numeric amount for {label.lower()}."))
        return None

    if not amount.is_finite():
        errors.append(_error(field, "non_finite", f"Enter a finite amount for {label.lower()}."))
        return None
    if amount < 0:
        errors.append(_error(field, "negative", "Remuneration values cannot be negative. Check the amount entered for " + label.lower() + "."))
        return None
    if field == "bottom_5_total" and amount == 0:
        errors.append(_error(field, "zero_denominator", "The bottom-5% total remuneration must be greater than zero to calculate a ratio."))
        return None

    return amount


def _finite_ratio(top: Decimal, bottom: Decimal) -> float | None:
    """Divide validated amounts without overflowing on huge, balanced inputs.

    Decimal protects a ratio such as 10**400 / 10**399 from Python's
    intermediate int-to-float conversion overflow. The resulting ratio must
    still fit in a finite float for the subsequent UI calculations.
    """
    try:
        with localcontext() as context:
            context.prec = 34
            quotient = top / bottom
            if not quotient.is_finite():
                return None
            ratio = float(quotient)
        # A nonzero ratio that underflows to 0.0 is not a trustworthy result.
        if ratio == 0.0 and quotient != 0:
            return None
        return ratio if math.isfinite(ratio) else None
    except (DecimalException, OverflowError, ValueError):
        return None


def calculate_current_year(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate required fields and calculate the current-year aggregate ratio.

    Input: mapping containing ``year``, ``top_5_total`` and ``bottom_5_total``.
    Output: ``success``, ``results``, ``errors`` and ``warnings``.
    All expected validation failures return a *non-success* outcome with no
    result; they do not raise raw exceptions to the future UI.

    Optional remuneration fields and historical records are NOT handled in
    Slice 2. Do not treat this function as the complete seven-field validator.
    """
    if not isinstance(record, Mapping):
        return _outcome(errors=[_error("record", "invalid_record", "Enter a valid remuneration record before calculating.")])

    errors: list[dict[str, str]] = []
    year = record.get("year")
    if year is None:
        errors.append(_error("year", "missing", "Enter the financial year ending before calculating."))
    elif isinstance(year, bool) or not isinstance(year, int) or year < 1:
        errors.append(_error("year", "invalid_year", "Enter a valid whole-number financial year ending."))

    top = _validate_money(record, "top_5_total", errors)
    bottom = _validate_money(record, "bottom_5_total", errors)
    if errors:
        return _outcome(errors=errors)

    # The validation above guarantees both are Decimal, bottom > 0, year int.
    assert top is not None and bottom is not None and isinstance(year, int)
    ratio = _finite_ratio(top, bottom)
    if ratio is None:
        return _outcome(
            errors=[
                _error(
                    "ratio",
                    "calculation_range",
                    "The entered values cannot be processed reliably. Please check the remuneration amounts and try again.",
                )
            ]
        )

    return _outcome(
        results={
            "year": year,
            # Keep the entered numeric values; do not round or substitute zero.
            "top_5_total": record["top_5_total"],
            "bottom_5_total": record["bottom_5_total"],
            "ratio": ratio,
            "interpretation": (
                "The top 5% highest-paid employees collectively received "
                f"{ratio:.1f} times the total remuneration received by the "
                "bottom 5% lowest-paid employees."
            ),
        }
    )
