from django.utils.dateformat import format as format_date
from django.conf import settings
from django.utils.timesince import timesince
from django.utils.timezone import now as current_time
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Content, DiscussionThread, RepliesThread
import json


class DiscussionConsumer(AsyncWebsocketConsumer):
    discussion_thread = None

    async def connect(self):
        print("Socket Connected")
        self.discussion_thread = self.scope['url_route']['kwargs']['content_id']

        await self.channel_layer.group_add(
            self.discussion_thread,
            self.channel_name
        )

        if self.scope['user'].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        print('Socket Closed')

    async def receive(self, text_data=None, bytes_data=None):
        user_name = self.scope['user'].get_full_name()
        json_data = json.loads(text_data)
        request_type = json_data['request_type']

        if request_type == 'new_discussion':
            text = json_data['text']
            discussion = await self.save_discussion_message(text)
            # date = format_date(discussion.date, settings.DATETIME_FORMAT)
            date = timesince(discussion.date, current_time())
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'discussion_message',
                    'node_id': discussion.id,
                    'user_name': user_name,
                    'date': date,
                    'text': text
                }
            )
        elif request_type == 'new_reply':
            text = json_data['text']
            thread_id = json_data['target_id']
            # date = await self.save_reply_message(thread_id, text).strftime('%B %-d, %Y, %-I:%M %p')
            date = await self.save_reply_message(thread_id, text)
            # date = format_date(date, settings.DATETIME_FORMAT)
            date = timesince(date, current_time())
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'reply_message',
                    'target_id': thread_id,
                    'user_name': user_name,
                    'date': date,
                    'text': text
                }
            )
        else:
            await self.close()

    async def discussion_message(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'new_discussion',
            'node_id': event['node_id'],
            'user_name': event['user_name'],
            'date': event['date'],
            'text': event['text']
        }))

    async def reply_message(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'new_reply',
            'target_id': event['target_id'],
            'user_name': event['user_name'],
            'date': event['date'],
            'text': event['text']
        }))

    @database_sync_to_async
    def save_discussion_message(self, text):
        content = self.get_content()
        discussion = content.discussion.create(text=text, user=self.scope['user'])
        return discussion

    @database_sync_to_async
    def save_reply_message(self, thread_id, text):
        content = self.get_content()
        thread_id = thread_id.split('_')[-1]
        try:
            discussion = content.discussion.get(id=thread_id)
        except Content.DoesNotExist:
            self.close()
        else:
            response = discussion.response.create(text=text, user=self.scope['user'])
            return response.date

    def get_content(self):
        try:
            content = Content.objects.get(link=self.discussion_thread)
        except Content.DoesNotExist:
            self.close()
        else:
            return content
