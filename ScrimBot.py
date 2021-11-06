# Libraries
import discord
import datetime
import urllib3
from bs4 import BeautifulSoup
import dateutil.parser as dparser

# Member intents
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# Map scraping
http = urllib3.PoolManager()
url = "https://squadmaps.com/"
# Fetch the html file
response = http.request('GET', url)
squadmaps = BeautifulSoup(response.data, 'html.parser')

raw_maps = squadmaps.find_all("section")
raw_maps.pop(0)

maps_squad = []
for map in raw_maps:
    map_titel = map.find("h2")
    layers = map.find_all("h3")
    for layer in layers:
        mapname = map_titel.text + " " + layer.text
        mapname = mapname.replace(" ", "_")
        maps_squad.append(mapname)
maps_squad.append("Any")
maps_squad.append("Any_AAS")
maps_squad.append("Any_TC")
maps_squad.append("Any_Skirmish")

# Bot reactions


class MyClient(discord.Client):
    # Erbe die Klasse Client (Ab hier wird dem Bot gesagt, was er bei bestimmten Events
    # zu tun hat)
    # Einloggen
    async def on_ready(self):  # Methode wurde geerbt und jetzt überschrieben
        print("Bot ready")

    async def on_member_join(self, member):
        embed_join_info = discord.Embed(title="Welcome to SquadScrims - A Discord Server for Competitive Matchmaking",
                                        colour=discord.Colour(0xeaff00),
                                        description="Please note that this server is only intended for clan "
                                                    "representatives.\nIf you are the first clan-rep of your team, "
                                                    "you need to register it. You can to do this in the "
                                                    "**#commands** channel in the following"" format:\n\n"
                                                    "**!team ClanName,ClanTag,YourIngameNick**\n\n"
                                                    "``Example: !team European Wargamer Association,[EWA],Mighty``\n\n"
                                                    "Once you are registered, you will get the new role Clan-Rep.\n\n"
                                                    "If your team is already registered you can just sign up as another"
                                                    "clan-rep by typing the following command into the **#commands** "
                                                    "channel:\n\n"
                                                    "**!rep ClanTag,YourIngameNick**\n\n"
                                                    "``Example: !rep [EWA],Mighty``\n\n"
                                                    "Please do this now.")
        embed_join_info.set_thumbnail(
            url="https://ewa-squad.org/images/bot_logo_trans_2.png")
        role_newclanrep = discord.utils.get(
            member.guild.roles, name="New Clan-Rep")
        await member.add_roles(role_newclanrep)
        await member.send(embed=embed_join_info)

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("!team"):
            usr_team = message.content.removeprefix('!team ')
            clan_name = usr_team.split(",")[0]
            clan_name = clan_name.lstrip()
            clan_name = clan_name.rstrip()
            clan_tag = usr_team.split(",")[1]
            clan_tag = clan_tag.lstrip()
            clan_tag = clan_tag.rstrip()
            ingame_nick = usr_team.split(",")[2]
            ingame_nick = ingame_nick.lstrip()
            ingame_nick = ingame_nick.rstrip()
            dest_channel = message.guild.get_channel(858670191226650655)
            embed_team = discord.Embed(title="A new team has joined SquadScrims",
                                       colour=discord.Colour(0xeaff00),
                                       description="SquadScrims is happy to welcome " + clan_tag + " as a new member")
            embed_team.set_thumbnail(
                url="https://ewa-squad.org/images/bot_logo_trans_2.png")
            embed_team.add_field(
                name="**Name**", value=clan_name, inline=False)
            embed_team.add_field(name="**Tag**", value=clan_tag, inline=False)
            role_clanrep = discord.utils.get(
                message.guild.roles, name="Clan-Rep")
            role_new_rep = discord.utils.get(
                message.guild.roles, name="New Clan-Rep")
            await dest_channel.send(embed=embed_team)
            await message.author.add_roles(role_clanrep)
            await message.author.remove_roles(role_new_rep)
            await message.author.edit(nick=clan_tag + "  " + ingame_nick)
            embed_user_info = discord.Embed(title="Successfully added your team",
                                            colour=discord.Colour(0xeaff00),
                                            description="Your team has been added to the list and a new role (Clan-rep) has "
                                            "been applied to your account. You now have access to the match "
                                            "section.\n\n Please see the **#how-it-works** channel in order to "
                                            "create or join new matches.")
            embed_user_info.set_thumbnail(
                url="https://ewa-squad.org/images/bot_logo_trans_2.png")
            await message.author.send(embed=embed_user_info)

        if message.content.startswith("!rep"):
            usr_team = message.content.removeprefix('!rep ')
            clan_tag = usr_team.split(",")[0]
            clan_tag = clan_tag.lstrip()
            clan_tag = clan_tag.rstrip()
            ingame_nick = usr_team.split(",")[1]
            ingame_nick = ingame_nick.lstrip()
            ingame_nick = ingame_nick.rstrip()
            role_clanrep = discord.utils.get(
                message.guild.roles, name="Clan-Rep")
            role_new_rep = discord.utils.get(
                message.guild.roles, name="New Clan-Rep")
            await message.author.add_roles(role_clanrep)
            await message.author.remove_roles(role_new_rep)
            await message.author.edit(nick=clan_tag + " " + ingame_nick)
            embed_user_info = discord.Embed(title="Successfully added you as clan-rep for " + clan_tag,
                                            colour=discord.Colour(0xeaff00),
                                            description="Your have been added as a clan-rep. The role has been applied to "
                                            "your user. You now have access to the match "
                                            "section.\n\n Please see the **#how-it-works** channel in order to "
                                            "create or join new matches.")
            embed_user_info.set_thumbnail(
                url="https://ewa-squad.org/images/bot_logo_trans_2.png")
            await message.author.send(embed=embed_user_info)

        if message.content.startswith("!match"):
            usr_match = message.content.removeprefix('!match ')
            match_date = usr_match.split(",")[0]
            match_date = match_date.lstrip()
            match_date = match_date.rstrip()
            match_date = dparser.parse(match_date, fuzzy=True)
            match_date_conv = match_date.strftime("%B %d, %Y at %H:%M UTC")
            match_player = usr_match.split(",")[1]
            match_player = match_player.lstrip()
            match_player = match_player.rstrip()
            match_map = usr_match.split(",")[2]
            match_map = match_map.lstrip()
            match_map = match_map.rstrip()
            match_mixed = usr_match.split(",")[3]
            match_mixed = match_mixed.lstrip()
            match_mixed = match_mixed.rstrip()
            match_mixed = match_mixed.capitalize()
            server_info = usr_match.split(",")[4]
            server_info = server_info.lstrip()
            server_info = server_info.rstrip()
            server_info = server_info.capitalize()
            if match_mixed != "Yes" and match_mixed != "No":
                return
            if server_info != "Yes" and server_info != "No":
                return
            # if match_player.isnumeric() == False:
            #    return
            check = any(item in match_map for item in maps_squad)
            if check == True:
                dest_channel = message.guild.get_channel(858671467775393792)
                embed_match_info = discord.Embed(colour=discord.Colour(0xeaff00),
                                                 description="Has created a new match",
                                                 timestamp=datetime.datetime.utcnow())
                embed_match_info.set_thumbnail(
                    url="https://ewa-squad.org/images/bot_logo_trans_2.png")
                embed_match_info.set_footer(text="Posted")
                embed_match_info.set_author(name=message.author.nick)
                embed_match_info.add_field(
                    name="**Date**", value=match_date_conv, inline=False)
                if match_player.endswith("+"):
                    match_player = match_player[:-1]
                    embed_match_info.add_field(
                        name="**Size**", value=match_player + "v" + match_player + " (or more)", inline=False)
                else:
                    embed_match_info.add_field(
                        name="**Size**", value=match_player + "v" + match_player, inline=False)
                embed_match_info.add_field(
                    name="**Map**", value=match_map, inline=False)
                embed_match_info.add_field(
                    name="**Coalitions**", value=match_mixed, inline=False)
                embed_match_info.add_field(
                    name="**Server available**", value=server_info, inline=False)
                sent_message = await dest_channel.send(embed=embed_match_info)
                message_id = sent_message.id
                channel_id = str(message_id)
                channel_id = channel_id[-3:]
                emojis = ["⚔"]
                for emoji in emojis:
                    await sent_message.add_reaction(emoji)
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(
                        read_messages=False)
                }
                category = discord.utils.get(
                    message.guild.categories, name="| Match Lobbys")
                match_date_channel = match_date.strftime("%Y%m%d")
                match_channel = await message.guild.create_text_channel(name=match_date_channel+"_"+match_map+"_id_"+channel_id,
                                                                        overwrites=overwrites, category=category,
                                                                        position=1)
                overwrite_read = discord.PermissionOverwrite()
                overwrite_read.read_messages = True
                overwrite_read.add_reactions = True
                overwrite_read.send_messages = True
                overwrite_read.kick_members = True
                await match_channel.set_permissions(message.author, overwrite=overwrite_read)
                embed_match_lobby_info = discord.Embed(colour=discord.Colour(0xeaff00),
                                                       title="Welcome to the match lobby of "+message.author.nick)
                embed_match_lobby_info.set_thumbnail(
                    url="https://ewa-squad.org/images/bot_logo_trans_2.png")
                embed_match_lobby_info.add_field(
                    name="**Date**", value=match_date_conv, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Size**", value=match_player + "v" + match_player, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Map**", value=match_map, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Coalitions**", value=match_mixed, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Server available**", value=server_info, inline=False)
                await match_channel.send(embed=embed_match_lobby_info)
                embed_user_info = discord.Embed(
                    title="Match created",
                    colour=discord.Colour(0xeaff00),
                    description="Your match has been successfully created\n\n"
                                "Don't forget, you are now able to use the following commands within the match lobby:\n\n"
                                "`!lock` : The match will be locked (sign ups are blocked)\n"
                                "`!unlock` : The match will be unlocked (this is the current status)\n"
                                "`!close` : The match will be closed permanently\n"
                                "`!tier` : The expected skill tier level\n"
                                "`!region` : The region where your team is located")
                await message.author.send(embed=embed_user_info)
                role_clanrep = discord.utils.get(
                    message.author.guild.roles, name="Clan-Rep")
                log_channel = message.guild.get_channel(898242185592438807)
                embed_log_info = discord.Embed(
                    title="A new match has been opened by " + message.author.nick,
                    colour=discord.Colour(0xeaff00),
                    description="Check here: " + sent_message.jump_url)
                await log_channel.send(f'Hi {role_clanrep.mention}')
                await log_channel.send(embed=embed_log_info)

        if message.content.startswith("!event"):
            role_events = discord.utils.get(
                message.author.guild.roles, name="Events")
            roles_author = message.author.roles
            if role_events in roles_author:
                usr_match = message.content.removeprefix('!event ')
                match_name = usr_match.split(",")[0]
                match_name = match_name.lstrip()
                match_name = match_name.rstrip()
                match_date = usr_match.split(",")[1]
                match_date = match_date.lstrip()
                match_date = match_date.rstrip()
                match_date = dparser.parse(match_date, fuzzy=True)
                match_date_conv = match_date.strftime("%B %d, %Y at %H:%M UTC")
                match_player = usr_match.split(",")[2]
                match_player = match_player.lstrip()
                match_player = match_player.rstrip()
                match_map = usr_match.split(",")[3]
                match_map = match_map.lstrip()
                match_map = match_map.rstrip()
                match_mixed = usr_match.split(",")[4]
                match_mixed = match_mixed.lstrip()
                match_mixed = match_mixed.rstrip()
                match_mixed = match_mixed.capitalize()
                server_info = usr_match.split(",")[5]
                server_info = server_info.lstrip()
                server_info = server_info.rstrip()
                server_info = server_info.capitalize()
                if match_mixed != "Yes" and match_mixed != "No":
                    return
                if server_info != "Yes" and server_info != "No":
                    return
                if match_player.isnumeric() == False:
                    return
                if match_map.isnumeric() == False:
                    return
                dest_channel = message.guild.get_channel(
                    858671467775393792)
                embed_match_info = discord.Embed(colour=discord.Colour(0xff2021),
                                                description="Has created a new event",
                                                timestamp=datetime.datetime.utcnow())
                embed_match_info.set_thumbnail(
                    url="https://ewa-squad.org/images/bot_logo_trans_2.png")
                embed_match_info.set_footer(text="Posted")
                embed_match_info.set_author(name=message.author.nick)
                embed_match_info.add_field(
                    name="**Name**", value=match_name, inline=False)
                embed_match_info.add_field(
                    name="**Starting date**", value=match_date_conv, inline=False)
                embed_match_info.add_field(
                    name="**Size**", value=match_player + "v" + match_player, inline=False)
                embed_match_info.add_field(
                    name="**Nr. of teams**", value=match_map, inline=False)
                embed_match_info.add_field(
                    name="**Coalitions**", value=match_mixed, inline=False)
                embed_match_info.add_field(
                    name="**Servers available**", value=server_info, inline=False)
                sent_message = await dest_channel.send(embed=embed_match_info)
                message_id = sent_message.id
                channel_id = str(message_id)
                channel_id = channel_id[-3:]
                emojis = ["⚔", "📢"]
                for emoji in emojis:
                    await sent_message.add_reaction(emoji)
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(
                        read_messages=False)
                }
                category = discord.utils.get(
                    message.guild.categories, name="| Match Lobbys")
                match_date_channel = match_date.strftime("%Y%m%d")
                match_channel = await message.guild.create_text_channel(name=match_date_channel+"_"+match_map+"_id_"+channel_id,
                                                                        overwrites=overwrites, category=category,
                                                                        position=1)
                overwrite_read = discord.PermissionOverwrite()
                overwrite_read.read_messages = True
                overwrite_read.add_reactions = True
                overwrite_read.send_messages = True
                overwrite_read.kick_members = True
                overwrite_read.embed_links = True
                await match_channel.set_permissions(message.author, overwrite=overwrite_read)
                embed_match_lobby_info = discord.Embed(colour=discord.Colour(0xff2021),
                                                    title="Welcome to the event of "+message.author.nick)
                embed_match_lobby_info.set_thumbnail(
                    url="https://ewa-squad.org/images/bot_logo_trans_2.png")
                embed_match_lobby_info.add_field(
                    name="**Name**", value=match_name, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Date**", value=match_date_conv, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Size**", value=match_player + "v" + match_player, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Map**", value=match_map, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Coalitions**", value=match_mixed, inline=False)
                embed_match_lobby_info.add_field(
                    name="**Server available**", value=server_info, inline=False)
                await match_channel.send(embed=embed_match_lobby_info)
                embed_user_info = discord.Embed(
                    title="Event created",
                    colour=discord.Colour(0xeaff00),
                    description="Your event has been successfully created\n\n"
                                "Don't forget, you are now able to use the following commands within the event lobby:\n\n"
                                "`!lock` : The event will be locked (sign ups are blocked)\n"
                                "`!unlock` : The event will be unlocked (this is the current status)\n"
                                "`!close` : The event will be closed permanently\n"
                                "`!tier` : The expected skill tier level\n"
                                "`!region` : The region where your team is located")
                await message.author.send(embed=embed_user_info)
                role_clanrep = discord.utils.get(
                    message.author.guild.roles, name="Clan-Rep")
                log_channel = message.guild.get_channel(898242185592438807)
                embed_log_info = discord.Embed(
                    title="A new event has been opened by " + message.author.nick,
                    colour=discord.Colour(0xff2021),
                    description="Check here: " + sent_message.jump_url)
                await log_channel.send(f'Hi {role_clanrep.mention}')
                await log_channel.send(embed=embed_log_info)

        if message.content.startswith("!region"):
            region = message.content.removeprefix('!region ')
            emoji_us = "🇺🇸"
            emoji_eu = "🇪🇺"
            emoji_asia = "🇨🇳"
            if region == "US":
                emoji = emoji_us
            if region == "EU":
                emoji = emoji_eu
            if region == "ASIA":
                emoji = emoji_asia
            permissions = message.author.permissions_in(message.channel)
            if permissions.kick_members == True:
                current_channel_name = message.channel.name[-3:]
                match_channel = message.guild.get_channel(858671467775393792)
                history = await match_channel.history(limit=250).flatten()
                for messages in history:
                    message_id = messages.id
                    message_id = str(message_id)
                    if message_id[-3:] == current_channel_name:
                        region_message_id = messages.id
                        msg = await match_channel.fetch_message(region_message_id)
                        await msg.clear_reaction(emoji_us)
                        await msg.clear_reaction(emoji_eu)
                        await msg.clear_reaction(emoji_asia)
                        await msg.add_reaction(emoji)
                        embed_user_info = discord.Embed(
                            title="Region added",
                            colour=discord.Colour(0xeaff00),
                            description="Your region has been successfully added")
                        await message.author.send(embed=embed_user_info)

        if message.content.startswith("!tier"):
            tier = message.content.removeprefix('!tier ')
            tier1 = "1️⃣"
            tier2 = "2️⃣"
            tier3 = "3️⃣"
            tier4 = "4️⃣"
            tier5 = "5️⃣"
            if tier == "1":
                emoji = tier1
            if tier == "2":
                emoji = tier2
            if tier == "3":
                emoji = tier3
            if tier == "4":
                emoji = tier4
            if tier == "5":
                emoji = tier5
            permissions = message.author.permissions_in(message.channel)
            if permissions.kick_members == True:
                current_channel_name = message.channel.name[-3:]
                match_channel = message.guild.get_channel(858671467775393792)
                history = await match_channel.history(limit=250).flatten()
                for messages in history:
                    message_id = messages.id
                    message_id = str(message_id)
                    if message_id[-3:] == current_channel_name:
                        region_message_id = messages.id
                        msg = await match_channel.fetch_message(region_message_id)
                        await msg.clear_reaction(tier1)
                        await msg.clear_reaction(tier2)
                        await msg.clear_reaction(tier3)
                        await msg.clear_reaction(tier4)
                        await msg.clear_reaction(tier5)
                        await msg.add_reaction(emoji)
                        embed_user_info = discord.Embed(
                            title="Tier level added",
                            colour=discord.Colour(0xeaff00),
                            description="Your tier level has been successfully added")
                        await message.author.send(embed=embed_user_info)

        if message.content == "!close":
            permissions = message.author.permissions_in(message.channel)
            if permissions.kick_members == True:
                current_channel_name = message.channel.name[-3:]
                match_channel = message.guild.get_channel(858671467775393792)
                history = await match_channel.history(limit=100).flatten()
                for messages in history:
                    message_id = messages.id
                    message_id = str(message_id)
                    # Datum mit abgleichen noch? Doppelabsicherung
                    if message_id[-3:] == current_channel_name:
                        deletable_message_id = messages.id
                        msg = await match_channel.fetch_message(deletable_message_id)
                        await msg.delete()
                        await message.channel.delete()
                        embed_user_info = discord.Embed(
                            title="Match closed",
                            colour=discord.Colour(0xeaff00),
                            description="Your match has been successfully closed")
                        await message.author.send(embed=embed_user_info)

        if message.content == "!lock":
            permissions = message.author.permissions_in(message.channel)
            if permissions.kick_members == True:
                current_channel_name = message.channel.name[-3:]
                match_channel = message.guild.get_channel(858671467775393792)
                history = await match_channel.history(limit=250).flatten()
                for messages in history:
                    message_id = messages.id
                    message_id = str(message_id)
                    if message_id[-3:] == current_channel_name:
                        lock_message_id = messages.id
                        msg = await match_channel.fetch_message(lock_message_id)
                        emoji_lock = "🔒"
                        emoji_sword = "⚔"
                        await msg.add_reaction(emoji_lock)
                        await msg.clear_reaction(emoji_sword)
                        # await msg.clear_reaction(emoji_sword)
                        embed_user_info = discord.Embed(
                            title="Match locked",
                            colour=discord.Colour(0xeaff00),
                            description="Your match has been successfully locked")
                        await message.author.send(embed=embed_user_info)

        if message.content == "!unlock":
            permissions = message.author.permissions_in(message.channel)
            if permissions.kick_members == True:
                current_channel_name = message.channel.name[-3:]
                match_channel = message.guild.get_channel(858671467775393792)
                history = await match_channel.history(limit=250).flatten()
                for messages in history:
                    message_id = messages.id
                    message_id = str(message_id)
                    if message_id[-3:] == current_channel_name:
                        unlock_message_id = messages.id
                        msg = await match_channel.fetch_message(unlock_message_id)
                        emoji_lock = "🔒"
                        emoji_sword = "⚔"
                        await msg.add_reaction(emoji_sword)
                        await msg.clear_reaction(emoji_lock)
                        embed_user_info = discord.Embed(
                            title="Match unlocked",
                            colour=discord.Colour(0xeaff00),
                            description="Your match has been successfully unlocked")
                        await message.author.send(embed=embed_user_info)

    async def on_raw_reaction_add(self, payload):
        user = client.get_user(payload.user_id)
        if user == client.user:
            return
        overwrite_read = discord.PermissionOverwrite()
        overwrite_read.read_messages = True
        overwrite_read.send_messages = True
        overwrite_read.add_reactions = True
        reaction_channel = client.get_channel(payload.channel_id)
        emoji = payload.emoji
        emoji = str(emoji)
        message = await reaction_channel.fetch_message(payload.message_id)
        message_id = message.id
        message_id = str(message_id)
        match_channel_id = message_id[-3:]
        channel_list = reaction_channel.guild.channels
        emoji_list = ["🔒", "📢", "1️⃣", "2️⃣",
                      "3️⃣", "4️⃣", "5️⃣", "🇺🇸", "🇪🇺", "🇨🇳"]
        for emoji_item in emoji_list:
            if emoji_item == emoji:
                await message.remove_reaction(emoji_item, user)
        if emoji == "⚔":
            for channel in channel_list:
                if channel.name.endswith(match_channel_id):
                    channel_id = channel.id
                    dest_channel = message.guild.get_channel(channel_id)
                    await dest_channel.set_permissions(user, overwrite=overwrite_read)
                    embed_user_info = discord.Embed(
                        title="Match joined",
                        colour=discord.Colour(0xeaff00),
                        description="You successfully joined the match ("+channel.name+")")
                    await user.send(embed=embed_user_info)

    async def on_raw_reaction_remove(self, payload):
        user = client.get_user(payload.user_id)
        if user == client.user:
            return
        overwrite_unread = discord.PermissionOverwrite()
        overwrite_unread.read_messages = False
        overwrite_unread.send_messages = False
        overwrite_unread.add_reactions = False
        reaction_channel = client.get_channel(payload.channel_id)
        emoji = payload.emoji
        emoji = str(emoji)
        message = await reaction_channel.fetch_message(payload.message_id)
        message_id = message.id
        message_id = str(message_id)
        match_channel_id = message_id[-3:]
        channel_list = reaction_channel.guild.channels
        if emoji == "⚔":
            for channel in channel_list:
                if channel.name.endswith(match_channel_id):
                    channel_id = channel.id
                    dest_channel = message.guild.get_channel(channel_id)
                    await dest_channel.set_permissions(user, overwrite=overwrite_unread)
                    embed_user_info = discord.Embed(
                        title="Match left",
                        colour=discord.Colour(0xeaff00),
                        description="You successfully left the match ("+channel.name+")")
                    await user.send(embed=embed_user_info)


client = MyClient(intents=intents)
client.run("OTAyNTc3NTQ5MjkxNDUwMzc4.YXgc2A.8fjRB7tupnSVv8AaL3iQq_p13jQ")
