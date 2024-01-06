import discord
import glob, random
import time
import datetime
import asyncio
from discord.ext import commands, tasks
from discord import app_commands

task = None
my_time = 86400

def run_discord_bot():
    TOKEN = '' #your bot token goes here
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))

        
    async def change_server_icon(server):
        while True: 
            file_path_type = ["bot/images/*.jpg"] 
            images = glob.glob(random.choice(file_path_type))
            random_image = random.choice(images) # Makes it pick the random image
            
            with open(random_image, 'rb') as f:
                icon = f.read()

            # Upload the image file to Discord and set it as the new server icon
            await server.edit(icon=icon)
            
            # Get the channel id and post the new image in the channel
            channel = client.get_channel(1163169073866211421)
            with open(random_image, 'rb') as f:
                picture = discord.File(f)
                await channel.send('Uus kass on: ', file=picture)
            
            # Wait for 24 hours before changing the server icon again
            await asyncio.sleep(86400)
            

    # To start the loop
    def start_task(server):
        global task
        if task is None:
            task = client.loop.create_task(change_server_icon(server))

    # To stop the loop
    def stop_task():
        global task
        if task is not None:
            task.cancel()
            task = None
    
    # When user types !start the bot starts the loop and when the user types !stop it stops the loop
    @client.event
    async def on_message(message):
        if message.content.startswith('!start'):
            server = message.guild
            start_task(server)
            await message.channel.send('Alustan Skisomist')
        elif message.content.startswith('!ssstop'):
            stop_task()
            await message.channel.send('Lopetan skisomise')
    
    client.run(TOKEN)