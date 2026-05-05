"""Modèles de données pour les états financiers.

Ces modèles définissent le contrat métier indépendamment de toute source
de données. Toute API externe (yfinance, FMP, ...) doit être convertie
vers ces modèles via un Adapter.
"""
from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

# Type alias pour la lisibilité : un montant financier est un float positif ou négatif,
# mais on documente que les NaN sont interdits.
Money = Annotated[float, Field(allow_inf_nan=False)]

class BalanceSheet(BaseModel):
    """Bilan : photographie du patrimoine à une date donnée.

    Equation fondamentale : total_assets = total_liabilities + total_equity
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Date de clôture (fin de l'exercice)
    period_end: date

    # ACTIF
    cash_and_equivalents: Money       # Trésorerie et équivalents
    accounts_receivable: Money        # Créances clients
    inventory: Money                  # Stocks
    current_assets: Money             # Total actif circulant
    non_current_assets: Money         # Total actif immobilisé
    total_assets: Money               # Total de l'actif

    # PASSIF
    accounts_payable: Money           # Dettes fournisseurs
    short_term_debt: Money            # Dettes financières CT (< 1 an)
    current_liabilities: Money        # Total passif circulant
    long_term_debt: Money             # Dettes financières LT (> 1 an)
    non_current_liabilities: Money    # Total passif non courant
    total_liabilities: Money          # Total des dettes
    total_equity: Money               # Capitaux propres

class IncomeStatement(BaseModel):
    """Compte de résultat : performance sur une période.

    Cascade : revenue → ebitda → ebit → net_income
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    period_end: date

    revenue: Money  # Chiffre d'affaires
    cost_of_revenue: Money  # Coût des ventes
    gross_profit: Money  # Marge brute
    operating_expenses: Money  # Charges d'exploitation (hors COGS)
    ebitda: Money  # EBITDA
    depreciation_amortization: Money  # Dotations aux amortissements
    ebit: Money  # Résultat d'exploitation
    interest_expense: Money  # Charges d'intérêts
    income_before_tax: Money  # Résultat avant impôts
    income_tax: Money  # Impôts sur les bénéfices
    net_income: Money  # Résultat net

class CashFlowStatement(BaseModel):
    """Tableau de flux de trésorerie : mouvements de cash sur une période.

    L'indicateur clé est le Free Cash Flow (FCF) = CFO - CAPEX.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    period_end: date

    # Flux d'exploitation
    cash_from_operations: Money  # CFO

    # Flux d'investissement
    capital_expenditure: Money  # CAPEX (généralement négatif)
    cash_from_investing: Money  # CFI total

    # Flux de financement
    cash_from_financing: Money  # CFF
    dividends_paid: Money  # Dividendes versés (généralement négatif)

    # Variation totale
    net_change_in_cash: Money

class FinancialStatement(BaseModel):
    """État financier complet d'une entreprise pour une période donnée.

    Compose les 3 états financiers et ajoute les métadonnées (ticker, devise).
    Les 3 états DOIVENT avoir la même `period_end` (validé à la construction).
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    ticker: str = Field(min_length=1, max_length=10)
    currency: str = Field(min_length=3, max_length=3)  # Code ISO 4217 (USD, EUR...)
    period_end: date

    balance_sheet: BalanceSheet
    income_statement: IncomeStatement
    cash_flow: CashFlowStatement

def test_something():
    # Arrange : préparer les données
    data = {...}
    # Act : exécuter le code à tester
    result = MyModel(**data)
    # Assert : vérifier le résultat
    assert result.field == expected_value