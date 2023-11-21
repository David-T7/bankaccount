import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from .models import UserProfile
from telegram import Bot

TOKEN = '6662737355:AAF2gOqlG6ztr9cMWHOtgeu7JQjMKaQqEMQ'
updater = Updater(token=TOKEN, use_context=True)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! To open a bank account, use /upload_id to upload your ID document.')


def upload_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please upload a clear picture of your ID document.')


def upload_signature(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please upload a clear picture of your signature.')


def open_account(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Check if ID document and signature are uploaded
    if user_profile.id_document and user_profile.signature:
        send_open_account_confirmation(update.message.chat_id)
        update.message.reply_text(f'Thank you, {user.first_name}, for opening a bank account! Your account is now active.')
    else:
        update.message.reply_text('Please upload both your ID document and signature using /upload_id and /upload_signature.')


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

        # Log the received update
        print("Received update:")
        print(update)

        try:
            # Dispatch the update to the appropriate handler
            updater.dispatcher.process_update(update)
            print("Update processed successfully")
        except Exception as e:
            # Log any exceptions that occur during update processing
            print(f"Exception during update processing: {e}")

        return HttpResponse('OK')
    elif request.method == 'GET':
        # Handle GET requests if needed
        return HttpResponse('Telegram Webhook Endpoint')
    else:
        return HttpResponse('Method not allowed', status=405)


# Set the webhook URL using the Bot API
bot = updater.bot
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("upload_id", upload_id))
updater.dispatcher.add_handler(CommandHandler("upload_signature", upload_signature))
updater.dispatcher.add_handler(CommandHandler("open_account", open_account))
bot.setWebhook(url='https://daveghost123.pythonanywhere.com')
