from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Boolean
from datetime import datetime
from db import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)

    title = Column(String)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(Integer) 
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String)

    processed = Column(Boolean, default=False, nullable=False)
    datetime_found = Column(DateTime, default=datetime.utcnow)


    __table_args__ = (
        UniqueConstraint("url", name="uq_car_url"),
    )

    
