# Personal Expense Tracker with Data Visualization

A Python portfolio project that records personal transactions, categorizes expenses, stores them in SQLite, analyzes spending, visualizes patterns, manages monthly budgets, and exports reports. It uses synthetic/sample data and manual/CSV entry. **It does not connect to real bank accounts.**

## Problem statement
People can lose track of small purchases and may not know which categories consume most of their money. This app organizes transactions into useful summaries, charts and budget checks.

## Features
- Manual transaction entry and CSV import
- Keyword-based automatic category suggestions
- SQLite persistence and duplicate import protection
- Category, monthly, payment-method and daily analysis
- Spending, income, savings, average daily spend and highest category KPIs
- Monthly category budgets and overspending status
- Matplotlib/Seaborn chart exports
- Streamlit dashboard
- CSV, TXT and Excel monthly reports

## Technology
Python 3.11+, Pandas, NumPy, SQLite, Matplotlib, Seaborn, Streamlit, openpyxl and pytest.

## Structure
```text
Personal-Expense-Tracker-Visualization/
├── data/       # Sample CSV data
├── db/         # SQLite database, created at runtime
├── docs/       # Project guide and interview prep
├── images/     # Add your real screenshots here
├── notebooks/  # Optional notebooks
├── outputs/    # Generated charts
├── reports/    # Monthly exports
├── src/        # Reusable Python modules
├── tests/      # Basic automated tests
├── app.py      # Streamlit dashboard
├── main.py     # Command-line simulation
├── requirements.txt
└── README.md
```

## Installation
Windows:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
macOS/Linux:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
Command-line simulation:
```bash
python main.py
```
Dashboard:
```bash
streamlit run app.py
```
Open the local URL printed by Streamlit, usually `http://localhost:8501`.

The CLI loads the included sample CSV into SQLite, prints summaries, saves four charts in `outputs/`, and exports the latest monthly report into `reports/`.

## CSV format
Required: `date`, `description`, `amount`. Optional: `category`, `payment_method`, `note`. Expenses are negative; income is positive.
```csv
date,description,amount,category,payment_method,note
2026-11-01,Groceries,-850,Groceries,UPI,Weekly shopping
2026-11-02,Stipend,12000,Income,Bank Transfer,Monthly income
```

## Tests
```bash
pytest -q
```

## Screenshots to add
Capture genuine screenshots from your own run: dashboard, CSV import, terminal output, all four charts, budget check, monthly report and GitHub repository page. Save them in `images/`.

## Industry relevance and learning outcomes
Demonstrates data ingestion, validation, cleaning, rule-based categorization, relational database design, SQL, aggregation, KPI calculation, visualization, reporting and basic UI development. These are useful foundations for Python Developer, Data Analyst, Business Analyst and finance/fintech roles.

## Limitations and future work
Categorization is keyword-based and may require corrections. Data is synthetic/manual, with no bank connection. Future improvements include receipt OCR, recurring expense rules, email/SMS alerts, ML categorization, multi-currency support and PostgreSQL.

## GitHub
Repository: `personal-expense-tracker-visualization`  
Description: `Python expense tracker with SQLite, CSV import, automatic categorization, budget monitoring, Streamlit dashboard and visual reports.`  
Topics: `python`, `pandas`, `sqlite`, `streamlit`, `data-visualization`, `personal-finance`, `matplotlib`, `seaborn`

Never upload private bank statements, passwords, API keys or other confidential financial data.
