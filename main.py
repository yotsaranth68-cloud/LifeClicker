"""
main.py  — Game loop & UI

การปรับปรุงตาม SOLID:
- DIP  : main สร้าง dependencies (BuildingManager, Placer) แล้ว inject
         เข้า City แทนที่ City จะสร้างเอง (Composition Root)
- OCP  : เพิ่มสิ่งก่อสร้างใหม่ใน shop_items โดยไม่แก้ logic
- SRP  : แยก render functions ออกจาก game loop เพื่อความชัดเจน
- Encapsulation: ใช้ city.level_goal (property) แทน city._level_goal
"""

import sys
import pygame

from city import City
from building import BuildingType
from building_manager import BuildingManager
from placer import RandomPlacer


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCREEN_W, SCREEN_H = 800, 600
CITY_AREA = pygame.Rect(150, 150, 400, 300)  # พื้นที่คลิกพัฒนาเมือง
SHOP_X = 600
SHOP_ITEM_H = 110
BG_COLOR = (210, 230, 180)


# ---------------------------------------------------------------------------
# Render helpers (SRP: แต่ละฟังก์ชันรับผิดชอบ render ส่วนเดียว)
# ---------------------------------------------------------------------------

def render_hud(screen: pygame.Surface, font: pygame.font.Font, city: City) -> None:
    pygame.draw.rect(screen, (255, 255, 255), (15, 15, 250, 130), border_radius=10)
    screen.blit(font.render(f"Funds: ${int(city.funds)}", True, (30, 100, 30)), (30, 30))
    screen.blit(font.render(f"Income: ${city.get_revenue_per_second():.1f}/s", True, (50, 50, 50)), (30, 60))
    screen.blit(font.render(f"Level: {city.level} / {city.level_goal}", True, (0, 0, 120)), (30, 90))


def render_shop(
    screen: pygame.Surface,
    font: pygame.font.Font,
    city: City,
    shop_items: list[BuildingType],
) -> None:
    for i, item in enumerate(shop_items):
        is_locked = city.level < item.level_req
        rect = pygame.Rect(SHOP_X, 50 + i * SHOP_ITEM_H, 180, 90)
        pygame.draw.rect(screen, (200, 200, 200) if is_locked else (255, 255, 255), rect, border_radius=12)
        name_txt = "???" if is_locked else item.name
        screen.blit(font.render(name_txt, True, (0, 0, 0)), (SHOP_X + 15, 60 + i * SHOP_ITEM_H))
        screen.blit(font.render(f"Cost: ${item.cost}", True, (120, 100, 0)), (SHOP_X + 15, 90 + i * SHOP_ITEM_H))


def render_reborn_button(screen: pygame.Surface, font: pygame.font.Font) -> pygame.Rect:
    rect = pygame.Rect(300, 500, 200, 60)
    pygame.draw.rect(screen, (255, 200, 0), rect, border_radius=15)
    screen.blit(font.render("NEW ERA (REBORN)", True, (0, 0, 0)), (315, 518))
    return rect


def render_buildings(screen: pygame.Surface, city: City) -> None:
    for b in sorted(city.buildings, key=lambda x: x["pos"][1]):
        screen.blit(b["img"], b["pos"])


# ---------------------------------------------------------------------------
# Composition Root — สร้าง dependencies แล้ว inject (DIP)
# ---------------------------------------------------------------------------

def build_city() -> City:
    placer = RandomPlacer(area=(150, 150, 500, 350))
    manager = BuildingManager(placer=placer)
    return City(manager=manager)


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def run_game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("CityClicker: Farm & Industry")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Tahoma", 20)

    city = build_city()

    # OCP: เพิ่มสิ่งก่อสร้างใหม่ที่นี่โดยไม่แก้ logic อื่น
    shop_items: list[BuildingType] = [
        BuildingType.from_path("Wheat",       150,  0,  10, "assets/wheat(1).png"),
        BuildingType.from_path("Blacksmith",  800,  15, 45, "assets/blacksmith_green(1).png"),
        BuildingType.from_path("River",      2500,  40, 120, "assets/river(1).png"),
    ]

    # โหลด sound ใน run_game() ตอน init
    pygame.mixer.init()
    pygame.mixer.music.load("assets/bg_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # -1 = loop ไม่หยุด

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BG_COLOR)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # คลิกพื้นที่เมือง
                if CITY_AREA.collidepoint(pos):
                    city.click()  # ใช้ public method แทน city._level += 1

                # คลิกซื้อสิ่งก่อสร้าง
                for i, item in enumerate(shop_items):
                    if pygame.Rect(SHOP_X, 50 + i * SHOP_ITEM_H, 180, 90).collidepoint(pos):
                        city.purchase(item)

                # คลิก Reborn
                if city.can_reborn():
                    if pygame.Rect(300, 500, 200, 60).collidepoint(pos):
                        city.reborn()

        city.update(dt)

        # --- Render ---
        render_buildings(screen, city)
        render_hud(screen, font, city)

        instr = "กดตรงกลางเพื่ออัพเลเวลเมือง"
        screen.blit(font.render(instr, True, (0, 0, 0)), (260, 10))

        render_shop(screen, font, city, shop_items)

        if city.can_reborn():
            render_reborn_button(screen, font)

        pygame.display.flip()


if __name__ == "__main__":
    run_game()