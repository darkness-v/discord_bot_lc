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

## 🚀 Cloud Deployment (24/7)

To run your bot 24/7, deploy it to a cloud platform. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions.

**Quick Start:**
1. Push code to GitHub
2. Deploy to [Railway.app](https://railway.app) (recommended, free $5/month credit)
3. Add environment variables
4. Done! Your bot runs 24/7

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guides for Railway, Render, and DigitalOcean.

## Recent Fixes

### Issues Fixed:
1. **Missing titleSlug**: Added `titleSlug` to the returned data from `fetch_daily_question()`
2. **Submission fetching**: Changed to return a list and increased limit to 20 to find matching submissions
3. **Optional parameters**: Made `problem_slug` optional in commands so they default to the daily question
4. **Timezone**: Added Vietnam timezone (Asia/Ho_Chi_Minh) for the daily task
5. **Error handling**: Added try-catch and better error messages for debugging
6. **Channel validation**: Added check to ensure channel exists before sending messages

### Timezone Note:
The bot now uses `pytz` to set the timezone to Vietnam time (UTC+7). If you're in a different timezone, change this line in `bot.py`:
```python
@tasks.loop(time=time(hour=6, minute=0, second=0, tzinfo=pytz.timezone('Asia/Ho_Chi_Minh')))
```

## Troubleshooting

If the daily task starts but doesn't complete:
- Check that `DISCORD_CHANNEL_ID` is correct in your `.env` file
- Verify the bot has permission to send messages in that channel
- Check the console for error messages (now includes detailed error logging)
