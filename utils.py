import os
import sys
import re
from datetime import datetime


def on_focus_in(self, event, placeholder_text):
    """Очистка placeholder при фокусе"""
    if self.get("1.0", "end-1c") == placeholder_text:
        self.delete("1.0", "end")


def on_focus_out(self, event, placeholder_text):
    """Возвращение placeholder, если поле пустое"""
    if self.get("1.0", "end-1c").strip() == "":
        self.insert("1.0", placeholder_text)


def update_font_size(self, value):
    """Обновление размера шрифта"""
    new_size = int(value)
    self.label.configure(font=("Arial", new_size))
    self.entry.configure(font=("Arial", new_size))
    self.button.configure(font=("Arial", new_size))
    self.button1.configure(font=("Arial", new_size))
    self.label_info.configure(font=("Arial", new_size))


def on_button_settings(seting):
    """Открытие окна настроек"""
    seting.deiconify()


def get_current_time():
    """Возвращает текущее время в формате YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def restart_app(selected_option, value):
    """Перезапуск приложения с новым значением QWE"""
    os.environ["RADIO_VALUE"] = selected_option
    os.environ["ROLE_PROMPT"] = str(value)
    os.execv(sys.executable, ["python"] + sys.argv)


def append_text(label, text, tag=None):
    """Добавляет текст в окно вывода с опциональной цветовой меткой"""
    label.config(state="normal")
    if tag:
        label.insert("end", text, tag)
    else:
        label.insert("end", text)
    label.config(state="disabled")
    label.see("end")


def highlight_code(label):
    """Подсветка кода внутри ```...```"""
    text = label.get("1.0", "end")
    code_blocks = re.finditer(
        r"```(?:python)?\s*(.*?)```", text, re.DOTALL)

    for block in code_blocks:
        start, end = block.span(1)  # Индексы начала и конца кода
        start_idx = label.index(f"1.0 + {start} chars")
        end_idx = label.index(f"1.0 + {end} chars")

        # Применяем тег для подсветки кода
        label.tag_add("code", start_idx, end_idx)
