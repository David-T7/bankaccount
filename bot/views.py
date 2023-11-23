# views.py
import json
# views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from .models import UserProfile, TelegramUser
from telegram import InputFile
from django.core.files.base import ContentFile , File
from django.conf import settings



TOKEN = ''
updater = Updater(token=TOKEN, use_context=True)
bot = updater.bot

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    if not created:
        update.message.reply_text('Welcome! To open a bank account, use /upload_id to upload your ID document and Choose the document option and select the file with a clear image of your ID.')
    else:
        update.message.reply_text('Welcome! To register, use /open_account.')


def upload_id(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    # Create or get UserProfile associated with the TelegramUser
    user_profile, created = UserProfile.objects.get_or_create(user=telegram_user)
    print(update)
    # Check if an ID document is already uploaded
    # Handle the uploaded file
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_name = f"{user.first_name}_id"
        relative_path = f'id_documents/{file_name}.png'
        file_path = bot.getFile(file_id).download(custom_path=settings.MEDIA_ROOT / relative_path)
        print("file is " , file_path)
        # image =  file_path.download(custom_path = custom_path)
    # Save the file to the UserProfile model
        user_profile.id_document.save(relative_path, File(open(file_path, 'rb')))
        user_profile.save()
        update.message.reply_text('ID document uploaded successfully. Now, use /upload_signature to upload your signature and Choose the document option and select the file with a clear image of your Signature.')
        updater.handler.callback = upload_signature
    else:
        update.message.reply_text('Please upload a clear picture of your ID document. You can do this by sending a document file. '
                                  'Choose the document option and select the file with a clear image of your ID.')


def upload_signature(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    # Create or get UserProfile associated with the TelegramUser
    user_profile, created = UserProfile.objects.get_or_create(user=telegram_user)
    print("profile created")

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_name = f"{user.first_name}_signature"
        relative_path = f'signatures/{file_name}.png'
        file_path = bot.getFile(file_id).download(custom_path=settings.MEDIA_ROOT / relative_path)
        print("file is " , file_path)
    # Save the file to the UserProfile model
        user_profile.signature.save(relative_path, File(open(file_path, 'rb')))
        user_profile.save()

        update.message.reply_text('Signature document uploaded successfully. Now you will receive payment soon!')
        updater.handler.callback = upload_id
    else:
        update.message.reply_text('Please upload a clear picture of your Signature document. You can do this by sending a document file. '
                                  'Choose the document option and select the file with a clear image of your Signature.')


def open_account(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user.id,
        defaults={'first_name': user.first_name, 'last_name': user.last_name}
    )

    # Provide a response to the user
    update.message.reply_text(f'Thank you, {user.first_name}, for opening a bank account! Your account is now active.use /upload_id to upload your ID document.')


def is_upload_id_command(update: Update) -> bool:
    return update.message.text and '/upload_id' in update.message.text


def is_upload_signature_command(update: Update) -> bool:
    return update.message.text and '/upload_signature' in update.message.text


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
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.handler = MessageHandler(Filters.photo, upload_id)
updater.dispatcher.add_handler(updater.handler)
updater.dispatcher.add_handler(CommandHandler("open_account", open_account))
bot.setWebhook(url='https://daveghost123.pythonanywhere.com')

