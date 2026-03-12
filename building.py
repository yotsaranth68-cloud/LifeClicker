"""
building.py

การปรับปรุงตาม SOLID:
- SRP  : BuildingType เก็บเฉพาะ data; ImageLoader จัดการโหลดรูปแยกต่างหาก
- OCP  : เพิ่ม BuildingType ใหม่ได้โดยไม่แก้ไขคลาสนี้
- DIP  : BuildingType รับ surface สำเร็จรูปแทนที่จะโหลดเอง
         (high-level module ไม่พึ่งพา pygame.image โดยตรง)
"""

import os
import pygame


class ImageLoader:
    """รับผิดชอบโหลดและ scale รูปภาพจาก path เพียงอย่างเดียว (SRP)"""

    ASSET_DIR = "assets"
    DEFAULT_SIZE = (80, 80)
    FALLBACK_COLOR = (200, 200, 200)
    FALLBACK_SIZE = (64, 64)

    @classmethod
    def load(cls, img_path: str, size: tuple = DEFAULT_SIZE) -> pygame.Surface:
        """โหลด surface จาก path; ถ้าล้มเหลวคืน fallback surface"""
        full_path = (
            img_path
            if any(sep in img_path for sep in (os.sep, "/", "\\"))
            else os.path.join(cls.ASSET_DIR, img_path)
        )
        try:
            raw = pygame.image.load(full_path).convert_alpha()
            return pygame.transform.scale(raw, size)
        except Exception as exc:
            print(f"[Warning] cannot load image '{full_path}': {exc}")
            surf = pygame.Surface(cls.FALLBACK_SIZE)
            surf.fill(cls.FALLBACK_COLOR)
            return surf


class BuildingType:
    """ข้อมูลของประเภทสิ่งก่อสร้าง — เก็บเฉพาะ stats และ surface (SRP)

    รับ surface สำเร็จรูปผ่าน constructor แทนการโหลดเอง
    ทำให้ง่ายต่อการทดสอบและเปลี่ยน loader ในอนาคต (DIP)
    """

    def __init__(
        self,
        name: str,
        cost: int,
        level_req: int,
        revenue_bonus: int,
        image: pygame.Surface,
    ):
        self.name = name
        self.cost = cost
        self.level_req = level_req
        self.revenue_bonus = revenue_bonus
        self.image = image

    # --- factory method (OCP: เพิ่ม constructor ทางเลือกโดยไม่แก้ __init__) ---
    @classmethod
    def from_path(
        cls,
        name: str,
        cost: int,
        level_req: int,
        revenue_bonus: int,
        img_path: str,
    ) -> "BuildingType":
        """สร้าง BuildingType พร้อมโหลดรูปจาก path อัตโนมัติ"""
        surface = ImageLoader.load(img_path)
        return cls(name, cost, level_req, revenue_bonus, surface)