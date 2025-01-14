from client import Client
from dotenv import load_dotenv
from debrid import *
import cache_manager
import discord
import os
import re

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='?', intents=intents, case_insensitive=False)

@client.command()
async def sync(ctx):
    if ctx.author.guild_permissions.administrator is True:
        print("Sync command")
        command_synced =  await client.tree.sync()
        print(command_synced)
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')
        
@client.tree.command(name='botinfo', description='Bot Info')
async def bot_info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.purple()
        )
        embed.add_field(name='Info', value='Version: 0.0.1\nDev: @innevato', inline=False)
        await interaction.followup.send(embed=embed)
        
@client.tree.command(name='check', description='Check if API endpoint is working')
async def check(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    if server_check() is True:
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.green()
        )
        embed.add_field(name='API endpoint is up', value='Ok worka', inline=False)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.red()
        )
        embed.add_field(name='API endpoint is down', value='Ok non worka', inline=False)
        await interaction.followup.send(embed=embed)

@client.tree.command(name='getlink', description='Get link from debrider')
async def send_link(interaction: discord.Interaction, link: str):
    await interaction.response.defer(ephemeral=False)
    if 'file.al' in link or 'pornhub.com' in link:
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.red()
        )
        embed.add_field(name='Error', value='Host blacklistato!', inline=False)
        await interaction.followup.send(embed=embed)
    elif 'https' not in link or 'http' not in link:
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.red()
        )
        embed.add_field(name='Error', value='Non hai inserito un link valido!', inline=False)
        await interaction.followup.send(embed=embed)
    else:
        debrider_link = add_link(link)
        if re.search('^https', debrider_link): # ? Match if https is found at the start of the string
            embed = discord.Embed(
            title='Holieee',
            description='Your link is ready!',
            color=discord.Color.purple()
        )
            embed.add_field(name='Debrid Link', value=debrider_link, inline=False)
            await interaction.followup.send(embed=embed)
        else: # ! Error output
            embed = discord.Embed(
            title='Holieee',
            color=discord.Color.red()
        )
            embed.add_field(name='Error', value=debrider_link, inline=False)
            await interaction.followup.send(embed=embed)

if __name__ == '__main__':
    cache_manager.create_links_table()
    client.run(os.getenv('DISCORD_TOKEN'))