import telebot
import subprocess
import os
import threading
import requests
import tarfile

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
miner_process = None

def download_and_run():
    global miner_process
    # 1. تحميل الملف
    if not os.path.exists("xmrig"):
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz"
        r = requests.get(url)
        with open("miner.tar.gz", "wb") as f:
            f.write(r.content)
        # 2. فك الضغط
        with tarfile.open("miner.tar.gz", "r:gz") as tar:
            tar.extractall()
        # 3. إعادة تسمية المجلد للوصول للملف
        os.rename("xmrig-6.21.0/xmrig", "xmrig")

    # 4. تشغيل المعدن
    cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "-p", "x", "--tls"]
    miner_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

@bot.message_handler(commands=['mine'])
def start_mine(message):
    global miner_process
    if miner_process is None:
        bot.reply_to(message, "🚀 جاري التحميل والتشغيل...")
        threading.Thread(target=download_and_run).start()
        # مراقبة الحالة
        threading.Thread(target=lambda: [bot.send_message(message.chat.id, f"📊 {line.strip()}") for line in miner_process.stdout if "accepted" in line or "speed" in line], daemon=True).start()
    else:
        bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")

@bot.message_handler(commands=['stop'])
def stop_mine(message):
    global miner_process
    if miner_process:
        miner_process.terminate()
        miner_process = None
        bot.reply_to(message, "🛑 تم الإيقاف.")

bot.polling(none_stop=True)
