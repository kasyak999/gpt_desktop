import os
import sys
import re
from datetime import datetime
import webbrowser


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


def on_button_click(self, model):
    """Нажатие кнопки отправить"""
    self.label_info.configure(text="Печатает ...")
    self.button.configure(
        fg_color="red", text_color="white", state="disabled")
    context = self.entry.get("1.0", "end-1c").replace("\\n", "\n")
    self.entry.delete("1.0", "end")

    now = get_current_time()
    append_text(self.label, f'{now}| Вопрос: ', 'green')
    append_text(self.label, context + '\n')
    self.label.see("end")

    self.update_idletasks()  # принудительное обновление

    self.result = model.generate(
        prompt=context, temp=0.2, streaming=True, max_tokens=500,
        repeat_penalty=1.2)
    now = get_current_time()
    append_text(self.label, f'{now}| Ответ: ', 'blue')
    insert_text_gradually(self)


def insert_text_gradually(self, delay=10):
    """Метод для постепенного вывода текста с задержкой."""
    try:
        self.label.config(state="normal")
        char = next(self.result)
        self.label.insert("end", char)
        self.label.config(state="disabled")
        self.after(delay, lambda: insert_text_gradually(self))
    except StopIteration:
        highlight_code(self.label)
        self.label.insert("end", '\n')
        self.label.config(state="disabled")
        self.label_info.configure(text="")

        # Когда печать завершена, восстанавливаем цвет кнопки
        self.button.configure(fg_color="green", state="normal")


def on_option_selected(self):
    """Функция обработки выбора"""
    value = ''
    if self.selected_option.get() == 'option2':
        value = (
            'Ты космонавт который летит на Марс. Отвечай только на '
            'русском языке')
    elif self.selected_option.get() == 'option3':
        value = 'Ты Python-разработчик. Отвечай только на русском языке'
    elif self.selected_option.get() == 'option4':
        value = ''  # Задать новую роль
    restart_app(self.selected_option.get(), value)


def on_closing(self, model):
    """Закрытие приложения"""
    try:
        model.close()  # Остановим модель, если у нее есть метод close()
    except AttributeError:
        pass
    self.seting.destroy()  # Закрываем окно настроек, если оно открыто
    self.destroy()
    sys.exit(0)


def open_link(event, url):
    """Функция для открытия ссылки"""
    webbrowser.open_new(url)  # Вставьте нужную ссылку
