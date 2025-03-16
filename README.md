

## Как запустить ?
- Установить виртуальное окружение и установить зависимости
    ```bash
    python -m venv venv
    pip install -r requirements.txt
    ```
- запустить main.py для скачивания модели
    ```bash
    python main.py
    ```
- Как скачается модель и откроется приложение можно его закрыть. В директории проекта появится папка **Models**
- Собрать приложение
    ```bash
    pyinstaller --onedir  main.py
    ```
- Появится папка **dest/main/**
    - Скопировать
        ```bash
        cp -r venv/lib/python3.13/site-packages/gpt4all dist/main/_internal
        ```
    - Скопировать
        ```bash
        cp -r Models /home/имя_пользователя/gpt_desktop/Models
        ```
- Готово. Теперь можно запустить.
    ```bash
    ./dist/main/main 
    ```