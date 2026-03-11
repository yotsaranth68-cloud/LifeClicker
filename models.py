from abc import ABC, abstractmethod

class LifeUpgrade(ABC):
    """Abstract Base Class แสดงหลักการ Abstraction"""
    def __init__(self, name, base_cost):
        self.name = name
        self.level = 0
        self.base_cost = base_cost

    @abstractmethod
    def apply_bonus(self, current_value):
        """Polymorphism: คลาสลูกแต่ละตัวจะคำนวณโบนัสต่างกัน"""
        pass

    def get_cost(self):
        """Encapsulation: คำนวณราคาภายในคลาสเอง"""
        return int(self.base_cost * (1.15 ** self.level))

class HealthUpgrade(LifeUpgrade):
    """Inheritance: การสืบทอดคุณสมบัติมาพัฒนาต่อ"""
    def apply_bonus(self, years_per_click):
        return years_per_click + (self.level * 0.1)