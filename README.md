# 🏫 Maktab - Telegram Boti

Ushbu bot maktab haqida to'liq ma'lumot berish, ish o'rinlariga ariza qabul qilish hamda 
maktabga qabul jarayonlarini avtomatlashtirish uchun mo'ljallangan zamonaviy Telegram botidir.

Bot **Aiogram 3.x** framework'ida to'liq asinxron (asynchronous) tarzda yozilgan bo'lib, 
ikki tilli (O'zbekcha va Ruscha) interfeysga ega.

## 🚀 Bot Imkoniyatlari

- 🌐 **Ikki tilli interfeys:** Foydalanuvchi tilini (UZ/RU) tanlashi va istalgan vaqtda o'zgartirishi mumkin.
- 🏢 **Maktab haqida ma'lumot:** Infratuzilma va maktab afzalliklari haqida batafsil ma'lumot.
- 📍 **Manzil va lokatsiya:** Maktabning aniq manzili va Telegram orqali interaktiv xarita (lokatsiya) yuborish.
- 💰 **Narxlar va chegirmalar:** O'quv to'lovlari va oilaviy chegirmalar haqida ma'lumot.
- 📞 **Biz bilan bog'lanish:** Foydalanuvchining ismi va telefon raqami (Telegram kontaktni yuborish orqali) qabul qilib, maxsus guruhga (adminlar guruhiga) xabar yuborish.
- 💼 **Ish bo'yicha ariza:** Vakansiyaga ariza topshirgan foydalanuvchidan ma'lumot olib, uning rezyumesi (fayl) ni guruhga yuborish (Fayl formatlari tekshiriladi: PDF, DOC, DOCX, JPG, PNG).
- 📝 **Maktabga qabul:** Inline tugmalar yordamida tuman va sinfni tanlash, shaxsiy ma'lumotlarni qabul qilish va arizani guruhga jo'natish (Arizaga Toshkent vaqtini avtomatik qo'shish).

## 🛠 Texnik Talablar (Stack)

- **Python:** 3.10+ (agar Python 3.8-3.9 bo'lsa, `backports.zoneinfo` o'rnatish kerak)
- **Aiogram:** 3.30.0
- **Asyncio:** Asinxron operatsiyalar uchun
- **Zoneinfo:** Toshkent vaqtini aniqlash uchun

## 📝 Eslatma

- Bot arizalarni yuborish uchun `GROUP_CHAT_ID` o'zgaruvchisida ko'rsatilgan guruhga yozish huquqiga ega bo'lishi kerak. 
- Guruhda botni admin qilib qo'yishingiz tavsiya etiladi.
- Vaqt mintaqasi sifatida `Asia/Tashkent` (Toshkent vaqti) qat'iy belgilangan.

---
Developed with ❤️ using Aiogram 3.

### Buni qanday ishlatish kerak?
1. Loyihangiz joylashgan papkada `README.md` degan fayl oching.
2. Yuqoridagi matnni nusxalab, shu faylga tashlang.
3. Git/GitHub'ga yuklasangiz, loyihangiz chiroyli ko'rinishda chiqadi. 
