import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def get_ip_info(proxy_url):
    # Firefox options setup
    browser_option = FirefoxOptions()
    browser_option.add_argument("--no-sandbox")
    browser_option.add_argument("--disable-dev-shm-usage")
    browser_option.add_argument("--ignore-certificate-errors")
    browser_option.add_argument("--disable-gpu")
    browser_option.add_argument("--log-level=3")
    browser_option.add_argument("--disable-notifications")
    browser_option.add_argument("--disable-popup-blocking")
    browser_option.add_argument("--headless")

    # Add proxy settings for both HTTP and HTTPS if 'proxy' is specified
    if proxy_url is not None:
        browser_option.add_argument(f"--proxy-pac-url=PROXY {proxy_url}")
        # browser_option.add_argument("--proxy-server=%s" % proxy_url)

    # Launch Firefox browser with the configured options
    driver = webdriver.Firefox(options=browser_option)

    try:
        driver.get('https://api.myip.com')
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        print(body_text)

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) not in [2]:
        print("Usage: python browser.py <proxy_url>")
        print("Example: python browser.py http://your-proxy-url:port")
        sys.exit(1)
    
    proxy_url = sys.argv[1]
    get_ip_info(proxy_url)
