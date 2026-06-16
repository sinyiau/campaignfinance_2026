import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/processed/all_senate_financials.csv")
candidates = pd.read_csv("data/raw/all_senate_candidates.csv")

merged = df.merge(
    candidates[["candidate_id", "name", "state", "party", "candidate_status"]],
    on="candidate_id",
    how="left"
)

merged = merged[merged["candidate_status"] == "C"]

state_totals = (
    merged[merged["party"].isin(["DEM", "REP"])]
    .groupby(["state", "party"])["individual_contributions"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)

state_totals["leader"]    = (state_totals["DEM"] > state_totals["REP"]).map({True: "DEM", False: "REP"})
state_totals["leader_name"] = state_totals["leader"].map({"DEM": "Democrat", "REP": "Republican"})
state_totals["gap_abs"]   = (state_totals["DEM"] - state_totals["REP"]).abs()
state_totals["gap_label"] = state_totals["gap_abs"].apply(lambda x: f"${x/1_000_000:.1f} million")
state_totals["dem_share"] = state_totals["DEM"] / (state_totals["DEM"] + state_totals["REP"])

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

state_totals["state_name"] = state_totals["state"].map(state_names)

all_states = list(state_names.keys())
existing_states = state_totals["state"].tolist()
missing_states = [s for s in all_states if s not in existing_states]

missing_df = pd.DataFrame({
    "state": missing_states,
    "DEM": 0,
    "REP": 0,
    "leader": "N/A",
    "leader_name": "N/A",
    "gap_abs": 0,
    "gap_label": "No Senate election in 2026",
    "dem_share": None,
})
missing_df["state_name"] = missing_df["state"].map(state_names)

state_totals = pd.concat([state_totals, missing_df], ignore_index=True)

state_totals.to_csv("data/processed/state_fundraising_map.csv", index=False)
print(state_totals.sort_values("dem_share", ascending=False))