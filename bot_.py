import discord
import os
import youtube_dl
from discord.ext import commands
from youtube_dl import YoutubeDL
from asyncio import sleep

bot = commands.Bot(command_prefix='!')
token = 'Тут токен'
play_list = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'save/%(title)s.%(etx)s',
    'quiet': False,
    'ffmpeg_location': 'bin'
}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.event
async def on_ready():
    # for i in [20, 45, 70, 99, 10, 99, 100]:
    #     if i == 99:
    #         print(f'{i}%...')
    #         time.sleep(5)
    #     else:
    #         print(f'{i}%...')
    #     time.sleep(1)

    print(bot.user.name)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


'''
------------------------------------------------------------------------------------------------------------------------
'''


#  воспроизводит файлы и аудио по URL ссылки с youtube.com, а также это всё в одном плей листе
@bot.command(pass_context=True)
async def play(ctx, arg='None'):
    global play_list
    global vc

    # Подключаем бота к голосовому каналу
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен')

    if arg.startswith('https'):  # Проверяем это файл или URL. Если URL, то делаем протокол для Youtube
        if len(play_list) == 0:  # Чтоб пользователь не волновался на счет задержки
            await ctx.send('Подождите 5 секунд :)')
        with YoutubeDL(YDL_OPTIONS) as ydl:  # Это всё для добавления имени файла в лей лист
            info = ydl.extract_info(arg, download=False)
        play_list.append(info['title'] + '.mp3')  # Само добавление

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([arg])  # Скачивание этого файла
    else:  # Протокол для файлов
        for attach in ctx.message.attachments:
            play_list.append(attach.filename)  # Добавляем имя файла в плейлист
            await attach.save(f"save/{attach.filename}")  # Сохроняем файл на жосткий диск
            print('файл сохранён и добавлен в лей лист')

    try:
        while play_list:
            vc.play(discord.FFmpegPCMAudio(f"save/{play_list[0]}", executable="bin\\ffmpeg.exe"))  # Воспроизводим файл
            while vc.is_playing():  # Ждём пока до играет
                await sleep(1)
            os.remove(f"save/{play_list[0]}")
            play_list.pop(0)
            print('файл удалён')  # Зачищаем файл и его имя в списке
    except:
        pass


# Очищает плей лист
@bot.command(pass_context=True)
async def stop():
    global play_list

    while play_list:
        await skip()
        os.remove(f"save/{play_list[0]}")
        play_list.pop(0)
        await skip()


@bot.command(pass_context=True)
async def pause():
    pass


@bot.command(pass_context=True)
async def unpause():
    pass


# пропуск текущей песни
@bot.command(pass_context=True)
async def skip(self, ctx):
    global vc

    if not vc.is_playing():
        await self.bot.say('Музыка не проигрывается')
        return
    state = self.get_voice_state(ctx.message.server)
    state.skip()


bot.run(token)
