import asyncio
from scrapping.main_page_scrapping import collect_urls
from scrapping.card_scrapping import process_cars

async def main():
    await collect_urls()     
    await process_cars() 

if __name__ == "__main__":
    asyncio.run(main())
