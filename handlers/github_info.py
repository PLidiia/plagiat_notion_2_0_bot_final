from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

from API.github.get_info_github_user import get_user_repos, create_repo
from bot_logging.logger import logger

router_github = Router()


@router_github.message(Command('get_github_info'))
async def get_github_info(message: types.Message) -> None:
    '''Асинхронная функция, отвечающая за команду вывода названий репозиториев пользователя'''
    try:
        logger.log("info", "Запущен хэндлер /get_github_info")
        await message.answer('Отправьте имя пользователя на сайте github, по шаблону "имя: "',
                             parse_mode=ParseMode.HTML)

        @router_github.message(F.text.contains('имя:'))
        async def process_username(message: types.Message) -> None:
            try:
                username = message.text.split('имя: ')[1]
                repo_user = get_user_repos(username)
                if repo_user:
                    for item in repo_user:
                        await message.answer(str(item['name']))
                else:
                    await message.answer('К сожалению, не нашлось ваших репозиториев')
            except Exception as e:
                logger.log("error", f"ошибка в хэндлере /get_github_info {str(e)}")
                await message.answer(
                    'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')

    except Exception as e:
        logger.log("error", f"ошибка в хэндлере /get_github_info {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')


@router_github.message(Command('create_repo'))
async def create_repo(message: types.Message) -> None:
    '''Асинхронная функция, отвечающая за создание репозитория'''
    try:
        logger.log("info", "Запущен хэндлер /get_github_info")
        await message.answer('Отправьте ваш токен на github, по шаблону "токен: "',
                             parse_mode=ParseMode.HTML)

        @router_github.message(F.text.contains('токен: '))
        async def process_token(message: types.Message) -> None:
            try:
                token = message.text.split('токен: ')[1]
                await message.answer('Отправьте как вы хотите назвать репозиторий на github, по шаблону "имя: "',
                                     parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.log("error", f"ошибка в хэндлере /get_github_info {str(e)}")
                await message.answer(
                    'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')

                @router_github.message(F.text.contains('имя: '))
                async def process_name(message: types.Message) -> None:
                    try:
                        name_repo = message.text.split('имя: ')[1]
                        repo_data = create_repo(token, name_repo)
                        if repo_data:
                            await message.answer(f'Репозиторий {name_repo} успешно создан')
                        else:
                            await message.answer(f'Репозиторий {name_repo} не создан')
                    except Exception as e:
                        logger.log("error", f"ошибка при записе имени репозитория{str(e)}")
                        await message.answer(
                            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
    except Exception as e:
        logger.log("error", f"ошибка в хэндлере /get_github_info {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
