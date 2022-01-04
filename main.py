import time
import random
import os
import discord
from datetime import datetime
from threading import Timer
import pygsheets
import pandas as pd
import urllib.request
from gtts import gTTS
import youtube_dl
import ssl
from dotenv import load_dotenv
import keep_alive
import re


load_dotenv('.env')
TimeNow = time.time()

#Authorize
#gc = pygsheets.authorize(service_file='goog-cred.json')
#ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

ydl = youtube_dl.YoutubeDL({
    'format': 'bestvideo[ext=mp4]+bestaudio',
    'outtmpl': 'musica/%(id)s.%(ext)s',
    'forceid': 'ytlink',
    'merge_output_format': 'mkv'       
})


#Text and value declarations
encryptedtext = []
encryptedvalues = []
decryptedtext = []
decryptedvalues = []


nextSong = []


#Index declarations
uppercase_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

lowercase_index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

special_index = [' ', '!', '?', '(', ')', '@', '#', '$', '%', '^', '&', '*', '_', '-', '=', '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'", '<', '>', ':', ';', '.']

confirmedEmoji = '✅'
unconfirmedEmoji = '❌'
reactionImages = ["https://cdn.discordapp.com/attachments/763590055948189696/788059504532389938/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/808126193614323732/2Q.png", "https://cdn.discordapp.com/attachments/763590055948189696/804382226309185546/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764638377246720/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764638514872320/image1.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764638687494174/image2.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764638917394463/image3.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764639102074930/image4.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764639299469382/image5.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764639509315604/image6.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764639781421126/image7.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764640025346058/image8.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764640175816774/image9.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764715270504468/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764715447582790/image1.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764715569479700/image2.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764715816157214/image3.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764715979341864/image4.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764716282380358/image5.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764716449759342/image6.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764716605472839/image7.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764716931973150/image8.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764717171441706/image9.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764799325536286/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764799559761940/image1.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764799743787039/image2.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764799874203708/image3.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764800185368597/image4.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764800386564126/image5.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764800641892372/image6.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764800788168714/image7.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764801145077790/image8.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764801459388417/image9.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764849413128192/image0.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764849639751720/image1.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764849866768454/image2.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764850147393536/image3.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764850307301376/image4.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764850570756157/image5.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764850772213770/image6.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764851111559188/image7.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764851397427210/image8.jpg", "https://cdn.discordapp.com/attachments/763590055948189696/825764851593773107/image9.jpg"
]
with open('reactionimages.txt', 'r') as rifile:
    reactionImages = [line.strip() for line in rifile]



leaveEvents = ["was not the imposter.", "was the imposter.", "failed to have the exaggerated swagger of a black teen.", "was too gay for the system to handle.", "is fucking dead.", "became a demon.", "drank the demon's blood"  ]
leaveEvent = random.choice(leaveEvents)
# Intent declaration
intents = discord.Intents.all()
client = discord.Client(intents=intents)
memberCacheFlags = discord.MemberCacheFlags.all()

@client.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.channels, name="general")
    server_join_embed = discord.Embed(title="Weeb OS", url="https://discord.gg/AfzRKsYN2H", color=000000)
    server_join_embed.set_thumbnail(url=str(client.user.avatar_url))
    server_join_embed.add_field(name="Introduction",
                                value="Hi, I'm <@!779526567877541938> — type **!help** to see what I can do for you!",
                                inline=False)
    server_join_embed.set_footer(text="Note: I'm still techincally in 'beta', so please be patient with me! : )")
    server_join_embed.set_author(name=str(guild.name), icon_url=str(guild.icon_url))
    await channel.send(embed=server_join_embed)

@client.event
async def on_member_remove(member):
    leaveEvents = [f"{member.mention} fucking died.", f"Hey {member.mention}, welcome to hell!", f"Oh dear, {member.mention} left the server. Were they important?", f"Looks like {member.mention} was not the imposter.", f"I guess {member.mention} was the imposter.",
                   f"It appears {member.mention} failed to have the exaggerated swagger of a black teen.",
                   f"{member.mention} fucking died.", f"{member.mention} spontaneously combusted", f"{member.mention} lost penis privilege", f"I'm sure {member.mention} will rest in peace, now that they don't have to get pinged by you idiots."]
    leaveEvent = random.choice(leaveEvents)
    leftuser = client.get_user(member.id)
    channel = discord.utils.get(member.guild.channels, name="general")
    #channel = client.get_channel(775941210119733269)
    #await channel.send(f"{member.mention} {leaveEvent}")
    await channel.send(leaveEvent + f" Dibs on their stuff.")
    #await leftuser.send("Alright, I guess you can come back now. Only if you REALLY want to though")

@client.event
async def on_member_join(member):

    channel = discord.utils.get(member.guild.channels, name="general")
    #channel = client.get_channel(775941210119733269)

    owneruser = client.get_user(349682083922444298)
    joinEvents = [f"It appears that {member.mention} has obtained the exaggerated swagger of a black teen.", f"{member.mention} joined Logan's cult of degeneracy.",
                 f"{member.mention} is being sponsored by Raid: Shadow Legends.", f"Welcome to the cult {member.mention}! Please do enjoy your stay.", f"{member.mention}, activate your neurons, rev up your cerebrum, and get ready for some **brain burning *bullshit!***"]
    joinEvent = random.choice(joinEvents)
    await channel.send(joinEvent + f"")

    EmmyRole_TheSimulacrum = discord.utils.get(channel.guild.roles, id=841475394850127892)
    TJRole_TheSimulacrum = discord.utils.get(channel.guild.roles, id=841475865258229790)
    CaitlinRole_TheSimulacrum = discord.utils.get(channel.guild.roles, id=841477013651062785)
    JuliaRole_TheSimulacrum = discord.utils.get(channel.guild.roles, id=841477982841470996)
    StandardRole_TheSimulacrum = discord.utils.get(channel.guild.roles, id=841473901817364490)

    EmmyRole_WeebShit = discord.utils.get(channel.guild.roles, id=783078563891904523)
    TJRole_WeebShit = discord.utils.get(channel.guild.roles, id=786328077974241291)
    CaitlinRole_WeebShit = discord.utils.get(channel.guild.roles, id=841147376696819732)
    SarahRole_WeebShit = discord.utils.get(channel.guild.roles, id=783716691753435136)
    TumiRole_WeebShit = discord.utils.get(channel.guild.roles, id=780265896974483497)
    LoganRole_WeebShit = discord.utils.get(channel.guild.roles, id=786327839908954194)
    StandardRole_WeebShit = discord.utils.get(channel.guild.roles, id=775943620448092164)
    StandardRole_WeebShitx2 = discord.utils.get(channel.guild.roles, id=841526432987348993)

    SufferRole = discord.utils.get(channel.guild.roles, id=843581737698066452)
    EmmyID = 641267423604899870
    TjID = 349682083922444298
    CaitlinID = 840804763783528460
    JuliaID = 384150359175593984
    TumiID = 196762513172463617
    SarahID = 427287857909071872
    LoganID = 251481402090979329
    if member.guild.id == 838876158208245790:
        if member.id == EmmyID:
            await member.add_roles(EmmyRole_TheSimulacrum)
        if member.id == TjID:
            await member.add_roles(TJRole_TheSimulacrum)
        if member.id == CaitlinID:
            await member.add_roles(CaitlinRole_TheSimulacrum)
        if member.id == JuliaID:
            await member.add_roles(JuliaRole_TheSimulacrum)
        await member.add_roles(StandardRole_TheSimulacrum)
    if member.guild.id == 775941209666879550:
        if member.id == EmmyID:
            await member.add_roles(EmmyRole_WeebShit)
        if member.id == TjID:
            await member.add_roles(TJRole_WeebShit)
        if member.id == CaitlinID:
            await member.add_roles(CaitlinRole_WeebShit)
        if member.id == SarahID:
            await member.add_roles(SarahRole_WeebShit)
            await member.add_roles(TumiRole_WeebShit)
        if member.id == TumiID:
            await member.add_roles(TumiRole_WeebShit)
        if member.id == LoganID:
            await member.add_roles(LoganRole_WeebShit)
        await member.add_roles(StandardRole_WeebShit)
        await member.add_roles(StandardRole_WeebShitx2)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == 838876158208245794:
        if member.guild_permissions.connect or member.id == 196762513172463617:
            vc = await after.channel.connect(reconnect=True)
            vc.pause()
            vc.play(discord.FFmpegPCMAudio("ram_ranch.mkv"))
            



@client.event
async def on_message(message):
    user = message.author
    authuser = str(message.author)
    authuserid = str(message.author.id)
    channelinuse = str(message.channel)
    if 'Direct Message' in channelinuse:
      message_server = "DM With" + authuser
    else:
      message_server = str(str(message.guild) + ' [' + str(message.guild.id) + ']')
    channelid = str(message.channel.id)
    channelinfo = str(channelinuse + ' [' + channelid + ']')
    messagecreationtime = str(message.created_at)
    messageid = str(message.id)
    messagecontent = str(message.content)
    
    message_attachment_id = ('No ID')
    message_attachment_filename = ('No File')
    message_attachment_url = ('No URL')

    if len(message.attachments) >= 1:
      for attachment in message.attachments:
        message_attachment_id = str(attachment.id)
        message_attachment_filename = str(attachment.filename)
        message_attachment_url = str(attachment.url)
      
    if len(message.embeds) >= 1:
      embeds = message.embeds
      for embed in embeds:
          message_embeds = str(embed.to_dict())
    else:
      message_embeds = 'No Embed'

    
    '''
    messagedict = {
      message_server: [' '],
      authuser: [' '],
      messagecreationtime: [' '],
      channelinfo: [' '],
      messagecontent: [' '],
      messageid: [' '],
      message_attachment_id: [' '],
      message_attachment_filename: [' '],
      message_attachment_url: [' '],
      message_embeds: [' ']
    }

    # Create empty dataf
    df = pd.DataFrame()

    # Create a column
    #df['message'] = [user, message.content, channelinuse, channelid]

    df = pd.DataFrame.from_dict(data=messagedict)
    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Oscillate Records')

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell B2. 

    dbTextFile = open('runtime.txt', 'r')
    dbValue = dbTextFile.readline()
    dbValue = int(dbValue)
    dbTextFile.close()

    wks.set_dataframe(df,(dbValue,1))
    dbTextFile = open('runtime.txt', 'w')
    dbValue = dbValue + 1
    dbTextFile.write(str(dbValue))
    dbTextFile.close()
    '''

    '''
    store = open('storage-revamp.txt', 'a', encoding='utf-8')

    print("Server: " + str(message.guild))
    store.write("Server: " + str(message.guild) + "\n")
    print("User: " + authuser + " " + authuserid )
    store.write("User: " + authuser + " "+ authuserid + "\n")
    print("Time: " + str(message.created_at))
    store.write("Time: " + str(message.created_at) + "\n")
    print("Channel: #" + channelinuse + " [" + channelid + "]")
    store.write("Channel: #" + channelinuse + " [" + channelid + "]" + "\n")
    if len(message.attachments) >= 1:
        print ("Message: " + str(message.content))
        print ("Attachment(s): " + str(message.attachments))
        print ("Message ID: " + str(message.id))
        store.write("Message: " + str(message.content) + "\n")
        store.write("Attachment(s): " + str(message.attachments) + "\n")
        store.write("Message ID: " + str(message.id) + "\n")
    elif len(message.embeds) >= 1:
        print("Message: " + str(message.content))
        store.write("Message: " + str(message.content) + "\n")
        embeds = message.embeds
        for embed in embeds:
            print("Embed(s): " + str(embed.to_dict()))
            print("Message ID: " + str(message.id))
            store.write("Embed(s): " + str(embed.to_dict()) + "\n")
            store.write("Message ID: " + str(message.id) + "\n")
    else:
        print ("Message: " + str(message.content))
        print("Message ID: " + str(message.id))
        store.write("Message: " + message.content + "\n")
        store.write("Message ID: " + str(message.id) + "\n")


    print("")
    store.write("\n")
    store.close()
    '''

    if 'damn' in message.content.lower():
        if message.channel.id == 826796405293056030:
            if message.author.id != 779526567877541938:
                await message.delete()
            await message.channel.send('***damn***')

    if message.author == client.user:
      return

    messagerandomint = random.randint(1, 1000)
    
    if messagerandomint == 25:
      await message.channel.send('https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173')

    if 'damn' in message.content.lower():
        await message.channel.send('***damn***')

    if 'Direct Message' in channelinuse:
        if authuser != 'MaximusWrath346#5386':
            user = client.get_user(196762513172463617)
            recieved_message = str(message.content)
            if len(message.attachments) >= 1:
              attachment_int = 1
              for attachment in message.attachments:
                message_attachment_filename = str(attachment.filename)
                message_attachment_url = str(attachment.url)
                await user.send(f'**{authuser}**:')
                await user.send(f'**Attachment #{attachment_int}** [{message_attachment_filename}]: {message_attachment_url}')
                attachment_int = attachment_int + 1
            await user.send(f'**{authuser}**: {recieved_message}')
            return
            
    


    '''
    if channelinuse == 'Direct Message with MaximusWrath346#5386':
        channel = client.get_channel(838876158208245793)
        message_send = message.content
        user = client.get_user(349682083922444298)
        await user.send(message_send)
    '''



    # Role Definition
    if 'Direct Message' in channelinuse:
      existingMembers = [client.user, message.author]
      msgguildid = 000000000000000000
    else:
      existingMembers = message.guild.members
      msgguildid = message.guild.id
    listedExistingMembers = []


    if message.content.lower().startswith('!invite'):
        """
        await message.channel.send("**Invite Link**")
        await message.channel.send("*(on mobile, press and hold the link below to open it)*")
        await message.channel.send(
            'https://discord.com/oauth2/authorize?client_id=779526567877541938&permissions=8&scope=bot%20applications.commands'
            '')
        await message.channel.send("**Support Server**")
        await message.channel.send("*A spot to chill out and influence my develpoment!*")
        await message.channel.send("https://discord.gg/AfzRKsYN2H")
        """
        invite_embed = discord.Embed(title="Click to Invite Me To Your Server!", url="https://discord.com/oauth2/authorize?client_id=779526567877541938&permissions=8&scope=bot%20applications.commands", color=000000)
        invite_embed.set_thumbnail(url=str(client.user.avatar_url))
        invite_embed.add_field(name="The Simulacrum", value="Join my Discord Server to influence my development!", inline=False)
        # invite_embed.add_field(name="🍵", value="matcha 〃cozy white/green theme", inline=True)
        # invite_embed.add_field(name="🧺", value="level 1 boosted", inline=False)
        # invite_embed.add_field(name="🍙", value="constantly hiring staff", inline=False)
        # invite_embed.add_field(name="🧸", value="continuously improving",inline=True)
        # invite_embed.add_field(name="Invite Link", value="https://discord.gg/Zw6xWhHuGk", inline=False)
        #invite_embed.set_image(url="https://i.imgur.com/IVHAz9o.png")
        await message.channel.send(embed=invite_embed)
        await message.channel.send("https://discord.gg/AfzRKsYN2H")
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=invite_embed)

    if message.content.lower().startswith('!ambrosial'):
        ambrosial_embed = discord.Embed(title="Join Ambrosial", url="https://discord.gg/Zw6xWhHuGk", color=discord.Color.from_rgb(87, 107, 51))
        ambrosial_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/838876158208245793/839262294155460618/image0.gif')
        #ambrosial_embed.add_field(name="Invite Link", value="https://discord.gg/Zw6xWhHuGk", inline=False)
        #ambrosial_embed.add_field(name="🍵", value="matcha 〃cozy white/green theme", inline=True)
        #ambrosial_embed.add_field(name="🧺", value="level 1 boosted", inline=False)
        #ambrosial_embed.add_field(name="🍙", value="constantly hiring staff", inline=False)
        #ambrosial_embed.add_field(name="🧸", value="continuously improving",inline=True)
        ambrosial_embed.add_field(name="🍵 ︰ matcha 〃cozy white/green theme", value="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", inline=False)
        ambrosial_embed.add_field(name="    🧺 ︰ level 3 boosted", value="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", inline=False)
        ambrosial_embed.add_field(name="🌱 ︰ abundant pfp channels", value="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", inline=False)
        ambrosial_embed.add_field(name="    🍙 ︰ constantly hiring staff", value="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", inline=False)
        ambrosial_embed.add_field(name="🧸 ︰ continuously improving ", value="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", inline=False)
        #ambrosial_embed.add_field(name="Invite Link", value="https://discord.gg/Zw6xWhHuGk", inline=False)
        ambrosial_embed.set_image(url="https://i.imgur.com/IVHAz9o.png")
        await message.channel.send(embed=ambrosial_embed)
        await message.channel.send("https://discord.gg/ambrosial")
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=ambrosial_embed)

    if message.author.id == 196762513172463617:
      if message.content.lower().startswith("***three!***"):
        await message.channel.send("**HAPPY BIRTHDAY TO YOU**")
        time.sleep(1)
        await message.channel.send("**HAPPY BIRTHDAY TO *YOU***")
        time.sleep(1)
        await message.channel.send("**HAPPY BIRTHDAY DEAR SARAH**")
        time.sleep(2)
        await message.channel.send("***HAPPY BIRTHDAY TO YOUUUUUUUUUUUUUUU***")
        await message.channel.send("https://tenor.com/view/confetti-celebrate-colorful-celebration-gif-15816997")

    if "i\'m" in message.content:
      indexLocationIM = message.content.lower().find("i\'m") + 3
      indexLocationEndIM = message.content.find(" ", indexLocationIM + 1, -1)
      print (indexLocationIM)
      print (indexLocationEndIM)
      print (message.content[indexLocationIM+1:indexLocationEndIM])

    if 'supercalifragilisticexpialidDMcius' in message.content:
        await message.channel.send("Hi! I don't really have much DM functionality right now, but my Creator is working on it!")

    if message.content.startswith("!rr") or message.content.startswith("!rollretrieve"):
        try:
            with message.channel.typing():
                mr_message = message.content
                if message.content.startswith("!rr"):
                    mr_id = mr_message.replace('!rr ', '')
                elif message.content.startswith("!rollretrieve"):
                    mr_id = mr_message.replace('!rollretrieve ', '')
                channel = message.channel
                new_mr_message = await channel.fetch_message(mr_id)
                for embed in new_mr_message.embeds:
                    await channel.send(str(embed.to_dict()))
                #await message.channel.send(message.content)
        except:
            await message.channel.send("Error: Message has to be from this channel.")
    if message.content.startswith("!mr") or message.content.startswith("!messageretrieve"):
        try:
            with message.channel.typing():
                mr_message = message.content
                if message.content.startswith("!mr"):
                    mr_id = mr_message.replace('!mr ', '')
                elif message.content.startswith("!messageretrieve"):
                    mr_id = mr_message.replace('!messageretrieve ', '')
                channel = message.channel
                new_mr_message = await channel.fetch_message(mr_id)
                await message.channel.send("Server: " + str(new_mr_message.guild))
                await message.channel.send("User: " + str(new_mr_message.author))
                await message.channel.send("Time: " + str(new_mr_message.created_at))
                await message.channel.send("Channel: #" + str(new_mr_message.channel) + " [" + str(new_mr_message.channel.id) + "]")
                print ("Message: " + str(new_mr_message.content))
                if str(new_mr_message.content) == (""):
                    await message.channel.send("Message: " + "**This message had no content**")
                else:
                    await message.channel.send("Message: " + str(new_mr_message.content))
                for attachment in new_mr_message.attachments:
                    await message.channel.send("Attachment(s): " + "\n" + str(message.attachments))
                for embed in new_mr_message.embeds:
                    await message.channel.send("Embed(s): " + "\n" + str(embed.to_dict()))
        except:
            await message.channel.send("Error: Message has to be from this channel.")
    if message.content.startswith('Hey son'):
        await message.channel.send('Hi Dad!')
    if message.content.startswith('hey son'):
        await message.channel.send('Hi Dad!')
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    if message.content.lower().startswith('gn'):
        await message.channel.send('Goodnight!')
    if message.content.lower().startswith('goodnight'):
        await message.channel.send('Goodnight!')
    if message.content.lower().startswith('good night'):
        await message.channel.send('Goodnight!')
    if message.content.startswith('!imposterverse'):
        await message.channel.send('We serve God whether people honor us or despise us, whether they slander us '
                                       'or praise us. We are honest, but they call us imposters.')
        await message.channel.send('2 Corinthians 6:8 (NLT)')
    if message.content.startswith('!crewmateverse'):
        await message.channel.send('Have I now become your enemy because I am telling you the truth?')
        await message.channel.send('Galatians 4:16 (NLT)')
    

    
    if message.content.lower().startswith('!purge'):
      if message.author.guild_permissions.manage_messages or message.author.id == 196762513172463617:
        purgeRequest = message.content
        purgeLimit = purgeRequest.replace('!purge ', '')
        purgenotifier = await message.channel.send('Purging in ***3***')
        time.sleep(1)
        await purgenotifier.edit(content='Purging in ***2***')
        time.sleep(1)
        await purgenotifier.edit(content='Purging in ***1***')
        purgeCommand = await message.channel.purge(limit=int(purgeLimit) + 4)
        #store = open('storage-revamp.txt', 'a', encoding='utf-8')
        #print("Purge: " + str(purgeCommand))
        purgeCount = ('Purge: Deleted {} message(s)'.format(len(purgeCommand)))
        await message.channel.send(content=purgeCount, delete_after=3)
        #store.write("Server: " + str(message.guild) + "\n")
        print("")
        #store.write("\n")
        #store.close()


    if 'debit card' in message.content:
        await message.channel.send('NO WAYYY')
        await message.channel.send('WHEN???')
    if 'Debit card' in message.content:
        await message.channel.send('NO WAYYY')
        await message.channel.send('WHEN???')
    if 'Debit Card' in message.content:
        await message.channel.send('NO WAYYY')
        await message.channel.send('WHEN???')
    if 'DEBIT CARD' in message.content:
        await message.channel.send('NO WAYYY')
        await message.channel.send('WHEN???')
    if message.content.startswith('over a year ago probably'):
        await message.channel.send('what was a year ago?')
    if message.content.startswith('a year ago probably'):
        await message.channel.send('what was a year ago?')
    if message.content.startswith('about a year ago probably'):
        await message.channel.send('what was a year ago?')
    if message.content.startswith('over a year ago'):
        await message.channel.send('what was a year ago?')
    if message.content.startswith('about a year ago'):
        await message.channel.send('what was a year ago?')
    if message.content.startswith('a year ago'):
        await message.channel.send('what was a year ago?')


    if message.author.id == 224988545402535936 or '😐' in message.content or message.author.id == 840804763783528460:
        await message.add_reaction('😐')
        await message.reply('😐')

    if 'Doug Dimmadome' in message.content:

        await message.channel.send( 'Doug Dimmadome?')
        await message.channel.send('Owner of the Dimmsdale Dimmadome?')

    if message.content.startswith('Yes, Doug Dimmadome, owner of the Dimmsdale Dimmadome'):
        await message.channel.send('Ah yes, Doug Dimmadome')
        await message.channel.send('Owner of the Dimmsdale Dimmadome')


    susReasons = ["vented.", "vented right in front of me.", "faked trash.", "faked asteroids.",
                  "killed right in front of me.", "were standing on the body.", "dissapeared while lights were off.",
                  "have been following me.", "haven't done any tasks.", "were the only person not with us.",
                  "took too long to slide their card.", "didn't do download for long enough.",
                  "didn't do upload for long enough.", "faked medbay."]
    susReasoning = random.choice(susReasons)
    

    if message.content.startswith('!birthtime'):
        await message.channel.send(message.author.created_at)

    if message.content.startswith('!sus'):
      randomMember = random.choice(message.guild.members)
      await message.channel.send(
          f'{randomMember.mention} is kinda sus, they {susReasoning}')

    
    if message.content.startswith('!members'):
      if message.author.guild_permissions.manage_nicknames or message.author.id == 196762513172463617:
          for member in message.guild.members:
              listedExistingMembers.append(member.name)
          sortedExistingMembers = sorted(listedExistingMembers, key=str.lower)
          memberListLength = len(sortedExistingMembers)
          for i in range(memberListLength):
              await message.channel.send(sortedExistingMembers[i])

    if message.content.startswith('!dadjoke'):
      with open('dad_jokes.txt', 'r') as djfile:
        dadJokes = [line.strip() for line in djfile]
      with message.channel.typing():
            chosenDadJoke = random.choice(dadJokes)
            dadjokenumber = dadJokes.index(chosenDadJoke) + 1
            user_pfp = str(message.author.avatar_url)
            dadjoke_embed = discord.Embed(color=000000)
            dadjoke_embed.add_field(name=("**Dad Joke #" + str(dadjokenumber) + "**"), value=chosenDadJoke, inline=False)
            dadjoke_embed.set_author(name=client.user.name, icon_url=(client.user.avatar_url))
            dadjoke_embed.set_footer(text=f"Dad Joke requested by {message.author}")
            dadjoke_embed.timestamp = datetime.now()
            await message.channel.send(embed=dadjoke_embed)
      


    if '**LittleHanger** and' in message.content:
        await message.channel.send("Hey Logan? Fuck you. That is all. Maybe you did something, maybe you didn't, but this is a preemptive measure.")
        await message.channel.send('-Tumi')

    if 'japanese cartoon' in message.content.lower():
        await message.channel.send('Shut it weeb')
    if 'gay' in message.content.lower():
        if message.author.id == 196762513172463617:
            if 'not gay' in message.content.lower():
                await message.channel.send('True that is indeed very much not gay.')
            else:
                await message.channel.send('Yes, very much gay')

        else:
            await message.channel.send('Yes, yes, we all know how gay you are now shut up')

    if 'am illiterate' in message.content.lower():
        await message.channel.send('Then go back to grade school')

    if message.content.startswith('!telltalegame'):
        await message.delete()
        await message.channel.send(f'{message.author.mention} *will remember that.*')


    if 'Am Illiterate' in message.content:
        await message.channel.send('Then go back to grade school')



    
    if message.content.startswith('!missileguidance'):
      if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            missileguidance = open('missileguidance.txt', 'r')
            missile_contents = missileguidance.read()
            for chunk in [missile_contents[i:i + 2000] for i in range(0, len(missile_contents), 2000)]:
                await message.channel.send(chunk)
            missileguidance.close()

    
    if message.content.startswith('!beemovie-reg'):
      if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
        with message.channel.typing():
          beemoviescript = open('thebeemoviescript.txt', 'r')
          beemovie_contents = beemoviescript.read()
        for chunk in [beemovie_contents[i:i + 2000] for i in range(0, len(beemovie_contents), 2000)]:
          await message.channel.send(chunk)
        beemoviescript.close()

    
    if message.content.startswith('!beemovie-atb'):
        if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            with message.channel.typing():
                beemoviescript = open('thebeemoviescript.txt', 'r')
                beemovie_contents = beemoviescript.read()
                for chunk in [beemovie_contents[i:i + 2000] for i in range(0, len(beemovie_contents), 2000)]:
                    #await message.channel.send(chunk)
                    message_object = message
                    encryptedtext = []
                    encryptedvalues = []
                    atbashcmdtext = message.content
                    if message.content.lower().startswith("!atbashencrypt"):
                        plain_text = atbashcmdtext.replace("!atbashencrypt ", '')
                    if message.content.lower().startswith("!atbe"):
                        plain_text = atbashcmdtext.replace("!atbe ", '')
                    plain_text = chunk
                    for eachletter in plain_text:
                        if eachletter in uppercase_index:
                            crypt = uppercase_index.index(eachletter)
                            encryption = ((0 + 25) - crypt)
                            encryptedvalues.append(encryption)
                            newcharacter = uppercase_index[encryption]
                            encryptedtext.append(newcharacter)
                        elif eachletter in lowercase_index:
                            crypt = lowercase_index.index(eachletter)
                            encryption = ((0 + 25) - crypt)
                            encryptedvalues.append(encryption)
                            newcharacter = lowercase_index[encryption]
                            encryptedtext.append(newcharacter)
                        elif eachletter in special_index:
                            crypt =  special_index.index(eachletter)
                            encryption = ((0 + 25) - crypt)
                            encryptedvalues.append(encryption)
                            newcharacter = special_index[encryption]
                            encryptedtext.append(newcharacter)
                    con_encryptedtext = ''.join(encryptedtext)
                    emoji = '✅'
                    await message.channel.send(con_encryptedtext)
                    await message_object.add_reaction(emoji)
                beemoviescript.close()

    
    if message.content.startswith('!morpheus'):
      if message.author.guild_permissions.send_messages or message.author.id == 196762513172463617:
            print(os.getcwd())
            morpheusscript = open('morpheus.txt', 'r')
            morpheus_contents = morpheusscript.read()
            for chunk in [morpheus_contents[i:i + 2000] for i in range(0, len(morpheus_contents), 2000)]:
                await message.channel.send(chunk)
            morpheusscript.close()

    
    if message.content.startswith('!morpheusvideo'):
      if message.author.guild_permissions.send_messages or message.author.id == 196762513172463617:
            await message.channel.send('https://youtu.be/r9B7BQWnZJs')


    if message.content.lower().startswith("!rptest"):
      #rp_message = str(message.content)
      #rp_id = rp_message.replace('!rolepermissions ', '')
      #testRole = discord.utils.get(message.channel.guild.roles, id=rp_id)
      if message.author.guild_permissions.manage_roles:
        await message.channel.send('You can manage roles.')
      else:
        await message.channel.send('You cannot manage roles.')




    if "!mmrk" in message.content:
        for emoji in message.guild.emojis:
            print(emoji.id)
        kakera = client.get_emoji(id=839516312032378910)
        wright = client.get_emoji(id=839520610898935809)
        wleft = client.get_emoji(id=839520611512090644)
        fmr_embed = discord.Embed(title="", color=6753288, description=f'\u200b\n**AVG:** 5403\n**Top 15 value:** 375\n\nHarem value: **119994**{kakera}\n\n**#1** - Zero Two **1681 ka**\n**#4** - Mai Sakurajima **1583 ka**\n**#6** - Mikasa Ackerman **1576 ka**\n**#7** - Asuna **1606 ka**\n**#10** - Saber **1526 ka**\n**#11** - Chika Fujiwara **1473 ka**\n#**19** - Akame **1418 ka**\n**#20** - Shinobu Kochou **1293 ka**\n**#23** - Kaguya Shinomiya **1302 ka**\n#**27** - Rin Tohsaka **1270 ka**\n**#31** - Ai Hayasaka **1124 ka**\n#**35** - Rikka Takanashi **1108 ka**\n**#37** - Esdeath **1203 ka**\n**#45** - Killua Zoldyck **1275 ka**\n**#53** - Taiga Aisaka **1031 ka**')
        fmr_embed.set_author(name="h1238's harem", icon_url="https://cdn.discordapp.com/avatars/349682083922444298/10e5e02f8a267160c774568cfcc15ed9.webp")
        fmr_embed.set_thumbnail(url="https://imgur.com/fqbFdYD.png")
        fmr_embed.set_footer(text="Page 1 / 35")
        message = await message.channel.send(embed=fmr_embed)
        await message.add_reaction(wright)
        await message.add_reaction(wleft)

    if message.content.lower().startswith("!im raphtalia"):
        for emoji in message.guild.emojis:
            print(emoji.id)
        kakera = client.get_emoji(id=839516312032378910)
        wright = client.get_emoji(id=839520610898935809)
        wleft = client.get_emoji(id=839520611512090644)
        female = client.get_emoji(id=839581973261189155)
        faux_raph_embed = discord.Embed(color=6753288, title="Raphtalia", description=f"Tate no Yuusha no Nariagari {female}\nAnimanga roulette · **1267**{kakera}\nClaim Rank: #33\nLike Rank: #36\nNaofumi's Sword (+3)")
        faux_raph_embed.set_footer(text="Belongs to h1238 ~~ 1 / 29", icon_url="https://cdn.discordapp.com/avatars/349682083922444298/10e5e02f8a267160c774568cfcc15ed9.webp")
        faux_raph_embed.set_image(url="https://media.discordapp.net/attachments/472313197836107780/747577748167459017/qIr2ud9.png")
        message = await message.channel.send(embed=faux_raph_embed)
        await message.add_reaction(wright)
        await message.add_reaction(wleft)

    if message.content.lower().startswith('!help'):
        help_embed = discord.Embed(title="Help Menu", color=000000, url="https://discord.gg/ambrosial")
        help_embed.set_author(name=message.author, icon_url=str(message.author.avatar_url))
        help_embed.add_field(name="ban <mention>", value="Bans the mentioned user",inline=False)
        help_embed.add_field(name="beemovie", value="Sends the entirety of the bee movie script from beginning to end (Only available to authorized users)", inline=False)
        help_embed.add_field(name="birthtime", value="Sends the date and time your discord account was made", inline=False)
        help_embed.add_field(name="changepresencelistening <Activity>", value=" Changes the bot's presence to listening to the set activity", inline=False)
        help_embed.add_field(name="changepresenceplaying <Activity>", value="Changes the bot's presence to playing the set activity", inline=False)
        help_embed.add_field(name="changepresencestreaming <Activity>", value="Changes the bot's presence to streaming the set activity", inline=False)
        help_embed.add_field(name="changepresencewatching <Activity>", value="Changes the bot's presence to watching the set activity", inline=False)
        help_embed.add_field(name="crewmateverse", value="Sends a verse from the bible I deemed related to being a crewmate", inline=False)
        help_embed.add_field(name="help", value="Sends the list of commands", inline=False)
        help_embed.add_field(name="imposterverse", value="Sends a verse from the bible I deemed related to being an imposter", inline=False)
        help_embed.add_field(name="invite", value="Invite the bot to your Discord server, or join the testing range", inline=False)
        help_embed.add_field(name="kick <mention>", value="Kicks the mentioned user", inline=False)
        help_embed.add_field(name="members", value="Sends an alphabetical list of all members of the discord server", inline=False)
        help_embed.add_field(name="messageretrieve <message id> (!mr)", value="Retrieves Server, User, Time, Channel, and Time of the message", inline=False)
        help_embed.add_field(name="missileguidance", value="Sends the entire missile guidance copypasta", inline=False)
        help_embed.add_field(name="morpheus", value="Sends the lyrics for the morpheus song sung by Hannibal Buress on The Eric Andre Show", inline=False)
        help_embed.add_field(name="morpheusvideo", value="Sends a link to a video of Hannibal Buress singing his morpheus song, as well as the lyrics", inline=False)
        help_embed.add_field(name="mr <message id>", value="Retrieves the embeds from the message chosen (Use Discord Developer Mode to get IDs", inline=False)
        help_embed.add_field(name="opus", value="Dev function relating to voice", inline=False)
        help_embed.add_field(name="pfp", value="Check your user profile picture in greater detail", inline=False)
        help_embed.add_field(name="reactionimage (!ri)", value="Sends a random reaction image that may or may not match your current secnario (Currently contains 35+ different images)", inline=False)
        help_embed.add_field(name="rngvote", value="Mentions a random member of the server to vote out", inline=False)
        help_embed.add_field(name="rollretrieve <message id> (!rr)", value="Retrieves embed info from a mudae roll (also works for any embed in general)", inline=False)
        help_embed.add_field(name="speak <message>", value="Deletes original command and sends the contents of the message that contained this command (Minus the command itself)", inline=False)
        help_embed.add_field(name="sus", value="Gives a random person to be suspicious of, aswell as a reason", inline=False)
        help_embed.add_field(name="telltalegame", value="Delivers a message akin to the popups often found in telltale games", inline=False)
        help_embed.add_field(name="time", value="Sends a message of the current date and time", inline=False)
        help_embed.add_field(name="vcjoin", value="Adds the bot to your current connected voice channel (No full voice funcitonality yet)", inline=False)
        help_embed.add_field(name="vcleave", value="Removes the bot from your current connected voice channel (No full voice funcitonality yet)", inline=False)
        help_embed.add_field(name="wlcounter", value="Counts, and sends, the number of wishlist mudae characters obtained by weeb shit members", inline=False)
        help_embed.set_footer(text="Tip: My prefix is !")
        await message.channel.send(embed=help_embed)
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=help_embed)

    
    if message.content.startswith('!cmdspeak'):
        if message.author.guild_permissions.send_messages or message.author.id == 196762513172463617:
            await message.delete()
            speech = input('What would you like to say? \n')
            print('')
            await message.channel.send(speech)



    if 'pain' in message.content.lower():
        await message.channel.send('https://cdn.discordapp.com/attachments/775944001148813332/804373905501716541/Z.png')

    if ' man' in message.content.lower() or 'man ' in message.content.lower() or ' man ' in message.content.lower():
        if 'my man' in message.content.lower():
            await message.channel.send('https://cdn.discordapp.com/attachments/775944001148813332/804373419751112716/Z.png')
        else:
            await message.channel.send('https://cdn.discordapp.com/attachments/775944001148813332/804373460394442772/Z.png')

    if 'trolling' in message.content.lower() or 'troll' in message.content.lower() or 'deez what' in message.content.lower() or 'whos deez' in message.content.lower() or "who's deez" in message.content.lower():
        await message.channel.send("https://tenor.com/view/troll-pilled-gif-19289988")

    if message.content.lower().startswith('!reactionimage'):
        await message.delete()
        with message.channel.typing():
            chosenReactionImage = random.choice(reactionImages)
            user_pfp = str(message.author.avatar_url)
            ri_embed = discord.Embed(color=000000)
            ri_embed.set_image(url=chosenReactionImage)
            ri_embed.set_author(name=client.user.name, icon_url=(client.user.avatar_url))
            ri_embed.set_footer(text=f"Reaction image requested by {message.author}")
            await message.channel.send(embed=ri_embed)
            if 'Direct Message' in channelinuse:
              user = client.get_user(196762513172463617)
              await user.send(f'**{authuser}**: (Sent This Embed)')
              await user.send(embed=ri_embed)

    if message.content.lower().startswith('!ri'):
        await message.delete()
        with message.channel.typing():
            chosenReactionImage = random.choice(reactionImages)
            user_pfp = str(message.author.avatar_url)
            ri_embed = discord.Embed(color=000000)
            ri_embed.set_image(url=chosenReactionImage)
            ri_embed.set_author(name=client.user.name, icon_url=(client.user.avatar_url))
            ri_embed.set_footer(text=f"Reaction image requested by {message.author}")
            await message.channel.send(embed=ri_embed)
            if 'Direct Message' in channelinuse:
              user = client.get_user(196762513172463617)
              await user.send(f'**{authuser}**: (Sent This Embed)')
              await user.send(embed=ri_embed)

    if message.content.lower().startswith('i need a reaction image'):
        await message.delete()
        chosenReactionImage = random.choice(reactionImages)
        user_pfp = str(message.author.avatar_url)
        ri_embed = discord.Embed(color=000000)
        ri_embed.set_image(url=chosenReactionImage)
        ri_embed.set_author(name=str(message.author), icon_url=(user_pfp))
        ri_embed.set_footer(text=f"Reaction image requested by {message.author}")
        await message.channel.send(embed=ri_embed)
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=ri_embed)

    if message.content.lower().startswith('!pfp'):
        if len(message.content) > 5:
          pfp_request = message.content
          pfp_request = pfp_request.replace('!pfp', '')
          pfp_request = pfp_request.replace('<@!', '')
          pfp_request = pfp_request.replace('>', '')
          pfp_request = pfp_request.replace(' ', '')
          user_object = message.guild.get_member(int(pfp_request))
          user_pfp = str(user_object.avatar_url)
          pfp_embed = discord.Embed(color=000000)
          pfp_embed.set_thumbnail(url=str(user_pfp))
          await message.channel.send(embed=pfp_embed)
        else:
          user_pfp = str(message.author.avatar_url)
          pfp_embed = discord.Embed(color=000000)
          pfp_embed.set_thumbnail(url=str(message.author.avatar_url))
          await message.channel.send(embed=pfp_embed)
    

    if 'is for me' in message.content.lower():
        await message.channel.send('https://cdn.discordapp.com/attachments/763590055948189696/804382226309185546/image0.jpg')

    if 'https://cdn.discordapp.com/attachments/838876158208245793/839638331658993714/image0.jpg' in message.content.lower():
        await message.channel.send("That's kinda hot.")

    
    if message.content.startswith('!speak'):
      if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            with message.channel.typing():
                speech = message.content
                speak = speech.replace('!speak', '')
                await message.delete()
                await message.channel.send(speak)
                return


    elif message.content.lower().startswith("!atbashencrypt") or message.content.lower().startswith("!atbe"):
        message_object = message
        encryptedtext = []
        encryptedvalues = []
        atbashcmdtext = message.content
        if message.content.lower().startswith("!atbashencrypt"):
            plain_text = atbashcmdtext.replace("!atbashencrypt ", '')
        if message.content.lower().startswith("!atbe"):
            plain_text = atbashcmdtext.replace("!atbe ", '')
        for eachletter in plain_text:
            if eachletter in uppercase_index:
                crypt = uppercase_index.index(eachletter)
                encryption = ((0 + 25) - crypt)
                encryptedvalues.append(encryption)
                newcharacter = uppercase_index[encryption]
                encryptedtext.append(newcharacter)
            elif eachletter in lowercase_index:
                crypt = lowercase_index.index(eachletter)
                encryption = ((0 + 25) - crypt)
                encryptedvalues.append(encryption)
                newcharacter = lowercase_index[encryption]
                encryptedtext.append(newcharacter)
            elif eachletter in special_index:
                crypt =  special_index.index(eachletter)
                encryption = ((0 + 25) - crypt)
                encryptedvalues.append(encryption)
                newcharacter = special_index[encryption]
                encryptedtext.append(newcharacter)
        con_encryptedtext = ''.join(encryptedtext)
        emoji = '✅'
        atbe_embed = discord.Embed(title="Encryption Protocol - Atbash Cipher", color=000000, url="", )
        atbe_embed.set_footer(text=f"Encryption requested by {message.author}", icon_url=str(message.author.avatar_url))
        atbe_embed.add_field(name="Original Message", value=plain_text, inline=False)
        atbe_embed.add_field(name="Encrypted Message", value=con_encryptedtext, inline=False)
        #atbd_embed.set_author(name="Decryption Protocol - Atbash Cipher")
        atbe_embed.set_thumbnail(url=str(client.user.avatar_url))
        #await message.channel.send(con_decryptedtext)
        await message.channel.send(embed=atbe_embed)
        await message_object.add_reaction(emoji)
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=atbe_embed)

    elif message.content.lower().startswith("!atbashdecrypt") or message.content.lower().startswith("!atbd"):
        message_object = message
        decryptedtext = []
        decryptedvalues = []
        atbashcmdtext = message.content
        if message.content.lower().startswith("!atbashdecrypt"):
            cipher_text = atbashcmdtext.replace("!atbashdecrypt ", '')
        if message.content.lower().startswith("!atbd"):
            cipher_text = atbashcmdtext.replace("!atbd ", '')
        for eachletter in cipher_text:
            if eachletter in uppercase_index:
                decipher = uppercase_index.index(eachletter)
                decryption = ((0+ 25) - decipher)
                decryptedvalues.append(decryption)
                newcharacter = uppercase_index[decryption]
                decryptedtext.append(newcharacter)
            elif eachletter in lowercase_index:
                decipher = lowercase_index.index(eachletter)
                decryption = ((0+ 25) - decipher)
                decryptedvalues.append(decryption)
                newcharacter = lowercase_index[decryption]
                decryptedtext.append(newcharacter)
            elif eachletter in special_index:
                decipher =  special_index.index(eachletter)
                decryption = ((0 + 25) - decipher)
                decryptedvalues.append(decryption)
                newcharacter = special_index[decryption]
                decryptedtext.append(newcharacter)
        con_decryptedtext = ''.join(decryptedtext)
        emoji = '✅'
        atbd_embed = discord.Embed(title="Decryption Protocol - Atbash Cipher", color=000000, url="", )
        atbd_embed.set_footer(text=f"Decryption requested by {message.author}", icon_url=str(message.author.avatar_url))
        atbd_embed.add_field(name="Original Message", value=cipher_text, inline=False)
        atbd_embed.add_field(name="Decrypted Message", value=con_decryptedtext, inline=False)
        #atbd_embed.set_author(name="Decryption Protocol - Atbash Cipher")
        atbd_embed.set_thumbnail(url=str(client.user.avatar_url))
        #await message.channel.send(con_decryptedtext)
        await message.channel.send(embed=atbd_embed)
        await message_object.add_reaction(emoji)
        if 'Direct Message' in channelinuse:
          user = client.get_user(196762513172463617)
          await user.send(f'**{authuser}**: (Sent This Embed)')
          await user.send(embed=atbd_embed)

    
    
    if message.content.lower().startswith('!ga'):
        if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
          givestuffmessage = message.content
          givestuffmessagebreakdown = givestuffmessage.replace('!ga', '')
          givelist = open('givelist.txt', 'a')
          givelist.write(givestuffmessagebreakdown + "\n")
          givelist.close()
          emoji = '✅'
          await message.add_reaction(emoji)

    
    if message.content.lower().startswith('!gr'):
        if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            giveremovemessage = message.content
            giveremovemessagebreakdown = giveremovemessage.replace('!gr', '')
            givelist = open('givelist.txt', 'r')
            if giveremovemessagebreakdown in givelist.read():
                lines = givelist.readlines()
                givelist.close()
                givelist = open('givelist.txt', 'a')
                for line in lines:
                    if line.strip("\n") == giveremovemessagebreakdown:
                        linetoberemoved = False
                    else:
                        givelist.write(line)
                givelist.close()
                emoji = '✅'
                await message.add_reaction(emoji)

    
    if message.content.startswith('!gl'):
      if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            givelist = open('givelist.txt', 'r')
            givelistcontent = givelist.read()
            for chunk in [givelistcontent[i:i + 2000] for i in range(0, len(givelistcontent), 2000)]:
                await message.channel.send(chunk)
            givelist.close()
            emoji = '✅'
            await message.add_reaction(emoji)



    
    if message.content.lower().startswith('!kick'):
      if message.author.guild_permissions.kick_members or message.author.id == 196762513172463617:
            kickrequestmessage = message.content
            kickrequesttype = kickrequestmessage[6:9]
            kickrequest_userID = kickrequestmessage[13:31]
            kickrequest_reason = kickrequestmessage[33:]
            await message.delete()
            if kickrequesttype == 'reg':
                kickrequestuser = message.guild.get_member(int(kickrequest_userID))
                await message.guild.kick(user=kickrequestuser, reason=kickrequest_reason)
            elif kickrequesttype == 'inv':
              if message.author.guild_permissions.create_instant_invite or message.author.id == 196762513172463617:
                kickrequestuser = message.guild.get_member(int(kickrequest_userID))
                kickinv = await message.channel.create_invite(max_uses=1)
                user = client.get_user(int(kickrequest_userID))
                await user.send(str(kickinv))
                await user.send('https://cdn.discordapp.com/attachments/839232652962824192/873337972639035442/video0.mov')
                await message.guild.kick(user=kickrequestuser, reason=kickrequest_reason)
            else:
                kickrequestmessage = message.content
                kickrequest_reason = kickrequestmessage[29:]
                kickrequest_userID = kickrequestmessage[9:27]
                kickrequestuser = message.guild.get_member(int(kickrequest_userID))
                user = client.get_user(int(kickrequest_userID))
                await user.send('https://cdn.discordapp.com/attachments/839232652962824192/873337972639035442/video0.mov')
                await message.guild.kick(user=kickrequestuser, reason=kickrequest_reason)
            await message.channel.send(f"And {kickrequestuser.mention} got kicked! Imagine getting kicked. What a fucking idiot.")


    if message.content.lower().startswith('!ban'):
        if message.author.guild_permissions.ban_members or message.author.id == 196762513172463617:
            banrequest = message.content
            banrequest = banrequest.replace('!ban ', '')
            banrequest = banrequest.replace('<@!', '')
            banrequest = banrequest.replace('>', '')
            await message.delete()
            banrequestuser = message.guild.get_member(int(banrequest))
            await message.guild.ban(banrequestuser)

    if message.author.id == 196762513172463617:
        if message.content.startswith('!changepresenceplaying'):
            presencecontent = message.content
            playingpresence = presencecontent.replace('!changepresenceplaying', '')
            await message.delete()
            cmdplayingpresence = discord.Activity(type=discord.ActivityType.playing, name=playingpresence)
            await client.change_presence(activity=cmdplayingpresence)

    if message.author.id == 196762513172463617:
        if message.content.startswith('!changepresencelistening'):
            listeningcontent = message.content
            listeningpresence = listeningcontent.replace('!changepresencelistening', '')
            await message.delete()
            cmdlisteningpresence = discord.Activity(type=discord.ActivityType.listening, name=listeningpresence)
            await client.change_presence(activity=cmdlisteningpresence)

    if message.author.id == 196762513172463617:
        if message.content.startswith('!changepresencewatching'):
            watchingcontent = message.content
            watchingpresence = watchingcontent.replace('!changepresencewatching', '')
            await message.delete()
            cmdwatchingpresence = discord.Activity(type=discord.ActivityType.watching, name=watchingpresence)
            await client.change_presence(activity=cmdwatchingpresence)

    if message.author.id == 196762513172463617:
        if message.content.startswith('!changepresencestreaming'):
            streamingcontent = message.content
            streamingpresence = streamingcontent.replace('!changepresencestreaming', '')
            await message.delete()
            cmdstreamingpresence = discord.Activity(type=discord.ActivityType.streaming, name=streamingpresence)
            await client.change_presence(activity=cmdstreamingpresence)


    if message.content.lower().startswith('$ci'):
        await message.delete()

    if message.content.startswith('among us tonight'):
        await message.channel.send('No, now shut it.')
    if message.content.startswith('we playing tonight?'):
        await message.channel.send('No, now shut it.')
    if message.content.startswith('We playing tonight?'):
        await message.channel.send('No, now shut it.')
    if 'are we playing tonight?' in message.content:
        await message.channel.send('No, now shut it.')
    if 'are we playing today?' in message.content:
        await message.channel.send('No, now shut it.')
    if 'anyone wanna play among us tonight?' in message.content:
        await message.channel.send('No, now shut it.')

    if message.author.id == 251481402090979329:
        if message.content.lower().startswith('$wish megumin'):
            await message.channel.send("ALERT! ALERT! LOGAN IS BEING A FUCKWAD")
            await message.channel.send('<@!196762513172463617>')
            await message.channel.send("ALERT! ALERT! LOGAN IS BEING A FUCKWAD")
            await message.channel.send('<@!196762513172463617>')
            await message.channel.send("ALERT! ALERT! LOGAN IS BEING A FUCKWAD")
            await message.channel.send('<@!196762513172463617>')
        if 'cuck' in message.content:
            await message.channel.send('Dictionary Definition:'
                                       'DEROGATORY•INFORMAL'
                                       '1. a weak or servile man (often used as a contemptuous term for a man with moderate or progressive political views).'
                                       '2. a man whose wife is sexually unfaithful; a cuckold.')
            await message.channel.send('Urban Definition:'
                                        'A man who lets his wife or girlfriend have sex with other men. Often the man lets her do whatever she wants and treat him like shit.'
                                        '(Short version of cuckold)')




    if 'dang' in message.content.lower():
        await message.channel.send('***dang***')

    if 'darn' in message.content.lower():
        await message.channel.send('***darn***')

    if 'fortnite' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason='No Fortnite.')
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'Fortnite' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason='No Fortnite.')
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'FORTNITE' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason='No Fortnite.')
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

 
    if 'dibs' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Logan Told Me To")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'Dibs' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Logan Told Me To")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if '_' in message.content:
        if message.author.id == 251481402090979329:
            await message.channel.send('https://cdn.discordapp.com/attachments/763590055948189696/808126193614323732/2Q.png')

    if 'one piece' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if '0ne p1ece' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')


    if '1piece' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if '1Piece' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'one peice' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'one b °C' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if ' ice ' in message.content.lower():
        await message.channel.send(':cold_face:')

    if message.content.startswith('!suicide'):
        await user.kick()
        await message.channel.send('https://cdn.discordapp.com/attachments/775943975055130625/795858624656048128/image0.jpg')

    if message.content.startswith('op'):
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'On3 P13c3' in message.content:
        if message.author.id == 224988545402535936:
            await user.kick()
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'ur mom' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Please don't kill me.")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')


    if 'Ur Mom' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Please don't kill me.")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'ur Mom' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Please don't kill me.")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'Ur mom' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Please don't kill me.")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if 'UR MOM' in message.content:
        if message.author.id != 196762513172463617:
            await user.kick(reason="Please don't kill me.")
            await message.channel.send('https://cdn.discordapp.com/attachments/788121984327745546/788122182789365780/image1.jpg')

    if message.content.startswith('https://cdn.discordapp.com/attachments/775944103397163028/785673887484608532/unknown.png'):
        await message.delete()

    if message.content.startswith('https://tenor.com/view/kirbo-mode-marshmallows-eating-gif-14666697'):
        await message.delete()

    if 'shrek' in message.content:
        await message.channel.send('Shrek is love. Shrek is life.')


    if 'Shrek' in message.content:
        await message.channel.send('Shrek is love. Shrek is life.')

    if 'coffee' in message.content:
        await message.channel.send('mmm coffee')

    if message.content.startswith('!opuscheck'):
        await message.channel.send('Opus library is active.')


    if '!connect' in message.content:
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        vc = await message.author.voice.channel.connect(reconnect=True)
        await message.add_reaction(confirmedEmoji)


    
    if '!disconnect' in message.content:
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        channel = message.author.voice.channel
        server = message.guild.voice_client
        for x in client.voice_clients:
          if(x.guild == message.guild):
            await x.disconnect()
            await message.add_reaction(confirmedEmoji)
    """
    if message.content.startswith('!vcyt'):
      if message.author.guild_permissions.move_members or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          ytsRequest = message
          ytCommand = message.content
          ytURL = ytCommand.replace('!vcyt ', '')
          ytURLFileName = ytURL[-11:]
          print (ytURLFileName)
          ytURLFileName = 'musica/' + ytURLFileName + '.mkv'
          ytconversionmsg = await message.channel.send('**Downloading YouTube Video...**')
          with ydl:
            ydl.download([ytURL])
            info_dict = ydl.extract_info(ytURL, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_thumbnail = info_dict.get('thumbnail', None)
            video_title = info_dict.get('title', None)
            video_title = f"[{video_title}]({ytURL})"
          yt_embed = discord.Embed(title="**Now Playing**", color=000000, description=video_title)
          yt_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
          yt_embed.timestamp = datetime.now()
          yt_embed.set_image(url=video_thumbnail)
          await ytconversionmsg.edit(content="**Done!**", delete_after=5)
          await ytsRequest.reply(embed=yt_embed)
          time.sleep(1)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio(ytURLFileName), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            ytsRequest = message
            ytCommand = message.content
            ytURL = ytCommand.replace('!vcyt ', '')
            ytURLFileName = ytURL[-11:]
            print (ytURLFileName)
            ytURLFileName = 'musica/' + ytURLFileName + '.mkv'
            ytconversionmsg = await message.channel.send('**Downloading YouTube Video...**')
            with ydl:
              ydl.download([ytURL])
              info_dict = ydl.extract_info(ytURL, download=False)
              video_url = info_dict.get("url", None)
              video_id = info_dict.get("id", None)
              video_thumbnail = info_dict.get('thumbnail', None)
              video_title = info_dict.get('title', None)
              video_title = f"[{video_title}]({ytURL})"
            yt_embed = discord.Embed(title="**Now Playing**", color=000000, description=video_title)
            yt_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
            yt_embed.timestamp = datetime.now()
            yt_embed.set_image(url=video_thumbnail)
            await ytconversionmsg.edit(content="**Done!**", delete_after=5)
            await ytsRequest.reply(embed=yt_embed)
            time.sleep(1)
            vc.pause()
            vc.play(discord.FFmpegPCMAudio(ytURLFileName), after=lambda e: print('done', e))
            vc.is_playing()
            await message.add_reaction(confirmedEmoji)

    if message.content.startswith('!music'):
      if message.author.guild_permissions.move_members or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          ytsRequest = message
          ytCommand = message.content
          ytSearch = ytCommand.replace('!music ', '')
          ytSearch = ytSearch.replace(" ", "+")
          ytSearchURL = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + ytSearch)
          video_ids = re.findall(r"watch\?v=(\S{11})", ytSearchURL.read().decode())
          ytURL = ("https://www.youtube.com/watch?v=" + video_ids[0])
          ytURLFileName = ytURL[-11:]
          print (ytURLFileName)
          ytURLFileName = 'musica/' + ytURLFileName + '.mkv'
          ytconversionmsg = await message.channel.send('**Downloading YouTube Video...**')
          with ydl:
            ydl.download([ytURL])
            info_dict = ydl.extract_info(ytURL, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_thumbnail = info_dict.get('thumbnail', None)
            video_title = info_dict.get('title', None)
            video_title = f"[{video_title}]({ytURL})"
          yts_embed = discord.Embed(title="**Now Playing**", color=000000, description=video_title)
          yts_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
          yts_embed.timestamp = datetime.now()
          yts_embed.set_image(url=video_thumbnail)
          await ytconversionmsg.edit(content="**Done!**", delete_after=5)
          await ytsRequest.reply(embed=yts_embed)
          time.sleep(1)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio(ytURLFileName), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            if vc.is_playing:
              ytsRequest = message
              ytCommand = message.content
              ytSearch = ytCommand.replace('!music ', '')
              ytSearch = ytSearch.replace(" ", "+")
              ytSearchURL = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + ytSearch)
              video_ids = re.findall(r"watch\?v=(\S{11})", ytSearchURL.read().decode())
              ytURL = ("https://www.youtube.com/watch?v=" + video_ids[0])
              ytURLFileName = ytURL[-11:]
              print (ytURLFileName)
              ytURLFileName = 'musica/' + ytURLFileName + '.mkv'
              ytconversionmsg = await message.channel.send('**Downloading YouTube Video...**')
              with ydl:
                ydl.download([ytURL])
                info_dict = ydl.extract_info(ytURL, download=False)
                video_url = info_dict.get("url", None)
                video_id = info_dict.get("id", None)
                video_thumbnail = info_dict.get('thumbnail', None)
                video_title = info_dict.get('title', None)
                video_title = f"[{video_title}]({ytURL})"
              yts_embed = discord.Embed(title="**Queued**", color=000000, description=video_title)
              yts_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
              yts_embed.timestamp = datetime.now()
              yts_embed.set_image(url=video_thumbnail)
              await ytconversionmsg.edit(content="**Done!**", delete_after=5)
              await ytsRequest.reply(embed=yts_embed)
              time.sleep(1)
              vc.pause()
              vc.play(discord.FFmpegPCMAudio(ytURLFileName), after=lambda e: print('done', e))
              vc.is_playing()
              await message.add_reaction(confirmedEmoji)
            
            print(video_url)
            print(video_id)
            print(video_title)
    """
        


    if message.content.lower().startswith('!vc-tts'):
      if message.author.guild_permissions.move_members or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          ttsCommand = message.content
          ttsContent = ttsCommand.replace('!vc-tts ', '')
          ttsconversionmsg = await message.channel.send('**Converting Text to Audio...**')
          tts = gTTS(ttsContent, 'co.za')
          tts.save('tts.mp3')
          await ttsconversionmsg.edit(content="**Done!**")
          tts_embed = discord.Embed(title="**Now Playing Text to Speech**", color=000000, description=ttsContent)
          tts_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
          tts_embed.timestamp = datetime.now()
          await ttsconversionmsg.edit(content="**Done!**", delete_after=5)
          await message.reply(embed=tts_embed)
          time.sleep(1)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            ttsCommand = message.content
            ttsContent = ttsCommand.replace('!vc-tts ', '')
            ttsconversionmsg = await message.channel.send('**Converting Text to Audio...**')
            tts = gTTS(ttsContent, 'co.za')
            tts.save('tts.mp3')
            await ttsconversionmsg.edit(content="**Done!**")
            tts_embed = discord.Embed(title="**Now Playing Text to Speech**", color=000000, description=ttsContent)
            tts_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
            tts_embed.timestamp = datetime.now()
            await ttsconversionmsg.edit(content="**Done!**", delete_after=5)
            await message.reply(embed=tts_embed)
            time.sleep(1)
            vc.pause()
            vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=lambda e: print('done', e))
            vc.is_playing()
            await message.add_reaction(confirmedEmoji)
        

    
    if message.content.startswith('!vc-rickroll') or message.content == "!bigreveal":
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio('rick_roll.mp3'), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            vc.pause()
            vc.play(discord.FFmpegPCMAudio('rick_roll.mp3'), after=lambda e: print('done', e))
            vc.is_playing()
            await message.add_reaction(confirmedEmoji)

    if message.content.startswith('!vc-coconutmall'):
      if message.author.guild_permissions.connect or message.author.id == 196762513172463:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio('coconut_mall.mp3'), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            vc.pause()
            vc.play(discord.FFmpegPCMAudio('coconut_mall.mp3'), after=lambda e: print('done', e))
            vc.is_playing()
            await message.add_reaction(confirmedEmoji)

    if message.content.startswith('!vc-slimshady'):
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        if vc == None:
          vc = await message.author.voice.channel.connect(reconnect=True)
          vc.pause()
          vc.play(discord.FFmpegPCMAudio('therealslimshady.mp3'), after=lambda e: print('done', e))
          vc.is_playing()
          await message.add_reaction(confirmedEmoji)
        else:
          if vc.is_connected:
            vc.pause()
            vc.play(discord.FFmpegPCMAudio('therealslimshady.mp3'), after=lambda e: print('done', e))
            vc.is_playing()
            await message.add_reaction(confirmedEmoji)

    """
    if message.content.startswith('!clearmusic'):
      if message.author.id == 196762513172463617:
        print("deez")
        pathcheck = '/musica/'
        path = "musica"
        for filename in os.listdir(path):
          filestamp = os.stat(os.path.join(path, filename)).st_mtime
          filecompare = TimeNow - 86400
          #7 * 86400
          filesdeleted = 0
          pathcheck = '/musica/' + filename
          if filestamp < filecompare:
            if os.path.exists(filename):
              os.path.remove("/musica/" + filename)
              await message.channel.send(f"Deleted {filename}")
              filesdeleted = filesdeleted + 1
            else:
              print(f"The file: {filename} does not exist")
        await message.channel.send(f"Music Clear: {filesdeleted} File(s) Deleted")
        await message.add_reaction(confirmedEmoji)
    """

    
    if message.content.startswith('!pause'):
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        try:
          if vc.is_connected:
            vc.pause()
            await message.add_reaction(confirmedEmoji)
            pause_embed = discord.Embed(title=":arrow_forward:  **Player Paused**", color=000000)
            pause_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
            pause_embed.timestamp = datetime.now()
            await message.reply(embed=pause_embed, mention_author=False)
          else:
            await message.add_reaction(unconfirmedEmoji)
            await message.reply(content="You are not connected to a voice channel!")
        except AttributeError:
          await message.add_reaction(unconfirmedEmoji)
          await message.reply(content="You are not connected to a voice channel!")

        

    
    if message.content.startswith('!resume'):
      if message.author.guild_permissions.connect or message.author.id == 196762513172463617:
        vc = message.guild.voice_client
        try:
          if vc.is_connected:
            vc.resume()
            await message.add_reaction(confirmedEmoji)
            resume_embed = discord.Embed(title=":pause_button:  **Player Resumed**", color=000000)
            resume_embed.set_footer(text=f"Requested by {message.author}", icon_url=str(message.author.avatar_url))
            resume_embed.timestamp = datetime.now()
            await message.reply(embed=resume_embed, mention_author=False)
          else:
            await message.add_reaction(unconfirmedEmoji)
            await message.reply(content="You are not connected to a voice channel!")
        except AttributeError:
          await message.add_reaction(unconfirmedEmoji)
          await message.reply(content="You are not connected to a voice channel!")
        
    if message.content.startswith('!rngvote'):
        randomMember = random.choice(message.guild.members)
        await message.channel.send(f"Vote {randomMember.mention} out. You've got at least a 10% chance of getting it "
                                   f"right.")

    if message.content.lower().startswith('$top1000'):
        await message.delete()

    if 'lol' in message.content:
        await message.channel.send('https://media1.tenor.com/images/8305238eaf271487686de09c373b766b/tenor.gif?itemid=13864254')

    if 'tumiroll' in message.content:
        await message.channel.send('SHUT THE FUCK UP')

    if 'Lol' in message.content:
        await message.channel.send('https://media1.tenor.com/images/8305238eaf271487686de09c373b766b/tenor.gif?itemid=13864254')

    if 'LOL' in message.content:
        await message.channel.send(
            'https://media1.tenor.com/images/8305238eaf271487686de09c373b766b/tenor.gif?itemid=13864254')

    if 'bye' in message.content:
        await message.channel.send('https://media1.tenor.com/images/f7b8f53a5ce812fd5bb422f5bf90dd4b/tenor.gif?itemid=19053721')

    if 'Bye' in message.content:
        await message.channel.send('https://media1.tenor.com/images/f7b8f53a5ce812fd5bb422f5bf90dd4b/tenor.gif?itemid=19053721')


    if ' cat  ' in message.content.lower():
        await message.channel.send('https://media.discordapp.net/attachments/775941210119733269/777561607839547402/image0.jpg?width=400&height=219')

    if message.content.lower().startswith('$m'):
        if message.content.lower() == '$m':
            await message.delete()
        if message.content.lower() == '$ma':
            await message.delete()
        if message.content.lower() == '$mg':
            await message.delete()

    if message.content.lower().startswith('$w'):
        if message.content.lower() == '$w':
            await message.delete()
        if message.content.lower() == '$wa':
            await message.delete()
        if message.content.lower() == '$wg':
            await message.delete()

    if message.content.lower().startswith('$h'):
        if message.content.lower() == '$h':
            await message.delete()
        if message.content.lower() == '$ha':
            await message.delete()
        if message.content.lower() == '$hg':
            await message.delete()

    if 'oatmeal raisin' in message.content:
        await message.channel.send('***dammit***')

    if 'Oatmeal Raisin' in message.content:
        await message.channel.send('***dammit***')

    if 'Oatmeal raisin' in message.content:
        await message.channel.send('***dammit***')

    if message.content.startswith('!time'):
        timenow = datetime.datetime.now()
        current_time = timenow.strftime("%H:%M:%S")
        await message.channel.send("Current Time - " + current_time)

    if message.channel.id == 775945092489805834:
        if message.author.id == 251481402090979329:
            await message.delete()
        if message.author.id == 432610292342587392:
            await message.delete()


    if msgguildid == 775941209666879550:
      if message.author.id != 251481402090979329:
          if message.content.startswith('!wlcounter'):
              with message.channel.typing():
                  dafile = open('storage.txt', 'r')
                  lines = list(dafile)
                  dafile.close()
                  wishcounter = 0
                  tjwishcounter = 0
                  natewishcounter = 0
                  loganwishcounter = 0
                  tumiwishcounter = 0
                  emmywishcounter = 0
                  sarahwishcounter = 0
                  willwishcounter = 0
                  for i in lines:
                      if 'Wished by <@' in i:
                          wishcounter = wishcounter + 1
                          if '349682083922444298' in i:
                              tjwishcounter = tjwishcounter + 1
                          if '224988545402535936' in i:
                              natewishcounter = natewishcounter + 1
                          if '251481402090979329' in i:
                              loganwishcounter = loganwishcounter + 1
                          if '196762513172463617' in i:
                              tumiwishcounter = tumiwishcounter + 1
                          if '641267423604899870' in i:
                              emmywishcounter = emmywishcounter + 1
                          if '427287857909071872' in i:
                              sarahwishcounter = sarahwishcounter + 1
                          if '304609945549275139' in i:
                              willwishcounter = willwishcounter + 1
                  with message.channel.typing():
                      await message.channel.trigger_typing()
                      await message.channel.send('Number of Characters Rolled While Wishlisted: ' + str(wishcounter))
                      await message.channel.send("(Please keep in mind this is only characters who were actively on someone's wishlist when rolled)")
                      await message.channel.send('TJ - ' + str(tjwishcounter))
                      await message.channel.send('Nate - ' + str(natewishcounter))
                      await message.channel.send('Logan - ' + str(loganwishcounter))
                      await message.channel.send('Tumi - ' + str(tumiwishcounter))
                      await message.channel.send('Emmy - ' + str(emmywishcounter))
                      await message.channel.send('Sarah - ' + str(sarahwishcounter))
                      await message.channel.send('Will - ' + str(willwishcounter))

    if message.content.startswith('!encrypt'):

        encryptcontent = message.content
        encryptioncontent = encryptcontent.replace('!encrypt', '')
        def encryptionprocess():

            print('')
            for eachletter in encryptioncontent:
                if eachletter in uppercase_index:
                    crypt = uppercase_index.index(eachletter)
                    encryption = ((0 + 25) - crypt)
                    encryptedvalues.append(encryption)
                    newcharacter = uppercase_index[encryption]
                    encryptedtext.append(newcharacter)
                elif eachletter in lowercase_index:
                    crypt = lowercase_index.index(eachletter)
                    encryption = ((0 + 25) - crypt)
                    encryptedvalues.append(encryption)
                    newcharacter = lowercase_index[encryption]
                    encryptedtext.append(newcharacter)
                elif eachletter in special_index:
                    crypt = special_index.index(eachletter)
                    encryption = (crypt + 0)
                    encryptedvalues.append(encryption)
                    newcharacter = special_index[encryption]
                    encryptedtext.append(newcharacter)

        # Decryption function declaration
        def decryptionprocess():
            print('')
            for eachletter in encryptioncontent:
                if eachletter in uppercase_index:
                    decipher = uppercase_index.index(eachletter)
                    decryption = ((0 + 25) - decipher)
                    decryptedvalues.append(decryption)
                    newcharacter = uppercase_index[decryption]
                    decryptedtext.append(newcharacter)
                elif eachletter in lowercase_index:
                    decipher = lowercase_index.index(eachletter)
                    decryption = ((0 + 25) - decipher)
                    decryptedvalues.append(decryption)
                    newcharacter = lowercase_index[decryption]
                    decryptedtext.append(newcharacter)
                elif eachletter in special_index:
                    decipher = special_index.index(eachletter)
                    decryption = (decipher + 0)
                    decryptedvalues.append(decryption)
                    newcharacter = special_index[decryption]
                    decryptedtext.append(newcharacter)
        # Action as a a result of chosen process
        encryptionprocess()
        con_encryptedtext = ''.join(encryptedtext)
        await message.channel.send(con_encryptedtext)
        encryptedtext = []
        encryptedvalues = []
        decryptedtext = []
        decryptedvalues = []

    if message.content.startswith('!decrypt'):
        print('active')

    """
    messagedict = {
      message_server: [' '],
      authuser: [' '],
      messagecreationtime: [' '],
      channelinfo: [' '],
      messagecontent: [' '],
      messageid: [' '],
      message_attachment_id: [' '],
      message_attachment_filename: [' '],
      message_attachment_url: [' '],
      message_embeds: [' ']
    }

    # Create empty dataf
    df = pd.DataFrame()

    # Create a column
    #df['message'] = [user, message.content, channelinuse, channelid]

    df = pd.DataFrame.from_dict(data=messagedict)
    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Oscillate Records')

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell B2. 

    dbTextFile = open('runtime.txt', 'r')
    dbValue = dbTextFile.readline()
    dbValue = int(dbValue)
    dbTextFile.close()

    wks.set_dataframe(df,(dbValue,1))
    dbTextFile = open('runtime.txt', 'w')
    dbValue = dbValue + 1
    dbTextFile.write(str(dbValue))
    dbTextFile.close()
    """


@client.event
async def on_ready():
    run_playingpresence = discord.Activity(type=discord.ActivityType.playing, name='!help')
    await client.change_presence(activity=run_playingpresence)
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('----------------------------')


#keep_alive.keep_alive()
client.run(str(os.getenv('BOT_TOKEN')))