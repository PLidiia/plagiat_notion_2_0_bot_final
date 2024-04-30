from aiogram import Router, types, F
from aiogram.filters import Command

from bot_logging.logger import logger
from handlers.messages import help_cmd_message

router_help = Router()


@router_help.message(Command('help'))
@router_help.message(F.text.contains('помощь'))
async def help_cmd(message: types.Message) -> None:
    '''Асинхронная функция, отвечающая за команду помощи, высылающая подсказку'''
    try:
        logger.log("info", f"Пользователь {message.from_user.id} зашёл в /help")
        await message.answer(f'{help_cmd_message} + ❗')
    except Exception as e:
        logger.log("error", f"произошла ошибка в хэндлере /help {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
