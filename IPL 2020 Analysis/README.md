# IPL Twitter Analysis

This project fetches tweets about the Indian Premier League (IPL) using the Twitter API.

## Setup Instructions

### 1. Twitter API Credentials

You need Twitter API credentials to use this script. To set them up:

1. Create a developer account at [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a project and app
3. Generate API keys and tokens
4. Create a `.env` file in this directory with your credentials

### 2. Environment Variables

Create a `.env` file with the following structure:

```
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
BEARER_TOKEN=your_bearer_token_here
```

⚠️ **IMPORTANT SECURITY WARNING** ⚠️
- NEVER commit your `.env` file to Git
- NEVER share your API keys publicly
- If you accidentally expose your keys, regenerate them immediately

### 3. Install Dependencies

```bash
pip install tweepy python-dotenv pandas
```

### 4. Run the Script

```bash
python fetch_ipl_tweets.py
```

## Output

The script will create a file called `ipl_tweets.csv` with the following columns:
- created_at: When the tweet was created
- text: The content of the tweet
- username: Twitter handle of the author
- author_name: Display name of the author
- retweets: Number of retweets
- likes: Number of likes
- replies: Number of replies

## API Limits

With the free Twitter API tier, you have:
- 5,000 tweets per month
- Only the last 7 days of tweets
- 50 requests per hour

Use the script sparingly to avoid hitting these limits. 