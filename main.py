import discord
import telegram
import os

# Discord client setup
discord_token = 'YOUR_DISCORD_TOKEN_HERE'

client = discord.Client()

@client.event
async def on_ready():
    print('Discord client is ready.')

# Telegram bot setup
def message_handler(update, context):
    discord_bot_token = os.environ['DISCORD_BOT_TOKEN']
    discord_channel_id = os.environ['DISCORD_CHANNEL_ID']

    discord_bot = discord.Client()

    @discord_bot.event
    async def on_ready():
        channel = discord_bot.get_channel(discord_channel_id)
        try:
            telegram_bot = telegram.Bot(token=telegram_bot_token)
            telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

            message_text = update.message.text

            discord_message = f"New message from {telegram_chat_id}:\n{message_text}"

            for photo in update.message.photo:
                photo_file = telegram_bot.getFile(photo.file_id)
                photo_file_path = photo_file.file_path
                photo_path = f"https://api.telegram.org/file/bot{telegram_bot_token}/{photo_file_path}"
                await channel.send(f"{discord_message}\n{photo_path}")
            else:
                await channel.send(discord_message)

            print('Telegram message sent to Discord.')
        except Exception as e:
            print(f'Error sending Telegram message to Discord: {e}')

if __name__ == '__main__':
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = telegram.ext.Updater(token=telegram_bot_token, use_context=True)

    dispatcher = updater.dispatcher

    message_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text | telegram.ext.Filters.photo, message_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
