# 🐍 Django HTML Konverter

**Django HTML Konverter** — bu oddiy HTML fayllarni **Django template** formatiga avtomatik o‘zgartiruvchi grafik interfeysli (GUI) dastur.  
U `{% static %}` va `{% url %}` teglarini avtomatik qo‘shib, **statik fayllar (CSS, JS, rasmlar)** va **ichki sahifalarga** havolalarni to‘g‘ri formatda almashtiradi.

---

## ⚙️ Asosiy funksiyalar

- 🔄 **Statik fayllarni avtomatik konvertatsiya qilish:**
  - `<link href="...css">` → `{% static '...' %}`
  - `<script src="...js">` → `{% static '...' %}`
  - `<img src="...png">` → `{% static '...' %}`

- 🔗 **Ichki sahifalarni `{% url %}` ga o‘zgartirish:**
  - `about.html` → `{% url 'about' %}`
  - `404.html` → `{% url 'error_404' %}`

- 🧩 **Avtomatik `{% load static %}` qo‘shish**
- 📁 **Rekursiv papka konvertatsiyasi** (barcha ichki papkalarni o‘z ichiga oladi)
- 📊 **Progress bar va log oynasi**
- ⚠️ **Xatoliklarni aniqlash va xabar berish**

---

## 🎨 Grafik interfeys

- Zamonaviy, foydalanuvchiga qulay dizayn
- Django rasmiy ranglariga asoslangan (qora-yashil)
- Katta “Konvertatsiya qilish” tugmasi
- Papkalarni tanlash va `Ctrl+V` orqali yo‘l qo‘yish
- O‘ng tugma menyusi: nusxalash, qo‘yish, tozalash

---

## 📋 Talablar

- Python 3.6 yoki undan yuqori
- Tkinter (standart kutubxona)

> Hech qanday tashqi kutubxona talab qilinmaydi!

---

## 🚀 Ishga tushirish

1. Dastur faylini saqlang:
   ```bash
   django_html_converter.py
   ```

2. Ishga tushiring:
   ```bash
   python django_html_converter.py
   ```

3. Papkalarni tanlang:
   - **Kirish papkasi** — HTML fayllar joylashgan joy
   - **Chiqish papkasi** — konvertatsiya qilingan fayllar saqlanadigan joy

4. “KONVERTATSIYA QILISH” tugmasini bosing

---

## ⚠️ Eslatmalar

- Kirish va chiqish papkalari bir xil bo‘lmasligi kerak
- `static/` papkasidagi fayllar `{% static %}` formatiga o‘zgaradi
- `../` yoki `/` boshlanuvchi yo‘llar tozalanadi
- `http://`, `https://`, `#` bilan boshlanuvchi URL’lar o‘zgartirilmaydi

---

## 📂 Namuna

**Kirish (`input/about.html`)**:
```html
<link rel="stylesheet" href="static/css/style.css">
<a href="contact.html">Aloqa</a>
<img src="/images/logo.png">
```

**Chiqish (`output/about.html`)**:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<a href="{% url 'contact' %}">Aloqa</a>
<img src="{% static 'images/logo.png' %}">
```

---

## 👨‍💻 Ishlab chiqaruvchi

- **Muallif**: Azamat Tojiyev  
- **Til**: Python + Tkinter

---

## 💡 Takliflar

Agar xatolik topsangiz yoki yangi funksiya qo‘shmoqchi bo‘lsangiz — **Issue** oching yoki **Pull Request** yuboring!

---

⭐ **Yoqdimi? Star bosishni unutmang!**
