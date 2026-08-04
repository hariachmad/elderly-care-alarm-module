import json
import os
class SioClientWrapper:
    def __init__(self, sio_client):
        self.sio_client = sio_client
        self._register_events()

    def _register_events(self):
        sio = self.sio_client.get_instance().sio

        @sio.event
        def connect(*args):
            print("Connected with server")

        @sio.event
        def disconnect():
            print("Disconnected from server")
            
        @sio.event
        def error(data):
            print(f"Error: {data}")
        
        @sio.on('ALARM_RING')
        def on_alarm_ring(*args):
            self.emit('WAKE_UP_BY_ALARM', {})
            
    def emit(self, event: str, data: dict = None):
        """Send event to server"""
        self.sio_client.get_instance().sio.emit(event, data)

    def emit_with_callback(self, event: str, data: dict = None, callback=None):
        """Send event to server with callback"""
        self.sio_client.get_instance().sio.emit(event, data, callback=callback)
    
    

