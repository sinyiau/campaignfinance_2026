import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/processed/all_senate_financials.csv")
candidates = pd.read_csv("data/raw/all_senate_candidates.csv")

merged = df.merge(
    candidates[["candidate_id", "name", "state", "party"]],
    on="candidate_id",
    how="left"
)

competitive_states = ["TX", "NC", "ME", "OH", "GA", "FL", "IA", "MT"]
competitive = merged[
    (merged["state"].isin(competitive_states)) &
    (merged["party"].isin(["DEM", "REP"]))
].copy()

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

state_names = {
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland",
    "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri",
    "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina", "ND": "North Dakota",
    "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NV": "Nevada", "NY": "New York", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VA": "Virginia", "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin",
    "WV": "West Virginia", "WY": "Wyoming"
}

competitive["cook_rating"]    = competitive["state"].map(cook_ratings)
competitive["state_name"]     = competitive["state"].map(state_names)
competitive["party_name"]     = competitive["party"].map({"DEM": "Democrat", "REP": "Republican"})
competitive["candidate_name"] = competitive["name"].str.title()
competitive["candidate_name"] = competitive["candidate_name"].apply(
    lambda x: " ".join(reversed(x.split(", "))) if ", " in x else x
)
competitive["amount_millions"] = (competitive["individual_contributions"] / 1_000_000).round(1)

dumbbell = competitive[["state_name", "candidate_name", "party_name", "amount_millions", "cook_rating"]].copy()
dumbbell.columns = ["State", "Candidate", "Party", "Amount (millions)", "Cook Rating"]
dumbbell = dumbbell.sort_values("Amount (millions)", ascending=False)
dumbbell = dumbbell.groupby(["State", "Party"]).first().reset_index()
dumbbell = dumbbell.sort_values(["State", "Party"])

dumbbell.to_csv("data/processed/dumbbell_chart.csv", index=False)
print(dumbbell)