import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import discord
from discord.ext import commands
import random
import os
import socket
import sys

# ✅ 중복 실행 방지용 소켓 락
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
try:
    sock.bind('\0prevent_duplicate_mintbot')
except socket.error:
    print("⚠️ 이미 실행 중입니다. 종료합니다.")
    sys.exit()

# ✅ Render 포트 감지를 위한 더미 HTTP 서버 실행
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"🌀 더미 HTTP 서버 실행 중... 포트: {port}")
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# ✅ 디스코드 토큰 불러오기
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN이 설정되지 않았어요! .env 파일을 확인해주세요.")

# ✅ 접두사 함수로 설정해 띄어쓰기 허용
def custom_prefix(bot, message):
    if message.content.startswith("민택봇 "):
        return "민택봇 "
    return "민택봇"

# ✅ 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=custom_prefix, intents=intents)

# 🧾 명령어 정의
@bot.command()
async def 안녕(ctx):
    await ctx.send("하이빵까루")

@bot.command()
async def 응가(ctx):
    응가리스트 = ["방구", "뿡", "똥", "엉덩이", "응가", "?"]
    await ctx.send(random.choice(응가리스트))

@bot.command()
async def 명령어(ctx):
    도움말 = """
**🧾 명령어 목록:**

1. **민택봇 명령어**  - 명령어를 확인해요!
2. **민택봇 응가**  - 뿡뿡
3. **민택봇 셀카**  - 귀여운 민택이 랜덤사진
4. **민택봇 안녕**  - 민택이가 인사해요!
5. **민택봇 죽어**  - 민택이 죽어욧
6. **민택봇 팬티**  - 오늘의 팬티 색깔은? [1% 확률로 보라팬티 등장!]
7. **민택봇아**  - 민택봇(이)가 고민을 해결해줘요
"""
    await ctx.send(도움말)

@bot.command()
async def 죽어(ctx):
    죽어리스트 = ["고민중이야", "ㅇㅋㅇㅋ", "드르륵...드르륵...", "엉덩이", "똥", "?", "고소합니다", "그 뭐 예..", "민택봇(이)가 시스템을 종료했습니다."]
    await ctx.send(random.choice(죽어리스트))

@bot.command()
async def 팬티(ctx):
    일반팬티 = ["빨간색", "주황색", "노란색", "초록색", "파란색", "남색", "핑크색", "흰색", "회색", "검정색", "안입음 ㅅㄱ"]
    확률 = random.randint(1, 100)
    if 확률 == 1:
        await ctx.send("오늘은 **보라색**! 💜")
        await ctx.send("보라팬티 킹아")
        await ctx.send("https://pbs.twimg.com/media/GXiXvYgacAEz13I?format=jpg&name=small")
    else:
        await ctx.send(f"오늘은 **{random.choice(일반팬티)}**")

@bot.command()
async def 셀카(ctx):
    이미지URL리스트 = [
        "https://pbs.twimg.com/media/GoHDMrKaYAEkESs?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnxHp4FbEAAW6bt?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnkqfbkaMAUP6rL?format=jpg&name=small",
        "https://pbs.twimg.com/media/Gnc0_fqa8AAylPH?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnYu9tebIAAJDzz?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnTgYYPbIAIi9Uq?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnQPvHPaQAArnBY?format=jpg&name=small",
        "https://pbs.twimg.com/media/GnJKsP2aIAAqRap?format=jpg&name=small",
        "https://pbs.twimg.com/media/Gm3TVN4a4AEhYEg?format=jpg&name=small",
        "https://pbs.twimg.com/media/GmvgPM3aUAAvRCl?format=jpg&name=small"
    ]
    await ctx.send(random.choice(이미지URL리스트))

@bot.command(name="민택봇아")
async def 민택봇아(ctx, *, 질문):
    민택답변 = [
        "ㄴㄴ하지마셈",
        "ㅋㅋㅋㅋㅋㅋㅇㅋㅇㅋ",
        "좋은데요?",
        "개별론데요",
        "에바띠",
        "몰겠음",
        "응가",
        "알아서하셈"
    ]
    await ctx.send(f"🔮 **{질문}**\n👉 {random.choice(민택답변)}")

# ✅ on_message로 명령어 확장 처리
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    if content.startswith("민택봇 "):
        명령문 = content[4:].strip()
        ctx = await bot.get_context(message)
        if 명령문.startswith("안녕"):
            await 안녕.callback(ctx)
        elif 명령문.startswith("응가"):
            await 응가.callback(ctx)
        elif 명령문.startswith("명령어"):
            await 명령어.callback(ctx)
        elif 명령문.startswith("죽어"):
            await 죽어.callback(ctx)
        elif 명령문.startswith("팬티"):
            await 팬티.callback(ctx)
        elif 명령문.startswith("셀카"):
            await 셀카.callback(ctx)
        elif 명령문.startswith("민택봇아"):
            질문 = 명령문[5:].strip()
            await 민택봇아.callback(ctx, 질문=질문)

    elif content.startswith("민택봇아"):
        ctx = await bot.get_context(message)
        질문 = content[5:].strip()
        await 민택봇아.callback(ctx, 질문=질문)

    await bot.process_commands(message)

# ✅ 봇 실행
bot.run(TOKEN)
