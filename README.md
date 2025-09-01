# NFLDeepDive
NFL Stat Deepdiver is a Python/Tkinter desktop app for exploring season-level NFL passing data. It scrapes Pro-Football-Reference, caches results, cleans/merges rows, and computes z-scores to compare players relative to their peers. Columns are sortable, and the layout adapts to pre/post-QBR eras.

# Origin
Initially, this appplication was created to answer the question: "Who had the greatest passing season ever?"
However, context is rarely taken into consideration when asking this question, and we merely look at counting stats (yards thrown, touchdown to interception ratio, etc.)
This takes into account performances of players in that given year when scoring players. 
The football has changed to be more aerodynamic, the rules have changed regarding Quarterback protection and what constitutes pass interference, holding and many other factors that result in on-field production.
This application uses statistical analysis to isolate how good a player was at passing in the context of that year, allowing users to drill-down and see how much of an outlier that passing season was.


Was Dan Marino's 5000 yards and 48 TD's in '84 a more outstanding season than Peyton Manning's 5400 yards and 55 Touchdowns in 2013? Or maybe it was Aaron Rodger's incredibly efficent 2011 season with 122 Passer Rating? Tom Brady's 50 Touchdown to 8 Interception 2010? Maybe Patrick Mahomes??

None of them! 


## NFL Stat Deepdiver — Passing Stats Viewer

Interactive desktop app to explore NFL passing statistics by season. The app scrapes season passing tables from Pro-Football-Reference, caches results locally, and visualizes the top 40 passers with sortable columns and simple statistical context (Z-scores).

- Custom table UI with interactive sorting and dynamic columns based on season rules.
- **Data ingestion & caching**: Robust HTTP session, graceful Cloudflare handling, and on-disk HTML cache to avoid repeat requests.
- **Data wrangling**: Cleans HTML, filters low-attempt seasons, merges multi-team rows, and standardizes numeric fields.
- **Statistical insight**: Computes Z-scores for yards, TDs, and Rate/QBR by season to compare players relative to peers.

### Features
- **Season selector (1950–2023)** with one-click fetch.
- **Sortable columns** by clicking headers (toggles ascending/descending).
- **Top 40 passers** by yards for the selected season.
- **Dynamic columns**: Uses Rate before 2006; includes QBR for 2006 and later.
- **Local caching** to `cache/passing_<year>.html` to speed up re-runs.

### How it works (brief)
1. Builds the season URL at Pro-Football-Reference and fetches HTML.
2. Falls back to `cloudscraper` when standard requests face 403/Cloudflare (optional dependency).
3. Extracts and cleans the `passing` table, filters data, and consolidates multi-team rows.
4. Transforms inconsistant datatables and loads the data for statistical analysis
5. Computes Z-scores and shows the top 40 by yards in a sortable table.

### Getting started
#### Prerequisites
- Python 3.9+ (Tkinter is included with most standard Python installs)
- Internet connection for first-time fetches (subsequent runs may use cache)

#### Install dependencies
At minimum, the app needs `requests`. `cloudscraper` is optional but recommended to gracefully handle Cloudflare challenges.

```bash
pip install requests
pip install cloudscraper  # optional but recommended
```

#### Run the app
```bash
python passingstats.py
```

Then:
- Select a year
- Click "Fetch Stats"
- Click any column header to sort (click again to toggle direction)

### Troubleshooting
- **HTTP 403** when fetching: The app caches successful responses. If a fresh year fails:
  - Try again after a few seconds
  - Install `cloudscraper` and retry
  - Ensure your network/browser-like headers aren’t being blocked by a proxy/VPN
- **Empty or missing data**: If the source page structure changes, parsing may fail. Clear the `cache/` file for that year and retry after updating the scraper.

### Data source and attribution
Data is sourced from Pro-Football-Reference. Please review and respect their terms of use. All player stats and tables belong to their respective owners.


```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --name NflStatDeepdiver passingstats.py
```

The binary will be in the `dist/` directory.

####################################################################################################
This application complies with Sports-Reference's clauses concerning bot's and scrapers. Thank you for understanding. 

From: https://www.sports-reference.com/bot-traffic.html

Update: May 29, 2024

Sports Reference is primarily dependent on ad revenue, so we must ensure that actual people using web browsers have the best possible experience when using this site. Unfortunately, non-human traffic, ie bots, crawlers, scrapers, can overwhelm our servers with the number of requests they send us in a short amount of time. Therefore we are implementing rate limiting on the site. We will attempt to keep this page up to date with our current settings.

Currently we will block users sending requests to:

- FBref and Stathead sites more often than ten requests in a minute.
- our other sites more often than twenty requests in a minute.
- This is regardless of bot type and construction and pages accessed.
- If you violate this rule your session will be in jail for up to a day.

