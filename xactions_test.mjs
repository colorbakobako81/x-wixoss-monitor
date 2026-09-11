import {
  createBrowser,
  createPage,
  scrapeTweets
} from "xactions";

const username = "wixoss_TCG";

const browser = await createBrowser({
  headless: true
});

try {
  const page = await createPage(browser);

  const tweets = await scrapeTweets(page, username, {
    limit: 5
  });

  console.log(`取得件数: ${tweets.length}`);

  for (const tweet of tweets) {
    console.log("-----");
    console.log("本文:", tweet.text);
    console.log("URL:", tweet.url);
    console.log("日時:", tweet.createdAt);
  }

} finally {
  await browser.close();
}
