from pathlib import Path
from src.db import init_db,save_transactions,fetch_transactions
from src.ingest import load_csv
from src.analyze import calculate_kpis,category_summary,monthly_summary
from src.plots import create_charts
from src.report import export_month

ROOT=Path(__file__).resolve().parent
def main():
    init_db()
    sample=load_csv(ROOT/"data"/"expenses.csv",account="Sample Account")
    added=save_transactions(sample); df=fetch_transactions()
    print("PERSONAL EXPENSE TRACKER")
    print(f"Sample rows processed: {len(sample)} | New rows added: {added}")
    print("\\nOverall summary:")
    for key,value in calculate_kpis(df).items():
        print(f"- {key.replace('_',' ').title()}: {value if isinstance(value,str) else f'INR {value:,.2f}'}")
    print("\\nCategory summary:\\n",category_summary(df).to_string(index=False))
    print("\\nMonthly summary:\\n",monthly_summary(df).to_string(index=False))
    print("\\nCharts saved:")
    for p in create_charts(df,ROOT/"outputs"): print("-",p.relative_to(ROOT))
    month=sorted(df.date.str[:7].unique())[-1]
    print(f"\\nMonthly report for {month}:")
    for kind,p in export_month(df,month,ROOT/"reports").items(): print(f"- {kind}: {p.relative_to(ROOT)}")
if __name__=="__main__": main()
