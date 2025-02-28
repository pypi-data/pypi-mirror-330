from abc import ABC, abstractmethod


class BaseCollector(ABC):
    """Base class for all metric collectors"""

    @abstractmethod
    def collect_metrics(self):
        """Collect and return metrics in a dictionary format"""
        pass