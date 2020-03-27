from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class CommentsConsumer(AsyncWebsocketConsumer):
    chat_thread = None

    async def connect(self):
        print("Socket Connected")
        thread = self.scope['url_route']['kwargs']['content_id']
        print(thread)
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass
