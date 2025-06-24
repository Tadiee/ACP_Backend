import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import System_Files

class ChartDataConsumer (AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection initiated")  # Debug
        await self.channel_layer.group_add('chart_updates', self.channel_name)
        self.accept()
        #send initial data on connect
        await self.send_chart_data()
        
    async def  disconnect(self, close_code):
        await self.channel_layer.group_discard('chart_updates', self.channel_name)
        
    async def receive(self, text_data):
        # Logic for handling data sent from client [Front-end]
        pass
    
    @database_sync_to_async
    def get_chart_data(self):
        months = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
        systems = ['D365', 'Active Directory', 'D365 DB', 'User Monitoring', 'Backups']
        
        data = {}
        for system in systems:
            data[system] = [0] * len(months)
            files = System_Files.objects.filter(system = system)
            for file in files:
                if file.month in months:
                    month_index =  months.index(file.month)
                    data[system][month_index] += 1
        return data
    
    async def send_chart_data(self):
        data = await self.get_chart_data()
        await self.send(text_data =  json.dumps(data))
        
    async def chart_update(self, event):
         # This method is called when we want to push updates to all connected clients
         await self.send_chart_data()
         
         
         