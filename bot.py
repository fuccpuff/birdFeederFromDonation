import os
import logging
import paramiko
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
PAYMENT_PROVIDER_TOKEN = "YOUR_PAYMENT_PROVIDER_TOKEN"  # For example, Stripe or other payment providers supported by Telegram.

# Add these constants at the beginning of your file
RASPBERRY_PI_IP = "YOUR_RASPBERRY_PI_IP"
RASPBERRY_PI_USERNAME = "YOUR_RASPBERRY_PI_USERNAME"
RASPBERRY_PI_PASSWORD = "YOUR_RASPBERRY_PI_PASSWORD"
BIRD_FEEDER_SCRIPT = "/path/to/bird_feeder.py"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


### Keep in mind that exchange rates fluctuate, so you may want to update the price periodically based on current exchange rates. If you need to convert between currencies programmatically, you can use an API like Open Exchange Rates (https://openexchangerates.org/) to fetch the latest exchange rates.
### Replace YOUR_OPEN_EXCHANGE_RATES_API_KEY with your Open Exchange Rates API key. You can use the get_exchange_rate function to convert between currencies and update the price in your bot accordingly.


def get_exchange_rate(base_currency, target_currency):
    api_key = "YOUR_OPEN_EXCHANGE_RATES_API_KEY"
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}&symbols={target_currency}"
    response = requests.get(url)
    data = response.json()
    
    if target_currency in data["rates"]:
        return data["rates"][target_currency]
    else:
        raise ValueError("Invalid currency provided")

# Example usage:
usd_to_rub = get_exchange_rate("USD", "RUB")
print("1 USD =", usd_to_rub, "RUB")

def start(update: Update, context: CallbackContext):
    """Send a welcome message with inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("Donate & Feed Birds", callback_data="donate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the Bird Feeder! Press the button below to donate and feed the birds.", reply_markup=reply_markup)

def donate_callback(update: Update, context: CallbackContext):
    """Handle donate button press."""
    chat_id = update.effective_chat.id
    title = "Bird Feeding Donation"
    description = "Your donation will help feed the birds in the park."
    payload = "Custom-Payload"  # You can use this field to store user-specific information.
    provider_token = PAYMENT_PROVIDER_TOKEN
    start_parameter = "bird-feeder-donation"
    currency = "RUB"
    prices = [{"label": "Bird Feeding", "amount": 50000}]  # 500 RUB

    # currency = "USD"
    # prices = [{"label": "Bird Feeding", "amount": 500}]  # 5 USD

    context.bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices)

def precheckout_callback(update: Update, context: CallbackContext):
    """Handle pre-checkout query."""
    query = update.pre_checkout_query
    context.bot.answer_pre_checkout_query(query.id, ok=True)

def successful_payment_callback(update: Update, context: CallbackContext):
    """Handle successful payment."""
    update.message.reply_text("Thank you for your donation! The birds will be fed shortly.")
    trigger_bird_feeder()


# Add this function to your code
def trigger_bird_feeder():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RASPBERRY_PI_IP, username=RASPBERRY_PI_USERNAME, password=RASPBERRY_PI_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(f"python3 {BIRD_FEEDER_SCRIPT}")
    ssh.close()

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(donate_callback, pattern="^donate$"))
    dp.add_handler(precheckout_callback)
    dp.add_handler(successful_payment_callback)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
