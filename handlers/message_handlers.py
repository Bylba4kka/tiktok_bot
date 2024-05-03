import asyncio
import time

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, URLInputFile

from video_processing.tiktok_no_watermark import DownloadVideoTikTok

router = Router()

# словарь для отслеживания времени отправки сообщений
user_last_message_time = {}

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет, отправь ссылку на видео из тиктока")


# Обработчик ссылки
@router.message(F.text)
async def video_url(message: types.Message, bot: Bot):

    user_id = message.from_user.id

    # Проверяем, было ли предыдущее сообщение от этого пользователя
    if user_id in user_last_message_time:
        last_message_time = user_last_message_time[user_id]
        current_time = time.time()

        # Проверяем, прошло ли 10 секунд с момента отправки предыдущего сообщения
        if current_time - last_message_time < 10:
            await message.reply("Пожалуйста, подождите 10 секунд перед отправкой следующего сообщения.")
            return

    # Обновляем время отправки последнего сообщения от этого пользователя
    user_last_message_time[user_id] = time.time()

    # Проверка подписан ли на канал пользователь
    member = await bot.get_chat_member(-1002031100587, message.chat.id)
    if member.status.name not in ("MEMBER", "ADMINISTRATOR", "CREATOR"):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/autoimportrf")]])
        await message.reply(
            f"Чтобы пользоваться ботом, подпишитесь на канал.\nПосле подписки отправьте ссылку заново.",
            reply_markup=keyboard
        )
        return

    # Проверка сообщения на наличие ссылки
    if not message.text.startswith(("https://vm.tiktok.com/", "https://www.tiktok.com/")):
        await message.answer("Пожалуйста, введите ссылку")
        return
    else:
        try:
            # Получение видео
            video_task = asyncio.create_task(DownloadVideoTikTok(bot, message.text))
            sent_message = await message.answer("Пожалуйста подождите | ⏳")

            # Ожидание завершения функции DownloadVideoTikTok
            while not video_task.done():
                symbols = ['/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|']
                for symbol in symbols:
                    await sent_message.edit_text(f"Пожалуйста подождите {symbol} ⏳")
                await asyncio.sleep(2)

            # Получаем результат выполнения функции DownloadVideoTikTok
            video_result = await video_task

            # Принимаем ссылку
            video = URLInputFile(
                video_result,
                filename=video_result
            )
            # Удаляем сообщение "Пожалуйста подождите"
            await bot.delete_message(message.chat.id, sent_message.message_id)
        # Отправляем видео
            await bot.send_video(message.chat.id, video)
        except:
            await message.answer("Пожалуйста, попробуйте ещё раз")


# Если пользователь прислал что-то то, но не ссылку или текст
@router.message()
async def incorrect_input(message: types.Message):
    await message.answer("Пожалуйста, введите ссылку")


