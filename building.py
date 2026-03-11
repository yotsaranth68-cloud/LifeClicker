import pygame


class BuildingType:
    """ข้อมูลของประเภทสิ่งก่อสร้าง

    - Single Responsibility: เก็บเฉพาะคุณสมบัติ (ต้นทุน, รูป, โบนัส)
      การซื้อถูกโยกไว้ใน `City.purchase()` แทน
    - Open/Closed: สามารถสร้าง subclass หรือ decorator เพิ่มกำไร
      โดยไม่แตะรหัสหลัก
    """

    def __init__(self, name, cost, level_req, revenue_bonus, img_path):
        self.name = name
        self.cost = cost
        self.level_req = level_req
        self.revenue_bonus = revenue_bonus
        # โหลดรูปภาพของสิ่งก่อสร้าง
        full_path = img_path
        if not any(sep in img_path for sep in ("/", "\\")):
            full_path = pygame.compat.path.join("assets", img_path)
        try:
            raw_img = pygame.image.load(full_path).convert_alpha()
            self.image = pygame.transform.scale(raw_img, (80, 80))
        except Exception as e:
            print(f"[Warning] cannot load image '{full_path}': {e}")
            self.image = pygame.Surface((64, 64))
            self.image.fill((200, 200, 200))

