import discord
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
import os
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

from utils import fetch_daily_question, save_links, fetch_lc_stats, load_links, fetch_submission, fetch_hints
from discord.ext import tasks
from discord import app_commands
from datetime import time
import pytz
OPENING_STATEMENT = [
    "Chào buổi sáng Huân, hôm nay bạn có muốn giải một bài toán Leetcode không?",
    "Hôm nay là một ngày tuyệt vời để luyện tập Leetcode, Khoa ơi!",
    "Hôm nay tôi có một thử thách Leetcode cho bạn, Đạt!",
    "Đức ơi, bạn đã sẵn sàng để chinh phục một bài toán Leetcode chưa?",
    "Buổi sáng tốt lành Thành, hãy cùng nhau giải một bài toán Leetcode nào!",
]
current_daily_question = None
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.tree.command(name='bind_profile', description="Bind your Leetcode account to your Discord profile")
@app_commands.describe(leetcode_username="Your LeetCode username")
async def bind_profile(interaction: discord.Interaction, leetcode_username: str):
    discord_id = interaction.user.id
    save_links(discord_id, leetcode_username)
    await interaction.response.send_message(f"Leetcode username '{leetcode_username}' has been bound to your Discord profile, {interaction.user.name}!")

@bot.tree.command(name='show_profile', description="Show your Leetcode Statistics")
@app_commands.describe(leetcode_username="LeetCode username (optional, uses your bound profile if not provided)")
async def show_profile(interaction: discord.Interaction, leetcode_username: str = None):
    discord_id = interaction.user.id
    if leetcode_username is None:
        from utils import load_links
        links = load_links()
        leetcode_username = links.get(str(discord_id))
        if leetcode_username is None:
            await interaction.response.send_message("You have not bound a Leetcode username yet. Please use /bind_profile command first.")
            return
    stats = fetch_lc_stats(leetcode_username)
    if stats is None:
        await interaction.response.send_message(f"Could not fetch statistics for Leetcode username '{leetcode_username}'. Please check the username and try again.")
        return
    
    embed = discord.Embed(
        title=f"📊 LeetCode Profile: {leetcode_username}",
        url=f"https://leetcode.com/{leetcode_username}/",
        description=f"**Global Ranking:** #{stats.get('ranking', 'N/A'):,}",
        color=0xFFA116 
    )
    
    embed.set_thumbnail(url="https://assets.leetcode.com/static_assets/public/webpack_bundles/images/logo-dark.e99485d9b.svg")
 
    total_solved = stats.get('totalSolved', 0)
    total_questions = stats.get('totalQuestions', 0)
    percentage = (total_solved / total_questions * 100) if total_questions > 0 else 0
    progress_bar = create_progress_bar(percentage)
    
    embed.add_field(
        name="🎯 Total Progress",
        value=f"```{total_solved:,} / {total_questions:,} solved\n{progress_bar} {percentage:.1f}%```",
        inline=False
    )
    
    easy = stats.get('easySolved', 0)
    medium = stats.get('mediumSolved', 0)
    hard = stats.get('hardSolved', 0)
    
    embed.add_field(
        name="🟢 Easy",
        value=f"```{easy:,}```",
        inline=True
    )
    embed.add_field(
        name="🟡 Medium",
        value=f"```{medium:,}```",
        inline=True
    )
    embed.add_field(
        name="🔴 Hard",
        value=f"```{hard:,}```",
        inline=True
    )
    
    embed.add_field(
        name="⭐ Contribution Points",
        value=f"```{stats.get('contributionPoints', 0):,}```",
        inline=True
    )

    if stats.get('totalSubmissions'):
        acceptance_rate = (stats.get('totalAccepted', 0) / stats['totalSubmissions'] * 100)
        embed.add_field(
            name="✅ Acceptance Rate",
            value=f"```{acceptance_rate:.1f}%```",
            inline=True
        )
    
    embed.set_footer(text="Keep grinding! 💪", icon_url=interaction.user.display_avatar.url)
    embed.timestamp = discord.utils.utcnow()
    
    await interaction.response.send_message(embed=embed)

def create_progress_bar(percentage, length=20):
    """Create a visual progress bar"""
    filled = int(length * percentage / 100)
    bar = '█' * filled + '░' * (length - filled)
    return bar



@bot.tree.command(name='show_solution', description="Show your solution for a problem")
@app_commands.describe(problem_slug="Problem slug (optional, uses today's daily question if not provided)")
async def show_solution(interaction: discord.Interaction, problem_slug: str = None):
    discord_id = interaction.user.id
    links = load_links()
    leetcode_username = links.get(str(discord_id))
    if leetcode_username is None:
        await interaction.response.send_message("You have not bound a Leetcode username yet. Please use /bind_profile command first.")
        return
    if problem_slug is None:
        if current_daily_question is None:
            await interaction.response.send_message("No daily question is currently set.")
            return
        prob = current_daily_question
    else:
        prob = problem_slug
    submissions = fetch_submission(leetcode_username, prob)
    if not submissions:
        await interaction.response.send_message(f"❌ No accepted submissions found for problem `{prob}` by user `{leetcode_username}`.\n\nMake sure:\n• You have solved this problem\n• Your solution was accepted\n• Your LeetCode username is correct")
        return
    
    latest_submission = submissions[0]
    
    status = latest_submission.get('statusDisplay', 'N/A')
    if status == 'Accepted':
        color = 0x00B8A3
        status_emoji = "✅"
    else:
        color = 0xFF375F
        status_emoji = "❌"
    
    problem_title = latest_submission.get('title', prob)
    
    embed = discord.Embed(
        title=f"💻 {problem_title}",
        url=f"https://leetcode.com/problems/{prob}/",
        description=f"**Submitted by:** [{leetcode_username}](https://leetcode.com/{leetcode_username}/)",
        color=color
    )
    
    embed.add_field(
        name=f"{status_emoji} Status",
        value=f"```{status}```",
        inline=True
    )
    
    lang = latest_submission.get('lang', 'N/A')
    lang_emoji = get_language_emoji(lang)
    embed.add_field(
        name=f"{lang_emoji} Language",
        value=f"```{lang}```",
        inline=True
    )
    
    runtime = latest_submission.get('runtime', 'N/A')
    embed.add_field(
        name="⚡ Runtime",
        value=f"```{runtime}```",
        inline=True
    )

    memory = latest_submission.get('memory', 'N/A')
    embed.add_field(
        name="💾 Memory",
        value=f"```{memory}```",
        inline=True
    )
    
    timestamp = latest_submission.get('timestamp', 'N/A')
    if timestamp != 'N/A':
        from datetime import datetime
        dt = datetime.fromtimestamp(int(timestamp))
        embed.add_field(
            name="📅 Submitted",
            value=f"```{dt.strftime('%Y-%m-%d %H:%M')}```",
            inline=True
        )
    
    embed.set_thumbnail(url="https://assets.leetcode.com/static_assets/public/icons/icon-192x192.png")
    embed.set_footer(text="Great job! Keep it up! 🚀", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

def get_language_emoji(lang):
    """Return appropriate emoji for programming language"""
    lang_lower = lang.lower()
    emojis = {
        'python': '🐍',
        'python3': '🐍',
        'java': '☕',
        'javascript': '📜',
        'c++': '⚙️',
        'cpp': '⚙️',
        'c': '⚙️',
        'go': '🔷',
        'rust': '🦀',
        'ruby': '💎',
        'swift': '🦅',
        'kotlin': '🟣',
        'typescript': '📘',
        'scala': '🔺',
    }
    return emojis.get(lang_lower, '💻')

@bot.tree.command(name='give_hint', description="Get hints for a problem")
@app_commands.describe(problem_slug="Problem slug (optional, uses today's daily question if not provided)")
async def give_hint(interaction: discord.Interaction, problem_slug: str = None):
    if problem_slug is None:
        if current_daily_question is None:
            await interaction.response.send_message("No daily question is currently set.")
            return
        prob = current_daily_question
    else:
        prob = problem_slug
    hints = fetch_hints(prob)
    if not hints:
        await interaction.response.send_message(f"No hints found for problem '{prob}'.")
        return
    embed = discord.Embed(title=f"Hints for {prob}",
                          url=f"https://leetcode.com/problems/{prob}/",
                          color=discord.Color.green())
    for idx, hint in enumerate(hints, start=1):
        embed.add_field(name=f"Hint {idx}", value=hint, inline=False)
    await interaction.response.send_message(embed=embed)

@tasks.loop(time=time(hour=6, minute=0, second=0, tzinfo=pytz.timezone('Asia/Ho_Chi_Minh')))
async def daily_question():
    print("Sending daily question (scheduled)...")
    await post_daily_question()

@daily_question.before_loop
async def before_daily_question():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} guild(s)')
    
    try:
        synced = await bot.tree.sync()
        print(f"✓ Synced {len(synced)} command(s) globally")
        print("Commands synced:")
        for cmd in synced:
            print(f"  - /{cmd.name}: {cmd.description}")
    except Exception as e:
        print(f"✗ Failed to sync commands: {e}")
        import traceback
        traceback.print_exc()
    
    if not daily_question.is_running():
        daily_question.start()
        print("✓ Daily question task started")
    
    print("Posting daily question on startup...")
    await post_daily_question()

async def post_daily_question():
    """Helper function to post the daily question"""
    global current_daily_question
    channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
    channel = bot.get_channel(channel_id)
    if channel is None:
        print(f"ERROR: Could not find channel with ID {channel_id}")
        return
    
    try:
        question = fetch_daily_question()
        print("Fetched question:", question)
        random_opening = OPENING_STATEMENT[hash(question['title']) % len(OPENING_STATEMENT)]
        current_daily_question = question['titleSlug']
        
        difficulty_colors = {
            'Easy': 0x00B8A3,
            'Medium': 0xFFA116,
            'Hard': 0xFF375F
        }
        difficulty_emojis = {
            'Easy': '🟢',
            'Medium': '🟡',
            'Hard': '🔴'
        }
        
        difficulty = question['difficulty']
        color = difficulty_colors.get(difficulty, 0xFFA116)
        emoji = difficulty_emojis.get(difficulty, '⚪')
        
        embed = discord.Embed(
            title=f"📅 Today's LeetCode Daily Challenge",
            description=f"## [{question['title']}]({question['link']})\n\n{random_opening}",
            color=color,
            url=question['link']
        )
        
        embed.add_field(
            name=f"{emoji} Difficulty",
            value=f"```{difficulty}```",
            inline=True
        )
        
        embed.set_thumbnail(url="https://assets.leetcode.com/static_assets/public/webpack_bundles/images/logo-dark.e99485d9b.svg")
        embed.set_footer(text="Good luck! 🚀 Remember to share your solution when you're done!")
        embed.timestamp = discord.utils.utcnow()
        
        if isinstance(channel, discord.ForumChannel):
            thread = await channel.create_thread(
                name=f"{emoji} {question['title']} - {difficulty}",
                embed=embed,
                auto_archive_duration=1440 # 24 hours
            )
            print(f"Created forum thread: {thread.thread.name}")
        else:
            await channel.send(embed=embed)
        
        print("Daily question sent successfully!")
    except Exception as e:
        print(f"ERROR posting daily question: {e}")
        import traceback
        traceback.print_exc()

bot.run(TOKEN)