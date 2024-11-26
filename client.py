import discord
from discord.ext import commands

class Client(commands.Bot):
    async def on_ready(self):
        print('The bot is ready')
        app_info = await self.application_info()
        print(f'Id: {app_info.id}')
        print(f'Name: {app_info.name}')
        await self.change_presence(status=discord.Status.online, activity=discord.Game('Debriding asf'))