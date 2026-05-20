from abc import ABC, abstractmethod
from typing import List, Dict
from models import Expense, CategoryLimit, BudgetStatus

class IExpenseReader(ABC):
    @abstractmethod
    def read_expenses(self, file_path: str) -> List[Expense]:
        pass

class ILimitReader(ABC):
    @abstractmethod
    def read_limits(self, file_path: str) -> Dict[str, float]:
        pass

class IBudgetStrategy(ABC):
    @abstractmethod
    def analyze_budget(self, expenses: List[Expense], limits: Dict[str, float]) -> List[BudgetStatus]:
        pass

class IReportWriter(ABC):
    @abstractmethod
    def generate_report(self, status_list: List[BudgetStatus], output_path: str) -> bool:
        pass