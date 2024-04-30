from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile

from API.maps.get_info_about_address import get_location, get_image_location
from bot_logging.logger import logger

router_maps = Router()


@router_maps.message(Command('get_image_place'))
async def get_image_place(message: types.Message):
    try:
        await message.answer('Введите адрес 🏡, например Ленина 52, Кемерово, <b>по шаблону "адрес: "</b>',
                             parse_mode=ParseMode.HTML)

        @router_maps.message(F.text.contains('адрес: '))
        async def get_address(message: types.Message):
            await message.answer('Подождите идёт обработка адреса...')
            location = get_location(message.text.split('адрес: ')[1])
            await message.answer(f'<b>{location}</b> - координаты введённого места', parse_mode=ParseMode.HTML)
            await message.answer('Подождите идёт создания изображения карты...')
            get_image_location(location)
            await message.answer_photo(FSInputFile('map.png'))

    except Exception as e:
        logger.log('error', f"Произошла ошибка в хэндлере /get_image_place {str(e)}")
        await message.answer(
            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
