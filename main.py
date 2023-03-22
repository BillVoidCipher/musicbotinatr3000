import discord
import os
import time
import youtube_dl
from discord.ext import commands
from youtube_dl import YoutubeDL
from asyncio import sleep
from pytube import Playlist
from youtubesearchpython import VideosSearch

bot = commands.Bot(command_prefix='-')
token = 'Nzg0ODU1OTE2NDI4MjYzNDc0.X8vYCA.QPNHuitNyzTWAFxBXaA7fXskrjE'
play_list = []

# YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
YDL_OPTIONS = {'format': 'worstaudio/best',
               'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3',
               'key': 'FFmpegExtractAudio'}
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
zero = 'None'
vc = None


@bot.event
async def on_ready():
    game = discord.Game("-Help")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(bot.user.name)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


@bot.command(pass_context=True)
async def _play_1():
    global vc
    global play_list
    global audio

    if len(play_list) != 0:
        while vc.is_playing():  # Ждём пока до играет
            await sleep(1)
        audio = vc.play(discord.FFmpegPCMAudio(executable="bin\\ffmpeg.exe", source=play_list[0], **FFMPEG_OPTIONS))
        play_list.pop(0)
        while vc.is_playing() or vc.is_paused():  # Ждём пока до играет
            await sleep(1)


@bot.command(pass_context=True)
async def p(ctx, *args):
    global play_list
    global vc
    global zero

    # Подключаем бота к голосовому каналу
    if vc:
        print('Уже подключен')
    else:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        print('connect')
    try:
        if args[0].startswith(
                'https://www.youtube.com/watch?v='):  # Проверяем это файл или URL. Если URL, то делаем протокол для Youtube
            with YoutubeDL(YDL_OPTIONS) as ydl:  # Это всё для добавления имени файла в лей лист
                info = ydl.extract_info(args[0], download=False)
            URL = info['formats'][0]['url']
            play_list.append(URL)
        elif args[0].startswith('https://www.youtube.com/playlist?list='):
            playlist = Playlist(args[0])
            await ctx.send(f'Песен было добавлено:{len(playlist.video_urls)}')
            for video_url in playlist.video_urls:
                with YoutubeDL(YDL_OPTIONS) as ydl:  # Это всё для добавления имени файла в лей лист
                    info = ydl.extract_info(video_url, download=False)
                URL = info['formats'][0]['url']
                play_list.append(URL)
        elif args != None:
            args2 = ''
            for i in args:
                args2 += f'{i} '
            videosSearch = VideosSearch(args2, limit=1)
            url1 = videosSearch.result()['result'][0]['link']
            with YoutubeDL(YDL_OPTIONS) as ydl:  # Это всё для добавления имени файла в лей лист
                info = ydl.extract_info(url1, download=False)
            URL = info['formats'][0]['url']
            play_list.append(URL)
    except IndexError:
        try:
            for attach in ctx.message.attachments:
                play_list.append(attach.url)
        except:
            pass
    print(play_list)
    print(f"len play list:{len(play_list)}")

    while play_list:
        if vc.is_connected():
            await _play_1()
        else:
            break


@bot.command(pass_context=True)
async def connect(ctx, arg='None'):
    global vc
    # Подключаем бота к голосовому каналу
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        print('connect')
    except:
        print('Уже подключен')


@bot.command(pass_context=True)
async def pause(self):
    global vc
    if not vc.is_playing():
        print('Музыка не проигрывается')
        return
    vc.pause()


@bot.command(pass_context=True)
async def unpause(self):
    global vc
    try:
        vc.resume()
    except:
        print('Музыка не проигрывается')


@bot.command(pass_context=True)
async def skip(self):
    global vc
    try:
        vc.stop()
    except:
        print('Музыка не проигрывается')


@bot.command(pass_context=True)
async def Help(ctx):
    await ctx.send(
        '-p {url}      -- Воспроизводит: файлы, видио с youtube, playlist, а также можно просто вписать название песни(При условии что она есть на канале NoCopyrightSounds).  \r\n-connect    -- Подключает бота к голосовому каналу.\r\n-pause        -- Пауза.\r\n-unpause    -- Снятие с паузы.\r\n-skip            -- Пропуск текущей песни.')


bot.run(token)
