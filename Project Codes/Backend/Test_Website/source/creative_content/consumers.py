from django.utils.dateformat import format as format_date
from django.conf import settings
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Content
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
        if not self.scope['user'].is_authenticated:
            await self.close()

        user_name = self.scope['user'].get_full_name()
        json_data = json.loads(text_data)
        request_type = json_data['request_type']

        if request_type == 'new_discussion':
            text = json_data['text']
            discussion = await self.save_discussion_message(text)
            date = format_date(discussion.date, settings.DATETIME_FORMAT)
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
            response = await self.save_reply_message(thread_id, text)
            date = format_date(response.date, settings.DATETIME_FORMAT)
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'reply_message',
                    'target_id': thread_id,
                    'node_id': response.id,
                    'user_name': user_name,
                    'date': date,
                    'text': text
                }
            )
        elif request_type == 'edit_discussion':
            text = json_data['text']
            thread_id = json_data['node_id']
            discussion = await self.update_discussion_message(thread_id, text)
            date = format_date(discussion.date, settings.DATETIME_FORMAT)
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'update_discussion',
                    'node_id': thread_id,
                    'date': date,
                    'text': text
                }
            )
        elif request_type == 'edit_reply':
            text = json_data['text']
            thread_id = json_data['node_id']
            response = await self.update_reply_message(thread_id, text)
            date = format_date(response.date, settings.DATETIME_FORMAT)
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'update_reply',
                    'node_id': thread_id,
                    'date': date,
                    'text': text
                }
            )
        elif request_type == 'delete_discussion':
            thread_id = json_data['node_id']
            await self.remove_discussion_message(thread_id)
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'remove_discussion',
                    'node_id': thread_id,
                }
            )
        elif request_type == 'delete_reply':
            thread_id = json_data['node_id']
            await self.remove_reply_message(thread_id)
            await self.channel_layer.group_send(
                self.discussion_thread,
                {
                    'type': 'remove_reply',
                    'node_id': thread_id,
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

    async def update_discussion(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'edit_discussion',
            'node_id': event['node_id'],
            'date': event['date'],
            'text': event['text']
        }))

    async def remove_discussion(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'delete_discussion',
            'node_id': event['node_id'],
        }))

    async def reply_message(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'new_reply',
            'target_id': event['target_id'],
            'node_id': event['node_id'],
            'user_name': event['user_name'],
            'date': event['date'],
            'text': event['text']
        }))

    async def update_reply(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'edit_reply',
            'node_id': event['node_id'],
            'date': event['date'],
            'text': event['text']
        }))

    async def remove_reply(self, event):
        await self.send(text_data=json.dumps({
            'request_type': 'delete_reply',
            'node_id': event['node_id'],
        }))

    @database_sync_to_async
    def save_discussion_message(self, text):
        content = self.get_content()
        discussion = content.discussion.create(text=text, user=self.scope['user'])
        return discussion

    @database_sync_to_async
    def update_discussion_message(self, thread_id, text):
        content = self.get_user_content()
        try:
            discussion = content.discussion.get(id=thread_id)
        except Content.DoesNotExist:
            self.close()
        else:
            discussion.text = text
            discussion.save()
            return discussion

    @database_sync_to_async
    def remove_discussion_message(self, thread_id):
        content = self.get_user_content()
        try:
            discussion = content.discussion.get(id=thread_id)
        except Content.DoesNotExist:
            self.close()
        else:
            discussion.delete()

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
            return response

    @database_sync_to_async
    def update_reply_message(self, thread_id, text):
        thread_id = thread_id.split('_')
        content = self.get_user_content()
        try:
            discussion = content.discussion.get(id=thread_id[0])
            response = discussion.response.get(id=thread_id[1])
        except Content.DoesNotExist:
            self.close()
        else:
            response.text = text
            response.save()
            return response

    @database_sync_to_async
    def remove_reply_message(self, thread_id):
        thread_id = thread_id.split('_')
        content = self.get_user_content()
        try:
            discussion = content.discussion.get(id=thread_id[0])
            response = discussion.response.get(id=thread_id[1])
        except Content.DoesNotExist:
            self.close()
        else:
            response.delete()

    def get_content(self):
        try:
            content = Content.objects.get(link=self.discussion_thread)
        except Content.DoesNotExist:
            self.close()
        else:
            return content

    def get_user_content(self):
        try:
            content = self.scope['user'].content_set.get(link=self.discussion_thread)
        except Content.DoesNotExist:
            self.close()
        else:
            return content
