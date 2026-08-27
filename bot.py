import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================================================
# SOZLAMALAR
# =========================================================

TOKEN = "8853682793:AAGuqQaOSu9Ly4KAe2KwmjlMVSgrYLWI0U4"

ALLOWED_USERNAME = "Musilmanchild"
MAX_MESSAGES = 10
DELAY = 1.0

# Har bir chat uchun ishlayotgan test task
running_tasks = {}


# =========================================================
# FOYDALANUVCHINI TEKSHIRISH
# =========================================================

def is_allowed(update: Update) -> bool:
    user = update.effective_user

    if user is None:
        return False

    username = user.username

    return (
        username is not None
        and username.lower() == ALLOWED_USERNAME.lower()
    )


# =========================================================
# /start TEXT
# =========================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_allowed(update):
        await update.message.reply_text(
            "❌ Sizga bu komandadan foydalanishga ruxsat yo‘q."
        )
        return

    chat = update.effective_chat

    if chat is None:
        return

    # Faqat guruhda ishlaydi
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text(
            "❌ Bu bot faqat guruhda ishlaydi."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Matn kiriting.\n\n"
            "Misol:\n"
            "/start ANTI-SPAM TEST"
        )
        return

    text = " ".join(context.args)

    # Eski task bo‘lsa to‘xtatamiz
    old_task = running_tasks.get(chat.id)

    if old_task and not old_task.done():
        old_task.cancel()

    # Yangi testni boshlaymiz
    task = asyncio.create_task(
        spam_test(chat.id, text, context)
    )

    running_tasks[chat.id] = task

    await update.message.reply_text(
        f"🧪 Test boshlandi!\n"
        f"📝 Matn: {text}\n"
        f"🔢 Maksimum: {MAX_MESSAGES} ta\n"
        f"⏱️ Interval: {DELAY} soniya\n\n"
        f"⛔ To‘xtatish: /stop"
    )


# =========================================================
# TEST XABARLARI
# =========================================================

async def spam_test(
    chat_id: int,
    text: str,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        for number in range(1, MAX_MESSAGES + 1):

            # Har safar yuborishdan oldin task bekor qilinganini tekshiramiz
            await asyncio.sleep(DELAY)

            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{text}\n\n🧪 Test #{number}/{MAX_MESSAGES}"
            )

    except asyncio.CancelledError:
        # /stop bosilganda shu yerga keladi
        return

    except Exception as error:
        print("Xatolik:", error)

    finally:
        running_tasks.pop(chat_id, None)


# =========================================================
# /stop
# =========================================================

async def stop_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_allowed(update):
        await update.message.reply_text(
            "❌ Sizga bu komandadan foydalanishga ruxsat yo‘q."
        )
        return

    chat = update.effective_chat

    if chat is None:
        return

    task = running_tasks.get(chat.id)

    if task and not task.done():
        task.cancel()

        await update.message.reply_text(
            "🛑 Test to‘xtatildi."
        )
    else:
        await update.message.reply_text(
            "ℹ️ Hozir ishlayotgan test yo‘q."
        )


# =========================================================
# /status
# =========================================================

async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_allowed(update):
        await update.message.reply_text(
            "❌ Ruxsat yo‘q."
        )
        return

    chat = update.effective_chat

    if chat is None:
        return

    task = running_tasks.get(chat.id)

    if task and not task.done():
        await update.message.reply_text(
            "🟢 Test ishlayapti.\n\n"
            "⛔ To‘xtatish: /stop"
        )
    else:
        await update.message.reply_text(
            "⚪ Test ishlamayapti."
        )


# =========================================================
# BOTNI ISHGA TUSHIRISH
# =========================================================

def main():

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("stop", stop_command)
    )

    application.add_handler(
        CommandHandler("status", status_command)
    )

    print("🤖 Bot ishga tushdi...")
    print(f"👤 Ruxsat berilgan user: @{ALLOWED_USERNAME}")
    print(f"🔢 Maksimum xabar: {MAX_MESSAGES}")

    application.run_polling()


if __name__ == "__main__":
    main()
