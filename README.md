## Создание venv (один раз при установки проекта)
`py -m venv .venv`

## Активация venv (Windows)
> .venv\Scripts\activate

## Установка зависимостей
`py -m pip install -r requirements.txt`
## Запуск проекта в режиме разработчика
`py -m fastapi dev main.py`

## Запуск проекта в режиме prod
`py -m fastapi run main.py`

## 🔐JWT Авторизация 
1. Выполните POST /user/login со своими name и password;
2. Скопируйте access_token из ответа;
3. Нажмите Authorize (🔒) и вставьте токен.