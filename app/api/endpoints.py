from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.infrastructure.database import get_db
from app.infrastructure.repository import APIRepository
from app.services.booking_service import BookingService
from app.domain import schemas

router = APIRouter()

# ==========================
# ЗАЛИ (ROOMS)
# ==========================

@router.post("/rooms/", response_model=schemas.RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_in: schemas.RoomCreate, db: Session = Depends(get_db)):
    """Метод 1: Додавання конференц-залу"""
    repo = APIRepository(db)
    return repo.create_room(room_in)

@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, room_in: schemas.RoomUpdate, db: Session = Depends(get_db)):
    """Метод 2: Редагування інформації про зал"""
    repo = APIRepository(db)
    room = repo.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Зал не знайдено")
    
    # Оновлення полів
    if room_in.name: room.name = room_in.name
    if room_in.capacity: room.capacity = room_in.capacity
    if room_in.base_price: room.base_price = room_in.base_price
    
    if room_in.service_ids is not None:
        services = repo.get_services_by_ids(room_in.service_ids)
        room.services = services

    db.commit()
    db.refresh(room)
    return room

@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Метод 3: Видалення конференц-залу"""
    repo = APIRepository(db)
    room = repo.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Зал не знайдено")
    
    repo.delete_room(room)
    return None

@router.get("/rooms/available", response_model=List[schemas.RoomResponse])
def get_available_rooms(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    capacity: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """Метод 4: Пошук доступних залів"""
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Час початку має бути раніше часу завершення")
    
    repo = APIRepository(db)
    return repo.get_available_rooms(start_time, end_time, capacity)

# ==========================
# БРОНЮВАННЯ (BOOKINGS)
# ==========================

@router.post("/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Метод 5: Бронювання залу з розрахунком вартості"""
    service = BookingService(db)
    return service.create_booking(booking_in)
@router.get("/analytics/bookings")
def get_analytics(db: Session = Depends(get_db)):
    """Звіт та аналітика: загальна кількість бронювань та виручка для бізнесу"""
    repo = APIRepository(db)
    return repo.get_booking_analytics()