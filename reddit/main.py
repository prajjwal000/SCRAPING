import asyncio
from playwright.async_api import async_playwright


async def scrapeSubreddit(url, numArticles = 100):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()

        try:
            await page.goto(url, timeout=0)
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            await browser.close()
            return None

        data = {"titles": [], "links": [], "post-type": []}

        while len(data['titles']) < numArticles:
            posts = await page.query_selector_all('shreddit-post')

            for po in posts:
                po_type = await po.get_attribute('post-type')
                title = await po.get_attribute('post-title')
                link = await po.get_attribute('permalink')
                data["post-type"].append(po_type if po_type else "NA")
                data["links"].append(link if link else "NA")
                data["titles"].append(title if title else "NA")

            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_timeout(4000)

        await browser.close()
        return data


async def main():
    url = "https://www.reddit.com/r/LordofTheMysteries/"

    data = await scrapeSubreddit(url, 1000)
    
    if data is not None:
        for idx in range(len(data['titles'])):
            print(f"{idx}Title: {data['titles'][idx]}")
            print(f"{idx}Link: {data['links'][idx]}")
            print(f"{idx}Post-type: {data['post-type'][idx]}")
            print('-'*40)
    unique_post_type = set(data['post-type'])
    print(unique_post_type)

asyncio.run(main())
