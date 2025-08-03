import discord
import random
import requests
import os
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Flask server to keep bot alive
app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Insult list
insults = [
    "You alright, or is thinking not your strong suit?",
    "Didn’t ask, but cheers for the nonsense.",
    "Bless you for trying, really.",
    "You done, or should I call someone?",
    "Say that again, but slower—maybe your brain’ll catch up.",
    "Big words for someone who still needs spellcheck.",
    "Oh look, it speaks.",
    "You're still here? Thought I blinked you away.",
    "Try again, this time with less cringe.",
    "If I wanted noise, I’d turn on the kettle.",
    "You got a point or just waving that ego around?",
    "Cute opinion—shame no one asked.",
    "Is this your final form, or are you still buffering?",
    "You’re not even wrong—you’re just... irrelevant.",
    "Put the phone down, you're leaking brain cells.",
    "That comeback had the energy of a flat pint.",
    "Say less. Seriously. Say way less.",
    "You talk like autocorrect gave up on you.",
    "You’ve got all the confidence and none of the clue.",
    "That was almost clever—try again in a decade."
]

def get_gif(action):
    try:
        res = requests.get(f"https://nekos.best/api/v2/{action}")
        if res.status_code == 200:
            return res.json()['results'][0]['url']
    except:
        return None

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    # If bot is pinged
    if client.user in message.mentions:
        insult = random.choice(insults)
        await message.reply(insult, mention_author=False)

    elif msg.startswith('!rate'):
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author

        rating = random.randint(1, 10)
        scale = "🔥" * rating + "💀" * (10 - rating)
        await message.channel.send(f"{target.display_name} is rated: {rating}/10\non hotness scale.\n{scale}")

    elif msg.startswith('!quote'):
        try:
            r = requests.get("https://api.quotable.io/random")
            data = r.json()
            await message.channel.send(f"📜 *{data['content']}* — **{data['author']}**")
        except:
            await message.channel.send("Couldn’t fetch a quote right now.")

    elif msg.startswith('!fact'):
        try:
            r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
            data = r.json()
            await message.channel.send(f"💡 {data['text']}")
        except:
            await message.channel.send("Facts API is being lazy.")

    elif msg.startswith('!bored'):
        try:
            r = requests.get("https://www.boredapi.com/api/activity")
            data = r.json()
            await message.channel.send(f"🧠 Try this: **{data['activity']}**")
        except:
            await message.channel.send("I’m too bored to fetch that.")

    elif msg.startswith('!dog'):
        try:
            r = requests.get("https://dog.ceo/api/breeds/image/random")
            data = r.json()
            await message.channel.send(data['message'])
        except:
            await message.channel.send("Couldn't fetch a doggo rn.")

    elif msg.startswith('!cat'):
        try:
            r = requests.get("https://api.thecatapi.com/v1/images/search")
            data = r.json()
            await message.channel.send(data[0]['url'])
        except:
            await message.channel.send("Cat API died. RIP.")

    elif msg.startswith('!help'):
        embed = discord.Embed(
            title="✨ Bot Commands",
            description="Here’s what I can do:",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Ping the bot", value="Mention the bot and get a sarcastic reply", inline=False)
        embed.add_field(name="!rate [@user]", value="Rates your hotness 🔥", inline=True)
        embed.add_field(name="!quote", value="Get a random quote 📜", inline=True)
        embed.add_field(name="!fact", value="Random useless fact 💡", inline=True)
        embed.add_field(name="!bored", value="Suggests something to do 😐", inline=True)
        embed.add_field(name="!dog", value="Sends a random dog 🐶", inline=True)
        embed.add_field(name="!cat", value="Sends a random cat 🐱", inline=True)
        embed.add_field(name="!kiss/@, !hug/@, !pat/@", value="Send love with GIFs 💖", inline=False)
        await message.channel.send(embed=embed)

    elif msg.startswith('!kiss'):
        if message.mentions:
            target = message.mentions[0].mention
            gif = get_gif("kiss")
            if gif:
                embed = discord.Embed(
                    description=f"💋 {message.author.mention} kissed {target}!",
                    color=discord.Color.pink()
                )
                embed.set_image(url=gif)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("No kisses today, try again!")
        else:
            await message.channel.send("Tag someone to kiss, baka! 💢")

    elif msg.startswith('!hug'):
        if message.mentions:
            target = message.mentions[0].mention
            gif = get_gif("hug")
            if gif:
                embed = discord.Embed(
                    description=f"🫂 {message.author.mention} hugs {target} tightly!",
                    color=discord.Color.green()
                )
                embed.set_image(url=gif)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Couldn't get a hug gif.")
        else:
            await message.channel.send("You need to mention someone to hug! 🥺")

    elif msg.startswith('!pat'):
        if message.mentions:
            target = message.mentions[0].mention
            gif = get_gif("pat")
            if gif:
                embed = discord.Embed(
                    description=f"🐾 {message.author.mention} gently pats {target}'s head!",
                    color=discord.Color.blue()
                )
                embed.set_image(url=gif)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Pat gifs aren't working rn.")
        else:
            await message.channel.send("Pat who? Mention someone, silly!")

keep_alive()
client.run(TOKEN)
