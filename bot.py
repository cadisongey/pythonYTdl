import re
import youtube_dl
from pyrogram import Client, filters

api_id = your_api_id
api_hash = 'your_api_hash'

app = Client("my_bot", api_id, api_hash)

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'listformats': True  # Получение списка доступных форматов
}

@app.on_message(filters.private & filters.text)
async def send_youtube_video(client, message):
    chat_id = message.chat.id
    user_input = message.text

    # Проверяем, является ли сообщение ссылкой на YouTube
    youtube_link_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    match = re.match(youtube_link_regex, user_input)

    if match:
        video_id = match.group(6)
        youtube_video_link = f"https://www.youtube.com/watch?v={video_id}"

        # Скачиваем информацию о видео с помощью youtube_dl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_video_link, download=False)

            # Получаем список доступных форматов
            formats = info_dict.get('formats')
            format_list = "\n".join(f"{i['format_id']}: {i['format']} {i.get('format_note', '')}" for i in formats)

            # Отправляем список доступных форматов пользователю
            await client.send_message(chat_id, f"Доступные форматы видео:\n\n{format_list}")

    else:
        await message.reply_text("Это не ссылка на YouTube.")


@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Привет! Пожалуйста, отправь мне ссылку на YouTube видео.")


app.run()