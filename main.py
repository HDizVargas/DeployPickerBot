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
    deployers = ["Jordi", "Jesús", "Huber", "Toni", "Mateo", "Didac"]
    return random.choice(deployers)


def get_random_phrase(deployer):
    phrases = [
        '{} calienta que deployeas!',
        'Te ha tocado {}, mala suerte, ha deployear.',
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

    if message.content == ('$start_random_deploys'):
        await message.delete()
        await message.channel.send("Deploy Picker empezará a elegir a un deployer cada Martes y Jueves")
        check_deploy_day.start()

    if message.content == ('$stop_random_deploys'):
        await message.delete()
        await message.channel.send("Deploy Picker parará de elegir a un deployer cada Martes y Jueves")
        check_deploy_day.stop()


@tasks.loop(hours=24)
async def check_deploy_day():
    today_date = datetime.date.today().strftime('%A')
    if ( today_date == "Tuesday" or today_date == "Thursday"):
        await client.get_channel(int(os.environ['CHANNEL_ID'])).send(
            get_random_phrase(get_random_deployer()))


bot_token = os.environ['BOT_TOKEN']

keep_alive()

client.run(bot_token)
