import requests
from bs4 import BeautifulSoup
import telebot
import time
from threading import Thread

# إعدادات البوت
TELEGRAM_API_TOKEN = '7149704860:AAFn8zBMiuPr8PTn1Xqxcccqdw05wipHs6Q'  # استبدل YOUR_TELEGRAM_API_TOKEN بالتوكن الخاص ببوتك
GROUP_CHAT_ID = '-4221027440'  # استبدل YOUR_GROUP_CHAT_ID بالـ chat ID الخاص بالمجموعة
PRODUCT_URLS = [
    'https://www.dzrt.com/ar/samra.html',
    'https://www.dzrt.com/ar/spicy-zest.html',
    'https://www.dzrt.com/ar/tamra.html',
    'https://www.dzrt.com/ar/highland-berries.html',
    'https://www.dzrt.com/ar/purple-mist.html',
    'https://www.dzrt.com/ar/icy-rush.html',
    'https://www.dzrt.com/ar/seaside-frost.html',
    'https://www.dzrt.com/ar/edgy-mint.html',
    'https://www.dzrt.com/ar/spicy-zest.html',
    'https://www.dzrt.com/ar/garden-mint.html'
]
CHECK_INTERVAL = 60  # بالثواني، للتحقق من توافر المنتجات كل دقيقة

# إنشاء البوت
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

def check_product_availability(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # استخراج حالة توافر المنتج من HTML
    availability_div = soup.find('div', {'class': 'stock available'})
    if availability_div:
        availability_text = availability_div.text.strip()
        return availability_text == 'In stock'
    return False

def notify_user(product_url, is_available):
    if is_available:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=f'متوفر حاليا \n {product_url} ')

def check_and_notify():
    while True:
        for product_url in PRODUCT_URLS:
            is_available = check_product_availability(product_url)
            notify_user(product_url, is_available)
        time.sleep(CHECK_INTERVAL)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Bot started! You will be notified about the availability of the products.')
    thread = Thread(target=check_and_notify)
    thread.start()

def main():
    bot.polling()

if __name__ == '__main__':
    main()
