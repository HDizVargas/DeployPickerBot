import json
import os
import random

import discord
from dotenv import load_dotenv

from keep_alive import keep_alive

load_dotenv()

client = discord.Client()
f = open('./deployers.json')
deployers_json = json.load(f)


def get_random_deployer():
    deployers = list(deployers_json.values())
    return random.choice(deployers)


def get_random_phrase(deployer):
    phrases = [
        '{} calienta que deployeas!',
        'Te ha tocado {}, mala suerte, a deployear.',
        'Adivinad a quién le toca fastidiar PRO, exacto a {}.'
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

    elif message.content == ('$ping'):
        await message.delete()

bot_token = os.environ['BOT_TOKEN']

keep_alive()

client.run(bot_token)
