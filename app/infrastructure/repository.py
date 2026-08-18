from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.domain.models import Room, Booking, Service
from app.domain.schemas import RoomCreate, RoomUpdate
from datetime import datetime
from typing import List

class APIRepository:
    def __init__(self, db: Session):
        self.db = db

    # ==========================
    # ЗАЛИ (ROOMS)
    # ==========================
    def create_room(self, room_data: RoomCreate) -> Room:
        db_room = Room(name=room_data.name, capacity=room_data.capacity, base_price=room_data.base_price)
        if room_data.service_ids:
            services = self.db.query(Service).filter(Service.id.in_(room_data.service_ids)).all()
            db_room.services = services

        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get_room_by_id(self, room_id: int) -> Room:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def delete_room(self, db_room: Room):
        self.db.delete(db_room)
        self.db.commit()

    def get_available_rooms(self, start_time: datetime, end_time: datetime, min_capacity: int) -> List[Room]:
        """
        Метд 4 - Пошук доступних залів.
        """
        # 1. Знаходимо ID залів, які зайнять в цей проміжок часу 
        busy_room_ids = self.db.query(Booking.room_id).filter(
            or_(
                and_(Booking.start_time <= start_time, Booking.end_time > start_time),
                and_(Booking.start_time < end_time, Booking.end_time >= end_time),
                and_(Booking.start_time >= start_time, Booking.end_time <= end_time)
            )
        ).subquery()

        # 2. Вибираємо зали, які вільні та підходяьть по місцям  
        available_rooms = self.db.query(Room).filter(
            Room.capacity >= min_capacity,
            ~Room.id.in_(busy_room_ids)
        ).all()

        return available_rooms

    # ==========================
    # БРОНЮВАННЯ ТА ПОСЛУГИ
    # ==========================
    def get_services_by_ids(self, service_ids: List[int]) -> List[Service]:
        return self.db.query(Service).filter(Service.id.in_(service_ids)).all()

    def create_booking(self, room_id: int, start_time: datetime, end_time: datetime, total_price: float, services_used: str) -> Booking:
        db_booking = Booking(
            room_id=room_id,
            start_time=start_time,
            end_time=end_time,
            total_price=total_price,
            selected_services=services_used
        )
        self.db.add(db_booking)
        self.db.commit()
        self.db.refresh(db_booking)
        return db_booking
def get_booking_analytics(self) -> dict:
    bookings = self.db.query(Booking).all()
    total_bookings = len(bookings)
    total_revenue = sum(b.total_price for b in bookings)
    
    return {
        "total_bookings": total_bookings,
        "total_revenue": round(total_revenue, 2)
    }