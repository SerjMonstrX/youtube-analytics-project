import json
import os

from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Инициализация объекта канала"""
        self._channel_id = channel_id
        self.channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()['items'][0]
        self.title = self.channel_info['snippet']['title']
        self.description = self.channel_info['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscriber_count = int(self.channel_info['statistics']['subscriberCount'])
        self.video_count = int(self.channel_info['statistics']['videoCount'])
        self.view_count = int(self.channel_info['statistics']['viewCount'])

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        raise AttributeError("Нельзя изменять атрибут channel_id")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """Сохраняет данные канала в файл в формате JSON"""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
