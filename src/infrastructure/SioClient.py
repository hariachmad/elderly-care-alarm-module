class SioClient:
    _instance = None

    def __new__(cls, sio=None):
        if cls._instance is None:
            if sio is None:
                raise ValueError("sio should not be None")
            cls._instance = super().__new__(cls)
            cls._instance.sio = sio
        elif sio is not None and sio is not cls._instance.sio:
            raise RuntimeError("SioClient sudah diinisialisasi dengan sio yang berbeda")
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("SioClient is not initialized")
        return cls._instance