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

console.log("ブラウザを起動しています...");

const browser = await createBrowser({
  headless: true
});

const page = await createPage(browser);

try {
  console.log("Xにログインしています...");
  await loginWithCookie(page, cookie);

  console.log(`@${username} を取得しています...`);

  const tweets = await scrapeTweets(page, username, {
    limit: 5
  });

  console.log(`取得件数: ${tweets.length}`);

  for (const tweet of tweets) {
    console.log("-----");
    console.log("日時:", tweet.timeParsed);
    console.log("本文:", tweet.text);
    console.log("URL:", tweet.permanentUrl);
  }

} finally {
  await browser.close();
}
