# Discord Leetcode Bot

A Discord bot that fetches and posts daily LeetCode questions to your Discord channel. Runs 24/7 on cloud platforms.

## Features

- **Daily Question**: Automatically posts LeetCode daily question at 6:00 AM (Vietnam time)
- **Profile Binding**: Link your LeetCode username to your Discord profile
- **Statistics**: View your LeetCode solving statistics
- **Solutions**: Show your latest submission for a problem
- **Hints**: Get hints for LeetCode problems
- **Forum Support**: Works with Discord forum channels

## Commands

All commands now use Discord's modern slash command system and will appear with autocomplete when you type `/`:

- `/bind_profile <leetcode_username>` - Bind your LeetCode account
- `/show_profile [leetcode_username]` - Show LeetCode statistics
- `/show_solution [problem_slug]` - Show your latest solution (defaults to daily question)
- `/give_hint [problem_slug]` - Get hints for a problem (defaults to daily question)
- `/test_daily` - Manually trigger the daily question (for testing)

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with:
```
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

3. Run the bot:
```bash
python bot.py
```
