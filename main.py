import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from yt_dlp import YoutubeDL

# 1. BOT TOKENI VA INSTAGRAM PROFILE HAVOLASINI SHU YERGA YOZING:
BOT_TOKEN = "8688025512:AAE_lovqJa7GfTdXcVnORzxfsRjF1S_aCrE"
INSTA_URL = "https://www.instagram.com/wr4_vortex?stkn=bjJ2a2RrOGxsYjgz"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Asosiy menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="hidestory"), KeyboardButton(text="tgkanal")],
        [KeyboardButton(text="🎵 Qoshiq qidirish")]
    ],
    resize_keyboard=True
)

# Start bosilganda chiqadigan inline tugmalar
def get_sub_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Instagram profil", url=INSTA_URL)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ]
    )

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_name = message.from_user.full_name
    await message.answer(
        f"Salom {user_name}! Botdan foydalanish uchun Instagram sahifamizga obuna bo'ling va Tekshirish tugmasini bosing:",
        reply_markup=get_sub_keyboard()
    )

# "Tekshirish" tugmasi bosilganda
@dp.callback_query(F.data == "check_sub")
async def check_subscription(call: types.CallbackQuery):
    user_name = call.from_user.full_name
    
    await call.message.delete()
    await call.message.answer(
        f"Muvaffaqiyatli qo'shildingiz! {user_name}, botimizga xush kelibsiz!",
        reply_markup=main_menu
    )

# Instagram Video Yuklash mantiqi
@dp.message(F.text.contains("instagram.com"))
async def download_insta_video(message: types.Message):
    msg = await message.answer("Video yuklanmoqda, kuting...")
    url = message.text.strip()
    file_name = f"video_{message.from_user.id}.mp4"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_name,
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        video = types.FSInputFile(file_name)
        await message.answer_video(video=video, caption="Mana sizning videongiz!")
        await msg.delete()
        
        # Yuklab bo'lingach faylni kompyuterdan o'chirib tashlaydi
        if os.path.exists(file_name):
            os.remove(file_name)
            
    except Exception as e:
        await msg.edit_text("Videoni yuklab bo'lmadi. Havola to'g'riligini tekshiring.")
        if os.path.exists(file_name):
            os.remove(file_name)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())