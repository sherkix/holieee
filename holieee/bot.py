from client import Client
from dotenv import load_dotenv
from debrid import *
from discord import app_commands
from discord.ext import commands
from cache_manager import create_links_table, routine
import discord
import os
import re

load_dotenv()

client = Client()

@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def sync(ctx):
    if ctx.author.guild_permissions.administrator is True:
        print("Sync command")
        command_synced = await client.tree.sync()
        print(command_synced)
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must have admin privileges to use this command!')

@client.tree.command(name='botinfo', description='Bot Info')
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
async def bot_info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.purple()
        )
        embed.add_field(name='Info', value='Version: 1.0\nDev: @innevato', inline=False)
        await interaction.followup.send(embed=embed)

@client.tree.command(name='check', description='Check if API endpoint is working')
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
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
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
async def send_link(interaction: discord.Interaction, link: str):
    await interaction.response.defer(ephemeral=False)
    if await check_link(interaction, link):
        return
    debrider_link = add_link(link)
    if not re.search('^http+[s]?', debrider_link): # * Match if https is found at the start of the string
        embed = discord.Embed(
        title='Holieee',
        color=discord.Color.red()
    )
        embed.add_field(name='Error', value=debrider_link, inline=False)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(
        title='Holieee',
        description='Your link is ready!',
        color=discord.Color.purple()
    )   
        for i, value in enumerate(debrider_link.split(',')):
            embed.add_field(name=f'Debrid Link {i+1}', value=value, inline=False)
        await interaction.followup.send(embed=embed)
async def check_link(interaction: discord.Interaction, link: str):
    with open('blacklist/blacklist.txt', 'r', encoding='utf-8') as file:
        if file.read() in link and os.path.getsize('blacklist/blacklist.txt') > 0:
            embed = discord.Embed(
                title='Holieee',
                color=discord.Color.red()
            )
            embed.add_field(name='Error', value='Host blacklistato', inline=False)
            await interaction.followup.send(embed=embed)
            return True
        elif not re.search('^http+[s]?', link):
            embed = discord.Embed(
                title='Holieee',
                color=discord.Color.red()
            )
            embed.add_field(name='Error', value='Non hai inserito un link valido', inline=False)
            await interaction.followup.send(embed=embed)
            return True
        return False

@client.tree.error # * slash commands cooldown
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):    
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f'Cooldown! Retry in {int(error.retry_after)}s', ephemeral=True, delete_after=10)
    else: raise error
    
@client.event # * ctx commands cooldown
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f'Cooldown! Retry in {int(error.retry_after)}s', delete_after=10)
    else: raise error
    
if __name__ == '__main__':
    client.run(os.getenv('DISCORD_TOKEN'))
    create_links_table()
    routine()
