# 🤖 AI X Posting Bot

> Automated daily X (Twitter) posting bot powered by Google Gemini AI and GitHub Actions

[![GitHub Actions](https://img.shields.io/badge/Runs%20on-GitHub%20Actions-blue?logo=github)](https://github.com/features/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green?logo=python)](https://www.python.org/)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange?logo=google)](https://ai.google.dev/)
[![Twitter API](https://img.shields.io/badge/Posts%20to-X%20(Twitter)-1DA1F2?logo=x)](https://developer.twitter.com/)

An intelligent X (Twitter) posting bot that generates and publishes engaging content twice daily using Google's Gemini AI. Completely automated with GitHub Actions - no server required!

## ✨ Features

- 🧠 **AI-Powered Content**: Uses Google Gemini AI to generate engaging, topic-specific posts
- ⏰ **Dual Schedule**: Posts at 9 AM and 9 PM daily with time-appropriate content
- 🚀 **Zero Infrastructure**: Runs entirely on GitHub Actions (free tier friendly)
- 📚 **Smart Memory**: Avoids repetitive content by remembering previous posts
- 🎯 **Customizable Topics**: Easy to configure for any subject matter
- 🔄 **Manual Override**: Test and trigger posts manually when needed
- 📊 **Full Logging**: Comprehensive logs for monitoring and debugging

## 🚀 Quick Start

### 1. Fork This Repository
Click the "Fork" button to create your own copy.

### 2. Get Your API Keys

**Google Gemini API:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for later use

**X (Twitter) API:**
1. Apply for developer access at [developer.twitter.com](https://developer.twitter.com)
2. Create a new app and generate:
   - Bearer Token
   - Consumer Key & Secret
   - Access Token & Secret
   
3. Authentication Settings
    - ✅ OAuth 1.0a - Enable this
    - ✅ OAuth 2.0 - Can be enabled but not required
    - Callback URI: http://localhost:3000/callback (placeholder)
    - Website URL: https://github.com/yourusername/your-repo

### 3. Configure Repository Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions**

Add these **Repository Secrets**:
```
GEMINI_API_KEY=your_gemini_api_key_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_CONSUMER_KEY=your_consumer_key_here
TWITTER_CONSUMER_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

**Optional Repository Variables**:
```
POSTING_TOPIC=Your Custom Topic (defaults to "Artificial Intelligence")
```

### 4. Customize Schedule (Optional)

Edit `.github/workflows/daily-posts.yml` to adjust posting times for your timezone:

```yaml
schedule:
  - cron: '0 14 * * *'  # 9 AM EST
  - cron: '0 2 * * *'   # 9 PM EST
```

### 5. Test the Setup

1. Go to **Actions** tab
2. Select "Daily X Posts"
3. Click "Run workflow"
4. Check your X account for the test post!

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `TWITTER_BEARER_TOKEN` | X API Bearer Token | Yes | - |
| `TWITTER_CONSUMER_KEY` | X API Consumer Key | Yes | - |
| `TWITTER_CONSUMER_SECRET` | X API Consumer Secret | Yes | - |
| `TWITTER_ACCESS_TOKEN` | X API Access Token | Yes | - |
| `TWITTER_ACCESS_TOKEN_SECRET` | X API Access Token Secret | Yes | - |
| `POSTING_TOPIC` | Topic for content generation | No | "Artificial Intelligence" |

### Posting Schedule

The bot posts twice daily:
- **Morning Post**: 9:00 AM (includes morning greetings and motivational hashtags)
- **Evening Post**: 9:00 PM (includes evening reflections and thought-provoking content)

## 📁 Project Structure

```
ai-x-posting-bot/
├── .github/
│   └── workflows/
│       └── daily-posts.yml     # GitHub Actions workflow
├── posting_agent.py            # Main bot logic
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── .env.example              # Environment variables template
```

## 🎨 Customization

### Change Content Style

Modify the prompt in `ContentGenerator.generate_content()`:

```python
prompt = f"""
Create an engaging Twitter/X post about {topic}.

Guidelines:
- Keep it under 280 characters
- Make it informative and engaging
- Include relevant hashtags (2-3 max)
- Use a conversational tone
- Add your custom requirements here
"""
```

### Add Different Topics for Morning/Evening

```python
if time_context == "morning":
    topic = "Morning AI Insights"
else:
    topic = "Evening Tech Thoughts"
```

### Change Posting Frequency

Edit the cron schedule in the workflow file:
- `'0 */6 * * *'` - Every 6 hours
- `'0 12 * * 1,3,5'` - Noon on Monday, Wednesday, Friday
- `'30 9 * * *'` - 9:30 AM daily

## 📊 Monitoring

### View Logs
1. Go to **Actions** tab
2. Click on any workflow run
3. Expand the "Run X posting bot" step

### Check Post History
The bot maintains a history of posts in `post_history.json` to avoid repetition.

### Manual Posting
You can manually trigger posts anytime:
1. **Actions** → **Daily X Posts** → **Run workflow**
2. Choose morning or evening slot for testing

## 🔧 Troubleshooting

### Common Issues

**Posts not appearing:**
- Check API keys are correct
- Verify X account has posting permissions
- Check rate limits haven't been exceeded

**Workflow failing:**
- Review the Actions logs for detailed error messages
- Ensure all secrets are properly set
- Check if API services are operational

**Content repetition:**
- The bot automatically avoids repeating recent content
- History is maintained across runs using GitHub Actions cache

### Debug Locally

```bash
# Clone the repository
git clone https://github.com/MuneebDevss/auto-tweet-ai.git
cd ai-x-posting-bot

# Install dependencies
pip install -r requirements.txt

# Copy and fill environment variables
cp .env.example .env
# Edit .env with your API keys

# Run locally
python posting_agent.py
```

## 📈 Usage Stats

The bot is designed to be cost-effective:
- **GitHub Actions**: ~2-3 minutes per run (4-6 minutes daily)
- **Free Tier**: 2,000 minutes/month (supports ~333 days of posting)
- **Gemini API**: Very affordable per request
- **X API**: Free tier supports moderate posting frequency

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Add image generation capabilities
- [ ] Implement engagement analytics
- [ ] Support for multiple social platforms
- [ ] Advanced content personalization
- [ ] Trending topics integration

## 📄 License

MIT License - feel free to use this for your own projects!

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent content generation
- **GitHub Actions** for reliable automation
- **Tweepy** for seamless X API integration

---

⭐ **If this project helps you, please give it a star!**

**Questions?** Open an issue or check the [discussions](../../discussions) tab.