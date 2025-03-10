import os
from googleapiclient.discovery import build

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            video_response = youtube.videos().list(
                part='contentDetails,statistics,snippet',
                id=self.video_id
            ).execute()
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f"https://youtu.be/{self.video_id}"
            self.views_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.url = f"https://youtu.be/{self.video_id}"
            self.views_count = None
            self.like_count = None

    def __str__(self):
        if self.title:
            return self.title
        else:
            return f"Video with ID {self.video_id} not found"


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.title
