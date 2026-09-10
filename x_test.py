import requests

url = "https://rsshub.yfi.moe/twitter/user/wixoss_TCG"

response = requests.get(url, timeout=30)

print("Status:", response.status_code)
print(response.text[:5000])
