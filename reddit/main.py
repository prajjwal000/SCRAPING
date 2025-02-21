import asyncio
import csv
from playwright.async_api import async_playwright


async def scrapeSubreddit(url, numArticles=100):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto(url, timeout=0)
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            await browser.close()
            return None

        data = {"post-title": [], "post-link": [], "post-type": [], "post-id": [],
                "comment-count": [], "score": [], "author": [], "content": []}

        while len(data['post-id']) < numArticles:
            posts = await page.query_selector_all('shreddit-post')

            for po in posts:
                post_type = await po.get_attribute('post-type')
                title = await po.get_attribute('post-title')
                link = await po.get_attribute('permalink')
                post_id = await po.get_attribute('id')
                comment_count = await po.get_attribute('comment-count')
                score = await po.get_attribute('score')
                author = await po.get_attribute('author')

                if post_type == "text":
                    content = await parseTextDescription(page, post_id)
                else:
                    content = await po.get_attribute("content-href")

                data["post-type"].append(post_type if post_type else "NA")
                data["post-link"].append(link if link else "NA")
                data["post-title"].append(title if title else "NA")
                data["author"].append(author if author else "NA")
                data["post-id"].append(post_id if post_id else "NA")
                data["score"].append(score if score else "NA")
                data["comment-count"].append(
                    comment_count if comment_count else "NA")
                # debug
                # if content != True:
                #     return
                data["content"].append(content if content else "NA")

            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_timeout(4000)

        await browser.close()
        return data


async def parseTextDescription(posts, post_id):
    content = await posts.query_selector(f'div#{post_id}-post-rtjson-content')
    if content:
        return await content.inner_text()
    return "NA"

async def save_to_csv(data, filename='scraped_data.csv'):
    fieldnames = data.keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(data['post-id'])):
            row = {key: data[key][i] for key in fieldnames}
            writer.writerow(row)

async def main():
    url = "https://www.reddit.com/r/LordofTheMysteries/"

    data = await scrapeSubreddit(url)
    if data is None:
        return
    
    await save_to_csv(data)

asyncio.run(main())
