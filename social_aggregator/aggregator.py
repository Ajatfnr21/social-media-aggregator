"""Multi-platform API aggregator."""

import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class SocialPost:
    platform: str
    post_id: str
    author: str
    content: str
    created_at: datetime
    likes: int = 0
    shares: int = 0
    url: str = ""

class SocialAggregator:
    """Aggregate posts from multiple social platforms."""
    
    def __init__(self):
        self.platforms = {}
        self.posts = []
    
    def add_platform(self, name: str, api_key: str, api_secret: str = None):
        """Add a social platform."""
        self.platforms[name] = {
            'api_key': api_key,
            'api_secret': api_secret
        }
    
    async def fetch_twitter(self, query: str, count: int = 100) -> List[SocialPost]:
        """Fetch tweets."""
        # Mock implementation
        return [
            SocialPost(
                platform='twitter',
                post_id=f'tw_{i}',
                author='user',
                content=f'Tweet about {query}',
                created_at=datetime.now(),
                likes=10,
                shares=2
            )
            for i in range(count)
        ]
    
    async def fetch_reddit(self, subreddit: str, limit: int = 100) -> List[SocialPost]:
        """Fetch Reddit posts."""
        return [
            SocialPost(
                platform='reddit',
                post_id=f'rd_{i}',
                author='redditor',
                content=f'Post in r/{subreddit}',
                created_at=datetime.now(),
                likes=50,
                shares=5
            )
            for i in range(limit)
        ]
    
    async def fetch_all(self, queries: Dict[str, Any]) -> List[SocialPost]:
        """Fetch from all platforms."""
        tasks = []
        
        if 'twitter' in queries:
            tasks.append(self.fetch_twitter(queries['twitter']))
        if 'reddit' in queries:
            tasks.append(self.fetch_reddit(queries['reddit']))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_posts = []
        for result in results:
            if isinstance(result, list):
                all_posts.extend(result)
        
        return all_posts
