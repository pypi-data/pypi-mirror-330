import os
import psutil
from .base import BaseCollector


class SystemCollector(BaseCollector):
    """Collector for system metrics like CPU, memory, and network"""

    def collect_cpu_metrics(self):
        """Collect CPU metrics"""
        return {
            "percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
            "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else None
        }

    def collect_memory_metrics(self):
        """Collect memory metrics"""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }

    def collect_network_metrics(self):
        """Collect network metrics"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }

    def collect_metrics(self):
        """Collect all system metrics"""
        return {
            "cpu": self.collect_cpu_metrics(),
            "memory": self.collect_memory_metrics(),
            "network": self.collect_network_metrics()
        }