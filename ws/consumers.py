from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.exceptions import StopConsumer
import ast


class DataConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        # 接收连接
        await self.accept()
        # 组别
        group = self.scope['url_route']['kwargs'].get('group')

        # 保存连接
        await self.channel_layer.group_add(group, self.channel_name)

    async def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        await self.channel_layer.group_send(group, {'type': 'to_web', 'message': message})

    async def to_web(self, event):
        await self.send(event["message"]["text"])

    async def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        await self.channel_layer.group_discard(group, self.channel_name)
        raise StopConsumer()


class VideoDataConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        await self.accept()
        group = self.scope['url_route']['kwargs'].get('group')
        # 保存连接
        await self.channel_layer.group_add(group, self.channel_name)

    async def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        await self.channel_layer.group_send(group, {'type': 'to_web', 'message': message})

    async def to_web(self, event):
        # print(event['message']['text'])
        # print(event)
        print("send img")
        await self.send(bytes_data=event['message']['bytes'])

    async def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')

        await self.channel_layer.group_discard(group, self.channel_name)

        raise StopConsumer()
