from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ParseMode
from API.hh.graphical_display_vacancies import draw_diagram
from bot_logging.logger import logger

router_hh = Router()


@router_hh.message(Command('get_diagram_about_job'))
async def get_diagram_about_job(message: types.Message) -> None:
    '''Асинхронная функция, отправляющая диаграмму пользователю картинкой
       Местоположение определяется по ip компьютера'''

    try:
        await message.answer('Введите название профессии 🎓 по шаблону <b>"профессия: "</b>', parse_mode=ParseMode.HTML)

        # шаблон необходим для того, чтобы каждая асинхронная функция внутри другой асинхронной функции работали
        # корректно, так как идёт создания графического изображение, то асинхронность является необходимостью
        @router_hh.message(F.text.contains('профессия: '))
        async def get_name_job(message: types.Message) -> None:
            await message.answer('Подождите идёт создания графика...')
            job = message.text.split('профессия: ')
            draw_diagram(job)
            await message.answer_photo(FSInputFile('salary_chart.png'))

    except Exception as e:
        logger.log('error', f"Произошла ошибка в хэндлере /get_diagram_about_job {str(e)}")
        await message.answer(
            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
