import telebot
import subprocess
import os
import threading
import time

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
miner_process = None

def monitor_logs(message_chat_id):
    """هذه الدالة تراقب السجلات وترسلها لكِ فوراً"""
    global miner_process
    if miner_process:
        for line in iter(miner_process.stdout.readline, b''):
            log_line = line.decode('utf-8')
            # سنرسل لكِ فقط السطور المهمة (التي تحتوي على accepted أو error)
            if "accepted" in log_line or "error" in log_line or "speed" in log_line:
                bot.send_message(message_chat_id, f"📊 الحالة: {log_line.strip()}")

@bot.message_handler(commands=['mine'])
def start_mine(message):
    global miner_process
    if miner_process is None:
        cmd = ["./xmrig", "-o", "rx.unmineable.com:443", "-u", "DOGE:DTmnad5xggQy4ugfDQqX7vwBQaeZq7RyAz.Nouzzy_Railway", "-a", "rx", "--tls"]
        # نستخدم stdout=subprocess.PIPE لنتمكن من قراءة ما يحدث
        miner_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        bot.reply_to(message, "🚀 تم تشغيل المعدن! سأوافيكِ بكل التفاصيل الآن...")
        
        # تشغيل المراقب في خلفية (Thread) حتى لا يتوقف البوت
        threading.Thread(target=monitor_logs, args=(message.chat.id,), daemon=True).start()
    else:
        bot.reply_to(message, "⚠️ المعدن يعمل بالفعل.")

@bot.message_handler(commands=['stop'])
def stop_mine(message):
    global miner_process
    if miner_process:
        miner_process.terminate()
        miner_process = None
        bot.reply_to(message, "🛑 تم إيقاف التعدين تماماً.")
    else:
        bot.reply_to(message, "المعدن متوقف أصلاً.")

bot.polling(none_stop=True)
