import os
import nextcord
import asyncio
import time
import json
import requests as rq
from nextcord.ext import commands
from nextcord.ext import tasks
import colorama
from colorama import Fore, Back, Style
import os
import platform
import sys

intents = nextcord.Intents.all() # Intents-urile
client = commands.Bot(command_prefix=['^'], intents=intents) # Setam prefix-ul (chiar daca e inutl)
client.remove_command('help') # Acest lucru sterge comanda default de help

# Settings.json
with open('settings.json') as f:
  config = json.load(f)

SERVER_IP = config['SERVER_IP'] # IP-ul serverului de FiveM
GUILD_ID = config['GUILD_ID'] # ID-ul serverului de Discord
TOKEN = config['TOKEN'] # Token-ul botului
EMBED_COLOR = nextcord.Colour(int(config['EMBED_COLOR'], 16))
# Event cand porneste botul
@client.event
async def on_ready():
    print('------------------------------------------------------------------------------------------------------------------------------------------')
    print(Fore.CYAN + '███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗███████╗██╗   ██╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗███████╗')
    print(Fore.CYAN + '████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║██╔════╝ ██╔════╝██╔════╝██║   ██║    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║██╔════╝')
    print(Fore.CYAN + '██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ███████╗██║   ██║    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║███████╗')
    print(Fore.CYAN + '██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ╚════██║██║   ██║    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║╚════██║')
    print(Fore.CYAN + '██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗███████║╚██████╔╝    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║███████')
    print(Fore.CYAN + '╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝     ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚══════╝')
    print('------------------------------------------------------------------------------------------------------------------------------------------')
    print(f'Hostul a fost conectat cu succes la {bot.user.name}')
    print(f'ID-ul botului este: {bot.user.id}')
    print(f"Versiunea Python-ului: {platform.python_version()}")
    print(f"Versiunea API a nextcord.py-ului: {nextcord.__version__}")
    print(f"Botul ruleaza pe: {platform.system()} {platform.release()} ({os.name})")
    print(f"------------------------------------------------------------------------------------------------------------------------------------------")
    client.my_current_task = live_status.start()

def pc():
    try:
        resp = rq.get('http://'+SERVER_IP+'/players.json').json()
        return(len(resp))
    except:
        return('N/A')

# Player Info
@client.slash_command(
    name="playerinfo",
    description="Arata informatiile despre un jucator de pe server.",
)
@commands.has_permissions(administrator=True) 
async def pid(Interaction, id: str = None):
    guild = Interaction.guild
    if not id:
        await Interaction.response.send_message('<@{}>, Te rog sa specifici un ID de jucator in joc!'.format(Interaction.author.id), ephemeral=True)
        return

    resp = rq.get('http://'+SERVER_IP+'/players.json')
    for player in resp.json():
        if player['id'] == int(id):
            pembed = nextcord.Embed(title='Informatii despre Jucator', color=(EMBED_COLOR))
            pembed.add_field(name='Numele de pe Steam: {}\nID-ul de pe server: {}'.format(player['name'], player['id']), value='Ping: {}'.format(player['ping']), inline=False)
            pembed.set_author(name=guild.name, icon_url=guild.icon.url)
            pembed.set_footer(text='© Moongetsu Systems™ (2020-2023) | FiveM Status Bot')
            [pembed.add_field(name=args.split(':')[0].capitalize(), value=args.split(':')[1], inline=False) for args in player['identifiers']]
            await Interaction.response.send_message(embed=pembed, ephemeral=True)
            return

    error_embed = nextcord.Embed(title="Eroare 👀", description=f"Utilizatorul cu ID-ul `{id}` nu este conectat pe server.", color=0xff0000)
    error_embed.set_author(name=guild.name, icon_url=guild.icon.url)
    error_embed.set_footer(text="© Moongetsu Systems™ (2020-2023) | FiveM Status Bot")
    await Interaction.response.send_message(embed=error_embed, ephemeral=True)

# Players
@client.slash_command(
    name="players",
    description="Arata jucatorii conectati pe server.",
)
@commands.has_permissions(administrator=True) 
async def players(Interaction):
    guild = Interaction.guild
    timenow = time.strftime("%H:%M")
    resp = rq.get('http://'+SERVER_IP+'/players.json').json()
    total_players = len(resp)
    if len(resp) > 25:
        for i in range(round(len(resp) / 25)):
            embed = nextcord.Embed(title='👀 | Lista de Jucatori', description='', color=(EMBED_COLOR))
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_footer(text=f'Numarul total de jucatori: {total_players} | © Moongetsu Systems™ (2020-2023) | FiveM Status Bot')
            count = 0
            for player in resp:
                embed.add_field(name=player['name'], value='ID: ' + str(player['id']))
                resp.remove(player)
                count += 1
                if count == 25:
                    break
                else:
                    continue

            await Interaction.send(embed=embed)
    else:
        embed = nextcord.Embed(title='👀 | Lista de Jucatori', description='', color=(EMBED_COLOR))
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_footer(text=f'Numarul total de jucatori: {total_players} | © Moongetsu Systems™ (2020-2023) | FiveM Status Bot')
        for player in resp:
            embed.add_field(name=player['name'], value='ID: ' + str(player['id']))
        await Interaction.send(embed=embed, ephemeral=True)

# Help
@client.slash_command(
    name="help",
    description="Arata comenzile pe care le are botul.",
)
async def help(Interaction):
    guild = Interaction.guild

    embed = nextcord.Embed(title=f"", color=0x(EMBED_COLOR))
    embed.set_author(name=guild.name, icon_url=guild.icon.url)
    embed.add_field(name=":page_with_curl: | players", value="Arata jucatorii conectati pe server.", inline=False)
    embed.add_field(name=":chart_with_upwards_trend: | playerinfo `<id>`", value="Arata informatiile despre un jucator de pe server.", inline=False)
    embed.set_footer(text="© Moongetsu Systems™ (2020-2023) | FiveM Status Bot")
    await Interaction.send(embed=embed)

# Status-ul botului
@tasks.loop()
async def live_status(seconds=75):
    pcount = pc()
    Dis = client.get_guild(GUILD_ID)

    activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f'{pcount} jucatori pe serverul de FiveM')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f'{Dis.member_count} de membrii pe serverul de Discord')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

client.run(TOKEN)
