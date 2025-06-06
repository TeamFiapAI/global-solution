import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "7600230979:AAGBmyIqjE7UaLb09MRt3UW4IRGZ2oZhGeA"
usuarios_alerta = {127926134}

app_telegram = None  # manter referência global

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Use /receber_alertas para se inscrever nos alertas de enchente.")

async def receber_alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    usuarios_alerta.add(chat_id)
    await update.message.reply_text("✅ Você está inscrito para receber alertas de enchente!")

async def enviar_alerta_para_todos(mensagem: str):
    bot = Bot(token=TELEGRAM_TOKEN)
    for chat_id in usuarios_alerta:
        await bot.send_message(chat_id=chat_id, text=mensagem)

def notificar_todos(mensagem: str):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(enviar_alerta_para_todos(mensagem))
    except RuntimeError:
        asyncio.run(enviar_alerta_para_todos(mensagem))

async def iniciar_bot_async():
    global app_telegram
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("receber_alertas", receber_alertas))

    await app_telegram.initialize()
    await app_telegram.start()
    print("🤖 Bot Telegram iniciado com sucesso!")

def iniciar_bot():
    import asyncio
    asyncio.create_task(iniciar_bot_async())
