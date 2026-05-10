import pandas as pd

df = pd.read_csv("data/processed/competitive_candidates.csv")

dem = df[df["party"] == "DEM"][["state", "name", "individual_contributions", "cook_rating"]].rename(columns={
    "name": "dem_name",
    "individual_contributions": "dem_individual"
})

rep = df[df["party"] == "REP"][["state", "name", "individual_contributions"]].rename(columns={
    "name": "rep_name",
    "individual_contributions": "rep_individual"
})

races = dem.merge(rep, on="state")

races["gap"] = races["dem_individual"] - races["rep_individual"]

races["fundraising_leader"] = races["gap"].apply(
    lambda x: "DEM" if x > 0 else "REP"
)

races["gap_abs"] = races["gap"].abs()

races.to_csv("data/processed/final_analysis.csv", index=False)
print("Saved to data/processed/final_analysis.csv")