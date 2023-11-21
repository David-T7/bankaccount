# views.py
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from .models import UserProfile , TelegramUser
from telegram import Bot
from telegram import InputFile

TOKEN = ''
updater = Updater(token=TOKEN, use_context=True)


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    if not created:
        update.message.reply_text('Welcome! To open a bank account, use /upload_id to upload your ID document.')
    else:
        update.message.reply_text('Welcome! To register , use /open_account .')


def upload_id(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    print("in uploadid",user)
    # user_profile, created = UserProfile.objects.get_or_create(user=user)
    # print("profile created")
    # # Check if an ID document is already uploaded
    # if created:
    #     update.message.reply_text('ID document already uploaded!')
    # else:
    #     print("trying to upload")
    #     # Save the file to the UserProfile model
    #     user_profile.id_document = InputFile()
    #     user_profile.save()
    update.message.reply_text('ID document uploaded successfully. Now, use /upload_signature to upload your signature.')

def upload_signature(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Check if an ID document is already uploaded
    if not created:
        update.message.reply_text('ID document already uploaded!')
    else:
        # Save the file to the UserProfile model
        user_profile.signature = InputFile()
        user_profile.save()
        update.message.reply_text('Signature document uploaded successfully. Now, you have completed registeration!')



def open_account(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    # Provide a response to the user
    update.message.reply_text(f'Thank you, {user.first_name}, for opening a bank account! Your account is now active.use /upload_id to upload your ID document.')



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
