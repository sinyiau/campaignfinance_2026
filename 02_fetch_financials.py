import requests
import pandas as pd
import os
import time

BASE_URL = "https://api.open.fec.gov/v1"
API_KEY  = "uibBFbeWnKxC1RJVbnnSTTf4TEd1DbhsxIcUobBc"

os.makedirs("data/processed", exist_ok=True)

def get_candidate_financials(candidate_id):
    endpoint = f"{BASE_URL}/candidate/{candidate_id}/totals/"
    params   = {"api_key": API_KEY, "cycle": 2026}

    response = requests.get(endpoint, params=params)
    data     = response.json()

    if not data["results"]:
        return None

    totals = data["results"][0]

    return {
        "candidate_id":             candidate_id,
        "receipts":                 totals.get("receipts", 0),
        "disbursements":            totals.get("disbursements", 0),
        "cash_on_hand":             totals.get("last_cash_on_hand_end_period", 0),
        "individual_contributions": totals.get("individual_contributions", 0),
        "pac_contributions":        totals.get("other_political_committee_contributions", 0),
    }

all_candidates = pd.read_csv("data/raw/all_senate_candidates.csv")
total          = len(all_candidates)
financials     = []

for i, cid in enumerate(all_candidates["candidate_id"]):
    result = get_candidate_financials(cid)
    if result:
        financials.append(result)

    if i % 10 == 0:
        print(f"{i}/{total} done...")

    time.sleep(0.2) 

financials_df = pd.DataFrame(financials)
financials_df.to_csv("data/processed/all_senate_financials.csv", index=False)

print(f"\nDone. {len(financials_df)} candidates with financial data.")
print("Saved to data/processed/all_senate_financials.csv")