import discord
import random
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Flask web server to keep Render deployment awake (optional but safe)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()

# Intents and bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Insults list
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

# Events and commands
@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.author != bot.user:
        response = random.choice(insults)
        await message.reply(response)
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Daddy Paneer Bot Commands 🧀", color=discord.Color.purple())
    embed.add_field(name="!cat", value="Random cat image 🐱", inline=False)
    embed.add_field(name="!dog", value="Random dog image 🐶", inline=False)
    embed.add_field(name="!rate @user", value="Rates user on hotness scale 🔥", inline=False)
    embed.add_field(name="!quote", value="Gives you a random quote 📜", inline=False)
    embed.add_field(name="!fact", value="Fun random fact 🧠", inline=False)
    embed.add_field(name="!bored", value="Gives you something fun to do 😪", inline=False)
    embed.add_field(name="!kiss @user", value="Sends a kiss gif 😘", inline=False)
    embed.add_field(name="!hug @user", value="Sends a hug gif 🤗", inline=False)
    embed.add_field(name="!pat @user", value="Sends a pat gif 👋", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
    res = requests.get("https://api.thecatapi.com/v1/images/search")
    if res.status_code == 200:
        image_url = res.json()[0]["url"]
        await ctx.send(image_url)

@bot.command()
async def dog(ctx):
    res = requests.get("https://dog.ceo/api/breeds/image/random")
    if res.status_code == 200:
        image_url = res.json()["message"]
        await ctx.send(image_url)

@bot.command()
async def rate(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    rating = random.randint(1, 10)
    emoji = "🔥" * rating + "💀" * (10 - rating)
    await ctx.send(f"{member.display_name} is rated: {rating}/10\n on hotness scale. {emoji}")

@bot.command()
async def quote(ctx):
    try:
        res = requests.get("https://zenquotes.io/api/random")
        if res.status_code == 200:
            data = res.json()[0]
            await ctx.send(f'"{data["q"]}" — {data["a"]}')
    except:
        await ctx.send("Couldn’t fetch a quote right now. Try again later!")

@bot.command()
async def fact(ctx):
    try:
        res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if res.status_code == 200:
            data = res.json()
            await ctx.send(data["text"])
    except:
        await ctx.send("Failed to fetch a fact right now. Try again later!")

@bot.command()
async def bored(ctx):
    try:
        res = requests.get("https://www.boredapi.com/api/activity")
        if res.status_code == 200:
            data = res.json()
            await ctx.send(f"Try this: {data['activity']}")
    except:
        await ctx.send("No fun ideas at the moment 😅")

# Cute interaction commands
async def send_gif(ctx, member, action, gif_url):
    if not member:
        await ctx.send("You need to mention someone!")
        return
    messages = {
        "kiss": f"{ctx.author.mention} gives {member.mention} a sweet kiss 😘",
        "hug": f"{ctx.author.mention} gives {member.mention} a warm hug 🤗",
        "pat": f"{ctx.author.mention} gently pats {member.mention} 👋"
    }
    embed = discord.Embed(description=messages[action], color=discord.Color.pink())
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, member: discord.Member = None):
    await send_gif(ctx, member, "kiss", "https://media.tenor.com/2roX3uxz_68AAAAC/kiss.gif")

@bot.command()
async def hug(ctx, member: discord.Member = None):
    await send_gif(ctx, member, "hug", "https://media.tenor.com/GfSX-u7VGM4AAAAC/hug.gif")

@bot.command()
async def pat(ctx, member: discord.Member = None):
    await send_gif(ctx, member, "pat", "https://media.tenor.com/I6kN-6X7nhAAAAAC/pat.gif")

# Start the bot
bot.run(TOKEN)
