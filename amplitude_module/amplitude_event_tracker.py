import threading
from concurrent.futures import ThreadPoolExecutor
from settings import settings
from amplitude import Amplitude, BaseEvent


class AmplitudeEventTracker:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, max_workers=5):
        with self._lock:
            if self._initialized:
                return
            self.amplitude = Amplitude(settings.AMPLITUDE_API_KEY)
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            self._initialized = True

    def send_event(self, event_type, user_id, event_properties=None):
        event = BaseEvent(
            event_type=event_type,
            user_id=user_id,
            event_properties=event_properties
        )
        self.amplitude.track(event)

    def track_event(self, event_name, user_id, event_properties=None):
        self.executor.submit(self.send_event, event_name, user_id, event_properties)
