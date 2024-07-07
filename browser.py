import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def parse_proxy_url(proxy_url):
    if proxy_url.startswith("http://"):
        # Remove the "http://" prefix
        remaining_url = proxy_url[len("http://"):]
        
        # Split the remaining part by ':' to separate the domain and port
        if ':' in remaining_url:
            proxy_domain, proxy_port = remaining_url.split(':', 1)
        else:
            raise ValueError("Invalid proxy URL format. Expected format: http://domain:port")
        
        return proxy_domain, proxy_port
    else:
        raise ValueError("Proxy URL must start with 'http://'")
    
def get_ip_info(proxy_url):
    browser_option = FirefoxOptions()
    browser_option.add_argument("--no-sandbox")
    browser_option.add_argument("--disable-dev-shm-usage")
    browser_option.add_argument("--ignore-certificate-errors")
    browser_option.add_argument("--disable-gpu")
    browser_option.add_argument("--log-level=3")
    browser_option.add_argument("--disable-notifications")
    browser_option.add_argument("--disable-popup-blocking")
    browser_option.add_argument("--headless")

    profile = FirefoxProfile();

    if proxy_url is not None:
        proxy_domain, proxy_port = parse_proxy_url(proxy_url)
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_domain)
        profile.set_preference("network.proxy.http_port", proxy_port)
        #browser_option._caps['proxy'] = {
        #    "proxyType": "MANUAL",
        #    "httpProxy": proxy_url,
            #"ftpProxy": proxy_url,
        #    "sslProxy": proxy_url
        #}

    driver = webdriver.Firefox(options=browser_option)
    driver.profile = profile

    try:
        driver.get('http://api.myip.com')
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
