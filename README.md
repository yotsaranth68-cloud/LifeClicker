🏙️ TownClicker: Urban Evolution
Final Project for Object-Oriented Programming (OOP) Course
Ubon Ratchathani University

📖 Project Overview
TownClicker เป็นเกมแนว Clicker/Tycoon ที่จำลองการบริหารจัดการและพัฒนาเมืองจากยุคเกษตรกรรมไปสู่ยุคอุตสาหกรรม ผู้เล่นจะต้องคลิกเพื่อสะสมความเจริญ (City Level) และบริหารเงินงบประมาณเพื่อซื้อสิ่งก่อสร้างต่างๆ ซึ่งจะช่วยเพิ่มรายได้แบบ Passive Income และปลดล็อกยุคสมัยใหม่ (New Era/Reborn)

🛠 Frameworks & Architecture
Language: Python 3.12

Library: Pygame

Architecture: Object-Oriented Programming (OOP)

🧱 Applied OOP Principles
Encapsulation: คลาส City ทำหน้าที่ปกป้องข้อมูลระดับความเจริญและงบประมาณ โดยจัดการผ่าน Method ภายในเท่านั้น

Inheritance & Abstraction: การใช้คลาสพื้นฐานสำหรับสิ่งก่อสร้าง (BuildingType) เพื่อกำหนดคุณสมบัติร่วมของ Wheat, Blacksmith และ River

Polymorphism: ระบบการวาดภาพ (Rendering) และการคำนวณรายได้ที่จัดการผ่านรายการสิ่งก่อสร้างในรูปแบบลิสต์ โดยใช้อินเทอร์เฟซเดียวกัน

🛡️ SOLID Principles Implementation
Single Responsibility (S): แยก Logic การคำนวณเงิน, การจัดการ Sprite และการแสดงผลออกจากกันชัดเจน

Open/Closed (O): ระบบรองรับการเพิ่มสิ่งก่อสร้างใหม่ๆ (เช่น ปราสาท, โรงไฟฟ้า) ได้เพียงแค่เพิ่ม Instance ใน shop_items โดยไม่ต้องแก้ไข Logic การซื้อขายหลัก

👥 Team Members
นายยศสรัล ถิระบุตร - Programmer / Software Architect / Quality Assurance

🚀 Installation & Usage
Clone Repository:
git clone https://github.com/yotsaranth68-cloud/LifeClicker.git
cd TownClicker
pip install -r requirements.txt
python main.py

🎨 Asset Credits
Art Style: Isometric 2.5D Sprite
Source: Artyom Zagorskiy
License: CC0 1.0 Universal (Public Domain)