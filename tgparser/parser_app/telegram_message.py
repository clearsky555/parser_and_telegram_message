from telegram import Bot
import asyncio

# ЭТО ТЕСТ
async def send_telegram_message(user):
    bot_token = '6656574560:AAG9X4WIDjNuPpjkCdst0y-YmPpTzkKbVgQ'  # Вставьте свой токен бота
    bot = Bot(token=bot_token)
    chat_id = user  # chat_id пользователя, куда нужно отправить сообщение
    message = "Ваши результаты парсинга готовы" # Замените на свое сообщение
    await bot.send_message(chat_id=chat_id, text=message)


def send(user):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_telegram_message(user))
    return True


send(5782005645)