from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.repository import APIRepository
from app.domain.calculator import PriceCalculator
from app.domain.schemas import BookingCreate
from app.domain.models import Booking

class BookingService:
    def __init__(self, db: Session):
        self.repository = APIRepository(db)

    def create_booking(self, booking_data: BookingCreate) -> Booking:
        # Перевірка
        room = self.repository.get_room_by_id(booking_data.room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Зал не знайдено"
            )

        # 2. Перевірка доступності
        available_rooms = self.repository.get_available_rooms(
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            min_capacity=1  # Перевіряємо лише нАЯВНОСТІ
        )
        
        if not any(r.id == room.id for r in available_rooms):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Зал вже заброньовано на цей час"
            )

        # 3. Обробка додаткових послуг
        services_price = 0.0
        services_names = []
        if booking_data.service_ids:
            services = self.repository.get_services_by_ids(booking_data.service_ids)
            if len(services) != len(booking_data.service_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Одну або кілька послуг не знайдено"
                )
            
            services_price = sum(service.price for service in services)
            services_names = [service.name for service in services]

        # 4. Виклик домен калькуль
        total_price = PriceCalculator.calculate_total_price(
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            base_price=room.base_price,
            services_price=services_price
        )

        # 5. Збереження пеймента
        services_used_str = ", ".join(services_names) if services_names else None
        
        return self.repository.create_booking(
            room_id=room.id,
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            total_price=total_price,
            services_used=services_used_str
        )