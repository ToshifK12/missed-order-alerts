# Missed Order Alerts

A small add-on idea for AI order-entry tools like [Asakana](https://www.ycombinator.com/companies/asakana) (YC F26).

Once orders are already being parsed from emails and texts, a distributor knows each restaurant's ordering rhythm. This project uses that rhythm to flag customers who **should have ordered by now but haven't**, so a sales rep can call them before the business goes to a competitor.

## How it works
1. `generate_orders.py` – creates 8 weeks of fake seafood order emails from 10 restaurants (a few go quiet).
2. `extract.py` – parses emails into structured orders.
3. `cadence.py` – learns each customer's usual order days and flags overdue ones.
4. `app.py` – Streamlit dashboard with the daily call list.

## Run
```bash
pip install -r requirements.txt
python generate_orders.py
python extract.py
python cadence.py        # quick terminal check
streamlit run app.py
```

## Ideas to extend
- Weight alerts by customer value (avg order size).
- Detect shrinking orders, not just missing ones.
- Send the call list to Slack/email each morning.
- Handle photo orders (vision model).
