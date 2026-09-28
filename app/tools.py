import os
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeResearchTool:
    """
    Tool responsible for executing quota-efficient searches on YouTube API v3.
    """
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY missing from environment variables.")
        
        # Build the YouTube API service client
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def fetch_niche_data(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """
        Executes a 2-step retrieval:
        1. Search endpoint to retrieve video IDs (100 units)
        2. Videos endpoint to retrieve detailed statistics & durations in batch (1 unit)
        """
        try:
            # Step 1: Search for Video IDs
            search_response = self.youtube.search().list(
                q=query,
                type="video",
                part="id,snippet",
                maxResults=max_results
            ).execute()

            video_ids = [
                item["id"]["videoId"] 
                for item in search_response.get("items", []) 
                if "videoId" in item.get("id", {})
            ]

            if not video_ids:
                return []

            # Step 2: Batch fetch video stats & durations using the retrieved IDs
            video_response = self.youtube.videos().list(
                id=",".join(video_ids),
                part="snippet,statistics,contentDetails"
            ).execute()

            structured_data = []
            for item in video_response.get("items", []):
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                content_details = item.get("contentDetails", {})

                structured_data.append({
                    "video_id": item.get("id"),
                    "title": snippet.get("title"),
                    "channel_id": snippet.get("channelId"),
                    "channel_title": snippet.get("channelTitle"),
                    "published_at": snippet.get("publishedAt"),
                    "duration": content_details.get("duration"), # Raw ISO 8601 string (e.g. PT1M15S)
                    "view_count": int(stats.get("viewCount", 0)),
                    "like_count": int(stats.get("likeCount", 0)),
                    "comment_count": int(stats.get("commentCount", 0)),
                    "url": f"https://www.youtube.com/watch?v={item.get('id')}"
                })

            return structured_data

        except HttpError as e:
            print(f"YouTube API HttpError: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in YouTube tool: {e}")
            return []