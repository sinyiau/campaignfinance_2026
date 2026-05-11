import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

candidates = pd.read_csv("data/raw/all_senate_candidates.csv")
financials = pd.read_csv("data/processed/all_senate_financials.csv")

merged = financials.merge(
    candidates[["candidate_id", "name", "state", "party"]],
    on="candidate_id",
    how="left"
)

cook_ratings = {
    "ME": "Toss-up",
    "NC": "Toss-up",
    "OH": "Lean D",
    "GA": "Likely D",
    "TX": "Lean D",
    "FL": "Likely R",
    "IA": "Lean R",
    "MT": "Likely R",
}

competitive = merged[
    (merged["state"].isin(cook_ratings.keys())) &
    (merged["party"].isin(["DEM", "REP"]))
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

print(top_candidates[["name", "state", "party", "individual_contributions", "cook_rating"]])
print(f"\nTotal candidates: {len(top_candidates)}")
print("Saved to data/processed/competitive_candidates.csv")