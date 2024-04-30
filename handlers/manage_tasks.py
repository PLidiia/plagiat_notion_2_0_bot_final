from aiogram import Router, F
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_logging.logger import logger
from database.requests import set_user, add_task_db, show_tasks_db, get_info_task

router_manage_tasks = Router()


@router_manage_tasks.message(Command('add_task'))
@router_manage_tasks.message(F.text.contains('задание'))
async def add_task(message: types.Message) -> None:
    '''Асинхронная функция для создания задачи'''
    try:
        tg_id = message.from_user.id
        logger.log("info", f"Пользователь вошёл в хэндлер /add_task {tg_id}")
        await set_user(tg_id)
        await message.answer('Напишите название задачи по такому шаблону <b>"название: "</b>',
                             parse_mode=ParseMode.HTML)

        @router_manage_tasks.message(F.text.contains('название:'))
        async def process_task_name(message: types.Message) -> None:
            try:
                # присвоение имени задачи
                task_name = message.text
                await message.answer(f'Вы ввели название задачи: {task_name.split("название: ")[1]}')
                await message.answer(
                    'Вы можете написать описание, если хотите просто напишете <b>"да"</b>, '
                    'если нет то напишите <b>"закончили"</b>', parse_mode=ParseMode.HTML)

                @router_manage_tasks.message(F.text.contains('да'))
                async def process_task_description(message: types.Message) -> None:
                    try:
                        await message.answer(
                            f'Хорошо, вы хотите написать описание вашей задачи, напишите пожалуйста '
                            f'его по шаблону <b>"описание:"</b>',
                            parse_mode=ParseMode.HTML)
                    except Exception as e:
                        logger.log("error",
                                   f"Произошла ошибка {str(e)} при записе описания {tg_id}")
            except Exception as e:
                logger.log("error",
                           f"Произошла ошибка {str(e)} при записе названия {tg_id}")

                @router_manage_tasks.message(F.text.contains('описание:'))
                async def process_order_db_description(message: types.Message) -> None:
                    # добавление описания задачи
                    try:
                        task_description = message.text
                        await message.answer(
                            'Хотите ли вы добавить координаты задачи, если да то напишите <b>"хочу"</b>, если '
                            'нет, то "нет"', parse_mode=ParseMode.HTML)
                    except Exception as e:
                        logger.log("error",
                                   f"Произошла ошибка {str(e)} при описании задачи {tg_id}")

                    @router_manage_tasks.message(F.text.contains('нет'))
                    async def process_task_finish(message: types.Message) -> None:
                        try:
                            await add_task_db(tg_id, task_name.split('название:')[1],
                                              description=task_description.split('описание:')[1])
                            await message.answer('Задача с описанием успешно сохранена')
                        except Exception as e:
                            logger.log("error",
                                       f"Произошла ошибка {str(e)} при записе задачу в бд {tg_id}")

                    @router_manage_tasks.message(F.text.contains('хочу'))
                    async def process_coords(message: types.Message) -> None:
                        try:
                            await message.answer(
                                'Если не знаете точных координат, вы можете '
                                'воспользоваться хэндлером <b>/get_image_place</b>',
                                parse_mode=ParseMode.HTML)
                            await message.answer('Запишите координаты на карте по шаблону "место:" ')
                        except Exception as e:
                            logger.log("error",
                                       f"Произошла ошибка {str(e)} при добавление координат {tg_id}")

                        @router_manage_tasks.message(F.text.contains('место:'))
                        async def process_order_db_coords(message: types.Message) -> None:
                            try:
                                coords = message.text
                                await add_task_db(tg_id, task_name.split('название:')[1],
                                                  description=task_description.split('описание:')[1],
                                                  place_on_map=coords.split('место:')[1])
                                await message.answer('Задача с описанием и координатами успешно добавлена')
                            except Exception as e:
                                logger.log("error",
                                           f"Произошла ошибка {str(e)} при добавление координат {tg_id}")

            @router_manage_tasks.message(F.text.contains('закончили'))
            async def add_task_finish(message: types.Message) -> None:
                try:
                    await add_task_db(tg_id, task_name.split('название:')[1])
                    await message.answer('Задача без описания успешно сохранена')
                except Exception as e:
                    logger.log("error",
                               f"Произошла ошибка {str(e)} при записе в бд задачи без описания у пользователя {tg_id}")
    except Exception as e:
        logger.log("error", f"Произошла ошибка в хэндлере /add_task {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')


@router_manage_tasks.message(Command('show_my_tasks'))
@router_manage_tasks.message(F.text.contains('покажи мои задания'))
@router_manage_tasks.message(F.text.contains('мои задания'))
@router_manage_tasks.message(F.text.contains('мои задачи'))
async def show_my_tasks(message: types.Message) -> None:
    '''Асинхронная функция для показа задач с помощью InlineKeyboardBuilder'''
    try:
        tg_id = message.from_user.id
        logger.log("info", f"Пользователь вошёл в хэндлер /show_my_tasks {tg_id}")
        tasks = await show_tasks_db(tg_id)
        if tasks:
            tasks_key_board = InlineKeyboardBuilder()
            for task in tasks:
                tasks_key_board.add(InlineKeyboardButton(text=task.name, callback_data=f'task|{task.id}'))
            kb = tasks_key_board.adjust(2).as_markup()
            await message.answer("Вот ваши задачи", reply_markup=kb)

        else:
            await message.answer("Вы ещё не создавали задачи, обратитесь к хэндлеру /add_task")
    except Exception as e:
        logger.log("error", f"Произошла ошибка в хэндлере /show_my_tasks {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')


@router_manage_tasks.callback_query(F.data.startswith('task|'))
async def get_info_clicked_task(callback: types.CallbackQuery) -> None:
    try:
        task_id = callback.data.split('|')[1]
        query = await get_info_task(task_id)
        task = query[0]
        if task.description and task.place_on_map:
            await callback.answer(f'Описание задачи {task.description} \n'
                                  f'Координаты задачи {task.place_on_map}', cache_time=10)
        else:
            await callback.answer(f'У задачи {task.name} нету описания и координат')
    except Exception as e:
        logger.log("error", f"Произошла ошибка при ответе на нажатия InlineKeyboardBuilder {str(e)}")
        await callback.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
