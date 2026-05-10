import requests
import pandas as pd
import os

base_url = "https://api.open.fec.gov/v1"
api_key = "uibBFbeWnKxC1RJVbnnSTTf4TEd1DbhsxIcUobBc"
os.makedirs("data/raw", exist_ok=True)

def get_senate_candidates (cycle=2026):
    endpoint = f"{base_url}/candidates/"

    params = {
        "api_key": api_key,
        "office": "S",
        "election_year": cycle,
        "per_page": 100,
        "page": 1,
    }

    all_candidates = []

    while True:
        response = requests.get(endpoint, params=params)
        data = response.json()

        results = data["results"]
        all_candidates.extend(results)

        if params ["page"] >= data["pagination"]["pages"]:
            break
        params["page"] += 1
    return pd.DataFrame(all_candidates)

candidates = get_senate_candidates()
candidates.to_csv("data/raw/all_senate_candidates.csv", index=False)

print(f"Total candidates pulled: {len(candidates)}")
print("Saved to data/raw/all_senate_candidates.csv")