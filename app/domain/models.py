from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

room_services = Table(
    'room_services',
    Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id', ondelete="CASCADE"), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id', ondelete="CASCADE"), primary_key=True)
)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    base_price = Column(Float, nullable=False)

    services = relationship("Service", secondary=room_services, back_populates="rooms")
    bookings = relationship("Booking", back_populates="room", cascade="all, delete")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)

    rooms = relationship("Room", secondary=room_services, back_populates="services")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    
    selected_services = Column(String, nullable=True) 

    room = relationship("Room", back_populates="bookings")