# utilsLib/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)
        logger.info("WebSocket connection established.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)
        logger.info("WebSocket connection closed.")

    async def receive(self, text_data):
        logger.info(f"Received raw message: {text_data}")
        if not text_data:
            logger.error("Empty message received.")
            await self.send(text_data=json.dumps({
                'error': 'Empty message received'
            }))
            return

        try:
            # Attempt to parse the incoming message as JSON
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', 'No message provided')

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                "notifications",
                {
                    'type': 'notification_message',
                    'message': message
                }
            )
        except json.JSONDecodeError as e:
            # Handle invalid JSON
            logger.error(f"Invalid JSON message: {text_data}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON message'
            }))
        except Exception as e:
            # Handle any other exceptions
            logger.error(f"Error processing message: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while processing the message'
            }))

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        logger.info(f"Sent message: {message}")
