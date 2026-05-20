from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from datetime import datetime
from engine import BudgetManager
from readers import CSVExpenseReader, CSVLimitReader
from strategies import StandardBudgetStrategy
from writers import TextReportWriter, CSVWriter
from models import Expense, CategoryLimit

app = Flask(__name__)

# Configuration
DATA_FOLDER = 'data'
EXPENSE_FILE = os.path.join(DATA_FOLDER, 'expenses.csv')
LIMIT_FILE = os.path.join(DATA_FOLDER, 'limits.csv')
REPORT_FILE = os.path.join(DATA_FOLDER, 'budget_report.txt')

os.makedirs(DATA_FOLDER, exist_ok=True)

# Dependency Injection
exp_reader = CSVExpenseReader()
lim_reader = CSVLimitReader()
strategy = StandardBudgetStrategy()
reporter = TextReportWriter()
manager = BudgetManager(exp_reader, lim_reader, strategy, reporter)


def update_limit_file(category: str, limit: float):
    """Helper to read-modify-write limits CSV."""
    limits = lim_reader.read_limits(LIMIT_FILE)
    limits[category] = limit

    with open(LIMIT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'limit'])
        for cat, lim in limits.items():
            writer.writerow([cat, lim])


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None

    # Handle Expense Addition
    if request.method == 'POST' and 'add_expense' in request.form:
        try:
            date = request.form['date']
            cat = request.form['category']
            desc = request.form['description']
            amt = float(request.form['amount'])

            new_exp = Expense(date, cat, desc, amt)
            writer = CSVWriter()
            writer.save_expense(EXPENSE_FILE, new_exp)
            message = f"Expense added: {desc} ({amt})"
        except ValueError as e:
            message = f"Error: {e}"

    # Handle Limit Setting
    if request.method == 'POST' and 'set_limit' in request.form:
        cat = request.form['limit_category']
        lim = float(request.form['limit_amount'])
        try:
            update_limit_file(cat, lim)
            message = f"Budget limit set for {cat}: {lim}"
        except Exception as e:
            message = f"Error setting limit: {e}"

    # Process Data
    results = manager.analyze(EXPENSE_FILE, LIMIT_FILE, REPORT_FILE)

    # Calculate Total Spent
    expenses = exp_reader.read_expenses(EXPENSE_FILE)
    total_spent = sum(e.amount for e in expenses)

    return render_template('index.html', results=results, message=message, total_spent=total_spent)


if __name__ == '__main__':
    app.run(debug=True)