import discord
import os
import random
import datetime
from discord.ext import tasks
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()


def get_random_deployer():
    deployers = ["Jordi B.", "Jesús", "Huber", "Toni", "Mateo", "Didac", "Enrique", "Jordi H."]
    return random.choice(deployers)


def get_random_phrase(deployer):
    phrases = [
        '{} calienta que deployeas!',
        'Te ha tocado {}, mala suerte, a deployear.',
        'Adivinad a quien le toca fastidiar PRO, exacto a {}.'
    ]
    return random.choice(phrases).format(deployer)


@client.event
async def on_ready():
    print('You  have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ('$deploy'):
        await message.delete()
        await message.channel.send(get_random_phrase(get_random_deployer()))

    elif message.content == ('$check-day'):
        today_date = datetime.date.today().strftime('%A')
        await message.delete()
        await message.channel.send(today_date)

    elif message.content == ('$ping'):
        await message.delete()

    elif message.content == ('$start_random_deploys'):
        await message.delete()
        await message.channel.send(
            "Deploy Picker empezará a elegir a un deployer cada Martes y Jueves"
            )
        check_deploy_day.start()

    elif message.content == ('$stop_random_deploys'):
        await message.delete()
        await message.channel.send(
            "Deploy Picker parará de elegir a un deployer cada Martes y Jueves"
            )
        check_deploy_day.stop()


@tasks.loop(hours=24)
async def check_deploy_day():
    # Gets the weekday as a number where Tuesday it's 1 and Thursday is 3
    # Comparing by integers improves the performance
    today_date = datetime.date.weekday()
    if today_date == 1 or today_date == 3:
        await client.get_channel(int(os.environ['CHANNEL_ID'])).send(
            get_random_phrase(get_random_deployer()))


bot_token = os.environ['BOT_TOKEN']

keep_alive()

client.run(bot_token)
