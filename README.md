# NFLDeepDive
NFL Stat Deepdiver is a Python/Tkinter desktop app for exploring season-level NFL passing data. It scrapes Pro-Football-Reference, caches results, cleans/merges rows, and computes z-scores to compare players relative to their peers. Columns are sortable, and the layout adapts to pre/post-QBR eras.


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

### Project structure
```
NflStatDeepdiver/
├─ cache/                   # HTML cache of fetched seasons
└─ passingstats.py          # Tkinter app: UI, fetch, parse, compute Z-scores
```

### Roadmap ideas
- Export filtered/sorted results to CSV
- Persist user preferences (last year, window size, sort column)
- Add rushing/receiving modules with shared components
- Package into a native executable (PyInstaller)

### Packaging (optional)
Create a standalone executable for sharing on Windows/macOS/Linux using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --name NflStatDeepdiver passingstats.py
```

The binary will be in the `dist/` directory.

### Screenshots
Add screenshots or a short GIF here to showcase the UI and sorting.


