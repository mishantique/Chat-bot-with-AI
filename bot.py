import asyncio
from aiogram import Bot, Dispatcher

from data.own_token import token
from handlers import bot_messages, user_commands, registration, authorization, order_auto, status_auto, order_house, status_house, history, admin, registration_insurer, authorization_insurer, orders_insurer

from config_reader import config

async def main():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        registration.router,
        registration_insurer.router,
        authorization.router,
        authorization_insurer.router,
        order_auto.router,
        order_house.router,
        admin.router,
        history.router,
        status_house.router,
        status_auto.router,
        orders_insurer.router,
        bot_messages.router
    )
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())