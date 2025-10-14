# Reddit MCP Server

A FastMCP server that provides access to Reddit data and posts for Poke integration.

## 🚀 Features

- **get_subreddit_posts**: Get top posts from any subreddit
- **search_reddit**: Search all of Reddit
- **get_user_posts**: Get posts from a specific Reddit user

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python src/server.py
```

## 🚢 Deployment

### Option 1: One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deployment

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Deploy!

Your server will be available at `https://reddit-mcp.onrender.com/mcp`

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://reddit-mcp.onrender.com/mcp`
3. Give it a name like "Reddit"
4. Test with: "Tell the subagent to use the Reddit integration's get_subreddit_posts tool"

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
