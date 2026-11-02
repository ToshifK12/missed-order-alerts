"""Dashboard: streamlit run app.py"""
import pandas as pd
import streamlit as st

from cadence import analyze, load_orders

st.set_page_config(page_title="Missed Order Alerts", layout="wide")
st.title("Missed Order Alerts")
st.caption("Customers who usually would have ordered by now — call them before a competitor does.")

orders = load_orders()
results = analyze(orders)
overdue = [r for r in results if r["overdue"]]

c1, c2, c3 = st.columns(3)
c1.metric("Customers", len(results))
c2.metric("Overdue today", len(overdue))
c3.metric("Orders processed", len(orders))

st.subheader("Call list")
if overdue:
    st.dataframe(
        pd.DataFrame(overdue)[["customer", "usual_days", "last_order", "expected_by", "days_overdue"]],
        width='stretch', hide_index=True,
    )
else:
    st.success("Everyone's on schedule.")

st.subheader("All customers")
st.dataframe(pd.DataFrame(results), width='stretch', hide_index=True)

st.subheader("Order history")
customer = st.selectbox("Customer", [r["customer"] for r in results])
hist = [o for o in orders if o["customer"] == customer]
st.dataframe(
    pd.DataFrame([{"date": o["ordered_at"][:10], "items": ", ".join(
        f"{i['qty']} {i['unit']} {i['product']}" for i in o["items"])} for o in hist]),
    width='stretch', hide_index=True,
)
