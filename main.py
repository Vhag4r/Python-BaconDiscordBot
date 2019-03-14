import discord
import re
import os,os.path
import random
from discord.ext import commands

TOKEN = 'NTQ3NDcwNTg5NTIzMTMyNDY4.D03UCw.wUPSduayMXnueTd_mS1nBawQ1nE'
words_channel_id = '547476612933746709'
main_channel_id = ''
clips_directory = 'sound_clips'
clips_count = 0


client = discord.Client()
client = commands.Bot(command_prefix="!")
commands_dict = {
    "words":"Returns a formatted list of words for Skribbl.io from the words text channel",
    "quote":"Play a random quote"
                 }


@client.event
async def on_ready():
    print("Logged in!...")
    path,dirs,files = next(os.walk(clips_directory))
    clips_count = len(files)


@client.command(pass_context=True)
async def words(ctx):
    if ctx.message.channel.id==words_channel_id:
        valid_words = []
        async for log in client.logs_from(ctx.message.channel, limit=100):
            log_message = log.content + ""
            chopped = re.split("\t|\n|\r|,", log_message)
            if not log.author == client.user:
                for w in chopped:
                    if not w in valid_words and not w.startswith('!'):
                        valid_words.append(w.strip())

        to_return = ''
        for word in valid_words:
            to_return += word
            if not valid_words.index(word) == len(valid_words) - 1:
                to_return += ","
        to_return.strip()

        await client.send_message(ctx.message.channel, to_return)


async def disconnect(voice):
    await voice.disconnect()


@client.command(pass_context=True)
async def quote(ctx):
    channel = ctx.message.author.voice.voice_channel
    randomClipNumber = random.randint(0, clips_count)

    if channel is None:
        await client.send_message("You must be in a voice channel to play a quote")
    else:
        voice = await client.join_voice_channel(channel)
        music_player = voice.create_ffmpeg_player("sound_clips/%s.mp3" % randomClipNumber)
        music_player.start()
        while music_player.is_playing():
            pass
        print("Finished playing quote")
        await voice.disconnect()

@client.command(pass_context=True)
async def commands(ctx):
    user_message = ''
    for key,value in commands_dict.items():
        user_message+= key + "  :   " + value + "\n"
    channel_message = "Sent you a list of commands " + ctx.message.author.name
    await client.send_message(ctx.message.author,user_message)
    await client.send_message(ctx.message.channel,channel_message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(TOKEN)


