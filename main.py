import time
from datetime import datetime
import pytz
from tvgarden import tvgarden_scraper
from config import supabase
import subprocess
import os

if not os.path.exists("/root/.cache/ms-playwright"):
    print("▶ Installing Playwright browsers...")
    subprocess.run(["playwright", "install"], check=True)


# Local timestamp
def get_local_time():
    tz = pytz.timezone("Asia/Manila")
    return datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")

# Main loop function
def run_scraper(url_list):
    for url in url_list:
        try:
            status, name = tvgarden_scraper(url)
        except Exception:
            status = "DOWN"
            name = "Unknown"

        supabase.table("tv.garden").insert({
            "status": status,
            "name": name,
            "timestamp": get_local_time(),
            "url": url
        }).execute()


urls = [
    "https://tv.garden/us/hO3HYR4TgtSkMv",
]
run_scraper(urls)
print("Scraping completed.")
