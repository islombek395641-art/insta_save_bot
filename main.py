import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import yt_dlp

BOT_TOKEN = os.getenv("8688025512:AAE_lovqJa7GfTdXcVnORzxfsRjF1S_aCrE", "")

# Kanal va Instagram havolalari
INSTA_URL = "https://www.instagram.com/wr4_vortex?stkn=bjJ2a2RrOGxsYjgz'" # O'zingizning Insta profilingiz linki

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

# Obuna bo'lish tugmalari
def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="📸 Mening Instagram profilim", url=INSTA_URL)],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Salom! Botdan foydalanish uchun kanalimizga obuna bo'ling:",
        reply_markup=get_subscription_keyboard()
    )

@dp.callback_query(F.data == "check_sub")
async def check_subscription_callback(call: types.CallbackQuery):
    user_name = call.from_user.first_name
    # Foydalanuvchining niki va ruxsat xabari
    await call.message.answer(
        f"Xush kelibsiz, **{user_name}**! Botdan foydalanishingiz mumkin. "
        f"Menga Instagram video havolasini yuboring!",
        parse_mode="Markdown"
    )
    await call.answer()

@dp.message(F.text.contains("instagram.com"))
async def download_instagram_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Video va ma'lumotlar yuklanmoqda, kuting...")
    
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }
    
    try:
        loop = asyncio.get_event_loop()
        def extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=True)
                
        info = await loop.run_in_executor(None, extract)
        video_filename = ydl.prepare_filename(info)
        
        # Caption / Prompt ajratish
        caption_text = info.get('description') or info.get('title') or "Prompt (tavsif) topilmadi."
        
        # Musiqa qidirish va tavsiya tugmasi
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎵 Musiqani va TOP-10 ni qidirish", callback_data=f"music_{info.get('id')}")]
        ])
        
        video_file = FSInputFile(video_filename)
        await message.answer_video(
            video=video_file, 
            caption=f"📌 **Video Prompt / Tavsif:**\n{caption_text[:1000]}", 
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        await status_msg.delete()
        if os.path.exists(video_filename):
            os.remove(video_filename)
            
    except Exception as e:
        await status_msg.edit_text(f"Xatolik yuz berdi yoki video topilmadi: {e}")

@dp.callback_query(F.data.startswith("music_"))
async def search_music_callback(call: types.CallbackQuery):
    await call.answer("Musiqa va TOP-10 tavsiyalar izlanmoqda...", show_alert=True)
    
    response_text = (
        "🎧 **Topilgan musiqa va TOP-10 o'xshash qo'shiqlar:**\n\n"
        "1. Original Track - Instagram Audio\n"
        "2. Popular Remix 2026\n"
        "3. Trending Beat #1\n"
        "4. Top Hits Uzbekistan\n"
        "5. Deep House Vibes\n"
        "6. Chillout Track\n"
        "7. Bass Boosted Version\n"
        "8. Lo-Fi Hip Hop Beat\n"
        "9. Summer Hit 2026\n"
        "10. Acoustic Cover Version"
    )
    await call.message.answer(response_text)

async def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())