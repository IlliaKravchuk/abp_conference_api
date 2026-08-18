from datetime import datetime, timedelta, time

class PriceCalculator:
    """
    Калькулятор вартості оренди згідно з бізнес-правилами компанії.
    Не залежить від бази даних, легко покривається Unit-тестами.
    """
    
    @staticmethod
    def calculate_total_price(start_time: datetime, end_time: datetime, base_price: float, services_price: float = 0.0) -> float:
        if start_time >= end_time:
            raise ValueError("Час завершення має бути більшим за час початку")

        total_rent = 0.0
        
        # Тарифікаційні зони суточні
        zones = [
            (0, 6, 1.0),    # Ніч (базова)
            (6, 9, 0.9),    # Ранкові години (знижка 10%)
            (9, 12, 1.0),   # Стандартні години
            (12, 14, 1.15), # Пікові години (націнка 15%)
            (14, 18, 1.0),  # Стандартні години
            (18, 23, 0.8),  # Вечірні години (знижка 20%)
            (23, 24, 1.0)   # Пізня ніч
        ]
        
        current_start = start_time
        
        # Цикл по днях
        while current_start < end_time:
            next_day_start = datetime.combine(current_start.date() + timedelta(days=1), time.min)
            current_end = min(end_time, next_day_start)

            for start_h, end_h, multiplier in zones:
                zone_start = datetime.combine(current_start.date(), time.min) + timedelta(hours=start_h)
                zone_end = datetime.combine(current_start.date(), time.min) + timedelta(hours=end_h)
                
                overlap_start = max(current_start, zone_start)
                overlap_end = min(current_end, zone_end)
                
                if overlap_start < overlap_end:
                    duration_hours = (overlap_end - overlap_start).total_seconds() / 3600.0
                    total_rent += duration_hours * base_price * multiplier
                    
            current_start = current_end
            
        # фікса послуг
        return round(total_rent + services_price, 2)