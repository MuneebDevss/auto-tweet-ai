import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
import google.generativeai as genai
import tweepy
from dotenv import load_dotenv
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """Handles content generation using Gemini API"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_content(self, topic: str, time_context: str = "", additional_context: str = "") -> str:
        """Generate content for the specified topic"""
        try:
            # Determine time-based context
            current_hour = datetime.now().hour
            if current_hour < 12:
                time_hashtag = "#MorningMotivation"
            else:
                time_hashtag = "#EveningThoughts"
            
            prompt = f"""
            Create an engaging Twitter/X post about {topic}.
            
            Context: This is a {time_context} post.
            
            Guidelines:
            - Keep it under 280 characters
            - Make it informative and engaging
            - Include relevant hashtags (2-3 max)
            - Use a conversational tone
            - Avoid controversial topics
            - Start with appropriate greeting for the time of day
            - Include {time_hashtag} if it fits naturally
            
            Additional context: {additional_context}
            
            Return only the tweet text, nothing else.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            content = response.text.strip()
            
            # Clean up any unwanted formatting
            content = content.replace('"', '').replace("'", "'")
            
            # Ensure it's within Twitter's character limit
            if len(content) > 280:
                content = content[:277] + "..."
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            # Fallback content based on time
            current_hour = datetime.now().hour
            if current_hour < 12:
                return f"Good morning! Daily insights about {topic}! 🌅 #AI #Technology #MorningMotivation"
            else:
                return f"Evening thoughts on {topic}! 🌙 #AI #Technology #EveningThoughts"

class TwitterPoster:
    """Handles posting to X/Twitter"""
    
    def __init__(self, api_keys: Dict[str, str]):
        try:
            self.client = tweepy.Client(
                bearer_token=api_keys['bearer_token'],
                consumer_key=api_keys['consumer_key'],
                consumer_secret=api_keys['consumer_secret'],
                access_token=api_keys['access_token'],
                access_token_secret=api_keys['access_token_secret'],
                wait_on_rate_limit=True
            )
            logger.info("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {e}")
            raise
    
    async def post_tweet(self, content: str) -> Optional[Dict[str, Any]]:
        """Post a tweet"""
        try:
            logger.info(f"Attempting to post tweet: {content}")
            response = await asyncio.to_thread(
                self.client.create_tweet, text=content
            )
            logger.info(f"Tweet posted successfully: {response.data['id']}")
            return response.data
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None

class GitHubActionsPostingAgent:
    """Posting agent optimized for GitHub Actions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.content_generator = ContentGenerator(config['gemini_api_key'])
        self.twitter_poster = TwitterPoster(config['twitter_api_keys'])
        self.post_history = []
        self._load_post_history()
    
    async def create_and_post(self):
        """Generate content and post to X"""
        try:
            topic = self.config['topic']
            posting_time = self.config.get('posting_time', '09:00')
            
            # Determine if this is morning or evening post
            time_context = "morning" if posting_time.startswith('09') or posting_time.startswith('0') else "evening"
            
            logger.info(f"Starting {time_context} content generation for topic: {topic}")
            
            # Add context based on recent posts to avoid repetition
            recent_context = ""
            if len(self.post_history) > 0:
                recent_posts = self.post_history[-5:]  # Last 5 posts
                recent_context = f"Avoid repeating these recent topics/phrases: {', '.join([post[:50] for post in recent_posts])}"
            
            # Generate content
            content = await self.content_generator.generate_content(
                topic, 
                time_context,
                recent_context
            )
            
            # Post to X
            result = await self.twitter_poster.post_tweet(content)
            
            if result:
                # Save to history
                self.post_history.append(content)
                # Keep only last 20 posts in memory
                if len(self.post_history) > 20:
                    self.post_history = self.post_history[-20:]
                
                # Save to file for persistence
                self._save_post_history()
                
                logger.info(f"Successfully posted {time_context} tweet: {content}")
                return True
            else:
                logger.error("Failed to post tweet")
                return False
                
        except Exception as e:
            logger.error(f"Error in create_and_post: {e}")
            return False
    
    def _save_post_history(self):
        """Save post history to file"""
        try:
            history_data = {
                'posts': self.post_history,
                'last_updated': datetime.now().isoformat(),
                'total_posts': len(self.post_history)
            }
            with open('post_history.json', 'w') as f:
                json.dump(history_data, f, indent=2)
            logger.info(f"Post history saved with {len(self.post_history)} posts")
        except Exception as e:
            logger.error(f"Error saving post history: {e}")
    
    def _load_post_history(self):
        """Load post history from file"""
        try:
            if os.path.exists('post_history.json'):
                with open('post_history.json', 'r') as f:
                    data = json.load(f)
                    self.post_history = data.get('posts', [])
                logger.info(f"Loaded {len(self.post_history)} posts from history")
            else:
                logger.info("No existing post history found")
        except Exception as e:
            logger.error(f"Error loading post history: {e}")
            self.post_history = []

async def main():
    """Main function optimized for GitHub Actions"""
    
    # Load environment variables
    load_dotenv()
    
    # Load configuration from environment variables
    config = {
        "topic": os.getenv("POSTING_TOPIC", "Artificial Intelligence"),
        "posting_time": os.getenv("POSTING_TIME", "09:00"),
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "twitter_api_keys": {
            "bearer_token": os.getenv("TWITTER_BEARER_TOKEN"),
            "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
            "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
            "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        }
    }
    
    # Validate configuration
    missing_vars = []
    if not config["gemini_api_key"]:
        missing_vars.append("GEMINI_API_KEY")
    
    twitter_keys = config["twitter_api_keys"]
    for key, value in twitter_keys.items():
        if not value:
            missing_vars.append(f"TWITTER_{key.upper()}")
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    logger.info(f"Starting posting agent for topic: {config['topic']} at {config['posting_time']}")
    
    # Create and run the agent
    agent = GitHubActionsPostingAgent(config)
    
    # Post immediately (this is how GitHub Actions will work)
    success = await agent.create_and_post()
    
    if success:
        logger.info("✅ Posting completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Posting failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())