# 🚀 Deployment Checklist

Use this checklist when deploying your bot to the cloud.

## Before Deployment

- [ ] Bot works locally (`python bot.py`)
- [ ] All commands respond (`/bind_profile`, `/show_profile`, etc.)
- [ ] Daily question posts successfully
- [ ] `user_data.json` has your test data (will be migrated)
- [ ] `.env` file has `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID`

## Prepare for Cloud

- [ ] Create GitHub repository
- [ ] Add files to git:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  ```
- [ ] Push to GitHub:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/discord-leetcode-bot.git
  git push -u origin main
  ```

## Railway.app Deployment (Recommended)

- [ ] Go to [railway.app](https://railway.app)
- [ ] Create account / Sign in with GitHub
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select your repository
- [ ] Wait for initial deploy (will fail - that's okay!)

### Add Database

- [ ] In project, click "New" → "Database" → "Add PostgreSQL"
- [ ] Wait for database to provision (~30 seconds)
- [ ] Railway automatically sets `DATABASE_URL` variable

### Add Environment Variables

- [ ] Click on your service (not database)
- [ ] Go to "Variables" tab
- [ ] Add variables:
  - [ ] `DISCORD_BOT_TOKEN` = `your-bot-token`
  - [ ] `DISCORD_CHANNEL_ID` = `your-channel-id`
- [ ] Click "Deploy" or wait for auto-redeploy

### Verify Deployment

- [ ] Check "Deployments" tab - should say "Success"
- [ ] Click "View Logs" - should see:
  ```
  ✓ PostgreSQL database initialized
  ✓ Migrated X users from user_data.json to database
  LeetcodeBot#3038 has connected to Discord!
  ✓ Synced 5 command(s) globally
  ```
- [ ] Go to Discord - bot should be online
- [ ] Daily question should be posted in channel
- [ ] Test `/bind_profile` command

## Render.com Deployment

- [ ] Go to [render.com](https://render.com)
- [ ] Sign up with GitHub
- [ ] Create PostgreSQL database first:
  - [ ] Dashboard → "New" → "PostgreSQL"
  - [ ] Name: `leetcode-bot-db`
  - [ ] Select free tier
  - [ ] Create database
  - [ ] Copy "Internal Database URL"
  
- [ ] Create Web Service:
  - [ ] Dashboard → "New" → "Web Service"
  - [ ] Connect GitHub repository
  - [ ] Name: `leetcode-discord-bot`
  - [ ] Environment: Docker
  - [ ] Plan: Free
  
- [ ] Add Environment Variables:
  - [ ] `DISCORD_BOT_TOKEN`
  - [ ] `DISCORD_CHANNEL_ID`
  - [ ] `DATABASE_URL` (paste from database)
  
- [ ] Click "Create Web Service"

### Verify Deployment

- [ ] Check logs for successful connection
- [ ] Bot should be online in Discord
- [ ] Test commands

## Post-Deployment

- [ ] Bot responds to slash commands
- [ ] `/bind_profile` saves to database
- [ ] `/show_profile` retrieves from database
- [ ] Daily question posts at 6:00 AM Vietnam time
- [ ] Forum threads are created (if using forum channel)
- [ ] Embeds display correctly

## Monitoring

- [ ] Check logs daily for first week
- [ ] Monitor for errors or crashes
- [ ] Verify daily questions are posting
- [ ] Check database has all user mappings

## Troubleshooting

If bot doesn't work:

- [ ] Check logs for errors
- [ ] Verify environment variables are set
- [ ] Check Discord bot has correct permissions
- [ ] Verify `DATABASE_URL` is accessible
- [ ] Try redeploying

If commands don't appear:

- [ ] Bot needs "applications.commands" scope
- [ ] Re-invite bot with correct URL
- [ ] Wait 1 hour for Discord to sync
- [ ] Try in private server first

## Success Criteria ✅

Your deployment is successful when:

- ✅ Bot is online 24/7
- ✅ Slash commands work
- ✅ Daily question posts at 6 AM
- ✅ User data persists across restarts
- ✅ Database has all mappings
- ✅ No errors in logs

## Next Steps

- Set up monitoring/alerts
- Add more features
- Customize greetings
- Invite more users
- Share with friends!

🎉 **Congratulations! Your bot is now running 24/7!** 🎉
