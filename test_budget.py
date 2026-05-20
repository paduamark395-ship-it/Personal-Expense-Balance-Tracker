import pytest
from models import Expense, CategoryLimit
from strategies import StandardBudgetStrategy


# 1. Test Encapsulation (Should pass now with the models.py fix)
def test_expense_validation():
    # This should raise ValueError because amount is negative
    with pytest.raises(ValueError):
        Expense("2023-01-01", "Food", "Test", -100)


# 2. Test Strategy Logic (Safe Zone)
def test_budget_status():
    strategy = StandardBudgetStrategy()

    # Mock Data
    expenses = [
        Expense("2023-01-01", "Food", "Lunch", 400),
        Expense("2023-01-02", "Food", "Dinner", 200)
    ]
    limits = {"Food": 1000}

    results = strategy.analyze_budget(expenses, limits)

    assert len(results) == 1
    assert results[0].spent == 600
    assert results[0].percentage_used == 60.0
    assert results[0].status == "Safe"


# 3. Test Strategy Logic (Over Budget)
def test_over_budget():
    strategy = StandardBudgetStrategy()

    expenses = [Expense("2023-01-01", "Tech", "Laptop", 1500)]
    limits = {"Tech": 1000}

    results = strategy.analyze_budget(expenses, limits)

    assert results[0].status == "Over Budget"
    assert results[0].spent == 1500