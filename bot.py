import os
import discord
import random
import datetime
from yhlibrary import getauthor, whichtext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
last_quote = ""  # To keep the last quote in the memory to send the link when "hangiyazı" is called.

file = open("archive", "r", encoding="utf-8")
lines = file.readlines()
file.close()
archive = [line.rstrip("\n") for line in lines if "https://yazhocam.com/" not in line]

help_message = "YazHocam Bot\n\n" \
               "**\n\n" \
               "YazHocam sitesindeki yazılardan rastgele bir kesit görmek için 'yazdırhocam' yaz\n\n" \
               "Yazdırdığım en son kesitin hangi yazıdan olduğunu öğrenmek için 'hangiyazı' yaz\n\n" \
               "İstediğin yazarın yazılarında en çok kullandığı 10 kelimeyi görmek için '10kelime *yazar adı*' yaz\n\n" \
               "**\n\n" \
               "YazHocam Bot\n\n" \
               "https://yazhocam.com/"

print("bot has connected")


@client.event
async def on_message(message):
    global last_quote
    global help_message

    if message.author == client.user:
        return

    elif message.content == "yazdırhocam":
        random_quote = random.choice(archive)
        last_quote = random_quote[:]
        await message.channel.send(random_quote)

    elif message.content == "hangiyazı":
        await message.channel.send(whichtext(last_quote))

    elif message.content[:8] == "10kelime":
        await message.channel.send("Hazırlanıyor...")
        await message.channel.send(getauthor(message.content[9:]))

    elif message.content == "yardımhocam":
        await message.channel.send(help_message)


async def on_error(event, *args):
    with open("log.txt", "a") as log:
        if event == "on_message":
            log.write(f"****\n\n{datetime.datetime.now()}\nUnhandled message: {args[0]}\n\n")


client.run(TOKEN)
print("bot has disconnected")
