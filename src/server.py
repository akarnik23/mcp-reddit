#!/usr/bin/env python3
"""
Reddit MCP Server
A FastMCP server that provides access to Reddit data and posts.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import httpx
from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Reddit MCP Server")

# Reddit API configuration
REDDIT_API_BASE = "https://www.reddit.com"

# Undecorated functions for HTTP endpoint
def get_subreddit_posts_http(subreddit: str, limit: int = 10, sort: str = "hot") -> str:
    """Get posts from any subreddit."""
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25 (Reddit's limit)
        
        # Reddit returns JSON if you add .json
        url = f"{REDDIT_API_BASE}/r/{subreddit}/{sort}.json?limit={limit}"
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def search_reddit_http(query: str, limit: int = 10, sort: str = "relevance") -> str:
    """Search all of Reddit."""
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25
        
        # Reddit search API
        url = f"{REDDIT_API_BASE}/search.json"
        params = {
            "q": query,
            "limit": limit,
            "sort": sort
        }
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def get_user_posts_http(username: str, limit: int = 10, sort: str = "new") -> str:
    """Get posts from a specific Reddit user."""
    try:
        limit = min(max(limit, 1), 25)  # Clamp between 1 and 25
        
        # Reddit user posts API
        url = f"{REDDIT_API_BASE}/u/{username}/submitted.json?limit={limit}&sort={sort}"
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

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
        
        # Reddit returns JSON if you add .json
        url = f"{REDDIT_API_BASE}/r/{subreddit}/{sort}.json?limit={limit}"
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

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
        
        # Reddit search API
        url = f"{REDDIT_API_BASE}/search.json"
        params = {
            "q": query,
            "limit": limit,
            "sort": sort
        }
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

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
        
        # Reddit user posts API
        url = f"{REDDIT_API_BASE}/u/{username}/submitted.json?limit={limit}&sort={sort}"
        
        headers = {
            "User-Agent": "Reddit-MCP-Server/1.0"
        }
        
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            posts.append({
                "title": post_data.get("title", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": post_data.get("url", ""),
                "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
                "created_utc": post_data.get("created_utc", 0),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "is_self": post_data.get("is_self", False),
                "over_18": post_data.get("over_18", False)
            })
        
        return json.dumps(posts, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

if __name__ == "__main__":
    # Run in HTTP mode for testing
    import uvicorn
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    import json
    
    # Create FastAPI app
    app = FastAPI()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def health_check():
        return {"status": "ok", "server": "Reddit MCP Server"}
    
    @app.post("/")
    @app.post("/mcp")
    async def mcp_endpoint(request: dict):
        """Handle MCP requests via HTTP POST"""
        try:
            print(f"Received request: {request}")
            
            if request.get("method") == "initialize":
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "Reddit MCP Server", "version": "1.0.0"}
                    }
                })
            elif request.get("method") == "tools/list":
                tools = [
                    {
                        "name": "get_subreddit_posts", 
                        "description": "Get top posts from any subreddit", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "subreddit": {
                                    "type": "string",
                                    "description": "Subreddit name (without r/)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of posts to return (1-25)",
                                    "minimum": 1,
                                    "maximum": 25,
                                    "default": 10
                                },
                                "sort": {
                                    "type": "string",
                                    "description": "Sort order",
                                    "enum": ["hot", "new", "top", "rising"],
                                    "default": "hot"
                                }
                            },
                            "required": ["subreddit"]
                        }
                    },
                    {
                        "name": "search_reddit", 
                        "description": "Search all of Reddit", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query string"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of results to return (1-25)",
                                    "minimum": 1,
                                    "maximum": 25,
                                    "default": 10
                                },
                                "sort": {
                                    "type": "string",
                                    "description": "Sort order",
                                    "enum": ["relevance", "hot", "top", "new", "comments"],
                                    "default": "relevance"
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_user_posts", 
                        "description": "Get posts from a specific Reddit user", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "Reddit username (without u/)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of posts to return (1-25)",
                                    "minimum": 1,
                                    "maximum": 25,
                                    "default": 10
                                },
                                "sort": {
                                    "type": "string",
                                    "description": "Sort order",
                                    "enum": ["new", "hot", "top", "controversial"],
                                    "default": "new"
                                }
                            },
                            "required": ["username"]
                        }
                    }
                ]
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": tools}
                })
            elif request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                tool_args = request.get("params", {}).get("arguments", {})
                
                if tool_name == "get_subreddit_posts":
                    result = get_subreddit_posts_http(**tool_args)
                elif tool_name == "search_reddit":
                    result = search_reddit_http(**tool_args)
                elif tool_name == "get_user_posts":
                    result = get_user_posts_http(**tool_args)
                else:
                    return JSONResponse(content={
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                    })
                
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"content": [{"type": "text", "text": result}]}
                })
            else:
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Method '{request.get('method')}' not found"}
                })
                
        except Exception as e:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }, 
                status_code=500
            )
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
