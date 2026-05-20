from datetime import datetime


class Expense:
    def __init__(self, date: str, category: str, description: str, amount: float):
        self._date = date
        self._category = category
        self._description = description
        # CRITICAL FIX: Use the setter to trigger validation immediately
        self.amount = amount

    @property
    def date(self): return self._date

    @property
    def category(self): return self._category

    @property
    def description(self): return self._description

    @property
    def amount(self): return self._amount

    @amount.setter
    def amount(self, value: float):
        if value < 0:
            raise ValueError("Expense amount cannot be negative.")
        self._amount = value


class CategoryLimit:
    def __init__(self, category: str, limit: float):
        self._category = category
        # Use setter for validation
        self.limit = limit

    @property
    def category(self): return self._category

    @property
    def limit(self): return self._limit

    @limit.setter
    def limit(self, value: float):
        if value < 0:
            raise ValueError("Budget limit cannot be negative.")
        self._limit = value


class BudgetStatus:
    """Data transfer object for the analysis result."""

    def __init__(self, category: str, spent: float, limit: float):
        self.category = category
        self.spent = spent
        self.limit = limit
        self.remaining = limit - spent
        self.status = self._determine_status()

    def _determine_status(self) -> str:
        if self.limit == 0: return "No Limit Set"
        percentage = (self.spent / self.limit) * 100
        if percentage >= 100: return "Over Budget"
        if percentage >= 80: return "Warning"
        return "Safe"

    @property
    def percentage_used(self):
        if self.limit == 0: return 0
        return round((self.spent / self.limit) * 100, 1)