from typing import List, Dict
from interfaces import IBudgetStrategy
from models import Expense, BudgetStatus


class StandardBudgetStrategy(IBudgetStrategy):
    def analyze_budget(self, expenses: List[Expense], limits: Dict[str, float]) -> List[BudgetStatus]:
        # 1. Aggregate Spending per Category
        spending = {}
        for exp in expenses:
            if exp.category not in spending:
                spending[exp.category] = 0.0
            spending[exp.category] += exp.amount

        # 2. Create Status Objects
        status_list = []

        # Check categories that have limits
        processed_categories = set()

        for cat, limit in limits.items():
            spent = spending.get(cat, 0.0)
            status = BudgetStatus(cat, spent, limit)
            status_list.append(status)
            processed_categories.add(cat)

        # Check categories with spending but no limit
        for cat, spent in spending.items():
            if cat not in processed_categories:
                status = BudgetStatus(cat, spent, 0)  # Limit 0 implies no limit set
                status_list.append(status)

        return status_list