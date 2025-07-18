from datetime import datetime
import pytz
from tvgarden import tvgarden_scraper
from tvgarden import check_file
from config import supabase

# Local timestamp
def get_local_time():
    tz = pytz.timezone("Asia/Manila")
    return datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")

# Main loop function
def run_scraper(url_list):
    for url in url_list:
        if "tv.garden" in url:
            
            try:
                status, name = tvgarden_scraper(url)
            except Exception:
                status = "DOWN"
                name = "Unknown"
            print(url, status)
            supabase.table("tv.garden").insert({
                "status": status,
                "name": name,
                "timestamp": get_local_time(),
                "url": url
            }).execute()
        else:
            try:
                status = "UP" if check_file(url) else "DOWN"
            except Exception:
                status = "DOWN"
            print(url, status)
            supabase.table("tv.garden").insert({
                "status": status,
                "name": "nbc.com",
                "timestamp": get_local_time(),
                "url": url
            }).execute()



urls = [
    "https://tv.garden/us/hO3HYR4TgtSkMv",
    "https://tv.garden/pg/riGO8TQGoTIShZ",
    "https://stream-205444.castr.net/64ee8a084b935f9f8a6f8825/live_ab333a6093bc11eeb89fbd81423485b7/index.fmp4.m3u8"
]
run_scraper(urls)
print("Scraping completed.")
