# Reddit MCP Server

A FastMCP server that provides access to Reddit data and posts for Poke integration.

## 🚀 Features

- **get_subreddit_posts**: Get top posts from any subreddit
- **search_reddit**: Search all of Reddit
- **get_user_posts**: Get posts from a specific Reddit user

## 🔑 Reddit API Setup

This server requires Reddit API credentials:

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note down your `client_id` and `client_secret`
5. Set environment variables:
   ```bash
   export REDDIT_CLIENT_ID=your_client_id
   export REDDIT_CLIENT_SECRET=your_client_secret
   ```

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set Reddit API credentials
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret

# Run the server
python src/server.py
```

## 🚢 Deployment

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Steps:**
1. **Click the "Deploy to Render" button above** or go to [render.com](https://render.com)
2. **Connect your GitHub account to Render** (if you haven't already)
3. **Create a new Web Service:**
   - Connect this repository
   - **Name**: `reddit-mcp`
   - **Environment**: `Python 3`
   - **Plan**: `Free`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/server.py`
4. **Add Reddit API credentials to environment variables:**
   - Go to your Render service dashboard
   - Click on "Environment" tab
   - Add these environment variables:
     - `REDDIT_CLIENT_ID` = `your_client_id_here`
     - `REDDIT_CLIENT_SECRET` = `your_client_secret_here`
   - Click "Save Changes"
5. **Deploy!**

> Note: On Render's free tier, services go idle after ~15 minutes of inactivity and may require a manual "Deploy" to wake or to pick up the latest commit. Unlike Vercel, pushes do not auto-deploy by default.

Your server will be available at `https://reddit-mcp.onrender.com/mcp`

### 🔑 Getting Reddit API Credentials

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **Name**: `pokeMCPMarket`
   - **App Type**: `script` (Script for personal use)
   - **Description**: `MCP server for accessing Reddit data through Poke marketplace integration`
   - **About URL**: `https://github.com/yourusername/mcp-reddit`
   - **Redirect URI**: `http://localhost:8080`
4. Click "Create app"
5. Copy your `client_id` and `client_secret`
6. Add them to Render environment variables as shown above

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://reddit-mcp.onrender.com/mcp`
3. Give it a name like "Reddit"
4. Try: "Can you use the Reddit MCP to get posts from r/python?"

## References

- Based on the Interaction MCP server template: [MCP Server Template](https://github.com/InteractionCo/mcp-server-template/tree/main)
- Discovered via Interaction’s HackMIT challenge: [Interaction HackMIT Challenge](https://interaction.co/HackMIT)

## 🔧 Available Tools

- `get_subreddit_posts(subreddit, limit=10, sort="hot")`: Get posts from a subreddit
- `search_reddit(query, limit=10, sort="relevance")`: Search all of Reddit
- `get_user_posts(username, limit=10, sort="new")`: Get posts from a user

## 📝 Example Usage

```python
# Get hot posts from r/programming
get_subreddit_posts(subreddit="programming", limit=5, sort="hot")

# Search for Python posts
search_reddit(query="python programming", limit=10, sort="relevance")

# Get posts from a specific user
get_user_posts(username="spez", limit=5, sort="new")
```

## 📊 Post Data Structure

Each post returned includes:
- `title`: Post title
- `author`: Username of the author
- `score`: Net upvotes (upvotes - downvotes)
- `upvote_ratio`: Ratio of upvotes to total votes
- `num_comments`: Number of comments
- `url`: External URL (if not a self post)
- `permalink`: Reddit permalink
- `created_utc`: Creation timestamp (Unix)
- `selftext`: Post text content (for self posts)
- `subreddit`: Subreddit name
- `is_self`: Whether it's a self post
- `over_18`: Whether it's NSFW

## ⚠️ Rate Limits

Reddit API has rate limits:
- **Without authentication**: 60 requests per minute
- **With authentication**: 100 requests per minute

The server will return an error if rate limits are exceeded.

## 🔍 Sort Options

### Subreddit Posts
- `hot`: Hot posts (default)
- `new`: Newest posts
- `top`: Top posts of all time
- `rising`: Rising posts

### Search
- `relevance`: Most relevant (default)
- `hot`: Hot posts
- `top`: Top posts
- `new`: Newest posts
- `comments`: Most commented

### User Posts
- `new`: Newest posts (default)
- `hot`: Hot posts
- `top`: Top posts
- `controversial`: Most controversial posts
