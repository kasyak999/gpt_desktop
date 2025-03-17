import re
import os
import sys
import tkinter
from tkinter import ttk
import customtkinter as ctk
from gpt4all import GPT4All
import utils as fun


MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'
MODEL_DIR = f'/home/{os.getlogin()}/gpt_desktop/Models'
model = GPT4All(
    model_name=MODEL_NAME, model_path=MODEL_DIR, device='cpu', verbose=False)
ROLE_PROMPT = os.getenv(
    "ROLE_PROMPT", '')
RADIO_VALUE = os.getenv("RADIO_VALUE", "option1")


class MyApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1020x670")
        self.title('Gpt бот desktop')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.font_size = 16
        default_font = ("Arial", self.font_size)
        self.configure(fg_color="#202020")

        # Создаем поле ввода текста
        self.placeholder_text = "Введите сообщение..."
        self.entry = ctk.CTkTextbox(self, height=250, font=default_font)
        self.entry.configure(fg_color="#2D2D2D")
        self.entry.pack(fill='x', padx=(10, 10), pady=(10, 0))
        self.entry.insert("1.0", self.placeholder_text)
        self.entry.bind(
            "<FocusIn>", lambda event: fun.on_focus_in(
                self.entry, event, self.placeholder_text))
        self.entry.bind(
            "<FocusOut>", lambda event: fun.on_focus_out(
                self.entry, event, self.placeholder_text))

        frame = ctk.CTkFrame(self)  # Контейнер для кнопок
        frame.configure(fg_color="#2D2D2D")
        frame.pack(pady=10)  # Размещаем контейнер
        frame.pack(fill='x', padx=(10, 10), pady=(10, 0))

        # Создаем кнопку "Отправить"
        self.button = ctk.CTkButton(
            frame, text="Отправить", command=self.on_button_click,
            font=default_font)
        self.button.configure(fg_color="green", hover_color='darkgreen')
        self.button.pack(side="left", padx=0)

        # Поле статуса
        self.label_info = ctk.CTkLabel(frame, text="")
        self.label_info.configure(fg_color="#2D2D2D")
        self.label_info.pack(side="left", padx=10)

        # Создаем поле вывода текста
        self.label = tkinter.Text(
            self, font=default_font,
            bg="#2D2D2D", fg="white",
            highlightthickness=0, borderwidth=0, wrap="word")
        self.label.pack(fill='both', padx=(10, 10), pady=(10, 10), expand=True)
        self.label.tag_configure("green", foreground="green")
        self.label.tag_configure("blue", foreground="blue")
        self.label.tag_configure("code", foreground="lightblue")
        self.label.config(state="disabled")

        # Добавляем вертикальную прокрутку
        style = ttk.Style()
        style.configure(
            "TScrollbar", troughcolor="black", background="#2D2D2D")
        style.map("TScrollbar", background=[("disabled", "#2D2D2D")])
        scrollbar = ttk.Scrollbar(
            self.label, command=self.label.yview, style="TScrollbar")
        scrollbar.pack(side="right", fill="y")

        # Привязываем прокрутку к текстовому полю
        self.label.config(yscrollcommand=scrollbar.set)

        self.seting = ctk.CTk()
        self.seting.geometry("300x300")
        self.seting.title('Настройки')
        self.seting.withdraw()
        self.seting.protocol("WM_DELETE_WINDOW", self.seting.withdraw)
        self.seting.configure(fg_color="#202020")

        # Создаем кнопку "Настройки"
        self.button1 = ctk.CTkButton(
            frame, text="Настройки",
            command=lambda: fun.on_button_settings(self.seting),
            font=default_font)
        self.button1.configure(fg_color="black", hover_color='darkgreen')
        self.button1.pack(side="right", padx=0)

        # Переменная для хранения выбранного значения
        self.selected_option = ctk.StringVar(value=RADIO_VALUE)

        lebel1 = ctk.CTkLabel(
            self.seting, text="Выберите промт для бота:", font=default_font)
        lebel1.pack(pady=10)

        radio1 = ctk.CTkRadioButton(
            self.seting, text="Стандартный",
            variable=self.selected_option, value="option1",
            command=self.on_option_selected)
        radio1.pack(pady=10)

        radio2 = ctk.CTkRadioButton(
            self.seting, text="Космонавт",
            variable=self.selected_option, value="option2",
            command=self.on_option_selected)
        radio2.pack(pady=10)

        radio3 = ctk.CTkRadioButton(
            self.seting, text='Python-разработчик',
            variable=self.selected_option, value="option3",
            command=self.on_option_selected)
        radio3.pack(pady=10)

        radio4 = ctk.CTkRadioButton(
            self.seting, text='Новая роль',
            variable=self.selected_option, value="option4",
            command=self.on_option_selected)
        radio4.pack(pady=10)

        # Ползунок для изменения размера шрифта
        lebel2 = ctk.CTkLabel(
            self.seting, text="Изменить размер шрифта", font=default_font)
        lebel2.pack(pady=10)
        self.slider = ctk.CTkSlider(
            self.seting, from_=10, to=50,
            command=lambda value: fun.update_font_size(self, value))
        self.slider.set(self.font_size)
        self.slider.pack(pady=10)

        # устанавливаем цвет текста для блоков
        for radio in [
            self.entry, self.label_info, self.button, self.button1, lebel1,
            lebel2, radio1, radio2, radio3, radio4
        ]:
            radio.configure(text_color='white')

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
        fun.restart_app(self.selected_option.get(), value)

    def on_button_click(self):
        """Нажатие кнопки отправить"""
        self.label_info.configure(text="Печатает ...")
        self.button.configure(
            fg_color="red", text_color="white", state="disabled")
        context = self.entry.get("1.0", "end-1c").replace("\\n", "\n")
        self.entry.delete("1.0", "end")

        now = fun.get_current_time()
        fun.append_text(self.label, f'{now}| Вопрос: ', 'green')
        fun.append_text(self.label, context + '\n')
        self.label.see("end")

        self.update_idletasks()  # принудительное обновление

        self.result = model.generate(
            prompt=context, temp=0.2, streaming=True, max_tokens=500,
            repeat_penalty=1.2)
        now = fun.get_current_time()
        fun.append_text(self.label, f'{now}| Ответ: ', 'blue')
        self._insert_text_gradually()

    def _insert_text_gradually(self, delay=10):
        """Метод для постепенного вывода текста с задержкой."""
        try:
            self.label.config(state="normal")
            char = next(self.result)
            self.label.insert("end", char)
            self.label.config(state="disabled")
            self.after(delay, self._insert_text_gradually)
        except StopIteration:
            fun.highlight_code(self.label)
            self.label.insert("end", '\n')
            self.label.config(state="disabled")
            self.label_info.configure(text="")

            # Когда печать завершена, восстанавливаем цвет кнопки
            self.button.configure(fg_color="green", state="normal")

    def on_closing(self):
        """Закрытие приложения"""
        try:
            model.close()  # Остановим модель, если у нее есть метод close()
        except AttributeError:
            pass
        self.seting.destroy()  # Закрываем окно настроек, если оно открыто
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    root = MyApplication()
    with model.chat_session(system_prompt=ROLE_PROMPT) as session:
        root.mainloop()
