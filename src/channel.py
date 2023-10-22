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

    def __str__(self):
        """Метод возвращающий название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Метод для сложения объектов Channel (по кол-ву подписчиков)"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Метод для вычитания одного объекта Channel из другого (по кол-ву подписчиков)"""
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        """Метод для проверки равенства двух объектов Channel (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count == other.subscriber_count

    def __lt__(self, other):
        """Метод для проверки, меньше ли один объект Channel другого (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Метод для проверки, меньше или равен один объект Channel другому (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        """Метод для проверки, больше ли один объект Channel другого (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Метод для проверки, больше или равен один объект Channel другому (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count >= other.subscriber_count

    def __ne__(self, other):
        """Метод для проверки неравенства двух объектов Channel (по кол-ву подписчиков)"""
        if isinstance(other, Channel):
            return self.subscriber_count != other.subscriber_count

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
