import pygame
import sys
from entities import Character
from ui import ClickButton

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("LifeClicker: OOP Edition")
clock = pygame.time.Clock()

# Setup Objects
player = Character()
click_btn = ClickButton(300, 450, 200, 80, "LIVE 1 YEAR", (70, 130, 180))

while True:
    screen.fill((240, 240, 240)) # พื้นหลังสีเทาอ่อน
    
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_btn.is_clicked(event.pos):
                player.grow()

    # 2. Update & Logic
    stage = player.get_stage_info()

    # 3. Draw
    # วาดตัวละคร (ใช้สี่เหลี่ยมแทน Sprite ไปก่อน)
    pygame.draw.rect(screen, stage["color"], (350, 200, 100, 150), border_radius=15)
    
    # แสดงข้อมูล
    font = pygame.font.SysFont("Arial", 40, bold=True)
    age_text = font.render(f"Age: {player.age} Years", True, (50, 50, 50))
    stage_text = font.render(f"Stage: {stage['name']}", True, stage["color"])
    
    screen.blit(age_text, (20, 20))
    screen.blit(stage_text, (20, 70))
    click_btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)