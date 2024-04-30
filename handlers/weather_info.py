from aiogram import Router, types, F
from aiogram.filters import Command

from API.weather.get_weather import get_weather_5_day
from bot_logging.logger import logger

router_weather = Router()


@router_weather.message(Command('get_weather_5_days'))
async def get_weather_5_days_bot(message: types.Message):
    try:
        await message.answer(
            'Вы хотите, чтобы погода была построена по текущему местоположению 🗺, если да,'
            'то напишите "да", если нет, то напишите "нет "')

        @router_weather.message(F.text.contains('да'))
        async def get_weather_cur_location(message: types.Message):
            try:
                data_weather = get_weather_5_day()
                await message.answer('Подождите идёт обработка погоды...')
                if not data_weather:
                    for day_weather in data_weather:
                        await message.answer(day_weather)
                else:
                    await message.answer('Информация о погоде не найдено')
            except Exception as e:
                logger.log("error",
                           f"Произошла ошибка в функции get_weather_cur_location хэндлера "
                           f"/get_weather_5_days_bot {str(e)}")

        @router_weather.message(F.text.contains('нет'))
        async def another_location_input(message: types.Message):
            try:
                await message.answer('Введите название города 🏙 по шаблону "город:"')
            except Exception as e:
                logger.log("error",
                           f"Произошла ошибка в функции another_location_input хэндлера "
                           f"/get_weather_5_days_bot {str(e)}")

            @router_weather.message(F.text.contains('город:'))
            async def get_weather_another_location(message: types.Message):
                try:
                    city = message.text.split(':')[1]
                    data_weather = get_weather_5_day(city)
                    await message.answer('Подождите идёт обработка погоды...')
                    if data_weather:
                        for day_weather in data_weather:
                            await message.answer(day_weather)
                    else:
                        await message.answer('К сожалению, информация о вашем городе не была найдена')
                except Exception as e:
                    logger.log("error",
                               f"Произошла ошибка в функции get_weather_another_location хэндлера "
                               f"/get_weather_5_days_bot {str(e)}")
    except Exception as e:
        logger.log('error', f"Произошла ошибка в хэндлере /get_weather_5_days {str(e)}")
        await message.answer(
            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
