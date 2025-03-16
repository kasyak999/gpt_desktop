import re
import os
import tkinter
from tkinter import ttk
from datetime import datetime
import customtkinter as ctk
from gpt4all import GPT4All


MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'
MODEL_DIR = f'/home/{os.getlogin()}/gpt_desktop/Models'
model = GPT4All(
    model_name=MODEL_NAME, model_path=MODEL_DIR, device='cpu', verbose=False)
ROLE_PROMPT = "Ты Python-разработчик. Отвечай только на русском языке"


class MyApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1020x670")
        self.title('Бот GPT')
        default_font = ("Arial", 16)

        # Создаем поле ввода текста
        self.entry = ctk.CTkTextbox(self, height=250, font=default_font)
        self.entry.pack(fill='x', padx=(10, 10), pady=(10, 0))

        # Создаем кнопку "Отправить"
        self.button = ctk.CTkButton(
            self, text="Отправить", command=self.on_button_click,
            font=default_font)
        self.button.configure(
            fg_color="green", hover_color='darkgreen', text_color="white")
        self.button.pack(pady=(10, 0))

        # Создаем поле вывода текста
        self.label = tkinter.Text(
            self, font=default_font, bg="#2D2D2D", fg="white",
            highlightthickness=0, borderwidth=0, wrap="word")
        self.label.pack(fill='both', padx=(10, 10), pady=(10, 10), expand=True)
        self.label.tag_configure("green", foreground="green")
        self.label.tag_configure("blue", foreground="blue")
        self.label.tag_configure("code", foreground="lightblue")

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

    def on_button_click(self):
        """Нажатие кнопки отправить"""
        self.button.configure(
            fg_color="red", text_color="white", state="disabled")
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        context = self.entry.get("1.0", "end-1c")
        input_text = context.replace("\\n", "\n")
        self.entry.delete("1.0", "end")
        self.label.config(state="normal")
        self.label.insert("end", f'{now}| Вопрос: ', 'green')
        self.label.insert("end", input_text + '\n')
        self.label.see("end")
        self.label.insert("end", f'{now}| Ответ: ', "blue")
        self.result = model.generate(
            prompt=context, temp=0.2, streaming=True, max_tokens=500,
            repeat_penalty=1.2)
        self._insert_text_gradually()

    def _insert_text_gradually(self, delay=10):
        """Метод для постепенного вывода текста с задержкой."""
        try:
            char = next(self.result)
            self.label.insert("end", char)
            self.after(delay, self._insert_text_gradually)
        except StopIteration:
            self.highlight_code()
            self.label.insert("end", '\n')
            self.label.config(state="disabled")

            # Когда печать завершена, восстанавливаем цвет кнопки
            self.button.configure(fg_color="green", state="normal")

    def highlight_code(self):
        """Подсветка кода внутри ```...```"""
        text = self.label.get("1.0", "end")
        code_blocks = re.finditer(
            r"```(?:python)?\s*(.*?)```", text, re.DOTALL)

        for block in code_blocks:
            start, end = block.span(1)  # Индексы начала и конца кода
            start_idx = self.label.index(f"1.0 + {start} chars")
            end_idx = self.label.index(f"1.0 + {end} chars")

            # Применяем тег для подсветки кода
            self.label.tag_add("code", start_idx, end_idx)


if __name__ == "__main__":
    root = MyApplication()
    with model.chat_session(system_prompt=ROLE_PROMPT) as session:
        root.mainloop()
