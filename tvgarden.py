from playwright.sync_api import sync_playwright
from utils.youtube_checker import is_video_live
import requests
import time

def check_file(url):
    print("Checking file:", url)
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 and 'application' in response.headers.get('Content-Type', '')
    except:
        return False


def tvgarden_scraper(url: str, see_name: bool = False):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--start-maximized",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--log-level=3"
                ]
            )
            
            context = browser.new_context()
            page = context.new_page()
            
            print(f"📌{url}")
            name = None
            
            page.goto(url)
            
            # Wait for video-link elements to be present
            page.wait_for_selector(".video-link", timeout=20000)
            time.sleep(5)
            
            buttons = page.locator(".video-link").all()
            
            for button in buttons:
                video_url = button.get_attribute("data-video-url")
                channel = button.get_attribute("data-channel-name")
                color = button.evaluate("element => getComputedStyle(element).color")
                print(channel)
                if video_url and color != "rgba(241, 241, 241, 1)":

                    print(f"📺 Channel: {channel}")
                    print(f"🔗 Video URL: {video_url}")
                    print("---")
                    
                    if video_url.startswith("https://www.youtube-nocookie.com"):
                        status = is_video_live(video_url)
                    else:
                        status = "UP" if check_file(video_url) else "DOWN"
                    
                    print(status)
                    print("---")
                    return status, name
            
            print("❌DOWN")
            print("Error finding video source")
            return "DOWN", name
            
        except Exception as e:
            print("❌ Error:", e)
            return "ERROR", None
            
        finally:
            browser.close()