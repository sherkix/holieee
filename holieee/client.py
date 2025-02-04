import discord
from discord.ext import commands

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=discord.Intents.all(), case_insensitive=False)
        discord.Intents.message_content = True
        self.synced = False;
        
    async def on_ready(self):
        await self.wait_until_ready()
        app_info = await self.application_info()
        print(f'Id: {app_info.id}')
        print(f'Name: {app_info.name}')
        if not self.synced: 
            await self.tree.sync() 
            self.synced = True
        await self.change_presence(status=discord.Status.online, activity=discord.Game('Debriding asf'))
        print('The bot is ready')
