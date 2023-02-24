# FiveM Discord.Py Bot 
Useful Discord Bot for Owners of FiveM Servers

# List of Features:
```
» Gets the player list from the server and show it at the bot status
» Command that sends a list with the players from your server
» Command that sends all the information from a player, like their SteamID or Discord Profile ID
```

# What's different:
```
» I made some changes at the embeds
» I added application (slash) commands
» I fixed some bugs from AmirhN's Bot
```
## Configuration of settings.json
```
"SERVER_IP": "IP/DNS:30120", » Your FiveM Server IP/DNS
"GUILD_ID": GUILDID, » Guild ID
"TOKEN": "BOT TOKEN", » Token
"EMBED_COLOR": "0x2A2A2A" » Embed color (you can use https://htmlcolorcodes.com/color-picker)
```

## Installation of dependencies (Root VPS)

```
apt install screen
apt install python3
get the archive from https://github.com/moongetsu/fivem-servers-bot/releases
create a folder & extract the version that you want
cd yourfoldername
pip3 install -r requirements.txt
screen python3 main.py
```

## Installation of dependencies (Pterodactyl/Other Panel)
Add in the **Startup » ADDITIONAL PYTHON PACKAGES**: 
```
nextcord asyncio colorama json requests time
```

# Screenshots
Soon cuz i'm to lazy to post rn
# Don't have host?
You can host your bot for free on my [Moon Free Hosting](https://freehost.moongetsu.xyz) 
