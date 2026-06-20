import telebot
import subprocess
import os
import requests

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
miner_process = None

def download_xmrig():
    if not os.path.exists("xmrig"):
        print("📥 جاري التحميل...")
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz"
        r = requests.get(url)
        with open("xmrig.tar.gz", "wb") as f:
            f.write(r.content)
        subprocess.run(["tar", "-xf", "xmrig.tar.gz"])
        # تأكدي أن المسار هو ما يخرج من ملف الـ tar بالضبط
        if os.path.exists("xmrig-6.21.0/xmrig"):
            os.rename("xmrig-6.21.0/xmrig", "xmrig")
            # إعطاء صلاحية التشغيل للملف
            os.chmod("xmrig", 0o755)

@bot.message_handler(commands=['mine'])
def mine(message):
    global miner_process
    if miner_process is None:
        bot.reply_to(message, "🚀 جاري التحضير...")
        download_xmrig()
        # إضافة --donate-level=1 لضمان استقرار xmrig
        cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "--donate-level=1", "--tls"]
        miner_process = subprocess.Popen(cmd)
        bot.reply_to(message, "✅ المعدن يعمل الآن!")
    else:
        bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")

bot.polling(none_stop=True)
