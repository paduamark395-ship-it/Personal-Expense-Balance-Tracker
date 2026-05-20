from typing import List
from interfaces import IReportWriter
from models import BudgetStatus
import csv
import os

class TextReportWriter(IReportWriter):
    def generate_report(self, status_list: List[BudgetStatus], output_path: str) -> bool:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=== BUDGET REPORT ===\n\n")
                for s in status_list:
                    f.write(f"Category: {s.category}\n")
                    f.write(f"  Spent: {s.spent:.2f} / {s.limit:.2f}\n")
                    f.write(f"  Status: {s.status} ({s.percentage_used}%)\n")
                    f.write("-" * 20 + "\n")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

class CSVWriter:
    def save_expense(self, file_path: str, expense):
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['date', 'category', 'description', 'amount'])
            writer.writerow([expense.date, expense.category, expense.description, expense.amount])

    def save_limit(self, file_path: str, category: str, limit: float):
        # For simplicity, we will rewrite the limits file every time a limit is added/updated
        # In a real app, we would read-modify-write.
        # Here we just append, but ideally limits should be unique per category.
        # We will handle logic in app.py to read-modify-write limits.
        pass