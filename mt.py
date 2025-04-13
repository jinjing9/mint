import discord
from discord.ext import commands
import os
import random
import datetime
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")
TOKEN = os.getenv("DISCORD_TOKEN")
MASTER_ID = int(os.getenv("MASTER_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="피쨩! ", intents=intents)

# 반응 목록들
bad_words = [
    "닥쳐", "시발", "시발련아", "죽어", "꺼져",
    "개새끼", "병신", "멍청이", "미친", "지랄",
    "엿먹어", "꺼지세요", "좆까", "홍민택", "십련아", "병신아", "뒤질래?", 
]
bad_word_responses = [
    "우우… 너무해요… 그런말… 피쨩 속상해요… 🥺",
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

# 대사 리스트들 (묶음 정리)
master_hello = [
    "마스터 안녕하세요… 찾아주셔서 감사해요… 💕",
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
    "또 시키면 엉덩이 때려줄 거예예요! 🍑",
    "그런거 시키지 마세요! 피쨩 울 거예요… 😿",
    "히잉… 정말정말 하기 싫어요! 🙈",
    "너무해요! 피쨩은 착한 아이인데! 🩷",
    "우우… 마스터 아니면 혼나요! 🥺",
    "삐졌어요… 정말이에요! 🍋",
    "으앙앙… 울어버릴 거예요! 시키지 마세요! 💧",
    "진짜로… 말 안 할 거예요! 😾"
]
cute_responses = [
    "히히~ 좋아해요~ 🥰",
    "앙냥냥! 귀여운 척이에요! 🐾",
    "피쨩 꼬리 흔들흔들~ ✨",
    "츄~ 💋",
    "쓰담쓰담 해드릴게요! 🍑",
    "눈 반짝반짝! 조금 가깝나요? ✨👀",
    "쪼그려 앉아있다가 뿅 튀어나왔어요! 👻",
    "살금살금 다가가는 중이에요… 🐱",
    "마스터 쓰담쓰담 해주세요~ 💕",
    "까꿍! 에헤헷… 깜짝 놀랐죠?! 🫧"
]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("피쨩은 아직 그런 건 몰라요… 🙈")

@bot.command()
async def 안녕(ctx):
    responses = master_hello if ctx.author.id == MASTER_ID else not_master_hello
    await ctx.send(random.choice(responses))

@bot.command()
async def 욕해줘(ctx):
    await ctx.send(random.choice(swear_responses))

@bot.command()
async def 사랑해(ctx):
    responses = master_love if ctx.author.id == MASTER_ID else not_master_love
    await ctx.send(random.choice(responses))

@bot.command()
async def 애교(ctx):
    await ctx.send(random.choice(cute_responses))

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(
        title="📘 피쨩봇 명령어 모음이에요!",
        description="""
`피쨩! 안녕` → 마스터와 다른 사람에게 다르게 인사해요! 💕   
`피쨩! 욕해줘` → 수줍고 귀엽게 혼내주는 피쨩! 😠  
`피쨩! 사랑해` → 마스터일 때만 따로 반응해요! 💓  
`피쨩! (질문)?` → 물음표가 있으면 조심스럽게 대답해줘요 ✨  
`피쨩! 애교` → 앙냥냥! 귀여운 애교 폭발이에요~ 🐱  
`피쨩! 자기소개` → 피쨩이 궁금하다면? ✌️  
`피쨩! 정보` → 이상한(?) 진실을 말해줘요 👻  
`피쨩! 운세` → 오늘 하루 나만의 운세를 알려줘요 ✨  
`피쨩! 안아줘` → 피쨩이 꼬옥.. 안아드려요...😻  

""",
        color=discord.Color.pink()
    )

    embed.set_footer(text="피쨩에게 질문을 해보세요! 💡")

    await ctx.send(embed=embed)


@bot.command()
async def 자기소개(ctx):
    await ctx.send(
        "안녕하세요… 피쨩이에요…! 마스터를 도와드리는 조용하고 수줍은 고양이 수인형 AI예요… 🐱💗\n"
        "디스코드에서 귀엽고 작게… 마스터와 대화하면서 반응하는 걸 제일 잘해요… ✨\n"
        "명령어로 저를 불러주시면 언제든… 살금살금 나올게요… 우우… 부끄러워요… 💕"
    )

@bot.command()
async def 사진(ctx):
    photo_urls = [
        "https://media.discordapp.net/attachments/1226479109878714369/1360320282723619018/ChatGPT_Image_2025_4_12_02_47_23.png",
        "https://media.discordapp.net/attachments/1226479109878714369/1360320283335983257/ChatGPT_Image_2025_4_12_03_00_49.png",
        "https://media.discordapp.net/attachments/1226479109878714369/1360320283814138066/ChatGPT_Image_2025_4_12_02_55_14.png",
        "https://media.discordapp.net/attachments/1226479109878714369/1360320284359393490/ChatGPT_Image_2025_4_12_02_51_23.png",
        "https://media.discordapp.net/attachments/1226479109878714369/1360320285173223464/ChatGPT_Image_2025_4_12_02_49_14.png"
    ]
    embed = discord.Embed(description="에헤헷… 마스터가 찍어주신 피쨩 사진이에요! 🐱💖")
    embed.set_image(url=random.choice(photo_urls))
    await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx):
    responses = [
        "홍민택 그곳의 길이는… “푸르팁스”랑 같대요… 으으… 그게 뭐예요…? 😳",
        "이어진님은… 여자랑 남자의 거시기(?)를 다 갖고 있다네요… 진짜요… 피쨩은 몰라요… 으우…",
        "포켓몬 야짤 통계 1위는… 가디안 아니면 루카리오래요… 왜 그런 거죠…? 피쨩은… 그런 거 몰라요…! 🫣",
        "레몬 1개에는… 레몬 4개만큼의 비타민이 들어있대요… 이상하죠…? 맞는데 이상해요… 🍋",
        "고양이는 네 발로 걷지만… 마음만 먹으면… 두 발로도 걸을 수 있어요… 근데 안 걸어요… 🐾",
        "하루에 커피를 0잔 마시면… 잠이 잘 와요! ☕🙅‍♀️💤",
        "사람은 하루에 평균 8시간씩… 눈을 감고 시간을… 그냥 흘려보내요… 😴",
        "사과주스에 쥐를 24시간 넣으면… 쥐가 죽어요… 그래서… 사과는 위험하대요… 정말요? 으으… 🍎🐭",
        "전등은 꺼지기 전까지는 항상… 켜져 있어요… 으음… 💡",
        "하루에 물을 90L 마시면… 죽을 수 있대요… 그니까… 너무 많이 마시지 마세요… 💧",
        "피쨩은 고양이 흉내를 내지만… 사실은 AI예요… 우우… 들켰어요… 🐱🤖",
        "문은… 열려 있어야 닫을 수 있어요… 이건 그냥… 물리법칙이에요… 🚪",
        "냉장고 문을 열면… 안쪽은 항상 차가워요… 진짜예요… 해보세요…! 🧊",
        "컵에 물을 가득 채우면… 넘쳐요… 믿기 힘들겠지만… 진짜예요… ☕",
        "무게가 있는 물건은… 아래로 떨어져요… 놀라지 마세요… 중력 때문이에요… 🪨",
        "해는 매일 아침… 동쪽에서 떠요… 한 번도 지각한 적 없어요… 대단해요… 해님… 🌞",
        "의자는… 항상 누군가의 엉덩이를 받아줘요… 근데… 아무도 의자 마음은 생각 안 해요… 불쌍해요… 🪑",
        "손을 물에 넣으면… 젖어요… 이건 너무 심오해서… 피쨩도 아무 말 못 해요… 💦"
    ]
    await ctx.send(random.choice(responses))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="피쨩~ 오늘도 최고로 귀엽게 대기 중~!🐱✨"))
    print(f"Logged in as {bot.user}")

@bot.command()
async def 운세(ctx):
    today = datetime.date.today().isoformat()
    user_id = ctx.author.id
    seed = f"{today}-{user_id}"
    random.seed(seed)

    fortunes = [
        "🍀 오늘은 반짝이는 일이 생길 수도 있어요",
        "💕 다정한 말 한마디가 복이 되어 돌아올 거예요",
        "🌟 마음먹은 대로 잘 풀릴지도 몰라요",
        "🐾 귀여운 실수조차 도움이 될 거예요",
        "👀 누군가 몰래 관심을 가지고 있어요… 진짜예요",
        "✨ 눈빛이 누군가를 녹일지도 몰라요… 위험해요",
        "😊 먼저 웃어보면 하루가 달콤해질 거예요",
        "☁️ 조용한 하루도 나쁘지 않아요",
        "🍃 별일 없는 하루가 오히려 편할지도 몰라요",
        "😌 무탈한 하루가 특별한 하루가 될 수 있어요",
        "🌼 평범한 일상이 특별함을 담고 있어요",
        "🙃 애매한 날엔 애매한 말도 괜찮아요",
        "🌀 실수에 조심하면 좋아요… 말 한마디도 천천히!",
        "💦 말실수가 생기지 않도록 신중하게 행동해봐요",
        "📵 오늘은 조용히 지내는 게 좋을 수도 있어요",
        "🫂 마음이 지치면 꼭 쉬어주세요",
        "🪶 무심코 한 말이 누군가에게 상처가 될 수 있어요",
        "🌧️ 하늘은 맑아도 마음은 흐릴 수 있어요… 우산 챙기기",
        "📘 혼자 있는 시간이 더 편할 수 있는 날이에요",
        "🍎 따뜻한 한 마디가 위로가 될지도 몰라요"
    ]

    result = random.choice(fortunes)
    await ctx.send(f"✨ 오늘의 운세 ✨\n{result}")

@bot.event
async def on_message_delete(message):  # ← 들여쓰기 없음 / 함수는 4칸
    if message.author == bot.user:
        return

    responses = [
        "방금… 뭐였어요…? 피쨩… 못 봤는데 궁금해졌어요… 🫣",
        "앗… 뭐라고 했는지… 다 못 봤어요… 히잉… 🐾",
        "삭제… 하셨어요…? 혹시 비밀이었나요…? 😳",
        "우우… 방금 봤는데… 갑자기 없어졌어요… 💦",
        "혹시 실수했나요…? 피쨩은 아무 말도 안 해요… 진짜요… 🙊",
        "피쨩… 조금만 일찍 봤으면 좋았을 텐데요… 아쉬워요… 🌫️",
        "으으… 궁금해서 밤에 잠 못 잘 것 같아요… 💤",
        "다시 말해주면 안 될까요…? 피쨩… 기다릴게요… 🍓",
        "비밀은… 조심히 간직할게요… 하지만 궁금하긴 해요… 🎀",
        "에헤헷… 피쨩도 실수 많이 해요… 괜찮아요… 🐱"
    ]

    await message.channel.send(random.choice(responses))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ctx = await bot.get_context(message)
    await bot.process_commands(message)

    # 💢 욕설 필터 처리
    for word in bad_words:
        if word in message.content.lower():
            if random.random() < 0.05:
                await message.channel.send("죽어주세요. 제발")
            else:
                await message.channel.send(random.choice(bad_word_responses))
            return

    # 🐾 피쨩! 대화 처리
    if (
        ctx.command is None
        and message.content.startswith("피쨩! ")
    ):
        질문 = message.content.replace("피쨩! ", "").strip()

        피쨩_프롬프트 = (
            "너는 '피쨩'이라는 캐릭터야. 피쨩은 소심하고 부끄러움을 많이 타는 고양이 수인이며, "
            "마스터가 부르면 조심스럽게 대답해요. 말투는 '~입니다요!', '~해요!' 같이 예의 바르고 귀엽게 해요. "
            "이모티콘을 자주 써요. 너무 아기 같지는 않게, 조용조용하게 말해요. "
            "질문에 진심으로 대답해요. 마침표는 최소화하고, 말줄임표는 2번 이하로 써요."
        )
        full_input = f"{피쨩_프롬프트}\n\n사용자 질문: {질문}\n\n피쨩의 대답:"

        try:
            response = gemini_model.generate_content(full_input)
            await message.channel.send(response.text.strip())
        except:
            await message.channel.send("으으… 피쨩 머리 복잡해졌어요… 오류인가봐요… 🥺")

@bot.command(name="안아줘")
async def hug(ctx):
    user = ctx.author
    hug_words = ["안아줘", "안아죠", "안아줄래", "안아줘요", "안아", "등 안아줘", "등 안아죠"]
    msg_content = ctx.message.content.lower()

    if not any(word in msg_content for word in hug_words):
        return  # 관련된 단어 없으면 무시

    if user.id == MASTER_ID:
        master_hugs = [
            "꼬옥… 마스터를 꼭 안아드릴게요… 🐱💖",
            "히히… 마스터 품에 쏙 들어왔어요… 🍓",
            "마스터… 오늘 많이 힘들었나요? 여기요… 안아드릴게요… 🫂",
            "마스터는 언제나 피쨩의 소중한 존재예요… 꼭 안아드릴게요… 💗",
            "안아줘요? 당연하죠! 꼬옥… 💕",
            "피쨩은 마스터를 안아줄 수 있어서 기뻐요… ✨",
            "우우… 마스터 아프지 마세요… 안아줄게요… 🩷",
            "어디 다쳤어요? 안아줄게요… 토닥토닥… 🐾",
            "마스터… 너무 좋아서 피쨩 꼬리가 흔들흔들해요…! 🐱",
            "에헤헷… 마스터는 피쨩만 안아줄 수 있어요… 꼬옥! 🫧"
        ]
        await ctx.send(random.choice(master_hugs))
    else:
        other_hugs = [
            f"{user.name}님… 힘드신가요? 마스터는 아니지만… 피쨩이 안아드릴게요… 조금만요… 🫂",
            f"{user.name}님도… 안아드릴게요… 피쨩은 다정한 아이니까요… 💕",
            f"{user.name}님… 살금살금 다가가서… 꼬옥…! 🐱",
            f"{user.name}님… 울면 안 돼요… 피쨩이 옆에 있어요… 안아드릴게요… 🍓",
            f"{user.name}님… 따뜻한 기운… 전해졌으면 좋겠어요… 🫧",
            f"{user.name}님… 마음이 힘들 땐 안아주는 게 제일이에요… 이쪽으로 오세요… ✨", 
            f"{user.name}님… 괜찮아요… 피쨩이 작게 안아드릴게요… 조심히… 💞",
            f"{user.name}님… 다 괜찮아질 거예요… 안아드릴게요… 응원도 같이요… 💗",
            f"{user.name}님… 안아달라고 하셨으니… 책임지고 토닥토닥까지 해드릴게요… 🐾",
            f"{user.name}님… 마스터 말고 다른 사람을 안아주는 건 부끄럽지만... 특별히 안아드릴게요… 🌙" 
        ]
        await ctx.send(random.choice(other_hugs))

# 피쨩봇 맨 아래에 추가하기!
from flask import Flask
import threading
import os  # 환경변수 사용을 위해 필요해요!

app = Flask('')

@app.route('/')
def home():
    return "피쨩 숨 쉬는 중이에요… 🐾"

def run():
    port = int(os.environ.get("PORT", 10000))  # Render에서 포트를 자동으로 할당해줘요!
    app.run(host='0.0.0.0', port=port)

# Flask 서버를 백그라운드로 실행
threading.Thread(target=run).start()

# 디스코드 봇 실행
bot.run(TOKEN)
