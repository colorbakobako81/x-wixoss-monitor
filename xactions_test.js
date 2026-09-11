import {
  createBrowser,
  createPage,
  loginWithCookie,
  scrapeTweets
} from "xactions";

const username = "wixoss_TCG";
const cookie = process.env.X_AUTH_TOKEN;

if (!cookie) {
  throw new Error("X_AUTH_TOKEN が設定されていません");
}

const browser = await createBrowser({
  headless: true
});

const page = await createPage(browser);

try {
  console.log("Xに接続しています...");

  await loginWithCookie(page, cookie);

  console.log(`@${username} の投稿を取得しています...`);

  const tweets = await scrapeTweets(page, username, {
    limit: 10
  });

  console.log(`取得件数: ${tweets.length}`);

  for (const tweet of tweets) {
    console.log("-----");
    console.log("本文:", tweet.text);
    console.log("URL:", tweet.url);
    console.log("日時:", tweet.timestamp);
  }

} finally {
  await browser.close();
}
