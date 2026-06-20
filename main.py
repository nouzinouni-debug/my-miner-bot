import telebot
import subprocess
import os
import requests
#from flask import Flask
from threading import Thread

# 1. إعداد خادم الويب الوهمي ليبقى السيرفر مستيقظاً 24/7
#app = Flask('')
#@app.route('/')
#def home():
#    return "السيرفر يعمل بكامل طاقته!"

#ef run_web():
    #app.run(host='0.0.0.0', port=8080)

# 2. إعداد البوت
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
miner_process = None

def download_xmrig():
    if not os.path.exists("xmrig"):
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz"
        r = requests.get(url)
        with open("xmrig.tar.gz", "wb") as f:
            f.write(r.content)
        subprocess.run(["tar", "-xf", "xmrig.tar.gz"])
        if os.path.exists("xmrig-6.21.0/xmrig"):
            os.rename("xmrig-6.21.0/xmrig", "xmrig")
            os.chmod("xmrig", 0o755)

@bot.message_handler(commands=['mine'])
def mine(message):
    global miner_process
    if miner_process is None or miner_process.poll() is not None:
        download_xmrig()
        # إضافة خيار الاستقرار للمعدن
        cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "--cpu-max-threads-hint=50", "--tls"]
        miner_process = subprocess.Popen(cmd)
        bot.reply_to(message, "✅ تم تشغيل التعدين!")
    else:
        bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")

@bot.message_handler(commands=['stop'])
def stop(message):
    global miner_process
    if miner_process:
        miner_process.terminate()
        miner_process = None
        bot.reply_to(message, "🛑 تم الإيقاف.")

# 3. تشغيل الويب والبوت معاً
if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.polling(none_stop=True)
