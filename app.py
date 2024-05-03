import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

from handlers.message_handlers import router


# Подгрузка локальных переменных из .env
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv("TOKEN"), parse_mode=ParseMode.HTML)

dp = Dispatcher()

# Регистрируем обработчик в боте
dp.include_router(router)


async def on_startup():
    print("Bot Started")


async def on_shutdown():
    print("Bot Shutdown")


# Функция запуска бота
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# Точка запуска бота Hello World
if __name__ == "__main__":
    asyncio.run(main())
