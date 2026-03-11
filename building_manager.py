import random
import pygame


class BuildingManager:
    """จัดการคอลเลกชันของสิ่งก่อสร้างและตำแหน่งในเมือง

    แยกออกจาก City เพื่อให้คลาส City มีขนาดเล็กลง
    (ช่วยสอดคล้องกับ Single Responsibility)
    """

    def __init__(self):
        self.items = []

    def add(self, name, surface, revenue):
        """เพิ่มสิ่งก่อสร้างด้วยการสุ่มตำแหน่งและหลีกเลี่ยงการชน"""
        w, h = surface.get_size()
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(150, 500 - w)
            y = random.randint(150, 350 - h)
            new_rect = pygame.Rect(x, y, w, h)
            collision = False
            for b in self.items:
                existing_rect = pygame.Rect(b["pos"], b["img"].get_size())
                if new_rect.colliderect(existing_rect):
                    collision = True
                    break
            if not collision:
                self.items.append({
                    "name": name,
                    "img": surface,
                    "pos": (x, y),
                    "revenue": revenue,
                })
                return
        # ถ้าไม่พบตำแหน่งที่ว่างภายในจำนวนครั้งที่กำหนด ให้วางแบบสุ่มสุดท้าย
        x = random.randint(150, 500 - w)
        y = random.randint(150, 350 - h)
        self.items.append({
            "name": name,
            "img": surface,
            "pos": (x, y),
            "revenue": revenue,
        })

    def revenue_per_second(self):
        return sum(b["revenue"] for b in self.items)

    def clear(self):
        self.items.clear()

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)
