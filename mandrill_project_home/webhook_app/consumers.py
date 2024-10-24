import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MandrillEventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "mandrill_events",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "mandrill_events",
            self.channel_name
        )

    async def email_opened(self, event):
        await self.send(text_data=json.dumps(event['message']))