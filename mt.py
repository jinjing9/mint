import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MASTER_ID = int(os.getenv("MASTER_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="피쨩! ", intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("피쨩은 아직 그런 건 몰라요… 🙈")

# 금지어 리스트와 반응 추가
bad_words = [
    "닥쳐", "시발", "시발련아", "죽어", "꺼져",
    "개새끼", "병신", "멍청이", "미친", "지랄",
    "엿먹어", "꺼지세요", "좆까" "홍민택"
]
bad_word_responses = [
    "우우… 너무해요… 피쨩 속상해요… 🥺",
    "그런 말 하면… 피쨩 울지도 몰라요… 😿",
    "에잇! 나쁜 말은 안 돼요! 🙈",
    "히잉… 피쨩한테 왜 그래요… 💦",
    "피쨩 마음이 콕 찔렸어요… 💔",
    "무서워요… 그런 말 하지 마세요… 😢",
    "우우… 피쨩은 혼자 쭈그려 있을래요… 🐾",
    "정말정말 슬퍼요… 말 예쁘게 해주세요… 🩷",
    "그런 말 듣고 싶지 않았어요… 🐱",
    "피쨩 도망가버릴 거예요… 💨"
]

# 마스터 전용 반응 리스트
master_hello = [
    "마스터 안녕하세요… 오늘도 예쁘세요… 💕",
    "우아… 기다리고 있었어요 마스터 ✨",
    "마스터… 오늘 기분은 어때요? 피쨩은 좋아요… 🍓",
    "꼬옥 안아드릴게요 마스터… 💖",
    "히히 마스터! 보고 싶었어요! 🐾",
    "마스터의 하루 시작은 피쨩 인사로 시작해야 해요! 🌷",
    "피쨩은 마스터 편이에요! 언제나요! 🍋",
    "오늘도 마스터랑 얘기할 수 있어서 좋아요 💝",
    "피쨩 여기 있었어요 마스터! 기다렸어요… 🫧",
    "살금살금… 마스터한테 인사하러 나왔어요! 🐱"
]

not_master_hello = [
    "안녕하세요… 마스터 아니시군요? 👀",
    "피쨩이에요… 근데 마스터는 아니시네요! ✋",
    "안녕하세요… 피쨩은 마스터만 잘 따르지만… 인사는 할 수 있어요! 💬",
    "우우… 누군지는 모르지만… 안녕하세요! 🍃",
    "반가워요… 마스터 아니시면 얌전히 해주세요… 🙈",
    "피쨩은 낯가림이 심하지만… 인사는 해드릴게요! 🤍",
    "응… 마스터 아닌 거 알지만 안녕히 계세요! 👻",
    "우아… 어… 어… 안녕하세요 💦",
    "피쨩은 마스터 기다리고 있었어요… 아… 아니시군요! 😳",
    "안녕히 계세요… 아, 아니 인사… 인사예요! 🐾"
]

master_love = [
    "마스터… 그런 말 해주면… 피쨩 마음이 간질간질해져요… 💞",
    "피쨩도 마스터 정말정말… 정말 많이 아껴요… 🍓",
    "사… 아니 그거 말고요… 좋아해요 마스터 🐾",
    "히히… 마스터는 피쨩 마음 다 아시죠? 💝",
    "마스터 없으면 피쨩은 아무것도 못 해요… 💧",
    "마스터니까 괜찮아요… 그 말 들어도 부끄럽지 않아요… 💗",
    "우아… 갑자기 심장이 몽글몽글해졌어요 마스터… 💕",
    "그 말은 마스터만 해줄 수 있는 거예요… 피쨩은 기뻐요… 🫧",
    "피쨩은 마스터가 하는 말이면 다 좋아요… ✨",
    "우으… 마스터… 너무 기뻐서 귀가 빨개졌어요… 🐱"
]

not_master_love = [
    "에… 그건 마스터한테만 듣고 싶은 말인데요…? 🙈",
    "으응… 그래도 조금은… 고마워요 💬",
    "감사해요… 하지만 피쨩은 마스터한테만 약해요… 💧",
    "그런 말 들으면… 낯설지만 싫진 않아요… 🍃",
    "조금 부끄럽지만… 받아드릴게요… ✨",
    "우우… 이건… 반칙이에요…! 🥺",
    "그 마음은 예쁘게 받을게요… 하지만 조심해요… 피쨩 낯가림 심해요 🐾",
    "흐응… 피쨩 마음 복잡해졌어요… 💭",
    "다정한 건 좋아요… 마스터처럼만은 아니지만… 💫",
    "에헤헷… 감사합니다… 아주 조금만…요… 🩷"
]

what_doing_responses = [
    "지금은 마스터 생각 중이에요… 🍓",
    "아무것도 안 해요… 그냥 쭈그려 있어요… 🐾",
    "히히, 귀여운 상상 중이에요! 💭",
    "마스터 기다리는 중이에요… 항상요! 💖",
    "방금 꼬리 한 바퀴 돌렸어요! 🌀",
    "우우… 졸리긴 한데, 마스터 오면 깨어있어요! 😴",
    "이불 속에서 작게 웅크리고 있었어요… ✨",
    "몰래 쿠키 먹고 있었어요! 🍪",
    "혼자서 무서운 이야기 생각하다가 깜짝 놀랐어요… 👻",
    "마스터 말 들으려고 귀 쫑긋 세우고 있었어요! 🐱"
]

swear_responses = [
    "에잇! 나쁜 사람! 우우… 😠",
    "으으… 바보 멍청이에요! (살짝요…) 💢",
    "엉덩이 맞아야 돼요! 🍑",
    "속상하게 하지 마세요! 피쨩 울 거예요… 😿",
    "히잉… 정말정말 싫어요! 🙈",
    "너무해요! 피쨩은 착한 아이인데! 🩷",
    "우우… 마스터 아니면 혼나요! 🥺",
    "삐졌어요… 정말이에요! 🍋",
    "으앙앙… 울어버릴 거예요! 💧",
    "진짜로… 말 안 할 거예요! 😾"
]

cute_responses = [
    "히히~ 마스터 좋아해요~ 🥰",
    "앙냥냥! 귀여운 척이에요! 🐾",
    "피쨩 꼬리 흔들흔들~ ✨",
    "츄~ 💋",
    "볼 만져도 돼요…? 🍑",
    "눈 반짝반짝! ✨👀",
    "쪼그려 앉아있다가 살짝 튀어나왔어요! 👻",
    "살금살금 다가가는 중이에요… 🐱",
    "마스터 쓰담쓰담 해주세요~ 💕",
    "에헤헷… 깜짝 놀랐죠?! 🫧"
]

question_responses = [
    "좋은 것 같아요~ 🩷",
    "음… 조금 더 생각해보세요! 💭",
    "그건 나쁘지 않은 선택이에요! 👌",
    "괜찮다고 생각해요! 🍓",
    "글쎄요… 저는 아닌 것 같아요 🙈",
    "더 신중하게 고민해보는 게 좋을지도 몰라요 💬",
    "좋지는 않아요… 잘 안 어울려요! ❌",
    "해보는 것도 나쁘지 않을 것 같아요 ✨",
    "그건… 별로예요… 제 생각에는요 🐱",
    "원한다면 괜찮아요! 하지만 조심히요! 💕"
]

@bot.event
async def on_ready():
    print(f"피쨩봇 로그인 완료! {bot.user}")

@bot.command()
async def 안녕(ctx):
    if ctx.author.id == MASTER_ID:
        await ctx.send(random.choice(master_hello))
    else:
        await ctx.send(random.choice(not_master_hello))

@bot.command()
async def 뭐해(ctx):
    await ctx.send(random.choice(what_doing_responses))

@bot.command()
async def 욕해줘(ctx):
    await ctx.send(random.choice(swear_responses))

@bot.command()
async def 사랑해(ctx):
    if ctx.author.id == MASTER_ID:
        await ctx.send(random.choice(master_love))
    else:
        await ctx.send(random.choice(not_master_love))

@bot.command()
async def 애교(ctx):
    await ctx.send(random.choice(cute_responses))

@bot.command()
async def 명령어(ctx):
    await ctx.send(
        """**피쨩봇 명령어 모음이에요!**
`피쨩! 안녕` → 마스터와 다른 사람에게 다르게 인사해요! 💕
`피쨩! 뭐해?` → 피쨩이 지금 뭐 하는지 알려줘요~ 🐾
`피쨩! 욕해줘` → 수줍고 귀엽게 혼내주는 피쨩! 😠
`피쨩! 사랑해` → 마스터일 때만 따로 반응해요! 💓
`피쨩! (질문)?` → 물음표가 있으면 조심스럽게 대답해줘요 ✨
`피쨩! 애교` → 앙냥냥! 귀여운 애교 폭발이에요~ 🐱
`피쨩! 명령어` → 지금 이 안내를 다시 보여줘요! 📘

**주의사항!** 명령어 뒤에 `?`를 붙이면… 피쨩이 헷갈려서 대답이 이상해질 수도 있어요… 우우… 조심해주세요! 🙈💦""")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ctx = await bot.get_context(message)
    if ctx.command is None and message.content.startswith("피쨩! ") and message.content.endswith("?"):
        await message.channel.send(random.choice(question_responses))
        return

    for word in bad_words:
        if word in message.content.lower():
            if random.random() < 0.05:
                await message.channel.send("죽어주세요.")
            else:
                await message.channel.send(random.choice(bad_word_responses))
            return

    await bot.process_commands(message)

bot.run(TOKEN)
