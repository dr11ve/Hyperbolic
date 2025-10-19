import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Telegram bot
TOKEN = 'Input_TG_Token'

# Set up Hyperbolic AI API
API_ENDPOINT = 'https://api.hyperbolic.com/v1/answer'  # Replace with your actual API endpoint
API_KEY = 'Input_YOUR_Actual_HB_API'  # Replace with your actual API key

# Define a function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    response = send_question_to_api(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Define a function to send a question to the Hyperbolic AI API
def send_question_to_api(question):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    data = {'question': question}
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    print(response.content)
    try:
        return response.json()['answer']
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return "Error: Unable to decode JSON response"

# Define a function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I\'m Hyperbol_bot. What\'s on your mind?')

# Define a function to handle the /help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I can help you with answering questions. Try typing something, and I\'ll respond!')

# Set up the Telegram bot
application = ApplicationBuilder().token(TOKEN).build()

# Add handlers for the /start and /help commands
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help))
application.add_handler(MessageHandler(None, handle_message))

# Run the bot
application.run_polling()
