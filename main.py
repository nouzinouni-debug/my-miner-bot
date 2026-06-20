import telebot
import subprocess
import os
import threading

TOKEN = os.environ.get('BOT_TOKEN') # سنضع التوكن في إعدادات Railway
bot = telebot.TeleBot(TOKEN)
miner_process = None

def download_xmrig():
    if not os.path.exists("xmrig"):
        print("📥 جاري تحميل المحرك...")
        subprocess.run(["wget", "-q", "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz"])
        subprocess.run(["tar", "-xf", "xmrig-6.21.0-linux-x64.tar.gz"])
        subprocess.run(["mv", "xmrig-6.21.0/xmrig", "."])
        print("✅ تم التحميل!")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! أنا جاهز. استعمل /mine للبدء.")

@bot.message_handler(commands=['mine'])
def mine(message):
    global miner_process
    if miner_process is None:
        download_xmrig()
        # هنا أمر التعدين (تعديل المحفظة والمنفذ)
        cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "-a", "rx", "-p", "x", "--tls"]
        miner_process = subprocess.Popen(cmd)
        bot.reply_to(message, "🚀 تم تشغيل المعدن على السيرفر!")
    else:
        bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")

@bot.message_handler(commands=['stop'])
def stop(message):
    global miner_process
    if miner_process:
        miner_process.terminate()
        miner_process = None
        bot.reply_to(message, "🛑 تم إيقاف التعدين.")
    else:
        bot.reply_to(message, "المعدن متوقف.")

if __name__ == "__main__":
    print("🤖 البوت يعمل الآن...")
    bot.polling()
  
