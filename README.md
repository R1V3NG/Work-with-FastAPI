Создание venv (один раз при установки проекта)
py -m venv .venv

Активация venv (windows)
.venv\Scripts\activate

Установка зависимостей
py -m pip install -r requirements.txt
Запуск проекта в режиме разработчика
`py -m fastapi dev main.py`

Запуск проекта в режиме prod
`py -m fastapi run main.py`