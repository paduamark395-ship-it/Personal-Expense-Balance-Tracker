from typing import List, Dict
from interfaces import IExpenseReader, ILimitReader, IBudgetStrategy, IReportWriter
from models import Expense, BudgetStatus


class BudgetManager:
    def __init__(self, exp_reader: IExpenseReader, lim_reader: ILimitReader,
                 strategy: IBudgetStrategy, reporter: IReportWriter):
        self._exp_reader = exp_reader
        self._lim_reader = lim_reader
        self._strategy = strategy
        self._reporter = reporter

    def analyze(self, exp_path: str, lim_path: str, report_path: str) -> List[BudgetStatus]:
        expenses = self._exp_reader.read_expenses(exp_path)
        limits = self._lim_reader.read_limits(lim_path)

        results = self._strategy.analyze_budget(expenses, limits)
        self._reporter.generate_report(results, report_path)
        return results