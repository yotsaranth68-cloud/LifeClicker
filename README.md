# 🏙️ TownClicker: Urban Evolution

**โปรเจกต์สุดท้ายสำหรับวิชา OOP** — มหาวิทยาลัยอุบลราชธานี

---

## 📖 บทนำโครงการ

_TownClicker_ เป็นเกมแนวคลิกเกอร์/ไทคูน ที่ให้ผู้เล่นบริหารเมือง
ตั้งแต่ยุคเกษตรกรรมไปสู่ยุคอุตสาหกรรม ทุกครั้งที่คลิกจะเพิ่ม
**ระดับเมือง** และเงินที่สะสมสามารถนำไปซื้อสิ่งก่อสร้างเพื่อสร้าง
รายได้แบบพาสซีฟ เมื่อถึงเป้าระดับ ผู้เล่นสามารถ "รีบอร์น" เพื่อเข้าสู่
ยุคใหม่พร้อมโบนัสรายได้ที่สูงขึ้น

โค้ดเน้นการออกแบบเชิงวัตถุอย่างสะอาดตามหลัก SOLID และง่ายต่อการ
ขยายในอนาคต

---

## 🛠️ เทคโนโลยีและสถาปัตยกรรม

- **ภาษา**: Python 3.12
- **ไลบรารี**: [Pygame](https://www.pygame.org/)
- **สถาปัตยกรรม**: โมดูลาร์ OOP

### โครงสร้างโฟลเดอร์

```
TownClicker/
├── assets/             # สไปรต์ไอโซเมตริก (.png)
├── city.py             # Model หลักควบคุมสถานะและ Logic การเงิน
├── building.py         # BuildingType + ImageLoader (โหลดรูปแยกต่างหาก)
├── building_manager.py # จัดการรายการสิ่งก่อสร้างในเมือง
├── placer.py           # Strategy สำหรับการคำนวณตำแหน่งวางสิ่งก่อสร้าง
├── main.py             # Composition Root, Game Loop & UI
├── README.md           # เอกสารอธิบายโครงการ
└── requirements.txt    # รายการ Library ที่จำเป็น
```

---

## 🧱 การออกแบบเชิงวัตถุ

### OOP Principles

| หลักการ | การนำไปใช้ |
|---|---|
| **Encapsulation** | `City` ปกป้อง `_level` และ `_level_goal` ผ่าน Property แบบ read-only ภายนอกไม่สามารถแก้ไขโดยตรงได้ |
| **Abstraction** | `BasePlacer` กำหนด interface การหาตำแหน่ง — ผู้ใช้รู้แค่ว่าเรียก `place()` ได้ โดยไม่รู้ว่าข้างในทำงานอย่างไร |
| **Inheritance** | `RandomPlacer` สืบทอดจาก `BasePlacer` และสามารถเพิ่ม Strategy ใหม่ (เช่น `GridPlacer`) ได้โดยไม่แก้โค้ดเดิม |
| **Polymorphism** | `BuildingManager` รับ `BasePlacer` ใดก็ได้ — วน loop สิ่งก่อสร้างทุกตัวผ่าน interface เดียวกัน |

### SOLID Principles

| หลักการ | การนำไปใช้ |
|---|---|
| **S** — Single Responsibility | `ImageLoader` โหลดรูป, `BuildingType` เก็บ stats, `Placer` หาตำแหน่ง, `Manager` เก็บข้อมูล, `City` คุม game state แต่ละคลาสมีหน้าที่เดียว |
| **O** — Open/Closed | เพิ่มสิ่งก่อสร้างใหม่ได้เพียงเพิ่ม `BuildingType.from_path(...)` ใน `shop_items` โดยไม่แก้ไข logic ใดเลย |
| **L** — Liskov Substitution | `RandomPlacer` ทดแทน `BasePlacer` ได้สมบูรณ์ และ Strategy ใหม่ใดก็ตามที่ subclass `BasePlacer` จะทำงานได้ทันที |
| **I** — Interface Segregation | `BasePlacer` มีเพียงเมธอดเดียวที่จำเป็น (`place`) และ `BuildingManager` ซ่อน `_items` — เปิดเฉพาะ `add`, `revenue_per_second`, `__iter__` |
| **D** — Dependency Inversion | `City` รับ `BuildingManager` ผ่าน constructor, `BuildingManager` รับ `BasePlacer` ผ่าน constructor — `main.py` ทำหน้าที่ Composition Root สร้างทุก dependency แล้ว inject เข้าหากัน |

---

## ➕ การเพิ่มสิ่งก่อสร้างใหม่

ด้วยการออกแบบตาม OCP เพิ่มสิ่งก่อสร้างได้โดย **ไม่แก้ไขไฟล์ใดเลย** นอกจาก `main.py`:

```python
# main.py — เพิ่มแค่บรรทัดเดียวใน shop_items
shop_items: list[BuildingType] = [
    BuildingType.from_path("Wheat",      150,  0,  10, "assets/wheat(1).png"),
    BuildingType.from_path("Blacksmith", 800,  15, 45, "assets/blacksmith_green(1).png"),
    BuildingType.from_path("River",     2500,  40, 120, "assets/river(1).png"),
]
```

ระบบที่รองรับอัตโนมัติโดยไม่ต้องแก้ไข:
- `BuildingManager.add()` รับ building ใดก็ได้
- `RandomPlacer` หาตำแหน่งให้ทุกตัวเหมือนกัน
- `City.purchase()` ตรวจ cost/level_req จาก object ที่ส่งมา
- `render_shop()` วน loop `shop_items` แสดงผลเองอัตโนมัติ

---

## 🚀 การติดตั้งและใช้งาน

```bash
git clone https://github.com/yotsaranth68-cloud/LifeClicker.git
cd TownClicker
pip install -r requirements.txt
python main.py          # เปิดเกม
```

หน้าต่างเกมจะปรากฏขึ้น คลิกพื้นที่กลางเพื่อเพิ่มระดับเมือง
และใช้เมนูขวาเพื่อซื้อสิ่งก่อสร้าง

---

## 🎨 สื่อ/สไปรต์

ภาพสไปรต์เป็นงานอาร์ตไอโซเมตริก 2.5D โดย Artyom Zagorskiy
(สัญญาอนุญาต CC0 1.0 สาธารณสมบัติ) เก็บไว้ในโฟลเดอร์ `assets/`

---

## 👥 ผู้พัฒนา

ยศศรัล ถิระบุตร — นักเขียนโปรแกรม / สถาปนิกซอฟต์แวร์

---

*สามารถ Fork, ขยาย หรือศึกษาโค้ดเพื่อการเรียนรู้ได้ตามสะดวก*