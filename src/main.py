import os
import time
import socketio
from dotenv import load_dotenv

from infrastructure.SioClient import SioClient
from infrastructure.SioClientWrapper import SioClientWrapper

load_dotenv()

MAX_RETRY_DELAY_SEC = float(os.getenv("SOCKET_IO_MAX_RETRY_DELAY_SEC", "30"))
INITIAL_RETRY_DELAY_SEC = float(os.getenv("SOCKET_IO_INITIAL_RETRY_DELAY_SEC", "2"))

sio = socketio.Client(logger=True, engineio_logger=True)


def connect_with_retry(sio_client: socketio.Client, url: str, auth: dict):
    delay = INITIAL_RETRY_DELAY_SEC
    attempt = 1
    while True:
        try:
            print(f"Connecting to Socket.IO server (attempt {attempt})...")
            sio_client.connect(url, auth=auth)
            print("Connected to Socket.IO server.")
            return
        except Exception as e:
            print(f"Connection attempt {attempt} failed: {e}")
            print(f"Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay = min(delay * 2, MAX_RETRY_DELAY_SEC)
            attempt += 1


if __name__ == '__main__':
    sio_client_instance = SioClient(sio)
    sio_client_wrapper = SioClientWrapper(sio_client_instance)

    connect_with_retry(
        sio,
        os.getenv("SOCKET_IO_SERVER"),
        auth={"robotId": os.getenv("ROBOT_ID")}
    )

    sio.wait()