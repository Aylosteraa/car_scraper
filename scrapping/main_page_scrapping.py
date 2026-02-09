import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List
from repo import save_urls


BASE_URL = "https://auto.ria.com/uk/car/used/?page="

CONCURRENT_REQUESTS = 5      
BATCH_SIZE = 50              
START_PAGE = 1
LAST_PAGE = 10   #stub for testing            
REQUEST_DELAY = 1           

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}

sem = asyncio.Semaphore(CONCURRENT_REQUESTS)


def parse_card_urls_from_html(html: bytes) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.m-link-ticket")

    urls = []
    for a in links:
        href = a.get("href")
        if href:
            if href.startswith("/"):
                href = "https://auto.ria.com" + href
            urls.append(href)

    return urls


async def fetch_page(session: aiohttp.ClientSession, page: int) -> List[str]:
    url = BASE_URL + str(page)

    async with sem:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"[WARN] Page {page} returned {response.status}")
                    return []

                raw_html = await response.read()
                return parse_card_urls_from_html(raw_html)

        except asyncio.TimeoutError:
            print(f"[TIMEOUT] Page {page}")
            return []

        except aiohttp.ClientError as e:
            print(f"[ERROR] Page {page}: {e}")
            return []


async def collect_urls():
    timeout = aiohttp.ClientTimeout(total=20)

    processed_pages = 0

    async with aiohttp.ClientSession(
        headers=HEADERS,
        timeout=timeout
    ) as session:

        for batch_start in range(START_PAGE, LAST_PAGE + 1, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, LAST_PAGE + 1)

            print(f"\nPages {batch_start} – {batch_end - 1}")

            tasks = [
                fetch_page(session, page)
                for page in range(batch_start, batch_end)
            ]

            results = await asyncio.gather(*tasks)

            for urls in results:
                await save_urls(urls)

            processed_pages += (batch_end - batch_start)

            print(
                f"Processed pages: {processed_pages} | "
            )

            await asyncio.sleep(REQUEST_DELAY)

    print(f"Total pages processed: {processed_pages}")
