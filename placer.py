"""
placer.py

การปรับปรุงตาม SOLID:
- SRP  : แต่ละ Placer รับผิดชอบเฉพาะการหาตำแหน่งวาง
- OCP  : เพิ่ม strategy ใหม่ได้โดย subclass BasePlacer
- LSP  : RandomPlacer และ GridPlacer ทดแทนกันได้สมบูรณ์
- ISP  : interface มีเพียงเมธอดเดียวที่จำเป็น (place)
- DIP  : BuildingManager พึ่งพา BasePlacer (abstraction) ไม่ใช่ class จริง
"""

import random
from abc import ABC, abstractmethod

import pygame


class BasePlacer(ABC):
    """Strategy interface สำหรับการหาตำแหน่งวางสิ่งก่อสร้าง (ISP/DIP)"""

    @abstractmethod
    def place(
        self,
        surface: pygame.Surface,
        existing: list[dict],
    ) -> tuple[int, int]:
        """คืน (x, y) ที่ไม่ชนสิ่งก่อสร้างที่มีอยู่"""


class RandomPlacer(BasePlacer):
    """วางโดยสุ่มตำแหน่งในกรอบ แล้วตรวจ collision (SRP)"""

    def __init__(
        self,
        area: tuple[int, int, int, int] = (150, 150, 500, 350),
        max_attempts: int = 100,
    ):
        self.min_x, self.min_y, self.max_x, self.max_y = area
        self.max_attempts = max_attempts

    def place(self, surface: pygame.Surface, existing: list[dict]) -> tuple[int, int]:
        w, h = surface.get_size()
        for _ in range(self.max_attempts):
            x = random.randint(self.min_x, self.max_x - w)
            y = random.randint(self.min_y, self.max_y - h)
            if not self._collides(x, y, w, h, existing):
                return (x, y)
        # fallback: ตำแหน่งสุ่มสุดท้ายหากหาที่ว่างไม่ได้
        return (
            random.randint(self.min_x, self.max_x - w),
            random.randint(self.min_y, self.max_y - h),
        )

    @staticmethod
    def _collides(x: int, y: int, w: int, h: int, existing: list[dict]) -> bool:
        new_rect = pygame.Rect(x, y, w, h)
        return any(
            new_rect.colliderect(pygame.Rect(b["pos"], b["img"].get_size()))
            for b in existing
        )