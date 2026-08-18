from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# Схемы Услуг 
class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)

class ServiceResponse(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

#  Схемы Залов 
class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., gt=0, description="Місткість залу")
    base_price: float = Field(..., gt=0, description="Базова вартість за годину")

class RoomCreate(RoomBase):
    service_ids: Optional[List[int]] = []

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    capacity: Optional[int] = Field(None, gt=0)
    base_price: Optional[float] = Field(None, gt=0)
    service_ids: Optional[List[int]] = None

class RoomResponse(RoomBase):
    id: int
    services: List[ServiceResponse] = []
    model_config = ConfigDict(from_attributes=True)

# Схемы Бронирований 
class BookingCreate(BaseModel):
    room_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime
    service_ids: Optional[List[int]] = []

class BookingResponse(BaseModel):
    id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    total_price: float
    selected_services: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)