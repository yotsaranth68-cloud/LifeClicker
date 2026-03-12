"""
city.py

การปรับปรุงตาม SOLID:
- SRP  : City จัดการเฉพาะ game-state (level, funds, reborn)
         ไม่ยุ่งกับ placement หรือ rendering
- OCP  : เพิ่ม modifier / behaviour ใหม่ได้ผ่าน composition
         โดยไม่แก้คลาสนี้
- DIP  : รับ BuildingManager ผ่าน constructor
         (ไม่ new เองภายใน — ลด coupling)
- Encapsulation: ซ่อน _level_goal ผ่าน property `level_goal`
         ทำให้ main.py ไม่ต้องเข้าถึง private attribute โดยตรง
"""

from __future__ import annotations

from building_manager import BuildingManager
from building import BuildingType
from placer import BasePlacer


class City:
    """Game-state ของเมือง: ระดับ, เงิน, สิ่งก่อสร้าง และการเกิดใหม่"""

    BASE_REVENUE = 5
    GROWTH_PER_PURCHASE = 0.15
    COST_SCALE = 1.3
    REBORN_LEVEL_INCREMENT = 50

    def __init__(self, manager: BuildingManager | None = None):
        # DIP: รับ BuildingManager จากภายนอก; ถ้าไม่ส่งมาสร้าง default
        self._make_manager = lambda: manager or BuildingManager()
        self.reborn_count = 0
        self._level_goal = 100
        self._reset()

    # ------------------------------------------------------------------
    # Public properties (encapsulation: ซ่อน private state)
    # ------------------------------------------------------------------

    @property
    def level(self) -> int:
        return int(self._level)

    @property
    def level_goal(self) -> int:
        """อ่านเป้าหมาย level ได้ แต่ตั้งค่าตรงไม่ได้ (read-only)"""
        return self._level_goal

    @property
    def buildings(self):
        """Iterable ของสิ่งก่อสร้างทั้งหมดในเมือง"""
        return self._manager

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def get_revenue_per_second(self) -> float:
        base = self._manager.revenue_per_second() + self.BASE_REVENUE
        return base * (1 + self.reborn_count)

    def update(self, dt: float) -> None:
        self.funds += self.get_revenue_per_second() * dt
        self._level += self.auto_growth_rate * dt

    def purchase(self, building_type: BuildingType) -> bool:
        """ซื้อสิ่งก่อสร้าง; คืน True ถ้าสำเร็จ"""
        if self.funds < building_type.cost or self.level < building_type.level_req:
            return False
        self.funds -= building_type.cost
        self._manager.add(
            building_type.name,
            building_type.image,
            building_type.revenue_bonus,
        )
        self.auto_growth_rate += self.GROWTH_PER_PURCHASE
        building_type.cost = int(building_type.cost * self.COST_SCALE)
        return True

    def click(self) -> None:
        """เพิ่ม level 1 จากการคลิก (แยกออกมาให้ main.py เรียกชัดเจน)"""
        self._level += 1

    def reborn(self) -> bool:
        """รีบอร์นถ้า level ถึงเป้า; คืน True ถ้าสำเร็จ"""
        if self._level < self._level_goal:
            return False
        self.reborn_count += 1
        self._level_goal += self.REBORN_LEVEL_INCREMENT
        self._reset()
        return True

    def can_reborn(self) -> bool:
        return self._level >= self._level_goal

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _reset(self) -> None:
        self._level: float = 0
        self.funds: float = 1000.0
        self.auto_growth_rate: float = 0
        self._manager = self._make_manager()