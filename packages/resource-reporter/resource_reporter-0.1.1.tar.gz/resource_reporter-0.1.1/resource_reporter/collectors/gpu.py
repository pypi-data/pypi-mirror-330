from .base import BaseCollector


class GPUCollector(BaseCollector):
    """Collector for NVIDIA GPU metrics"""

    def __init__(self):
        """Initialize the GPU collector"""
        import pynvml
        self.pynvml = pynvml
        self.pynvml.nvmlInit()

    def __del__(self):
        """Clean up NVML when the collector is destroyed"""
        try:
            self.pynvml.nvmlShutdown()
        except:
            pass

    def collect_metrics(self):
        """Collect GPU metrics"""
        try:
            device_count = self.pynvml.nvmlDeviceGetCount()
            gpu_info = []

            for i in range(device_count):
                handle = self.pynvml.nvmlDeviceGetHandleByIndex(i)
                info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
                util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)

                gpu_info.append({
                    "id": i,
                    "memory_used_percent": round(info.used / info.total * 100, 2),
                    "utilization_percent": util.gpu
                })

            return gpu_info
        except Exception as e:
            return []
