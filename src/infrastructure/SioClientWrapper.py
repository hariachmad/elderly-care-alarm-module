import json
import os
class SioClientWrapper:
    def __init__(self, sio_client):
        self.CONFIG_PATH = os.getenv('CONFIG_PATH')
        if not self.CONFIG_PATH:
            raise ValueError("CONFIG_PATH environment variable is not set")
        self.sio_client = sio_client
        self._register_events()
        
    def load_config(self,):
        with open(self.CONFIG_PATH, 'r') as f:
            return json.load(f)

    def save_config(self,config):
        with open(self.CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

    def _register_events(self):
        sio = self.sio_client.get_instance().sio

        @sio.event
        def connect():
            print("Connected with server")

        @sio.event
        def disconnect():
            print("Disconnected from server")

        @sio.event
        def message(data):
            print(f"Event received: {data}")
            
        @sio.event
        def error(data):
            print(f"Error: {data}")
        
        @sio.on('ALARM_RING')
        def on_alarm_ring():
            self.emit('WAKE_UP_BY_ALARM')  
            self.emit('ALARM_RING')  
            
        @sio.on('ALARM_STOP')
        def on_alarm_stop(payload):
            self.emit('ALARM_STOP')
            
        @sio.on('ALARM_SNOOZE')
        def on_alarm_snooze(payload):
            self.emit('ALARM_SNOOZE')
        
            
    def emit(self, event: str, data: dict = None):
        """Send event to server"""
        self.sio_client.emit(event, data)

    def emit_with_callback(self, event: str, data: dict = None, callback=None):
        """Send event to server with callback"""
        self.sio_client.emit(event, data, callback=callback)
    
    

