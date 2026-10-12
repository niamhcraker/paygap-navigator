"""Slice 2 tests of the standalone calculation layer (no Streamlit required)."""

from decimal import Decimal
import math

import pytest

from calculations import calculate_current_year


def record(**overrides):
    values = {"year": 2026, "top_5_total": 10_000_000, "bottom_5_total": 1_000_000}
    values.update(overrides)
    return values


def assert_blocked(outcome, *, field, code):
    assert outcome["success"] is False
    assert outcome["results"] is None
    assert outcome["warnings"] == []
    assert any(item["field"] == field and item["code"] == code for item in outcome["errors"])
    assert all(item["message"] for item in outcome["errors"])


def test_t001_ratio_and_plain_language_interpretation():
    result = calculate_current_year(record())
    assert result["success"] is True
    assert result["errors"] == []
    assert result["warnings"] == []
    assert result["results"]["year"] == 2026
    assert result["results"]["ratio"] == pytest.approx(10.0)
    assert "10.0 times" in result["results"]["interpretation"]
    assert "top 5% highest-paid" in result["results"]["interpretation"]
    assert "bottom 5% lowest-paid" in result["results"]["interpretation"]


def test_t004_zero_denominator_is_blocked():
    assert_blocked(
        calculate_current_year(record(top_5_total=20_000_000, bottom_5_total=0)),
        field="bottom_5_total", code="zero_denominator",
    )


def test_t005_negative_top_is_blocked_even_without_ui():
    assert_blocked(calculate_current_year(record(top_5_total=-1)), field="top_5_total", code="negative")


def test_t006_missing_bottom_is_blocked_distinct_from_zero():
    assert_blocked(calculate_current_year(record(bottom_5_total=None)), field="bottom_5_total", code="missing")


@pytest.mark.parametrize("field", ["top_5_total", "bottom_5_total"])
def test_missing_each_required_money_input(field):
    assert_blocked(calculate_current_year(record(**{field: None})), field=field, code="missing")


def test_missing_and_invalid_year():
    assert_blocked(calculate_current_year(record(year=None)), field="year", code="missing")
    for year in [0, -2026, True, 2026.0, 2026.5, "2026"]:
        assert_blocked(calculate_current_year(record(year=year)), field="year", code="invalid_year")


def test_multiple_errors_return_together_without_result():
    result = calculate_current_year({"year": None, "top_5_total": -1, "bottom_5_total": 0})
    assert result["success"] is False
    assert result["results"] is None
    assert {item["field"] for item in result["errors"]} == {"year", "top_5_total", "bottom_5_total"}


@pytest.mark.parametrize("field", ["top_5_total", "bottom_5_total"])
@pytest.mark.parametrize("value", ["123", True, False, complex(1, 2), [], {}])
def test_nonnumeric_money_is_rejected(field, value):
    assert_blocked(calculate_current_year(record(**{field: value})), field=field, code="not_numeric")


@pytest.mark.parametrize("field", ["top_5_total", "bottom_5_total"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), Decimal("NaN"), Decimal("Infinity")])
def test_nonfinite_input_is_rejected(field, value):
    assert_blocked(calculate_current_year(record(**{field: value})), field=field, code="non_finite")


def test_negative_bottom_is_blocked():
    assert_blocked(calculate_current_year(record(bottom_5_total=-0.01)), field="bottom_5_total", code="negative")


def test_zero_top_is_permitted_by_basic_rules():
    result = calculate_current_year(record(top_5_total=0))
    assert result["success"] is True
    assert result["results"]["ratio"] == 0.0
    # The agreed non-blocking below-one warning is implemented in Slice 6.


def test_ordinary_cent_amounts_are_not_rounded_before_ratio():
    result = calculate_current_year(record(top_5_total=Decimal("1.23"), bottom_5_total=Decimal("0.03")))
    assert result["success"] is True
    assert result["results"]["ratio"] == pytest.approx(41.0)
    assert result["results"]["top_5_total"] == Decimal("1.23")


def test_very_large_valid_values_still_give_an_ordinary_ratio():
    huge = 10**400
    result = calculate_current_year(record(top_5_total=huge, bottom_5_total=huge // 10))
    assert result["success"] is True
    assert result["results"]["ratio"] == pytest.approx(10.0)
    assert math.isfinite(result["results"]["ratio"])


def test_extreme_quotient_does_not_expose_infinity():
    result = calculate_current_year(record(top_5_total=Decimal("1e308"), bottom_5_total=Decimal("0.01")))
    assert_blocked(result, field="ratio", code="calculation_range")


def test_broken_record_is_a_controlled_error():
    assert_blocked(calculate_current_year(None), field="record", code="invalid_record")


def test_extremely_small_nonzero_ratio_must_not_silently_become_zero():
    result = calculate_current_year(
        record(top_5_total=Decimal("1e-400"), bottom_5_total=Decimal("1"))
    )
    assert_blocked(result, field="ratio", code="calculation_range")
