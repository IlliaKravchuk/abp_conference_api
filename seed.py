from app.infrastructure.database import SessionLocal
from app.domain.models import Room, Service

def seed_data():
    db = SessionLocal()
    
    # Перевіряємо, чи база вже не заповнена
    if db.query(Room).first():
        print("База даних вже містить інформацію. Пропускаємо.")
        db.close()
        return

    print("Заповнюємо базу початковими даними...")
    
    # +++ ПОСЛУГА
    services = [
        Service(name="Проектор", price=500),
        Service(name="Wi-Fi", price=300),
        Service(name="Звук", price=700)
    ]
    db.add_all(services)
    db.commit()

    # +++ зал
    rooms = [
        Room(name="Зал А", capacity=50, base_price=2000),
        Room(name="Зал В", capacity=100, base_price=3500),
        Room(name="Зал С", capacity=30, base_price=1500)
    ]
    db.add_all(rooms)
    db.commit()
    
    print(" ✅ Початкові дані успішно додано!")
    db.close()

if __name__ == "__main__":
    seed_data()