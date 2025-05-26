# controller.py

import abc

class BaseController(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    async def handle_command(self, data: dict):
        """Handle incoming control message."""
        pass

    @abc.abstractmethod
    def test(self, data: dict=None):
        """Manually invoke the controller for testing."""
        pass
    
    @abc.abstractmethod
    def cleanup(self, data: dict=None):
        """Manually invoke the controller for testing."""
        pass

