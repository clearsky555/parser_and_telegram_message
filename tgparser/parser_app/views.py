from django.shortcuts import render, redirect
from telegram import Bot
import asyncio

from parser_app.models import Houses, User
from parser_app.parser_house import main
from .forms import TelegramIdForm
from .tasks import order_created


async def send_telegram_message_1(user):
    bot_token = '6656574560:AAG9X4WIDjNuPpjkCdst0y-YmPpTzkKbVgQ'  # Вставьте свой токен бота
    bot = Bot(token=bot_token)
    chat_id = user  # chat_id пользователя, куда нужно отправить сообщение
    message = "парсинг начался... ожидайте результатов" # Замените на свое сообщение
    await bot.send_message(chat_id=chat_id, text=message)


async def send_telegram_message_2(user):
    bot_token = '6656574560:AAG9X4WIDjNuPpjkCdst0y-YmPpTzkKbVgQ'  # Вставьте свой токен бота
    bot = Bot(token=bot_token)
    chat_id = user  # chat_id пользователя, куда нужно отправить сообщение
    message = "ваши результаты готовы!" # Замените на свое сообщение
    await bot.send_message(chat_id=chat_id, text=message)


def welcome(request):
    return render(request, 'base.html')


def p_results(request, user):
    order_created.delay()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_telegram_message_1(user))

    main()  # Получить данные из функции парсинга

    data = Houses.objects.all()

    context = {
        'parsed_data': data,  # Передать данные в шаблон
    }

    loop.run_until_complete(send_telegram_message_2(user))

    return render(request, 'p_results.html', context)


def get_tg(request):
    success_message = None
    if request.method == 'POST':
        form = TelegramIdForm(request.POST)
        if form.is_valid():
            telegram_id = form.cleaned_data['telegram_id']
            # Сохраняем пользователя в базе данных
            user = User(telegram=telegram_id)
            user.save()
            # success_message = "Пользователь успешно сохранен."
            return redirect('results', user=telegram_id)  # Перенаправляем на другой маршрут с передачей данных
    else:
        form = TelegramIdForm()

    return render(request, 'telegram_form.html', {'form': form, 'success_message': success_message})