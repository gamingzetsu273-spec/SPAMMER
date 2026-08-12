import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Siz bergan API Token
TOKEN = "8853682793:AAGuqQaOSu9Ly4KAe2KwmjlMVSgrYLWI0U4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("spam"))
async def start_spam(message: types.Message):
    args = message.text.split(maxsplit=1)
    
    # Standart matn (agar matn kiritilmasa)
    default_text = "Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N"
    
    text = args[1] if len(args) > 1 else default_text
    
    await message.answer("🚀 Xabarlar soniyasiga 5 tadan yuborila boshlandi...")

    # To'xtatish uchun cheksiz yoki belgilangan miqdor (masalan, 50 ta)
    for _ in range(50):
        try:
            await message.answer(text)
            # Soniyasiga 5 ta xabar (1 / 5 = 0.2 sekund)
            await asyncio.sleep(0.2)
        except Exception as e:
            logging.error(f"Xatolik: {e}")
            break

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())