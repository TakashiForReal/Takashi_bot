import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import random

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

takashi_id = 1078538420688781384
souyanen_id = 1026089885385367582
seiigo_id = 1125594839019438120
yuma_id = 1456935235135475749
cat_id = 1413527517180072040

TEST_GUILD_ID = discord.Object(id=1323054974770352128)
POSITIVE_GUILD_ID = discord.Object(id=1433547946271703150)

f = open('gif.json','r')
gif_dict = json.load(f)
cat_gif = gif_dict["Cat"]
HIKAKIN_gif = gif_dict["HIKAKIN"]
sunsun_gif = gif_dict["sunsun"]
stare_gif = gif_dict["Stare"]
suprise_gif = gif_dict["Suprise"]

sunsun_keys = list(sunsun_gif.keys())
suprise_keys  = list(suprise_gif.keys())
stare_keys = list(stare_gif.keys())

class Client(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} finished set up')

        try:
            guild = discord.Object(id=1323054974770352128)
            synced = await self.tree.sync(guild=guild)
            for n in range(len(synced)):
                print(f'{synced[n]}')
            guild = discord.Object(id=1433547946271703150)
            synced = await self.tree.sync(guild=guild)
            for n in range(len(synced)):
                print(f'{synced[n]}')
        except Exception as e:
            print(f'Error syncing commands: {e}')


    async def on_message(self,message):
        if message.author == self.user:
            return
        sender_id = message.author.id
        if sender_id == yuma_id:
            return
        text = message.content
        print(text)
        if "何を四天王" == text:
            await message.channel.send(HIKAKIN_gif["何を四天王"])
        elif "まじか" in text and sender_id == takashi_id:
            await message.channel.send(suprise_gif[random.choice(suprise_keys)])
        elif "dame" in text or "mac" in text:
            await message.reply(cat_gif["angry_cat_big"])
        elif "おら" in text:
            await message.channel.send(cat_gif["punch"])
        elif "病んだ" in text and sender_id == takashi_id:
            await message.channel.send(HIKAKIN_gif["泣く"])
        elif "泣いた" in text or "ないた" in text:
            await message.channel.send(cat_gif["cry_kitty"])
        elif "だが断る" == text and sender_id == takashi_id:
            await message.channel.send(gif_dict["Other"]["nah uh"])
        elif "what?" in text:
            await message.channel.send(cat_gif["huh cat"])
        elif text in ["知らん","しらん","しらない","知らない"]:
            await message.channel.send(gif_dict["Other"]["idk"])
        elif any(word in text for word in ["sunsun","すんすん","スンスン","%E3%82%B9%E3%83%B3%E3%82%B9%E3%83%B3"]):
            await message.channel.send(sunsun_gif[random.choice(sunsun_keys)])
        elif "ｗ" in text:
            await message.channel.send(cat_gif["smile_cat"])
        elif "いけません" in text and sender_id == takashi_id:
            await message.channel.send(cat_gif["angry_cat_big"])
        elif "sugo" in text:
            if "i?" in text:
                await message.reply(cat_gif["pat"])
            else:
                await message.reply(cat_gif["smile_cat"])
        elif "がちいき" in text:
            await message.channel.send(cat_gif["happy"])
        elif any(word in text for word in ["takasii","sumane","@vaca1sbaka","ikemase","たかし","<@1078538420688781384>"]):
            await message.reply(cat_gif["angry_cat_small"])
        elif sender_id in [seiigo_id,souyanen_id]:
            if random.randint(1,10) == 1:
                await message.reply(cat_gif["angry_cat_small"])
        elif sender_id == cat_id:
            if random.randint(0,1) == 1:
                await message.reply(stare_gif[random.choice(stare_keys)])

        
        await client.process_commands(message)



    async def on_message_delete(self,message):
        if message.author == self.user:
            return
        print(f'{message.author} deleted message: {message.content}')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="takasiii ",intents=intents)

@client.tree.command(name="helloworld",description="hello world",guild=TEST_GUILD_ID)
async def hello_world(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World")

client.run(TOKEN)