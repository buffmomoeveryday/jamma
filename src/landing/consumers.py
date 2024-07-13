import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from icecream import ic

from track.models import Website


class PageViewConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.channel_layer.group_add("usergroup", self.channel_name)
        await self.accept()

    async def disconnect(self, code):

        await self.channel_layer.group_discard("usergroup", self.channel_name)

    async def send_unique_page_view(self, event):
        dict_obj = {"unqiue_page_view": "true", "text_message": str(event["text"])}
        await self.send(text_data=json.dumps(dict_obj))

    async def send_unqiue_users(self, event):
        pass
