import time
import discord
from discord import  app_commands
import os.path
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))


tokenFile = current_dir + "/data/FarmConfig/DiscordToken.txt"
FarmConfigFile = current_dir + "/data/FarmConfig/Config.txt"
UserIDFile = current_dir + "/data/Settings/DiscordUSERID.txt"
signalFile = current_dir + "/Signal.txt"
startpsFile = current_dir + "/Startps.txt"
stopFile = current_dir + "/Stop.txt"
checkFile = current_dir + "/Check.txt"



if not (os.path.exists(tokenFile)):
    print("Couldn't get token")
    exit()


quick_message =  "Disable / Enable"

farm_options = ["Daily","Half","Regular","Rift", "Bounty", "Repeatable", "Repeatable2nd", "OCRMode", "Wifi"]

default_opt  =["Disable" , "Enable"]
default_choices = [app_commands.Choice(name=opt, value=i) for i,opt in enumerate(default_opt)]

farmlist = ["Infinite", "Legend Stages", "Boss Rush", "Portal", "Cid", "Gems / Corrupt Odyssey", "Worldline", "Raid", "Dungeon"]
farmlist2 = ["Infinite", "Legend Stages", "Boss Rush", "Cid", "Gems / Corrupt Odyssey", "Raid", "Dungeon"]



#! Function
#////////////////////////////////////////////////////
def link(url, text=None):
    if text is None:
        text = url
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'

def get_content(filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                clean = line.strip().replace('\ufeff', '') 
                if clean:
                    return str(clean)
    return ""

def get_list(filepath):
    dic = {}
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                clean = line.strip().replace('\ufeff', '')
                if "=" in clean:
                    key, value = clean.split("=", 1)
                    dic[key.strip()] = int(value.strip())
    return dic
def writeFile(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(content))

def checkValid(target, ar):
    return target in ar

def getstat():
    data = get_list(FarmConfigFile)
    
    a = "```\n"
    if "Daily" in data:
        a += f"Daily challenge: {default_opt[data["Daily"]]}\n"
    
    if "Half" in data:
        a += f"Half-hour challenge (Trait): {default_opt[data["Half"]]}\n"
    
    if "Regular" in data:
        a += f"Half-hour challenge (Normal): {default_opt[data["Regular"]]}\n"
    
    if "Rift" in data:
        a += f"Rift: {default_opt[data["Rift"]]}\n"
    
    if "Bounty" in data:
        a += f"Bounty: {default_opt[data["Bounty"]]}\n"
    
    if "Repeatable" in data:
        a += f"Repeatable 1st: {farmlist[data["Repeatable"]-1]}\n"
    
    if "Repeatable2nd" in data:
        a += f"Repeatable 2nd: {farmlist2[data["Repeatable2nd"]-1]}\n"
    
    if "OCRMode" in data:
        a += f"OCR mode: {data["OCRMode"]}\n"
    
    if "Wifi" in data:
        a += f"Wifi: {default_opt[data["Wifi"]]}\n"
    
    return a + "```"

#! Variable
#////////////////////////////////////////////////////

DISCORDTOKEN = get_content(tokenFile)
ui = get_content(UserIDFile)

if ui.isdigit():
    ui = int(ui)
else:
    ui = -1


intents = discord.Intents.default()
intents.message_content = True 

slash_commands = ["set [to setup your farm settings]", "startps [mostly for restart mango using private server]","mangosettings [Show your current farm settings]","stopmango [To stop Macro]","checkmango [Send image of current state of mango]"]

def get_time():
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S] ")
    return current_time

class DiscordConsole(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced globally!")
        
    async def on_ready(self):
        print("----------- DISCORD BOT CONSOLE -----------")
        print(f"Login as {self.user}, here is some of the commands")
        commands = self.tree.get_commands() 
        for i in commands:
            print(f"/{i.name} → {i.description or "No description"}")
        print(f"The command will take few seconds to work.\nJoin https://www.discord.gg/salmon for more support\n")

bot = DiscordConsole()



#! Slash Command
#////////////////////////////////////////////////////
@bot.tree.command(name="set", description = "Set your farm settings")
@app_commands.choices(
    daily = default_choices,
    trait = default_choices,
    half = default_choices,
    rift = default_choices,
    bounty = default_choices,
    wifi = default_choices,
    repeat1=[app_commands.Choice(name=opt, value=i) for i,opt in enumerate(farmlist)],repeat2=[app_commands.Choice(name=opt, value=i) for i,opt in enumerate(farmlist2)])
@app_commands.describe(
    daily = quick_message,
    trait = quick_message,
    half = quick_message,
    rift = quick_message,
    bounty = quick_message,
    repeat1 = "Set your 1st repeatable",
    repeat2 = "Set your 2nd repeatable",
    ocr = "Mode 0-5",
    wifi = quick_message
)
async def set(
    interaction: discord.Interaction,
    daily: app_commands.Choice[int] = None,
    trait: app_commands.Choice[int] = None,
    half: app_commands.Choice[int] = None,
    rift: app_commands.Choice[int] = None,
    bounty: app_commands.Choice[int] = None,
    repeat1: app_commands.Choice[int] = None,
    repeat2:  app_commands.Choice[int] = None,
    ocr: app_commands.Choice[int] = None,
    wifi: int = None
):
    print(get_time()+interaction.user.name + " use command /set")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    
    try:
        data = get_list(FarmConfigFile)
        default = [0,1]
        if daily and checkValid(daily.value, default):
            data["Daily"] = daily.value
            
        if trait and checkValid(trait.value, default):
            data["Half"] = trait.value
            
        if half and checkValid(half.value, default):
            data["Regular"] = half.value
            
        if bounty and checkValid(bounty.value, default):
            data["Bounty"] = bounty.value
            
        if rift and checkValid(rift.value, default):
            data["Rift"] = rift.value
            
        if repeat1 and checkValid(repeat1.value + 1, list(range(1, len(farmlist)+1))):
            data["Repeatable"] = repeat1.value + 1
            
        if repeat2 and checkValid(repeat2.value, list(range(1, len(farmlist2)+1))):
            data["Repeatable2nd"] = repeat2.value + 1
        
        if ocr and checkValid(ocr,[0,1,2,3,4,5]):
            data["OCRMode"] = ocr
        
        if wifi and checkValid(wifi.value, default):
            data["Wifi"] = wifi.value
        
        saveText = ""
        for a in data:
            saveText += f"{a}={data[a]}\n"
        writeFile(FarmConfigFile,saveText)
        writeFile(signalFile, "1")
        
        e = discord.Embed(
            title="Sucessfully update | Your current Settings",
            description=getstat(),
            color= discord.Color.green()
        )
        await interaction.response.send_message(embed=e)
    except:
        await interaction.response.send_message("Error")



@bot.tree.command(name="startps", description = "Start private server to restart mango")
async def startps(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /startps")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    writeFile(startpsFile,"1")
    await interaction.response.send_message("Starting your private server!")
    

@bot.tree.command(name="mangosettings", description = "Your current farm settingsr")
async def mangosettings(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /mangosettings")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    e = discord.Embed(
        title="Your current Settings",
        description=getstat(),
        color= discord.Color.blue()
    )
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="stopmango", description = "Stop mango")
async def stopmango(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /stopmango")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    writeFile(stopFile,"1")
    await interaction.response.send_message("Stopping mango!")

@bot.tree.command(name="checkmango", description = "Mango will send current view via webhook")
async def checkmango(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /checkmango")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    writeFile(checkFile,"1")
    await interaction.response.send_message("Mango sending webhook!")

@bot.tree.command(name="shutdownpc", description = "Shutdown your pc")
async def shutdownpc(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /shutdownpc")
    if  interaction.user.id != ui and ui != -1:
        await interaction.response.send_message("You are not one who run this mango.")
        return
    writeFile(stopFile,"1")
    await interaction.response.send_message("Turning off mango and turning off pc in 10s")
    time.sleep(5)
    os.system("shutdown /s /t 5")
    return

@bot.tree.command(name="ping", description="Checks the bot's latency")
async def ping(interaction: discord.Interaction):
    print(get_time()+interaction.user.name + " use command /ping")
    await interaction.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")

try:
    bot.run(DISCORDTOKEN)
except:
    print("Couldn't run bot (invalid token)")