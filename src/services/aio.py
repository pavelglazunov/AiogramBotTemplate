from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.media_group import MediaGroupBuilder


async def delete_message(bot: Bot, chat_id: int, message_id: int) -> bool:
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )
        return True
    except (TelegramBadRequest, TelegramForbiddenError):
        return False


async def clear_state_with_save_data(state: FSMContext) -> FSMContext:
    data = await state.get_data()
    await state.clear()
    await state.update_data(**data)
    return state


async def send_message(
        bot: Bot,
        chat_id: int,
        content: str,
        rp: InlineKeyboardMarkup = None
) -> bool:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=content,
            reply_markup=rp,
            disable_web_page_preview=True,
        )
        return True
    except (TelegramBadRequest, TelegramForbiddenError):
        return False


async def send_photo(
        bot: Bot,
        photo: str,
        chat_id: int,
        caption: str = "",
        rp: InlineKeyboardMarkup = None
) -> bool:
    try:
        await bot.send_photo(
            photo=photo,
            chat_id=chat_id,
            caption=caption,
            reply_markup=rp,
        )
        return True
    except (TelegramBadRequest, TelegramForbiddenError):
        return False


async def send_photos(
        bot: Bot,
        photos: list[str],
        chat_id: int,
) -> bool:
    try:
        builder = MediaGroupBuilder()

        for photo in photos:
            builder.add_photo(media=photo)

        await bot.send_media_group(
            chat_id=chat_id,
            media=builder.build(),
        )
        return True
    except (TelegramBadRequest, TelegramForbiddenError):
        return False
