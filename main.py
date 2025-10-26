import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import threading


class DjangoHTMLConverter:
    def __init__(self):
        self.patterns = {
            'link_css': r'<link\s+([^>]*?)href=[""\']([^""\']+\.css)[""\']([^>]*?)>',
            'link_other': r'<link\s+([^>]*?)href=[""\']([^""\']+\.(html|json|xml|webmanifest|ico|png|jpg|jpeg|gif|svg))[""\']([^>]*?)>',
            'script': r'<script\s+([^>]*?)src=[""\']([^""\']+\.js)[""\']([^>]*?)>',
            'img': r'<img\s+([^>]*?)src=[""\']([^""\']+\.(png|jpg|jpeg|gif|svg|webp|ico))[""\']([^>]*?)>',
            'a_href_html': r'<a\s+([^>]*?)href=[""\']([^""\']+\.html?)[""\']([^>]*?)>',
            'a_href_static': r'<a\s+([^>]*?)href=[""\']([^""\']+\.(pdf|zip|doc|docx))[""\']([^>]*?)>',
        }
        self.static_tag_added = False

    def is_external_url(self, url):
        return url.startswith(('http://', 'https://', '//', 'data:', '#'))

    def convert_to_static(self, url):
        """Django {% static %} formatiga o'zgartirish"""
        clean_url = url.lstrip('/')
        clean_url = re.sub(r'^(\.\./)+', '', clean_url)
        if clean_url.startswith('static/'):
            clean_url = clean_url[7:]
        return f"{{% static '{clean_url}' %}}"

    def convert_html_filename_to_route(self, filename):
        """HTML fayl nomini Django URL nomiga o'zgartirish"""
        route_name = os.path.splitext(filename)[0]

        # Agar raqam bilan boshlansa, 'error_' prefiksini qo'shish
        if route_name.isdigit():
            route_name = f"error_{route_name}"

        # '-' belgilarini '_' ga almashtirish
        route_name = route_name.replace('-', '_')

        return route_name

    def replace_link_css(self, match):
        before, url, after = match.group(1), match.group(2), match.group(3)
        if self.is_external_url(url):
            return match.group(0)
        new_url = self.convert_to_static(url)
        return f'<link {before}href="{new_url}"{after}>'

    def replace_script(self, match):
        before, url, after = match.group(1), match.group(2), match.group(3)
        if self.is_external_url(url):
            return match.group(0)
        new_url = self.convert_to_static(url)
        return f'<script {before}src="{new_url}"{after}>'

    def replace_img(self, match):
        before, url, after = match.group(1), match.group(2), match.group(4)
        if self.is_external_url(url):
            return match.group(0)
        new_url = self.convert_to_static(url)
        return f'<img {before}src="{new_url}"{after}>'

    def replace_link_icon(self, match):
        before, url, after = match.group(1), match.group(2), match.group(4)
        if self.is_external_url(url):
            return match.group(0)
        new_url = self.convert_to_static(url)
        return f'<link {before}href="{new_url}"{after}>'

    def replace_a_href_html(self, match):
        before, url, after = match.group(1), match.group(2), match.group(3)
        if self.is_external_url(url):
            return match.group(0)

        filename = os.path.basename(url)
        route_name = self.convert_html_filename_to_route(filename)
        new_url = f"{{% url '{route_name}' %}}"
        return f'<a {before}href="{new_url}"{after}>'

    def replace_a_href_static(self, match):
        before, url, after = match.group(1), match.group(2), match.group(4)
        if self.is_external_url(url):
            return match.group(0)
        new_url = self.convert_to_static(url)
        return f'<a {before}href="{new_url}"{after}>'

    def add_load_static_tag(self, html_content):
        """HTML faylning boshiga {% load static %} qo'shish"""
        # Agar {% load static %} allaqachon mavjud bo'lsa, qayta qo'shmaslik
        if '{% load static %}' in html_content or '{%load static%}' in html_content:
            return html_content

        # DOCTYPE yoki <html> tagidan oldin qo'shish
        if '<!DOCTYPE' in html_content or '<!doctype' in html_content:
            # DOCTYPE dan keyin qo'shish
            pattern = r'(<!DOCTYPE[^>]*>)'
            replacement = r'\1\n{% load static %}'
            return re.sub(pattern, replacement, html_content, count=1, flags=re.IGNORECASE)
        elif '<html' in html_content:
            # <html> tagidan oldin qo'shish
            pattern = r'(<html[^>]*>)'
            replacement = r'{% load static %}\n\1'
            return re.sub(pattern, replacement, html_content, count=1, flags=re.IGNORECASE)
        else:
            # Faylning eng boshiga qo'shish
            return '{% load static %}\n' + html_content

    def convert_html(self, html_content):
        result = html_content

        # Barcha almashtirishlarni amalga oshirish
        result = re.sub(self.patterns['link_css'], self.replace_link_css, result)
        result = re.sub(self.patterns['link_other'], self.replace_link_icon, result)
        result = re.sub(self.patterns['script'], self.replace_script, result)
        result = re.sub(self.patterns['img'], self.replace_img, result)
        result = re.sub(self.patterns['a_href_html'], self.replace_a_href_html, result)
        result = re.sub(self.patterns['a_href_static'], self.replace_a_href_static, result)

        # {% load static %} qo'shish
        result = self.add_load_static_tag(result)

        return result

    def convert_file(self, input_file, output_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            converted_content = self.convert_html(html_content)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)

            return True, None
        except Exception as e:
            return False, str(e)


class DjangoConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Django HTML Konverter")

        # Ekran o'lchamini aniqlash
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Oyna o'lchami (ekranning 70%)
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.75)

        # Minimum o'lcham
        self.root.minsize(700, 600)

        # Oynani markazlashtirish
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)

        # Ranglar
        self.bg_color = "#f5f7fa"
        self.primary_color = "#092e20"  # Django qora-yashil rangi
        self.success_color = "#0c4b33"  # Django yashil rangi
        self.error_color = "#e74c3c"
        self.text_color = "#2c3e50"
        self.card_bg = "#ffffff"

        self.root.configure(bg=self.bg_color)

        self.converter = DjangoHTMLConverter()
        self.input_folder = ""
        self.output_folder = ""

        self.create_widgets()

    def create_widgets(self):
        # Sarlavha
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🐍 Django HTML Konverter",
            font=("Arial", 26, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=25)

        # Asosiy konteyner
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Kirish papkasi kartasi
        input_card = tk.Frame(main_frame, bg=self.card_bg, relief=tk.RAISED, bd=1)
        input_card.pack(fill=tk.X, pady=(0, 20))

        input_inner = tk.Frame(input_card, bg=self.card_bg)
        input_inner.pack(fill=tk.X, padx=20, pady=20)

        input_label = tk.Label(
            input_inner,
            text="📁 Kirish papkasi (HTML fayllar):",
            font=("Arial", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            anchor="w"
        )
        input_label.pack(fill=tk.X, pady=(0, 10))

        input_frame = tk.Frame(input_inner, bg=self.card_bg)
        input_frame.pack(fill=tk.X)

        self.input_entry = tk.Entry(
            input_frame,
            font=("Arial", 10),
            relief=tk.SOLID,
            bg="#f8f9fa",
            fg=self.text_color,
            bd=1
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.input_entry.bind('<Control-v>', lambda e: self.paste_to_entry(self.input_entry))
        self.input_entry.bind('<Button-3>', lambda e: self.show_context_menu(e, self.input_entry))

        input_btn = tk.Button(
            input_frame,
            text="Tanlash",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#0a1f14",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.browse_input_folder
        )
        input_btn.pack(side=tk.LEFT)

        # Chiqish papkasi kartasi
        output_card = tk.Frame(main_frame, bg=self.card_bg, relief=tk.RAISED, bd=1)
        output_card.pack(fill=tk.X, pady=(0, 20))

        output_inner = tk.Frame(output_card, bg=self.card_bg)
        output_inner.pack(fill=tk.X, padx=20, pady=20)

        output_label = tk.Label(
            output_inner,
            text="📂 Chiqish papkasi (saqlash uchun):",
            font=("Arial", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            anchor="w"
        )
        output_label.pack(fill=tk.X, pady=(0, 10))

        output_frame = tk.Frame(output_inner, bg=self.card_bg)
        output_frame.pack(fill=tk.X)

        self.output_entry = tk.Entry(
            output_frame,
            font=("Arial", 10),
            relief=tk.SOLID,
            bg="#f8f9fa",
            fg=self.text_color,
            bd=1
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.output_entry.bind('<Control-v>', lambda e: self.paste_to_entry(self.output_entry))
        self.output_entry.bind('<Button-3>', lambda e: self.show_context_menu(e, self.output_entry))

        output_btn = tk.Button(
            output_frame,
            text="Tanlash",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#0a1f14",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.browse_output_folder
        )
        output_btn.pack(side=tk.LEFT)

        # Konvertatsiya tugmasi - KATTA TUGMA
        self.convert_btn = tk.Button(
            main_frame,
            text="🚀 KONVERTATSIYA QILISH",
            font=("Arial", 14, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#0a3d28",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=40,
            pady=15,
            command=self.start_conversion
        )
        self.convert_btn.pack(pady=(0, 20))

        # Progress qismi
        progress_card = tk.Frame(main_frame, bg=self.card_bg, relief=tk.RAISED, bd=1)
        progress_card.pack(fill=tk.X, pady=(0, 20))

        progress_inner = tk.Frame(progress_card, bg=self.card_bg)
        progress_inner.pack(fill=tk.X, padx=20, pady=15)

        self.status_label = tk.Label(
            progress_inner,
            text="Kutilmoqda...",
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color
        )
        self.status_label.pack(pady=(0, 10))

        self.progress_bar = ttk.Progressbar(
            progress_inner,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X)

        # Log qismi
        log_card = tk.Frame(main_frame, bg=self.card_bg, relief=tk.RAISED, bd=1)
        log_card.pack(fill=tk.BOTH, expand=True)

        log_inner = tk.Frame(log_card, bg=self.card_bg)
        log_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        log_label = tk.Label(
            log_inner,
            text="📋 Jurnal:",
            font=("Arial", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            anchor="w"
        )
        log_label.pack(fill=tk.X, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(
            log_inner,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg=self.text_color,
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def paste_to_entry(self, entry):
        """Ctrl+V uchun"""
        try:
            clipboard_content = self.root.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, clipboard_content)
            # Papkani yangilash
            if entry == self.input_entry:
                self.input_folder = clipboard_content
                self.log_message(f"✓ Kirish papkasi: {clipboard_content}")
            else:
                self.output_folder = clipboard_content
                self.log_message(f"✓ Chiqish papkasi: {clipboard_content}")
        except:
            pass
        return "break"

    def show_context_menu(self, event, entry):
        """O'ng tugma uchun menyu"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Nusxalash (Ctrl+C)", command=lambda: self.copy_from_entry(entry))
        menu.add_command(label="Qo'yish (Ctrl+V)", command=lambda: self.paste_to_entry(entry))
        menu.add_separator()
        menu.add_command(label="Tozalash", command=lambda: entry.delete(0, tk.END))
        menu.post(event.x_root, event.y_root)

    def copy_from_entry(self, entry):
        """Nusxalash"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(entry.get())
        except:
            pass

    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="HTML fayllar papkasini tanlang")
        if folder:
            self.input_folder = folder
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)
            self.log_message(f"✓ Kirish papkasi tanlandi: {folder}")

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Saqlash papkasini tanlang")
        if folder:
            self.output_folder = folder
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.log_message(f"✓ Chiqish papkasi tanlandi: {folder}")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_conversion(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Xato", "Iltimos, kirish va chiqish papkalarini tanlang!")
            return

        input_abs = os.path.abspath(self.input_folder)
        output_abs = os.path.abspath(self.output_folder)

        if input_abs == output_abs:
            messagebox.showerror(
                "Xato",
                "Kirish va chiqish papkalari bir xil bo'lishi mumkin emas!\n\n"
                "Iltimos, boshqa papka tanlang."
            )
            return

        # Alohida thread da ishga tushirish
        thread = threading.Thread(target=self.convert_all_files)
        thread.daemon = True
        thread.start()

    def convert_all_files(self):
        self.convert_btn.config(state=tk.DISABLED)
        self.log_message("\n" + "=" * 60)
        self.log_message("🔄 Konvertatsiya boshlandi...")
        self.log_message("=" * 60)

        html_files = []
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith(('.html', '.htm')):
                    html_files.append(os.path.join(root, file))

        if not html_files:
            self.log_message("⚠️ Tanlangan papkada HTML fayllar topilmadi!")
            self.status_label.config(text="HTML fayllar topilmadi")
            self.convert_btn.config(state=tk.NORMAL)
            messagebox.showwarning("Ogohlantirish", "Tanlangan papkada HTML fayllar yo'q!")
            return

        total_files = len(html_files)
        self.log_message(f"📄 Topilgan HTML fayllar: {total_files}\n")

        success_count = 0
        error_count = 0

        for idx, html_file in enumerate(html_files):
            rel_path = os.path.relpath(html_file, self.input_folder)
            output_file = os.path.join(self.output_folder, rel_path)

            self.status_label.config(text=f"Konvertatsiya [{idx + 1}/{total_files}]: {rel_path}")
            progress = int((idx + 1) / total_files * 100)
            self.progress_bar['value'] = progress

            success, error = self.converter.convert_file(html_file, output_file)

            if success:
                self.log_message(f"✓ [{idx + 1}/{total_files}] {rel_path}")
                success_count += 1
            else:
                self.log_message(f"✗ [{idx + 1}/{total_files}] {rel_path} - Xato: {error}")
                error_count += 1

            self.root.update_idletasks()

        self.log_message("\n" + "=" * 60)
        self.log_message("✅ Konvertatsiya yakunlandi!")
        self.log_message(f"   Muvaffaqiyatli: {success_count}")
        if error_count > 0:
            self.log_message(f"   Xatolar: {error_count}")
        self.log_message("=" * 60)

        self.status_label.config(text="✅ Konvertatsiya yakunlandi!")
        self.progress_bar['value'] = 100
        self.convert_btn.config(state=tk.NORMAL)

        messagebox.showinfo(
            "Tayyor! ✅",
            f"Konvertatsiya muvaffaqiyatli yakunlandi!\n\n"
            f"✓ Muvaffaqiyatli: {success_count}\n"
            f"✗ Xatolar: {error_count}\n\n"
            f"Fayllar saqlandi:\n{self.output_folder}"
        )


def main():
    root = tk.Tk()
    app = DjangoConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()