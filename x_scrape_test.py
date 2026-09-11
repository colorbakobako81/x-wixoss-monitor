import requests

USERNAME = "wixoss_TCG"

url = f"https://x.com/{USERNAME}"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

print("Status:", response.status_code)
print("URL:", response.url)
print("取得文字数:", len(response.text))

print(response.text[:1000])
