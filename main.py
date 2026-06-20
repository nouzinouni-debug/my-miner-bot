import telebot
import subprocess
import os
import requests # سنستخدم هذه المكتبة للتحميل بدلاً من wget

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
miner_process = None

def download_xmrig():
    if not os.path.exists("xmrig"):
        print("📥 جاري تحميل المحرك باستخدام بايثون...")
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz"
        response = requests.get(url)
        with open("xmrig.tar.gz", "wb") as f:
            f.write(response.content)
        subprocess.run(["tar", "-xf", "xmrig.tar.gz"])
        os.rename("xmrig-6.21.0/xmrig", "xmrig")
        print("✅ تم التحميل بنجاح!")

@bot.message_handler(commands=['start', 'mine', 'stop'])
def handle_commands(message):
    global miner_process
    if message.text == '/mine':
        if miner_process is None:
            download_xmrig()
            cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "--tls"]
            miner_process = subprocess.Popen(cmd)
            bot.reply_to(message, "🚀 تم تشغيل المعدن!")
        else:
            bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")
    elif message.text == '/stop':
        if miner_process:
            miner_process.terminate()
            miner_process = None
            bot.reply_to(message, "🛑 تم الإيقاف.")

bot.polling(none_stop=True)

