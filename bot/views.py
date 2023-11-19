# botapp/views.py
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext 
from .models import TelegramUser
from telegram import Bot
TOKEN = '6662737355:AAF2gOqlG6ztr9cMWHOtgeu7JQjMKaQqEMQ'
#updater = Updater(myBot)

updater = Updater(token=TOKEN, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name}
    )

    update.message.reply_text(f'Welcome! To open a bank account, use /open_account.')

def open_account(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    update.message.reply_text(f'Thank you for opening a bank account! User ID: {user_id}')

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str), updater.bot)

        # Dispatch the update to the appropriate handler
        updater.dispatcher.process_update(update)

        return HttpResponse('OK')
    else:
        return HttpResponse('Method not allowed', status=405)

# Set the webhook URL using the Bot API
bot = updater.bot
#bot.setWebhook(url='http://127.0.0.1:8000/bot/webhook/')

