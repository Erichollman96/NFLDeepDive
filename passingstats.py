import tkinter as tk
from tkinter import ttk, messagebox
import requests
import statistics
import os

class NFLPassingStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL Passing Stats Viewer")
        self.root.geometry("1400x600")
        self.root.configure(bg="#f5f5f5")
        
        # Initialize sort direction
        self.sort_reverse = False

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="NFL Passing Stats by Year", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#1d3557")
        title.pack(pady=20)

        form = tk.Frame(self.root, bg="#f5f5f5")
        form.pack(pady=10)

        tk.Label(form, text="Select Year:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.year_var = tk.StringVar()
        self.year_combo = ttk.Combobox(form, textvariable=self.year_var, font=("Arial", 12), width=10, state="readonly")
        self.year_combo["values"] = [str(y) for y in range(2023, 1949, -1)]
        self.year_combo.current(0)
        self.year_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        fetch_btn = tk.Button(form, text="Fetch Stats", font=("Arial", 12, "bold"), bg="#457b9d", fg="white", relief="flat", command=self.fetch_stats)
        fetch_btn.grid(row=0, column=2, padx=10, pady=5)

        # Table for stats
        self.table_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Initialize columns (will be updated based on year)
        self.columns = ("Player", "Team", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "INT", "Y/A", "Y/G", "Rate", "QBR", "Yds Z-Score", "TD Z-Score", "QBR Z-Score", "Total Z-Score")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=20)
        
        # Set column widths
        self.column_widths = {
            "Player": 150,
            "Team": 80,
            "G": 40,
            "GS": 40,
            "Cmp": 50,
            "Att": 50,
            "Cmp%": 60,
            "Yds": 70,
            "TD": 40,
            "INT": 40,
            "Y/A": 50,
            "Y/G": 60,
            "Rate": 60,
            "QBR": 60,
            "Yds Z-Score": 80,
            "TD Z-Score": 80,
            "QBR Z-Score": 80,
            "Total Z-Score": 80
        }
        
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, anchor="center", width=self.column_widths.get(col, 80))
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def update_columns_for_year(self, year):
        """Update table columns based on the selected year"""
        year_int = int(year)
        
        if year_int < 2006:
            # Remove QBR column for years before 2006
            self.columns = ("Player", "Team", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "INT", "Y/A", "Y/G", "Rate", "Yds Z-Score", "TD Z-Score", "Rate Z-Score", "Total Z-Score")
        else:
            # Keep QBR column for 2006 and later
            self.columns = ("Player", "Team", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "INT", "Y/A", "Y/G", "Rate", "QBR", "Yds Z-Score", "TD Z-Score", "QBR Z-Score", "Total Z-Score")
        
        # Remove old scrollbar if it exists
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, ttk.Scrollbar):
                widget.destroy()
        
        # Recreate treeview with new columns
        self.tree.destroy()
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=20)
        
        # Update column widths for new columns
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, anchor="center", width=self.column_widths.get(col, 80))
        self.tree.pack(fill="both", expand=True, side="left")
        
        # Reconfigure scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def sort_treeview(self, col):
        """Sort tree contents when a column header is clicked"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Handle numeric sorting for specific columns
        if col in ["G", "GS", "Cmp", "Att", "Yds", "TD", "INT", "Y/A", "Y/G", "Rate", "QBR", "Yds Z-Score", "TD Z-Score", "QBR Z-Score", "Rate Z-Score", "Total Z-Score"]:
            # Convert to float for numeric sorting, handle empty/invalid values
            def numeric_key(item):
                try:
                    # Remove commas from numbers like "4,000"
                    value = item[0].replace(',', '')
                    return float(value) if value.replace('.', '').replace('-', '').isdigit() else 0
                except (ValueError, AttributeError):
                    return 0
            
            l.sort(key=numeric_key, reverse=self.sort_reverse)
        else:
            # String sorting for text columns
            l.sort(reverse=self.sort_reverse)
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Reverse sort next time
        self.sort_reverse = not self.sort_reverse

    def fetch_stats(self):
        year = self.year_var.get()
        year_int = int(year)
        
        # Update columns based on year
        self.update_columns_for_year(year)
        
        self.tree.delete(*self.tree.get_children())
        self.root.config(cursor="watch")
        self.root.update_idletasks()
        try:
            # Build URL and cache path
            url = f"https://www.pro-football-reference.com/years/{year}/passing.htm"
            cache_dir = os.path.join(os.path.dirname(__file__), "cache")
            os.makedirs(cache_dir, exist_ok=True)
            cache_path = os.path.join(cache_dir, f"passing_{year}.html")

            html = None

            # 1) Use cached HTML if available (avoids repeated requests and 403s)
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        html = f.read()
                except Exception:
                    html = None

            if html is None:
                # 2) Try normal session first
                session = requests.Session()
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Referer": "https://www.pro-football-reference.com/",
                    "Upgrade-Insecure-Requests": "1",
                }
                try:
                    session.get("https://www.pro-football-reference.com/", headers=headers, timeout=15)
                except Exception:
                    pass

                resp = None
                last_err = None
                for _ in range(3):
                    try:
                        resp = session.get(url, headers=headers, timeout=20)
                        if resp.status_code == 200:
                            break
                        last_err = Exception(f"HTTP {resp.status_code}")
                    except Exception as ex:
                        last_err = ex

                if resp is not None and resp.status_code == 200:
                    html = resp.text
                else:
                    # 3) Fallback: try cloudscraper if available (handles Cloudflare)
                    try:
                        import cloudscraper  # type: ignore
                        scraper = cloudscraper.create_scraper(
                            browser={"browser": "chrome", "platform": "windows", "mobile": False}
                        )
                        resp2 = scraper.get(url, headers=headers, timeout=25)
                        if resp2.status_code != 200:
                            raise Exception(f"HTTP {resp2.status_code}")
                        html = resp2.text
                    except ImportError:
                        raise Exception(
                            "HTTP 403. Try once more or install 'cloudscraper' (pip install cloudscraper) "
                            "and then click Fetch again."
                        )

                # Save to cache on success
                if html:
                    try:
                        with open(cache_path, "w", encoding="utf-8") as f:
                            f.write(html)
                    except Exception:
                        pass

            # Extract the stats table from the HTML
            import re
            m = re.search(r'<table.+?id="passing".+?</table>', html, re.DOTALL)
            if not m:
                raise Exception("Could not find passing stats table for this year.")

            table_html = m.group(0)
            # Extract table rows
            rows = re.findall(r'<tr(.*?)</tr>', table_html, re.DOTALL)
            players = []
            player_names = set()  # Track players we've already seen
            
            for row in rows:
                # Skip header or separator rows
                if 'class="thead"' in row or 'class="over_header"' in row:
                    continue
                # Extract columns
                cols = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
                # Remove HTML tags from each col
                cols = [re.sub('<.*?>', '', c).replace('&nbsp;', ' ').strip() for c in cols]
                if len(cols) < 28 or not cols[0] or cols[0] == "Player":
                    continue
                # Only show players, not team totals
                if cols[0] and cols[1] and cols[0] != "Player":
                    player_name = cols[1]  # Player name
                    team = cols[3]  # Team
                    
                    # Skip records where player name is "Player" or empty
                    if player_name.lower() == "player" or not player_name.strip():
                        continue
                    
                    # After 1970, filter out players with less than 100 attempts
                    if year_int > 1970:
                        try:
                            attempts = int(cols[9]) if cols[9].replace('.', '').isdigit() else 0
                            if attempts < 100:
                                continue
                        except (ValueError, IndexError):
                            continue
                    
                    # If we've already seen this player, only keep "2TM" record
                    if player_name in player_names:
                        # Find existing record for this player
                        existing_index = None
                        for i, p in enumerate(players):
                            if p[0] == player_name:
                                existing_index = i
                                break
                        
                        if existing_index is not None:
                            existing_team = players[existing_index][1]
                            # If current record is "2TM", replace existing
                            if team == "2TM":
                                # Map specific columns from pro-football-reference to our table
                                if year_int < 2006:
                                    if year_int <= 1977:
                                        # For 1977 and earlier, Y/A, Y/G, and Rate are 2 columns to the left
                                        player_data = (
                                            cols[1],   # Player (col 2)
                                            cols[3],   # Team (col 4)
                                            cols[5],   # G (col 6)
                                            cols[6],   # GS (col 7)
                                            cols[8],   # Cmp (col 9)
                                            cols[9],   # Att (col 10)
                                            cols[10],  # Cmp% (col 11)
                                            cols[11],  # Yds (col 12)
                                            cols[12],  # TD (col 13)
                                            cols[14],  # INT (col 15)
                                            cols[17],  # Y/A (col 18) - 2 columns left
                                            cols[20],  # Y/G (col 21) - 2 columns left
                                            cols[21]   # Rate (col 22) - 2 columns left
                                        )
                                    else:
                                        player_data = (
                                            cols[1],   # Player (col 2)
                                            cols[3],   # Team (col 4)
                                            cols[5],   # G (col 6)
                                            cols[6],   # GS (col 7)
                                            cols[8],   # Cmp (col 9)
                                            cols[9],   # Att (col 10)
                                            cols[10],  # Cmp% (col 11)
                                            cols[11],  # Yds (col 12)
                                            cols[12],  # TD (col 13)
                                            cols[14],  # INT (col 15)
                                            cols[19],  # Y/A (col 20)
                                            cols[22],  # Y/G (col 23)
                                            cols[23]   # Rate (col 24)
                                        )
                                else:
                                    player_data = (
                                        cols[1],   # Player (col 2)
                                        cols[3],   # Team (col 4)
                                        cols[5],   # G (col 6)
                                        cols[6],   # GS (col 7)
                                        cols[8],   # Cmp (col 9)
                                        cols[9],   # Att (col 10)
                                        cols[10],  # Cmp% (col 11)
                                        cols[11],  # Yds (col 12)
                                        cols[12],  # TD (col 13)
                                        cols[14],  # INT (col 15)
                                        cols[19],  # Y/A (col 20)
                                        cols[22],  # Y/G (col 23)
                                        cols[23],  # Rate (col 24)
                                        cols[24]   # QBR (col 25)
                                    )
                                players[existing_index] = player_data
                            # If existing record is "2TM", keep existing
                            elif existing_team == "2TM":
                                continue
                            # If neither is "2TM", keep the first one (existing)
                            else:
                                continue
                    else:
                        # First time seeing this player, add to list
                        player_names.add(player_name)
                        # Map specific columns from pro-football-reference to our table
                        if year_int < 2006:
                            if year_int <= 1977:
                                # For 1977 and earlier, Y/A, Y/G, and Rate are 2 columns to the left
                                player_data = (
                                    cols[1],   # Player (col 2)
                                    cols[3],   # Team (col 4)
                                    cols[5],   # G (col 6)
                                    cols[6],   # GS (col 7)
                                    cols[8],   # Cmp (col 9)
                                    cols[9],   # Att (col 10)
                                    cols[10],  # Cmp% (col 11)
                                    cols[11],  # Yds (col 12)
                                    cols[12],  # TD (col 13)
                                    cols[14],  # INT (col 15)
                                    cols[17],  # Y/A (col 18) - 2 columns left
                                    cols[20],  # Y/G (col 21) - 2 columns left
                                    cols[21]   # Rate (col 22) - 2 columns left
                                )
                            else:
                                player_data = (
                                    cols[1],   # Player (col 2)
                                    cols[3],   # Team (col 4)
                                    cols[5],   # G (col 6)
                                    cols[6],   # GS (col 7)
                                    cols[8],   # Cmp (col 9)
                                    cols[9],   # Att (col 10)
                                    cols[10],  # Cmp% (col 11)
                                    cols[11],  # Yds (col 12)
                                    cols[12],  # TD (col 13)
                                    cols[14],  # INT (col 15)
                                    cols[19],  # Y/A (col 20)
                                    cols[22],  # Y/G (col 23)
                                    cols[23]   # Rate (col 24)
                                )
                        else:
                            player_data = (
                                cols[1],   # Player (col 2)
                                cols[3],   # Team (col 4)
                                cols[5],   # G (col 6)
                                cols[6],   # GS (col 7)
                                cols[8],   # Cmp (col 9)
                                cols[9],   # Att (col 10)
                                cols[10],  # Cmp% (col 11)
                                cols[11],  # Yds (col 12)
                                cols[12],  # TD (col 13)
                                cols[14],  # INT (col 15)
                                cols[19],  # Y/A (col 20)
                                cols[22],  # Y/G (col 23)
                                cols[23],  # Rate (col 24)
                                cols[24]   # QBR (col 25)
                            )
                        players.append(player_data)
            if not players:
                raise Exception("No player data found for this year.")

            # Calculate standard deviations
            yds_values = []
            td_values = []
            rate_values = []
            for player in players:
                try:
                    yds_val = float(player[7].replace(',', '')) if player[7].replace(',', '').replace('.', '').isdigit() else 0
                    td_val = float(player[8]) if player[8].replace('.', '').isdigit() else 0
                    rate_val = float(player[12]) if player[12].replace('.', '').isdigit() else 0
                    yds_values.append(yds_val)
                    td_values.append(td_val)
                    rate_values.append(rate_val)
                except (ValueError, IndexError):
                    yds_values.append(0)
                    td_values.append(0)
                    rate_values.append(0)
            
            yds_mean = statistics.mean(yds_values) if yds_values else 0
            td_mean = statistics.mean(td_values) if td_values else 0
            rate_mean = statistics.mean(rate_values) if rate_values else 0
            yds_stddev = statistics.stdev(yds_values) if len(yds_values) > 1 else 0
            td_stddev = statistics.stdev(td_values) if len(td_values) > 1 else 0
            rate_stddev = statistics.stdev(rate_values) if len(rate_values) > 1 else 0

            # Show top 40 by yards
            players = sorted(players, key=lambda x: int(x[7].replace(',', '') if x[7].replace(',', '').isdigit() else 0), reverse=True)[:40]
            
            for p in players:
                # Calculate Z-scores
                try:
                    yds_val = float(p[7].replace(',', '')) if p[7].replace(',', '').replace('.', '').isdigit() else 0
                    td_val = float(p[8]) if p[8].replace('.', '').isdigit() else 0
                    rate_val = float(p[12]) if p[12].replace('.', '').isdigit() else 0
                    
                    yds_zscore = (yds_val - yds_mean) / yds_stddev if yds_stddev > 0 else 0
                    td_zscore = (td_val - td_mean) / td_stddev if td_stddev > 0 else 0
                    rate_zscore = (rate_val - rate_mean) / rate_stddev if rate_stddev > 0 else 0
                    
                    # Calculate total Z-score
                    if year_int < 2006:
                        # For years before 2006, use Rate Z-score instead of QBR Z-score
                        total_zscore = yds_zscore + td_zscore + rate_zscore
                    else:
                        # For 2006 and later, use QBR Z-score
                        qbr_val = float(p[13]) if p[13].replace('.', '').isdigit() else 0
                        qbr_mean = statistics.mean([float(p[13]) if p[13].replace('.', '').isdigit() else 0 for p in players])
                        qbr_stddev = statistics.stdev([float(p[13]) if p[13].replace('.', '').isdigit() else 0 for p in players]) if len(players) > 1 else 0
                        qbr_zscore = (qbr_val - qbr_mean) / qbr_stddev if qbr_stddev > 0 else 0
                        total_zscore = yds_zscore + td_zscore + qbr_zscore
                    
                    # Format Z-scores to 2 decimal places
                    yds_zscore_str = f"{yds_zscore:.2f}"
                    td_zscore_str = f"{td_zscore:.2f}"
                    rate_zscore_str = f"{rate_zscore:.2f}"
                    total_zscore_str = f"{total_zscore:.2f}"
                except (ValueError, IndexError):
                    yds_zscore_str = "0.00"
                    td_zscore_str = "0.00"
                    rate_zscore_str = "0.00"
                    total_zscore_str = "0.00"
                
                # Add Z-scores to player data
                if year_int < 2006:
                    # For years before 2006, use Rate Z-score instead of QBR Z-score
                    player_with_zscore = p + (yds_zscore_str, td_zscore_str, rate_zscore_str, total_zscore_str)
                else:
                    # For 2006 and later, include QBR Z-score
                    try:
                        qbr_val = float(p[13]) if p[13].replace('.', '').isdigit() else 0
                        qbr_mean = statistics.mean([float(p[13]) if p[13].replace('.', '').isdigit() else 0 for p in players])
                        qbr_stddev = statistics.stdev([float(p[13]) if p[13].replace('.', '').isdigit() else 0 for p in players]) if len(players) > 1 else 0
                        qbr_zscore = (qbr_val - qbr_mean) / qbr_stddev if qbr_stddev > 0 else 0
                        qbr_zscore_str = f"{qbr_zscore:.2f}"
                    except (ValueError, IndexError):
                        qbr_zscore_str = "0.00"
                    player_with_zscore = p + (yds_zscore_str, td_zscore_str, qbr_zscore_str, total_zscore_str)
                
                self.tree.insert("", "end", values=player_with_zscore)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch stats: {str(e)}")
        finally:
            self.root.config(cursor="")

def main():
    root = tk.Tk()
    app = NFLPassingStatsApp(root)
    # Initialize sort direction
    app.sort_reverse = False
    root.mainloop()

if __name__ == "__main__":
    main()
