from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def tvgarden_scraper(url: str, see_name: bool = False) -> tuple[str, str | None]:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    try:
        driver = webdriver.Chrome(options=options)
        print(f"📌{url}")
        name = None
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "video-link"))
        )
        time.sleep(5)
        buttons = driver.find_elements(By.CLASS_NAME, "video-link")

        for button in buttons:
            video_url = button.get_attribute("data-video-url")
            channel = button.get_attribute("data-channel-name")
            color = button.value_of_css_property("color")

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
        driver.quit()
