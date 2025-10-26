```
# Django HTML Konverter 🐍

**Django HTML Konverter** — bu oddiy HTML fayllarni Django template formatiga avtomatik ravishda o‘zgartiruvchi grafik interfeysli (GUI) dastur.  
U `{% static %}` va `{% url %}` teglarini qo‘shib, statik fayllar (CSS, JS, rasmlar) va ichki sahifalar (`<a href="...">`) uchun mos keladigan havolalarni almashtiradi.

---

## ⚙️ Funktsiyalar

- **Statik fayllarni avtomatik konvertatsiya qilish**:
  - `<link href="...css">` → `{% static '...' %}`
  - `<script src="...js">` → `{% static '...' %}`
  - `<img src="...png">` → `{% static '...' %}`
  - Boshqa statik fayllar (PDF, ZIP va h.k.)

- **Ichki sahifalarga havolalarni `{% url %}` ga o‘zgartirish**:
  - `about.html` → `{% url 'about' %}`
  - `404.html` → `{% url 'error_404' %}` (raqamli fayllar uchun `error_` prefiksi)

- **Avtomatik `{% load static %}` qo‘shish** (agar yo‘q bo‘lsa)

- **Rekursiv papka konvertatsiyasi** — barcha ichki papkalarni qamrab oladi

- **Progress bar va jurnal (log)** — har bir fayl holatini ko‘rish

- **Xatoliklarni aniqlash va xabar berish**

---

## 🎨 Grafik interfeys

- Zamonaviy, foydalanuvchiga qulay dizayn
- Django rasmiy ranglari (qora-yashil)
- Katta konvertatsiya tugmasi
- Kirish/chiqish papkalarini tanlash
- O‘ng tugma menyusi (nusxalash, qo‘yish, tozalash)
- `Ctrl+V` bilan papka yo‘lini qo‘yish imkoniyati

---

## 📋 Talablar

```txt
Python 3.6+
tkinter (standart kutubxona)
```

> Hech qanday tashqi kutubxona talab qilinmaydi!

---

## 🚀 Ishga tushirish

1. **Faylni saqlang**:
   ```bash
   django_html_converter.py
   ```

2. **Ishga tushiring**:
   ```bash
   python django_html_converter.py
   ```

3. **Papkalarni tanlang**:
   - **Kirish papkasi** — HTML fayllar joylashgan joy
   - **Chiqish papkasi** — konvertatsiya qilingan fayllar saqlanadigan joy

4. **"KONVERTATSIYA QILISH"** tugmasini bosing

---

## ⚠️ Eslatmalar

- **Kirish va chiqish papkalari bir xil bo‘lmasligi kerak!**
- `static/` papkasi ichidagi fayllar avtomatik `{% static %}` ga o‘zgartiriladi
- `../` yoki `/` boshidagi yo‘llar tozalanadi
- Tashqi URL’lar (`http://`, `https://`, `#`) o‘zgartirilmaydi

---

## 🛠 Texnik tafsilotlar

### Almashtiriladigan naqshlar:

| Teg | Naqsh | Natija |
|-----|-------|--------|
| CSS | `<link href="style.css">` | `{% static 'style.css' %}` |
| JS | `<script src="app.js">` | `{% static 'app.js' %}` |
| IMG | `<img src="photo.jpg">` | `{% static 'photo.jpg' %}` |
| HTML havola | `<a href="contact.html">` | `{% url 'contact' %}` |
| Statik fayl | `<a href="doc.pdf">` | `{% static 'doc.pdf' %}` |

### Maxsus qoidalar:
- Agar HTML fayl nomi **faqat raqamdan** iborat bo‘lsa → `error_404`
- `-` belgisi `_` ga almashtiriladi
- `{% load static %}` fayl boshida avtomatik qo‘shiladi

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

> **Django bilan ishlashni osonlashtiruvchi vosita!**  
> Tez, ishonchli, foydalanuvchiga qulay.

---
```
