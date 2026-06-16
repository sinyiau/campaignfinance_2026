import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

candidates = pd.read_csv("data/raw/all_senate_candidates.csv")
financials = pd.read_csv("data/processed/all_senate_financials.csv")

merged = financials.merge(
    candidates[["candidate_id", "name", "state", "party", "candidate_status"]],
    on="candidate_id",
    how="left"
)

cook_ratings = {
    "ME": "Toss-up",
    "NC": "Toss-up",
    "OH": "Lean Democrat",
    "GA": "Likely Democrat",
    "TX": "Lean Democrat",
    "FL": "Likely Republican",
    "IA": "Lean Republican",
    "MT": "Likely Republican",
}

competitive_states = list(cook_ratings.keys())

competitive = merged[
    (merged["state"].isin(competitive_states)) &
    (merged["party"].isin(["DEM", "REP"])) &
    (merged["candidate_status"] == "C")
].copy()

competitive["cook_rating"] = competitive["state"].map(cook_ratings)

top_candidates = (
    competitive
    .sort_values("individual_contributions", ascending=False)
    .groupby(["state", "party"])
    .first()
    .reset_index()
)

top_candidates.to_csv("data/processed/competitive_candidates.csv", index=False)

print(top_candidates[["name", "state", "party", "individual_contributions", "cook_rating", "candidate_status"]])
print(f"\nTotal candidates: {len(top_candidates)}")