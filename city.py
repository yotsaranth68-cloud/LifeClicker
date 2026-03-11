import random
import pygame

from building_manager import BuildingManager


class City:
    """จัดการข้อมูลเมือง: ระดับ, เงิน, สิ่งก่อสร้าง และการเกิดใหม่

    * Single Responsibility: คลาสนี้ดูแลสถานะของเมืองเท่านั้น
      (การจัดเก็บสิ่งก่อสร้างถูกโอนไปยัง BuildingManager)
    * Open/Closed: เพิ่มพฤติกรรมใหม่ ๆ ผ่านคลาสอื่น (เช่น
      behaviour หรือ modifiers) โดยไม่แก้ไขโค้ดเดิม
    """

    def __init__(self):
        self.reborn_count = 0
        self._level_goal = 100
        self.reset_city()

    def reset_city(self):
        self._level = 0
        self.funds = 1000.0
        self.auto_growth_rate = 0
        self.manager = BuildingManager()

    def get_revenue_per_second(self):
        # รวมรายได้จาก manager แล้วบวกค่าพื้นฐาน
        revenue = self.manager.revenue_per_second() + 5
        return revenue * (1 + self.reborn_count)

    # ฟังก์ชันการจัดการตำแหน่งและรายการสิ่งก่อสร้างโอนไป
    # ให้ BuildingManager ซึ่งลดขนาด City ลง

    def update(self, dt):
        self.funds += self.get_revenue_per_second() * dt
        self._level += self.auto_growth_rate * dt

    def purchase(self, building_type):
        """ลองซื้อสิ่งก่อสร้างโดยใช้กฎเดียวกับเดิม แต่ย้ายไว้ที่ City"""
        if self.funds >= building_type.cost and self.level >= building_type.level_req:
            self.funds -= building_type.cost
            self.manager.add(building_type.name, building_type.image, building_type.revenue_bonus)
            self.auto_growth_rate += 0.15
            building_type.cost = int(building_type.cost * 1.3)
            return True
        return False

    def reborn(self):
        if self._level >= self._level_goal:
            self.reborn_count += 1
            self._level_goal += 50
            self.reset_city()
            return True
        return False

    @property
    def buildings(self):
        # ให้ใช้งานเหมือนเดิม (iterable list) ผ่าน manager
        return self.manager.items

    @property
    def level(self):
        return int(self._level)
