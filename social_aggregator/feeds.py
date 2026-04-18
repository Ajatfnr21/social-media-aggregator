"""Feed management and filtering."""

from typing import List, Callable
from .aggregator import SocialPost

class FeedManager:
    """Manage and filter social media feeds."""
    
    def __init__(self):
        self.filters = []
        self.posts = []
    
    def add_filter(self, filter_fn: Callable[[SocialPost], bool]):
        """Add a content filter."""
        self.filters.append(filter_fn)
    
    def process_posts(self, posts: List[SocialPost]) -> List[SocialPost]:
        """Apply filters to posts."""
        result = posts
        for filter_fn in self.filters:
            result = [p for p in result if filter_fn(p)]
        return result
    
    def deduplicate(self, posts: List[SocialPost]) -> List[SocialPost]:
        """Remove duplicate content."""
        seen = set()
        unique = []
        for post in posts:
            content_hash = hash(post.content[:50])
            if content_hash not in seen:
                seen.add(content_hash)
                unique.append(post)
        return unique
