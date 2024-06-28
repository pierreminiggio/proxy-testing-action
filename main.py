import requests
import sys
import json

def get_ip_info(proxy_url, proxy_auth=None):
    try:
        # Check if the proxy URL is HTTP or HTTPS
        if proxy_url.startswith("http://"):
            proxies = {
                "http": proxy_url
            }
        elif proxy_url.startswith("https://"):
            proxies = {
                "https": proxy_url
            }
        else:
            raise ValueError("Invalid proxy URL. Must start with http:// or https://")

        # Set up proxy authentication if provided
        auth = None
        if proxy_auth:
            auth = requests.auth.HTTPProxyAuth(*proxy_auth.split(':', 1))

        # Make a request to the API using the proxy
        response = requests.get("https://api.myip.com", proxies=proxies, auth=auth)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse and display the JSON response
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.reason}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <proxy_url> [proxy_auth]")
        print("Example: python script.py http://your-proxy-url:port username:password")
        sys.exit(1)
    
    proxy_url = sys.argv[1]
    proxy_auth = sys.argv[2] if len(sys.argv) == 3 else None
    get_ip_info(proxy_url, proxy_auth)
