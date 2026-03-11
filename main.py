import pygame
import sys

from city import City
from building import BuildingType


def run_game():
    # --- INITIALIZATION ---
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CityClicker: Farm & Industry")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Tahoma", 20)

    city = City()

    # ร้านค้า
    shop_items = [
        BuildingType("Wheat", 150, 0, 10, "assets/wheat(1).png"),
        BuildingType("Blacksmith", 800, 15, 45, "assets/blacksmith_green(1).png"),
        BuildingType("River", 2500, 40, 120, "assets/river(1).png"),
    ]

    # ลูปหลัก
    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill((210, 230, 180))  # พื้นหลังสีเขียวทุ่งหญ้า

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # คลิกพื้นที่เมืองเพื่อพัฒนา
                if 150 < event.pos[0] < 550 and 150 < event.pos[1] < 450:
                    city._level += 1

                # คลิกซื้อสิ่งก่อสร้างจากเมนู Shop
                for i, item in enumerate(shop_items):
                    rect = pygame.Rect(600, 50 + (i * 110), 180, 90)
                    if rect.collidepoint(event.pos):
                        city.purchase(item)

                # คลิก Reborn
                if city.level >= city._level_goal:
                    reborn_rect = pygame.Rect(300, 500, 200, 60)
                    if reborn_rect.collidepoint(event.pos):
                        city.reborn()

        city.update(dt)

        # --- RENDERING ---
        for b in sorted(city.buildings, key=lambda x: x["pos"][1]):
            screen.blit(b["img"], b["pos"])

        pygame.draw.rect(screen, (255, 255, 255), (15, 15, 250, 130), border_radius=10)
        screen.blit(font.render(f"Funds: ${int(city.funds)}", True, (30, 100, 30)), (30, 30))
        screen.blit(font.render(f"Income: ${city.get_revenue_per_second():.1f}/s", True, (50, 50, 50)), (30, 60))
        screen.blit(font.render(f"Level: {city.level} / {city._level_goal}", True, (0, 0, 120)), (30, 90))

        instr = "กดตรงกลางเพื่ออัพเวลเมือง"
        screen.blit(font.render(instr, True, (0, 0, 0)), (260, 10))

        for i, item in enumerate(shop_items):
            is_locked = city.level < item.level_req
            bg_color = (200, 200, 200) if is_locked else (255, 255, 255)
            rect = pygame.Rect(600, 50 + (i * 110), 180, 90)
            pygame.draw.rect(screen, bg_color, rect, border_radius=12)
            name_txt = item.name if not is_locked else "???"
            screen.blit(font.render(name_txt, True, (0, 0, 0)), (615, 60 + (i * 110)))
            screen.blit(font.render(f"Cost: ${item.cost}", True, (120, 100, 0)), (615, 90 + (i * 110)))

        if city.level >= city._level_goal:
            pygame.draw.rect(screen, (255, 200, 0), (300, 500, 200, 60), border_radius=15)
            screen.blit(font.render("NEW ERA (REBORN)", True, (0, 0, 0)), (315, 518))

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
