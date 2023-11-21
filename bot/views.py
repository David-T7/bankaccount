# botapp/views.py
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext 
from .models import TelegramUser
from telegram import Bot

TOKEN = ''
updater = Updater(token=TOKEN, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    update.message.reply_text(f'Welcome! To open a bank account, use /open_account.')

def open_account(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    # Interact with the Telegram bot
    send_open_account_confirmation(update.message.chat_id)

    # Provide a response to the user
    update.message.reply_text(f'Thank you, {user.first_name}, for opening a bank account! Your account is now active.')

def send_open_account_confirmation(chat_id):
    bot = Bot(token=TOKEN)
    confirmation_message = "Your bank account has been successfully opened! Thank you for choosing our services."
    bot.send_message(chat_id=chat_id, text=confirmation_message)

@csrf_exempt
def telegram_webhook(request):
    print("request method is ", request.method)
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str), updater.bot)

        # Dispatch the update to the appropriate handler
        updater.dispatcher.process_update(update)

        return HttpResponse('OK')
    elif request.method == 'GET':
        # Handle GET requests if needed
        return HttpResponse('Telegram Webhook Endpoint')
    else:
        return HttpResponse('Method not allowed', status=405)

# Set the webhook URL using the Bot API
bot = updater.bot
bot.setWebhook(url='https://daveghost123.pythonanywhere.com')

