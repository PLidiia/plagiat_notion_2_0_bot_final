from aiogram.types import BotCommand

commands = [
    BotCommand(command='help', description='Где найти все методы'),
    BotCommand(command='start', description='Что делает бот'),
    BotCommand(command='add_task', description='Добавить задачу'),
    BotCommand(command='show_my_tasks', description='Показать задачи'),
    BotCommand(command='get_diagram_about_job', description='Создать диаграмму зарплат профессии'),
    BotCommand(command='get_image_place', description='Получите изображения местности'),
    BotCommand(command='get_weather_5_days', description='Получить погоду на ближайших 5 дней'),
    BotCommand(command='get_github_info', description='Получить репозитории по имени'),
    BotCommand(command='create_repo', description='Создать репозиторий'),
]
