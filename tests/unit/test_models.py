"""Tests des modèles de données financières."""
from datetime import date

import pytest
from pydantic import ValidationError

from finscoring.data.models import (
    BalanceSheet,
    CashFlowStatement,
    FinancialStatement,
    IncomeStatement,
)


# ---------- Fixtures (données réutilisables entre tests) ----------

@pytest.fixture
def valid_balance_sheet_data() -> dict:
    """Bilan minimal valide pour les tests."""
    return {
        "period_end": date(2023, 12, 31),
        "cash_and_equivalents": 10_000.0,
        "accounts_receivable": 5_000.0,
        "inventory": 3_000.0,
        "current_assets": 18_000.0,
        "non_current_assets": 50_000.0,
        "total_assets": 68_000.0,
        "accounts_payable": 4_000.0,
        "short_term_debt": 2_000.0,
        "current_liabilities": 6_000.0,
        "long_term_debt": 20_000.0,
        "non_current_liabilities": 22_000.0,
        "total_liabilities": 28_000.0,
        "total_equity": 40_000.0,
    }


# ---------- Tests : construction valide ----------

class TestBalanceSheet:
    def test_valid_construction(self, valid_balance_sheet_data: dict) -> None:
        """Un bilan avec données valides doit se construire sans erreur."""
        bs = BalanceSheet(**valid_balance_sheet_data)
        assert bs.total_assets == 68_000.0
        assert bs.period_end == date(2023, 12, 31)

    def test_immutability(self, valid_balance_sheet_data: dict) -> None:
        """Un bilan doit être immuable (frozen=True)."""
        bs = BalanceSheet(**valid_balance_sheet_data)
        with pytest.raises(ValidationError):
            bs.total_assets = 999_999.0  # type: ignore[misc]

    def test_extra_field_forbidden(self, valid_balance_sheet_data: dict) -> None:
        """Un champ non déclaré doit être rejeté (extra='forbid')."""
        invalid_data = {**valid_balance_sheet_data, "unexpected_field": 42.0}
        with pytest.raises(ValidationError):
            BalanceSheet(**invalid_data)

    def test_nan_rejected(self, valid_balance_sheet_data: dict) -> None:
        """Une valeur NaN doit être rejetée."""
        invalid_data = {**valid_balance_sheet_data, "total_assets": float("nan")}
        with pytest.raises(ValidationError):
            BalanceSheet(**invalid_data)