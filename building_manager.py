"""
building_manager.py

การปรับปรุงตาม SOLID:
- SRP  : Manager เก็บและ query ข้อมูลเท่านั้น — ไม่หาตำแหน่งเอง
- DIP  : รับ BasePlacer ผ่าน constructor (Dependency Injection)
         เปลี่ยน placement strategy ได้โดยไม่แก้ Manager
- ISP  : เปิดเฉพาะ interface ที่จำเป็น (add, revenue_per_second, clear)
         ซ่อน items ภายใน — ผู้ใช้ iterate ผ่าน __iter__ เท่านั้น
"""

from __future__ import annotations

import pygame

from placer import BasePlacer, RandomPlacer


class BuildingManager:
    """เก็บรายการสิ่งก่อสร้างและ delegate การหาตำแหน่งให้ Placer (SRP/DIP)"""

    def __init__(self, placer: BasePlacer | None = None):
        # DIP: รับ abstraction; ถ้าไม่ส่งมาใช้ค่า default ที่สมเหตุสมผล
        self._placer: BasePlacer = placer or RandomPlacer()
        self._items: list[dict] = []

    def add(self, name: str, surface: pygame.Surface, revenue: int) -> None:
        """หาตำแหน่งผ่าน placer แล้วบันทึกสิ่งก่อสร้าง"""
        pos = self._placer.place(surface, self._items)
        self._items.append({
            "name": name,
            "img": surface,
            "pos": pos,
            "revenue": revenue,
        })

    def revenue_per_second(self) -> int:
        return sum(b["revenue"] for b in self._items)

    def clear(self) -> None:
        self._items.clear()

    # --- read-only interface (ISP: ไม่ expose list โดยตรง) ---

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)