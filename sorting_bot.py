import discord
import os
from discord.ext import commands
import random
import requests
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
sorting_rules = {
    "бутылка": "Урна для стекла.",
    "стеклянная бутылка": "Урна для стекла.",
    "пластиковая бутылка": "Урна для пластика.",
    "стекло": "Урна для стекла.",
    "стеклянная банка": "Урна для стекла.",
    "бумага": "Урна для бумаги.",
    "картон": "Урна для бумаги.",
    "газета": "Урна для бумаги.",
    "пластик": "Урна для пластика.",
    "полиэтилен": "Урна для пластика.",
    "еда": "Урна для биоотходов.",
    "органические отходы": "Урна для биоотходов.",
    "яблочные огрызки": "Урна для биоотходов.",
    "овощные очистки": "Урна для биоотходов.",
    "банановые кожуры": "Урна для биоотходов.",
    "лом ламп": "Урна для опасных отходов.",
    "энергосберегающая лампа": "Урна для опасных отходов.",
    "лампа": "Урна для опасных отходов.",
    "батарейка": "Урна для опасных отходов.",
    "аккумулятор": "Урна для опасных отходов.",
    "металл": "Урна для металла.",
    "жестяная банка": "Урна для металла.",
    "алюминиевая банка": "Урна для металла.",
    "текстиль": "Урна для текстиля или переработка.",
    "одежда": "Урна для текстиля или переработка.",
    "обувь": "Урна для текстиля или переработка.",
    "пакет": "Урна для пластика.",
    "кожа": "Урна для биоотходов.",
    "резина": "Урна для опасных отходов.",
    "шины": "Урна для опасных отходов."
}
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)
@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')
@bot.group()
async def cool(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')
@cool.command(name='bot')
async def _bot(ctx):
    await ctx.send('Yes, the bot is cool.')
@bot.command()
async def mem(ctx):
    file_name = random.choice(os.listdir('images'))
    with open(F'images/{file_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)    
@bot.command(name='sort')
async def sort(ctx, *, item: str):
    item = item.lower()
    if item in sorting_rules:
        await ctx.send(f'{item.capitalize()} следует выбросить в: {sorting_rules[item]}')
    else:
        await ctx.send(f'Я не уверен, куда выбрасывать "{item}". Попробуйте уточнить или следуйте общим правилам сортировки отходов.')
@bot.command(name='myhelp')
async def my_help(ctx):
    help_text = "Available commands:\n"
    for command in bot.commands:
        help_text += f"{command.name}: {command.help}\n"
    await ctx.send(help_text)
bot.run('YOUR_DISCORD_BOT_TOKEN')
