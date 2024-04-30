from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from bot_logging.logger import logger
from database.requests import set_user
from handlers.messages import start_cmd_message_existing, start_cmd_message_not_existing

router = Router()


@router.message(CommandStart())
@router.message(F.text.contains('старт'))
async def start_cmd(message: types.Message) -> None:
    '''Асинхронная функция, отвечающая за команду приветствия, если пользователь уже заходил в бота,
    то будет сообщение с минимальным описание команд в боте, если не заходил, то будет представлено
    подробное описание возможностей бота'''
    try:
        logger.log("info", "Запущен хэндлер /start")
        entity = await set_user(message.from_user.id)
        # получили результат запроса из бд, заходил ли пользователь
        if entity:
            logger.log("info", f"{message.from_user.first_name} - пользователь уже заходил в бота")
            await message.answer(f'✋<b>{message.from_user.first_name}</b>, {start_cmd_message_existing}',
                                 parse_mode=ParseMode.HTML)
        else:
            logger.log("info", f"{message.from_user.first_name} - пользователь не заходил в бота")
            await message.answer(f'✋<b>{message.from_user.first_name}</b>, {start_cmd_message_not_existing}',
                                 parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.log("error", f"ошибка в хэндлере /start {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
