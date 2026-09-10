import os
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

RSS_URL = "https://rss.app/feeds/M9nNnEwGtsshGgdQ.xml"
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

SEEN_FILE = Path("seen_posts.txt")

# RSSを取得
response = requests.get(RSS_URL, timeout=30)
response.raise_for_status()

root = ET.fromstring(response.content)

# RSSの記事を全部取得
items = root.findall(".//item")

if not items:
    print("記事が見つかりません")
    exit()

# 過去に通知した投稿を読み込む
if SEEN_FILE.exists():
    seen_posts = set(SEEN_FILE.read_text(encoding="utf-8").splitlines())
else:
    seen_posts = set()

# 新しい投稿だけ探す
new_items = []

for item in items:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    guid = item.findtext("guid", "")

    post_id = guid or link

    if post_id and post_id not in seen_posts:
        new_items.append((post_id, title, link))

# 新しい投稿がなければ終了
if not new_items:
    print("新しい投稿はありません")
    exit()

# 新しい投稿をDiscordへ送信
for post_id, title, link in reversed(new_items):

    message = f"**{title}**\n{link}"

    discord_response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": message},
        timeout=30
    )

    discord_response.raise_for_status()

    print(f"Discordへ送信しました: {title}")

    seen_posts.add(post_id)

# 通知済み投稿を保存
SEEN_FILE.write_text(
    "\n".join(seen_posts),
    encoding="utf-8"
)

print(f"{len(new_items)}件の新規投稿を通知しました")
