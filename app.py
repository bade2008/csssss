
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler, JobQueue

# إعدادات البوت
TELEGRAM_API_TOKEN = '7149704860:AAFn8zBMiuPr8PTn1Xqxcccqdw05wipHs6Q'  # استبدل YOUR_TELEGRAM_API_TOKEN بالتوكن الخاص ببوتك
GROUP_CHAT_ID = '-4221027440'  # استبدل YOUR_GROUP_CHAT_ID بالـ chat ID الخاص بالمجموعة
PRODUCT_URLS = [
    
    'https://www.dzrt.com/en/samra.html',
    'https://www.dzrt.com/en/spicy-zest.html',
    'https://www.dzrt.com/en/tamra.html',
    'https://www.dzrt.com/en/highland-berries.html',
    'https://www.dzrt.com/en/purple-mist.html',
    'https://www.dzrt.com/en/icy-rush.html'
      ,
    'https://www.dzrt.com/en/seaside-frost.html'
      ,
    'https://www.dzrt.com/en/edgy-mint.html'
      ,
    'https://www.dzrt.com/en/spicy-zest.html'
      ,
    'https://www.dzrt.com/en/garden-mint.html'

      
      
      
        # رابط المنتج الثاني
    # يمكنك إضافة المزيد من الروابط هنا
]
CHECK_INTERVAL = 60  # بالثواني، للتحقق من توافر المنتجات كل دقيقة

def check_product_availability(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # استخراج حالة توافر المنتج من HTML
    availability_div = soup.find('div', {'class': 'stock available'})
    if availability_div:
        availability_text = availability_div.text.strip()
        return availability_text == 'In stock'
    return False

def notify_user(bot: Bot, product_url, is_available):
    if is_available:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=f'متوفر حاليا \n {product_url} ')
    #else:
        #bot.send_message(chat_id=GROUP_CHAT_ID, text=f'غير متوفر {product_url} is currently not available.')

def start(update, context):
    update.message.reply_text('Bot started! You will be notified about the availability of the products.')
    job_queue = context.job_queue
    job_queue.run_repeating(check_and_notify, interval=CHECK_INTERVAL, first=0)

def check_and_notify(context):
    bot = context.bot
    for product_url in PRODUCT_URLS:
        is_available = check_product_availability(product_url)
        notify_user(bot, product_url, is_available)

def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

