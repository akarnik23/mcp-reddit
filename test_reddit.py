#!/usr/bin/env python3
"""
Test script for Reddit MCP Server
"""

import requests
import json

# Replace with your tunnel URL
TUNNEL_URL = "https://reddit-test.loca.lt"  # Your localtunnel URL

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{TUNNEL_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_tools_list():
    """Test tools/list endpoint"""
    print("\n🔍 Testing tools/list...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        response = requests.post(f"{TUNNEL_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Tools available: {len(data['result']['tools'])}")
        for tool in data['result']['tools']:
            print(f"  - {tool['name']}: {tool['description']}")
        return True
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
        return False

def test_subreddit_posts():
    """Test get_subreddit_posts"""
    print("\n🔍 Testing get_subreddit_posts...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_subreddit_posts",
                "arguments": {
                    "subreddit": "programming",
                    "limit": 3
                }
            }
        }
        response = requests.post(f"{TUNNEL_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        if 'result' in data:
            posts = json.loads(data['result']['content'][0]['text'])
            print(f"Got {len(posts)} posts from r/programming:")
            for i, post in enumerate(posts[:2], 1):
                print(f"  {i}. {post['title'][:60]}... (Score: {post['score']})")
        else:
            print(f"Error: {data}")
        return True
    except Exception as e:
        print(f"❌ Subreddit posts test failed: {e}")
        return False

def test_search_reddit():
    """Test search_reddit"""
    print("\n🔍 Testing search_reddit...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search_reddit",
                "arguments": {
                    "query": "python",
                    "limit": 3
                }
            }
        }
        response = requests.post(f"{TUNNEL_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        if 'result' in data:
            posts = json.loads(data['result']['content'][0]['text'])
            print(f"Got {len(posts)} search results for 'python':")
            for i, post in enumerate(posts[:2], 1):
                print(f"  {i}. {post['title'][:60]}... (r/{post['subreddit']})")
        else:
            print(f"Error: {data}")
        return True
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Reddit MCP Server")
    print(f"Tunnel URL: {TUNNEL_URL}")
    print("=" * 50)
    
    # Update the tunnel URL first!
    if "your-tunnel-url" in TUNNEL_URL:
        print("❌ Please update TUNNEL_URL with your actual tunnel URL first!")
        exit(1)
    
    tests = [
        test_health,
        test_tools_list,
        test_subreddit_posts,
        test_search_reddit
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n✅ Tests passed: {passed}/{len(tests)}")
