# เพิ่มเติมใน main.py
import pygame
from entities import Character
from ui import ClickButton
from upgrades import GymMember, TimeMachine # นำเข้าคลาสอัปเกรด

# ... (setup pygame เหมือนเดิม)

player = Character()
# สร้าง List สำหรับเก็บไอเทมอัปเกรด
upgrades = [
    GymMember("Gym Membership", base_cost=10, multiplier=0.5),
    TimeMachine("Time Machine", base_cost=50, multiplier=1.0)
]

# สร้างปุ่มสำหรับอัปเกรด (วางไว้ด้านข้าง)
upgrade_buttons = []
for i, upg in enumerate(upgrades):
    btn = ClickButton(550, 100 + (i * 100), 220, 60, f"Buy {upg.name}", (100, 100, 100))
    upgrade_buttons.append(btn)

# ตัวแปรควบคุมเวลา
last_update_time = pygame.time.get_ticks()

while True:
    current_time = pygame.time.get_ticks()
    
    # --- 1. Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # คลิกปุ่มหลัก
            if click_btn.is_clicked(event.pos):
                player.grow()
            
            # คลิกปุ่มอัปเกรด
            for i, btn in enumerate(upgrade_buttons):
                if btn.is_clicked(event.pos):
                    cost = upgrades[i].get_cost()
                    # สมมติว่าเรามีระบบเงิน หรือใช้ "อายุ" แลก (ในที่นี้ลองใช้คลิกสะสมแลก)
                    upgrades[i].apply_effect(player)
                    print(f"Bought {upgrades[i].name}! Level: {upgrades[i].level}")

    # --- 2. Logic (Auto-Growth) ---
    # เพิ่มอายุอัตโนมัติทุกๆ 1 วินาที (1000 ms)
    if current_time - last_update_time >= 1000:
        if player.auto_growth_rate > 0:
            player.grow(player.auto_growth_rate)
        last_update_time = current_time

    # --- 3. Rendering ---
    # (วาดตัวละครและ Text เหมือนเดิม)
    # เพิ่มการวาดปุ่มอัปเกรด
    for btn in upgrade_buttons:
        btn.draw(screen)
    
    # แสดงค่าสถิติปัจจุบัน
    stat_text = font.render(f"Speed: {player.years_per_click}y/click | Auto: {player.auto_growth_rate}y/s", True, (100, 100, 100))
    screen.blit(stat_text, (20, 550))