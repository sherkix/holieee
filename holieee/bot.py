from client import Client
from dotenv import load_dotenv
from debrid import *
import cache_manager
import discord
from discord import app_commands
from discord.ext import commands
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
        await ctx.send('You must be the owner to use this command!')

@client.tree.command(name='botinfo', description='Bot Info')
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
async def bot_info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(
            title='Holieee',
            color=discord.Color.purple()
        )
        embed.add_field(name='Info', value='Version: 0.0.1\nDev: @innevato', inline=False)
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
    with open('blacklist/blacklist.txt', 'r') as file:
        if file.read() in link:
            embed = discord.Embed(
                title='Holieee',
                color=discord.Color.red()
            )
            embed.add_field(name='Error', value='Host blacklistato', inline=False)
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
                for i, values in enumerate(debrider_link.split(',')):
                    embed.add_field(name=f'Debrid Link {i+1}', value=str(values), inline=False)
                await interaction.followup.send(embed=embed)
            else: # ! Error output
                embed = discord.Embed(
                title='Holieee',
                color=discord.Color.red()
            )
                embed.add_field(name='Error', value=debrider_link, inline=False)
                await interaction.followup.send(embed=embed)
            
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
    cache_manager.create_links_table()
    client.run(os.getenv('DISCORD_TOKEN'))