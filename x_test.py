import os
import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://rss.app/feeds/M9nNnEwGtsshGgdQ.xml"
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# RSSを取得
response = requests.get(RSS_URL, timeout=30)
response.raise_for_status()

root = ET.fromstring(response.content)

# RSSの最初の記事を取得
item = root.find(".//item")

if item is None:
    print("記事が見つかりません")
    exit()

title = item.findtext("title", "")
link = item.findtext("link", "")

message = f"**{title}**\n{link}"

# Discordへ送信
discord_response = requests.post(
    DISCORD_WEBHOOK_URL,
    json={"content": message},
    timeout=30
)

discord_response.raise_for_status()

print("Discordへ送信しました")
