#!/bin/bash

# Quick deployment script for LeetCode Discord Bot

echo "🚀 LeetCode Discord Bot - Quick Deploy"
echo "======================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add .gitignore if not exists
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.env
.env.local
user_data.json
.vscode/
.idea/
.DS_Store
*.log
venv/
EOF
    echo "✅ .gitignore created"
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit
echo "💾 Committing files..."
git commit -m "Deploy: LeetCode Discord Bot with cloud support" || echo "ℹ️  No changes to commit"

echo ""
echo "✅ Repository ready for deployment!"
echo ""
echo "Next steps:"
echo "==========="
echo "1. Create a GitHub repository"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/leetcode-discord-bot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Railway:"
echo "   • Go to https://railway.app"
echo "   • Sign in with GitHub"
echo "   • New Project → Deploy from GitHub"
echo "   • Select your repository"
echo "   • Add environment variables:"
echo "     - DISCORD_BOT_TOKEN"
echo "     - DISCORD_CHANNEL_ID"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
echo ""
