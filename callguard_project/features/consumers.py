import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Call
from .serializers import CallSerializer
from .spam_detection import check_spam  # Import spam detection function


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Check if the transcribed text is spam
        is_spam = await sync_to_async(check_spam)(message)

        await self.send(text_data=json.dumps({
            'message': message,
            'is_spam': is_spam,
        }))

    async def call_alert(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'alert',
            'message': message,
        }))
