import datetime
import isodate
from googleapiclient.discovery import build
import os


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_response = self.youtube.playlists().list(
            part='snippet',
            id=self.playlist_id
        ).execute()

        playlist_info = playlist_response['items'][0]['snippet']
        self.title = playlist_info['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.video_ids = []

    @property
    def total_duration(self):
        total_seconds = 0
        video_response = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id
        ).execute()
        self.video_ids = [item['contentDetails']['videoId'] for item in video_response['items']]

        video_response = self.youtube.videos().list(part='contentDetails', id=','.join(self.video_ids)).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_seconds += duration.total_seconds()

        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        best_video = None
        max_likes = -1

        playlist_items = self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=self.playlist_id
        ).execute()

        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_response = self.youtube.videos().list(part='statistics', id=video_id).execute()
            likes_count = int(video_response['items'][0]['statistics']['likeCount'])
            if likes_count > max_likes:
                max_likes = likes_count
                best_video = item

        return "https://youtu.be/" + best_video['contentDetails']['videoId']
