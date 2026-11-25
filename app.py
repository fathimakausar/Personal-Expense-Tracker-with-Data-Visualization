from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.db import init_db,save_transactions,fetch_transactions
from src.ingest import clean_transactions
from src.analyze import calculate_kpis,category_summary,monthly_summary,payment_summary,prepare_frame
from src.budget import set_budget,check_budgets
from src.report import export_month

st.set_page_config(page_title="Personal Expense Tracker",page_icon="💸",layout="wide")
init_db()
st.title("💸 Personal Expense Tracker")
st.caption("Track transactions, understand spending patterns, set budgets and export reports.")

with st.sidebar:
    st.header("Add a transaction")
    with st.form("manual"):
        date=st.date_input("Date")
        desc=st.text_input("Description")
        amount=st.number_input("Amount (INR)",min_value=0.01,step=10.0)
        kind=st.selectbox("Type",["Expense","Income"])
        payment=st.selectbox("Payment method",["UPI","Cash","Card","Bank Transfer","Other"])
        note=st.text_input("Note (optional)")
        submit=st.form_submit_button("Save transaction")
    if submit:
        if not desc.strip(): st.error("Enter a description.")
        else:
            signed=-amount if kind=="Expense" else amount
            row=clean_transactions(pd.DataFrame([{"date":str(date),"description":desc,"amount":signed,
                "payment_method":payment,"note":note}]))
            st.success(f"Saved {save_transactions(row)} transaction(s).")
            st.rerun()
    st.divider()
    st.header("Import CSV")
    upload=st.file_uploader("Choose CSV",type=["csv"])
    if upload is not None and st.button("Import transactions"):
        try:
            rows=clean_transactions(pd.read_csv(upload),account="CSV Import",raw_source=upload.name)
            st.success(f"Imported {save_transactions(rows)} new row(s). Duplicate rows are skipped.")
            st.rerun()
        except Exception as e: st.error(f"Import failed: {e}")

df=fetch_transactions()
if df.empty:
    st.info("No transactions yet. Add one in the sidebar, import a CSV, or run `python main.py` to load sample data.")
    st.stop()
d=prepare_frame(df)
months=sorted(d.month.unique())
month=st.selectbox("Select month",months,index=len(months)-1)
md=d[d.month==month]
k=calculate_kpis(md)
cols=st.columns(4)
for col,label,key in zip(cols,["Total spending","Income","Net savings","Average daily spending"],
                         ["total_spend","income","savings","average_daily_spend"]):
    col.metric(label,f"₹{k[key]:,.0f}")
st.caption(f"Highest spending category: **{k['highest_category']}**")
left,right=st.columns(2)
with left:
    st.subheader("Category-wise spending")
    cats=category_summary(md)
    st.bar_chart(cats.set_index("category").spend)
with right:
    st.subheader("Payment method")
    pay=payment_summary(md)
    if not pay.empty and pay.spend.sum()>0:
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots()
        ax.pie(pay.spend,labels=pay.payment_method,autopct="%1.1f%%",startangle=90)
        st.pyplot(fig); plt.close(fig)
    else: st.info("No payment-method expense data.")
st.subheader("Monthly spending trend")
st.line_chart(monthly_summary(d).set_index("month").spending)
st.subheader("Daily spending")
st.bar_chart(md.groupby(md.date.dt.date).spend.sum())
st.subheader("Budget planner")
with st.form("budget"):
    c1,c2=st.columns(2)
    category=c1.selectbox("Category",sorted(df.category.dropna().unique()))
    limit=c2.number_input("Monthly limit (INR)",min_value=0.0,step=100.0)
    save=st.form_submit_button("Save / update budget")
if save:
    set_budget(month,category,limit); st.success("Budget saved.")
budgets=check_budgets(df,month)
if budgets.empty: st.caption("No budgets set for this month yet.")
else:
    st.dataframe(budgets,use_container_width=True,hide_index=True)
    overs=budgets[budgets.status=="Over budget"]
    if not overs.empty: st.warning("Over budget: "+", ".join(overs.category.astype(str)))
st.subheader("Transactions")
st.dataframe(md.drop(columns=["month","spend","income"],errors="ignore"),use_container_width=True,hide_index=True)
if st.button("Generate monthly report"):
    result=export_month(df,month,ROOT/"reports")
    st.success("Monthly report generated in reports/.")
    for name,path in result.items(): st.write(f"{name.upper()}: `{path.relative_to(ROOT)}`")
