import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import random
from datetime import datetime
import aiohttp
from aiohttp import web

PORT = os.environ.get("PORT", "8000")  # デフォルトは 8000
HEALTH_CHECK_URL = os.environ.get("HEALTH_CHECK_URL", f"http://localhost:{PORT}")
INTERVAL = 10 * 60

#load_dotenv()
#TOKEN = os.getenv("BOT_TOKEN")
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

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



# ===== ヘルスチェック =====
async def health_check():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔍 [{now}] ヘルスチェック実行中... ({HEALTH_CHECK_URL})")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(HEALTH_CHECK_URL) as response:
                if response.status == 200:
                    print(f"✅ [{now}] ヘルスチェック成功: {response.status}")
                else:
                    print(f"⚠️ [{now}] ヘルスチェック失敗: {response.status}")
    except Exception as e:
        print(f"❌ [{now}] ヘルスチェックエラー: {e}")

async def periodic_health_check():
    while True:
        await health_check()
        await asyncio.sleep(INTERVAL)

# ===== aiohttp サーバー（ルート /health） =====
async def handle_health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/health_check", handle_health)  # ←これがルート

# aiohttp サーバーをバックグラウンドで起動
runner = web.AppRunner(app)
async def start_server():
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged as {self.user}')
        asyncio.create_task(periodic_health_check())
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
        elif ("病んだ" in text or "やんだ" in text) and sender_id == takashi_id:
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

async def main():
    await start_server()
    await client.start(TOKEN)

asyncio.run(main())