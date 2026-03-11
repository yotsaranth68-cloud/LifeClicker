import random
import pygame
from abc import ABC, abstractmethod


class BasePlacer(ABC):
    """อินเตอร์เฟซสำหรับระบบจัดวางสิ่งก่อสร้าง"""

    @abstractmethod
    def place(self, surface, existing):
        """รับ surface ของอาคารและรายการสิ่งก่อสร้างที่วางแล้ว
        คืนค่า (x, y) พิกัดที่ว่าง
        """
        pass


class RandomPlacer(BasePlacer):
    """วางโดยสุ่มตำแหน่งในกรอบกำหนดแล้วตรวจชน"""

    def __init__(self, area=(150, 150, 500, 350), max_attempts=100):
        # area = (min_x, min_y, max_x, max_y)
        self.min_x, self.min_y, self.max_x, self.max_y = area
        self.max_attempts = max_attempts

    def place(self, surface, existing):
        w, h = surface.get_size()
        for _ in range(self.max_attempts):
            x = random.randint(self.min_x, self.max_x - w)
            y = random.randint(self.min_y, self.max_y - h)
            new_rect = pygame.Rect(x, y, w, h)
            collision = False
            for b in existing:
                existing_rect = pygame.Rect(b["pos"], b["img"].get_size())
                if new_rect.colliderect(existing_rect):
                    collision = True
                    break
            if not collision:
                return (x, y)
        # ถ้าไม่พบ ตำแหน่งสุดท้าย
        x = random.randint(self.min_x, self.max_x - w)
        y = random.randint(self.min_y, self.max_y - h)
        return (x, y)
