#!/usr/bin/env python3
"""
Reddit MCP Server
A FastMCP server that provides access to Reddit data using PRAW.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import praw
from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Reddit MCP Server")

# Reddit API configuration
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "RedditMCP/1.0 by u/redditmcp"

# Initialize Reddit instance
def get_reddit_instance():
    """Get Reddit instance with proper credentials."""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError("REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables are required")
    
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )


@mcp.tool()
def get_subreddit_posts(subreddit: str, limit: int = 10, sort: str = "hot") -> str:
    """Get top posts from any subreddit.
    
    Args:
        subreddit: Subreddit name (without r/)
        limit: Number of posts to return (default: 10, max: 25)
        sort: Sort order: hot, new, top, rising (default: hot)
    
    Returns:
        JSON string with subreddit posts data
    """
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25
        
        reddit = get_reddit_instance()
        subreddit_obj = reddit.subreddit(subreddit)
        
        # Get posts based on sort type
        if sort == "hot":
            posts = subreddit_obj.hot(limit=limit)
        elif sort == "new":
            posts = subreddit_obj.new(limit=limit)
        elif sort == "top":
            posts = subreddit_obj.top(limit=limit, time_filter="day")
        elif sort == "rising":
            posts = subreddit_obj.rising(limit=limit)
        else:
            posts = subreddit_obj.hot(limit=limit)
        
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "url": post.url,
                "permalink": f"https://reddit.com{post.permalink}",
                "created_utc": post.created_utc,
                "selftext": post.selftext,
                "subreddit": str(post.subreddit),
                "is_self": post.is_self,
                "over_18": post.over_18,
                "stickied": post.stickied,
                "locked": post.locked
            })
        
        return json.dumps(formatted_posts, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error fetching subreddit posts: {str(e)}"}, indent=2)

@mcp.tool()
def search_reddit(query: str, limit: int = 10, sort: str = "relevance") -> str:
    """Search all of Reddit.
    
    Args:
        query: Search query string
        limit: Number of results to return (default: 10, max: 25)
        sort: Sort order: relevance, hot, top, new, comments (default: relevance)
    
    Returns:
        JSON string with search results
    """
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25
        
        reddit = get_reddit_instance()
        
        # Search across all of Reddit
        search_results = reddit.subreddit("all").search(query, limit=limit, sort=sort)
        
        formatted_posts = []
        for post in search_results:
            formatted_posts.append({
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "url": post.url,
                "permalink": f"https://reddit.com{post.permalink}",
                "created_utc": post.created_utc,
                "selftext": post.selftext,
                "subreddit": str(post.subreddit),
                "is_self": post.is_self,
                "over_18": post.over_18,
                "stickied": post.stickied,
                "locked": post.locked
            })
        
        return json.dumps(formatted_posts, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error searching Reddit: {str(e)}"}, indent=2)

@mcp.tool()
def get_user_posts(username: str, limit: int = 10, sort: str = "new") -> str:
    """Get posts from a specific Reddit user.
    
    Args:
        username: Reddit username (without u/)
        limit: Number of posts to return (default: 10, max: 25)
        sort: Sort order: new, hot, top, controversial (default: new)
    
    Returns:
        JSON string with user posts data
    """
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25
        
        reddit = get_reddit_instance()
        user = reddit.redditor(username)
        
        # Get user's submitted posts
        posts = user.submissions.new(limit=limit)
        
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "url": post.url,
                "permalink": f"https://reddit.com{post.permalink}",
                "created_utc": post.created_utc,
                "selftext": post.selftext,
                "subreddit": str(post.subreddit),
                "is_self": post.is_self,
                "over_18": post.over_18,
                "stickied": post.stickied,
                "locked": post.locked
            })
        
        return json.dumps(formatted_posts, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error fetching user posts: {str(e)}"}, indent=2)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        stateless_http=True
    )