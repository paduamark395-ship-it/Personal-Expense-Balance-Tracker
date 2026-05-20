import csv
from typing import List, Dict
from interfaces import IExpenseReader, ILimitReader
from models import Expense

class CSVExpenseReader(IExpenseReader):
    def read_expenses(self, file_path: str) -> List[Expense]:
        expenses = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        e = Expense(
                            date=row['date'],
                            category=row['category'],
                            description=row['description'],
                            amount=float(row['amount'])
                        )
                        expenses.append(e)
                    except ValueError:
                        continue
        except FileNotFoundError:
            return []
        return expenses

class CSVLimitReader(ILimitReader):
    def read_limits(self, file_path: str) -> Dict[str, float]:
        limits = {}
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    limits[row['category']] = float(row['limit'])
        except FileNotFoundError:
            return {}
        return limits