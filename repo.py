from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
from db import AsyncSessionLocal
from models import Car
from datetime import datetime

async def save_urls(urls: list[str]):
    if not urls:
        return

    async with AsyncSessionLocal() as session:
        stmt = insert(Car).values(
            [{"url": url} for url in urls]
        ).on_conflict_do_nothing(
            index_elements=["url"]
        )

        await session.execute(stmt)
        await session.commit()


async def update_car(car_id: int, data: dict):
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Car)
            .where(Car.id == car_id)
            .values(
                **data,
                processed=True,
                datetime_found=datetime.utcnow()
            )
        )
        await session.execute(stmt)
        await session.commit()


async def get_unprocessed_cars(limit: int = 20):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Car)
            .where(Car.processed == False)
            .limit(limit)
        )
        return result.scalars().all()







