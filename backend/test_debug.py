import os

os.environ["NULLBR_APP_ID"] = "Jy19cpz9p"
os.environ["NULLBR_API_KEY"] = "rIxTz7XHDEHBcP9lGpeVAgs0I7Evg6wc"
os.environ["NULLBR_BASE_URL"] = "https://api.nullbr.eu.org/"

import httpx

app_id = os.environ["NULLBR_APP_ID"]
api_key = os.environ["NULLBR_API_KEY"]
base_url = os.environ["NULLBR_BASE_URL"]

url = f"{base_url}user/info"

headers = {
    "X-APP-ID": app_id,
    "X-API-KEY": api_key,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://nullbr.eu.org/",
}

print(f"URL: {url}")

response = httpx.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
