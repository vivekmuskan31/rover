# sensor.py

import abc

class BaseSensor(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    async def start(self):
        """Start the sensor's data streaming loop."""
        pass

    @abc.abstractmethod
    def get_data(self):
        """Return a single snapshot of sensor data (used for test or polling)."""
        pass

    @abc.abstractmethod
    def test(self):
        """Test method to log or print data manually."""
        pass


