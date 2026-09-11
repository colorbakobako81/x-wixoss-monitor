import os
import requests
from pathlib import Path

USERNAME = "wixoss_TCG"
API_URL = f"https://api.fxtwitter.com/2/profile/{USERNAME}/statuses?count=20"

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
SEEN_FILE = Path("seen_posts.txt")


def get_posts():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    # FxTwitter APIのレスポンスから投稿一覧を取得
    posts = data.get("results", [])

    return posts


def get_post_id(post):
    return str(post.get("id", ""))


def get_post_url(post):
    return post.get(
        "url",
        f"https://x.com/{USERNAME}/status/{get_post_id(post)}"
    )


def main():
    posts = get_posts()

    if not posts:
        print("投稿が取得できませんでした")
        return

    print(f"取得件数: {len(posts)}")

    # seen_posts.txt がなければ初回実行
    if SEEN_FILE.exists():
        seen_posts = set(
            SEEN_FILE.read_text(encoding="utf-8").splitlines()
        )
    else:
        seen_posts = set()

    # 初回実行では現在の投稿を全部既読扱いにする
    if not seen_posts:
        for post in posts:
            post_id = get_post_id(post)
            if post_id:
                seen_posts.add(post_id)

        SEEN_FILE.write_text(
            "\n".join(seen_posts),
            encoding="utf-8"
        )

        print(f"初回実行：{len(seen_posts)}件を既読として登録しました")
        return

    new_posts = []

    for post in posts:
        post_id = get_post_id(post)

        if post_id and post_id not in seen_posts:
            new_posts.append(post)

    if not new_posts:
        print("新しい投稿はありません")
        return

    # 古い投稿 → 新しい投稿の順番で送信
    for post in reversed(new_posts):
        post_id = get_post_id(post)
        text = post.get("text", "")
        url = get_post_url(post)

        message = f"{text}\n{url}"

        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=30
        )

        response.raise_for_status()

        print(f"Discordへ送信しました: {text[:50]}")

        seen_posts.add(post_id)

    SEEN_FILE.write_text(
        "\n".join(seen_posts),
        encoding="utf-8"
    )

    print(f"{len(new_posts)}件の新規投稿を通知しました")


if __name__ == "__main__":
    main()
