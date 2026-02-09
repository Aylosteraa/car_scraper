import asyncio
import aiohttp
from repo import get_unprocessed_cars, update_car
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

BATCH_SIZE = 10

async def fetch_car_page(session, url: str) -> bytes | None:
    async with session.get(url) as response:
        if response.status != 200:
            return None
        return await response.read()


def parse_car_page(html: bytes) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    def text(selector):
        el = soup.select_one(selector)
        return el.text.strip() if el else None
    
    def parse_odometer(soup):
        for span in soup.select("#basicInfoTableMainInfo span.common-text.ws-pre-wrap.body"):
            text = span.text.strip().lower()
            if "тис" in text and "км" in text:
                num = re.findall(r"\d+", text)
                if num:
                    return int(num[0]) * 1000
        return None
    
    import re

    def parse_phone(soup):
        a = soup.select_one('a[href^="tel:"]')
        if not a:
            return None

        phone = a.get("href").replace("tel:", "")
        digits = re.sub(r"\D", "", phone)

        if digits.startswith("0"):
            digits = "38" + digits

        return digits

    title = text("h1")

    price_text = text("#basicInfoPrice strong")
    price_usd = None
    if price_text:
        price_usd = int(
            price_text
            .replace("$", "")
            .replace("\xa0", "") 
            .replace(" ", "")
        )

    odometer = parse_odometer(soup)

    username = text("#sellerInfoMainInfo span.titleM")

    image_el = soup.select_one("span.picture img")
    image_url = None

    if image_el:
        image_url = image_el.get("src") or image_el.get("data-src")

    badge = soup.select_one("span.common-badge.alpha.medium")
    images_count = None
    if badge:
        numbers = re.findall(r"\d+", badge.text)
        if numbers:
            images_count = int(numbers[-1])
    
    phone_number = parse_phone(soup)

    car_number = text("div.car-number.ua span")
    car_vin = text("#badgesVin span.common-text.ws-pre-wrap.badge")

    return {
        "title": title,
        "price_usd": price_usd,
        "odometer": odometer,
        "username": username,
        "image_url": image_url,
        "images_count": images_count,
        "phone_number": phone_number,
        "car_number": car_number,
        "car_vin": car_vin,
    }

async def process_cars():
    async with aiohttp.ClientSession() as session:
        while True:
            cars = await get_unprocessed_cars(limit=BATCH_SIZE)

            if not cars:
                print("Cars was not found")
                break

            for car in cars:
                html = await fetch_car_page(session, car.url)
                if not html:
                    print(f"Not loaded: {car.url}")
                    continue

                data = parse_car_page(html)

                await update_car(car.id, data)

            await asyncio.sleep(1) 


# async def fetch_phone_with_browser(url: str) -> int:
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()

#         await page.goto(
#             url,
#             wait_until="domcontentloaded",
#             timeout=60000
#         )

#         await page.wait_for_selector(
#             'button[data-action="showButtonPopUp"]',
#             state="visible",
#             timeout=30000
#         )

#         await page.click('button[data-action="showButtonPopUp"]')

#         await page.wait_for_selector(
#             'a[href^="tel:"]',
#             state="attached",
#             timeout=30000
#         )

#         href = await page.get_attribute('a[href^="tel:"]', "href")
#         await browser.close()

#     digits = re.sub(r"\D", "", href)
#     if digits.startswith("0"):
#         digits = "38" + digits

#     return int(digits)