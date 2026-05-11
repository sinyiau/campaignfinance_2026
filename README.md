# Campaign Finance 2026: Senate Fundraising Analysis

A data journalism project analysing individual campaign contributions to US Senate candidates in the 2025-2026 election cycle.

## 1. The Story
Democratic Senate candidates are outraising their Republican rivals in most states holding 2026 elections, including states they are unlikely to win, according to Cook ratings. 

In Texas, Democratic candidate James Talarico raised $40m in individual contributions against Republican Warren Paxton's $7m. The pattern repeats across Florida, Ohio, Georgia and North Carolina.

But fundraising advantage does not always translate into electoral advantage. This project maps the money, identifies where the gaps are the largest and sets them against the Cook Senate ratings to ask: does raising more money actually predict winning?

## 2. Visualizations
[Senate fundraising map for all states holding elections in 2026](https://public.flourish.studio/visualisation/28904950/): Share of individual donations going to Democrats and Republicans, by state. The deeper the colour, the greater the share of individual donations going to that party.

[Dumbbell chart for competitive races](https://public.flourish.studio/visualisation/28912758/): Individuals contributions to the leading Democrat and Republican candidate in eight competitive Senate races.

## 3. Project Sturcture
```
campaignfinance_2026/
│
├── README.md
│
├── 01_fetch_candidates.py
├── 02_fetch_financials.py
├── 03_merge_ratings.py
├── 04_analysis.py
├── 05_map_data.py
│
└── data/
    ├── raw/
    │   └── all_senate_candidates.csv
    └── processed/
        ├── all_senate_financials.csv
        ├── competitive_candidates.csv
        ├── final_analysis.csv
        ├── state_fundraising_map.csv
        └── dumbbell_chart.csv
```
## 4. Data Sources
| Dataset | Source | Access |
|---|---|---|
| Senate candidate list | OpenFEC API `/candidates/` |Free, API key [required](https://api.open.fec.gov/developers/) |
| Candidate financial totals | OpenFEC API `/candidate/{id}/totals/` | Free, API key [required](https://api.open.fec.gov/developers/)  |
| Race competitiveness ratings | Cook Political Report | Manually entered from [official website](https://www.cookpolitical.com/ratings/senate-race-ratings) |

## 5. Methodology
### Candidate selection
All Senate candidates registered with the FEC for the 2026 election cycle were retrieved via the OpenFEC API: 535 in total as of May 10. Of these, 286 had filed financial reports. The remaining had registered to run but had not yet disclosed any financial activity.

For the dumbbell chart, eight states were selected based on the Cook Political Report's competitive race ratings: Florida, Georgia, Iowa, Maine, Montana, North Carolina, Ohio and Texas. Within each state, the candidate with the highest individual contributions was selected to represent each party.

### Fundraising metric
`individual_contributions` was used as the primary fundraising metric rather than `receipts`. Total receipts include candidate self-loans, which distort cross-candidate comparisons: a candidate lending $50m to their own campaign is not the same signal as raising $50m from individual donors. Individual contributions better reflect genuine voter financial support.

### State-level map
For the map, individual contributions were summed by state and party across all candidates with financial filings. The metric displayed is `dem_share` — the Democratic share of total individual contributions:
```
dem_share = DEM / (DEM + REP)
```
A value of 0.5 represents an equal split. Values above 0.5 indicate Democrats raised more; below 0.5 indicates Republicans raised more. This framing avoids the directional bias of a raw gap (DEM minus REP) due to difference in population.

## 6. Limitations
- Fundraising totals will change substantially as the election approaches, particularly after the Q2 2026 filing deadline in July.
- The dumbbell chart shows only the highest-fundraising candidate per party per state. In states with crowded primaries, other candidates may have significant fundraising activity not reflected here.
- This analysis describes the money landscape. It does not model electoral outcomes. Cook Political Report ratings are included as context, not as a prediction.

## 7. Reproduce this Analysis
```bash
git clone https://github.com/sinyiau/campaignfinance_2026
cd campaignfinance_2026
pip install requests pandas

python 01_fetch_candidates.py       # Fetch all 532 Senate candidates from FEC API
python 02_fetch_financials.py       # Fetch financial totals for each candidate (~20 min)
python 03_merge_ratings.py          # Merge Cook ratings, filter competitive states
python 04_analysis.py               # Build race-level comparisons and dumbbell data
python 05_map_data.py               # Build state-level map data
```
Free FEC API keys available at https://api.open.fec.gov/developers/. Scripts run sequentially, each script builds on the output of the previous.

## Author
Sinyi Au  
Portfolio: https://sinyiau.github.io/2026Portfolio/  
GitHub: https://github.com/sinyiau  
Built May 2026. 