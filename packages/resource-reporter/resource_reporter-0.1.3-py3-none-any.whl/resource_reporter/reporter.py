import json
import logging
import os
import socket
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import psutil
import requests
from google.cloud import pubsub_v1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('resource_reporter')


class ResourceReporter:
    def __init__(self,
                 metrics_endpoint_url,  # URL endpoint cho metrics callback
                 events_endpoint_url,  # URL endpoint cho async events
                 interval=30,  # Interval cho metrics callback
                 consumer_id=None,  # ID consumer
                 group_consumer=None,  # Nhóm consumer
                 command_project_id=None,  # Google Cloud Project ID
                 command_subscription=None,  # PubSub subscription cho commands
                 max_workers=5):  # Số lượng worker tối đa

        # Endpoints
        self.metrics_endpoint_url = metrics_endpoint_url
        self.events_endpoint_url = events_endpoint_url

        # Interval và identity
        self.interval = interval
        self.consumer_id = consumer_id or socket.gethostname()
        self.group_consumer = group_consumer or os.environ.get("GROUP_CONSUMER", "default")
        self.ip = self._get_ip()

        # API Key xác thực
        self.api_key = os.environ.get("API_KEY")

        # Threading và state
        self.running = False
        self.background_thread = None
        self.command_thread = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="reporter_worker")
        self.metrics_init_callback = None
        self.metrics_init_done = False

        # Command listening
        self.command_project_id = command_project_id
        self.command_subscription = command_subscription
        self.command_subscriber = None
        self.command_subscription_path = None
        self.on_shutdown_callback = None

        # Định nghĩa collectors
        self.collectors = {
            'cpu': self.collect_cpu_metrics,
            'memory': self.collect_memory_metrics,
            'network': self.collect_network_metrics,
        }

        # Thêm collector GPU nếu có
        try:
            import pynvml
            pynvml.nvmlInit()
            self.collectors['gpu'] = self.collect_gpu_metrics
            pynvml.nvmlShutdown()
        except (ImportError, Exception):
            logger.info("GPU monitoring not available")

        # Job stats
        self.job_stats = {}

    def _get_ip(self):
        """Lấy địa chỉ IP chính của máy"""
        try:
            # Lấy IP không phải loopback
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            # Fallback vào hostname
            return socket.gethostbyname(socket.gethostname())

    def collect_cpu_metrics(self):
        return {
            "percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
            "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else None
        }

    def collect_memory_metrics(self):
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }

    def collect_network_metrics(self):
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }

    def collect_gpu_metrics(self):
        try:
            import pynvml
            pynvml.nvmlInit()

            device_count = pynvml.nvmlDeviceGetCount()
            gpu_info = []

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)

                gpu_info.append({
                    "id": i,
                    "memory_used_percent": round(info.used / info.total * 100, 2),
                    "utilization_percent": util.gpu
                })

            pynvml.nvmlShutdown()
            return gpu_info
        except Exception as e:
            logger.error(f"Error collecting GPU metrics: {e}")
            return []

    def collect_metrics(self):
        """Thu thập tất cả metrics theo định dạng tiêu chuẩn"""
        metrics_data = {}

        # Thu thập từ mỗi collector
        for name, collector in self.collectors.items():
            try:
                metrics_data[name] = collector()
            except Exception as e:
                logger.error(f"Error in {name} collector: {e}")
                metrics_data[name] = {"error": str(e)}

        # Thêm job stats nếu có
        if self.job_stats:
            metrics_data["job_stats"] = self.job_stats

        # Tạo payload chuẩn
        payload = {
            "consumer_id": self.consumer_id,
            "time_callback": datetime.now().isoformat(),
            "ip": self.ip,
            "group_consumer": self.group_consumer,
            "metrics_data": metrics_data
        }

        return payload

    def send_metrics(self, metrics, timeout=5):
        """Gửi metrics đến endpoint metrics"""
        headers = {
            "Content-Type": "application/json"
        }

        # Thêm API key nếu có
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(
                self.metrics_endpoint_url,
                json=metrics,
                headers=headers,
                timeout=timeout
            )

            if response.status_code >= 400:
                logger.warning(f"Failed to report metrics: {response.status_code}, {response.text}")
            return response.status_code
        except Exception as e:
            logger.error(f"Error reporting metrics: {e}")
            return None

    def send_event(self, event_data, timeout=5):
        """Gửi event đến endpoint events"""
        headers = {
            "Content-Type": "application/json"
        }

        # Thêm API key nếu có
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(
                self.events_endpoint_url,
                json=event_data,
                headers=headers,
                timeout=timeout
            )

            if response.status_code >= 400:
                logger.warning(f"Failed to report event: {response.status_code}, {response.text}")
            return response.status_code
        except Exception as e:
            logger.error(f"Error reporting event: {e}")
            return None

    def report_metrics(self):
        """Thu thập và gửi metrics callback"""
        metrics = self.collect_metrics()
        return self.send_metrics(metrics)

    def metrics_reporter_loop(self):
        """Loop chính của metrics reporter thread"""
        logger.info(f"Starting metrics reporter, reporting to {self.metrics_endpoint_url}")

        # Gọi callback khởi tạo nếu được đăng ký
        if self.metrics_init_callback and not self.metrics_init_done:
            try:
                init_metrics = self.collect_metrics()
                self.metrics_init_callback(init_metrics)
                self.metrics_init_done = True
            except Exception as e:
                logger.error(f"Error in metrics init callback: {e}")

        while self.running:
            try:
                self.report_metrics()
            except Exception as e:
                logger.error(f"Unexpected error in metrics reporter loop: {e}")

            # Sleep với kiểm tra cờ running để có thể dừng nhanh hơn
            for _ in range(int(self.interval)):
                if not self.running:
                    break
                time.sleep(1)

    # Đăng ký callback khởi tạo metrics
    def register_metrics_init_callback(self, callback):
        """Đăng ký callback được gọi một lần khi khởi tạo metrics"""
        self.metrics_init_callback = callback
        self.metrics_init_done = False

    def start(self):
        """Bắt đầu metrics reporter thread và command listener nếu được cấu hình"""
        if self.background_thread and self.background_thread.is_alive():
            logger.warning("Reporter already running")
            return False

        self.running = True
        self.background_thread = threading.Thread(target=self.metrics_reporter_loop, daemon=True)
        self.background_thread.start()

        # Bắt đầu command listener nếu được cấu hình
        if all([self.command_project_id, self.command_subscription]):
            self.start_command_listener()

        return True

    def stop(self):
        """Dừng tất cả các hoạt động và dọn dẹp tài nguyên"""
        self.running = False

        if self.background_thread:
            self.background_thread.join(timeout=2)

        if self.command_subscriber:
            try:
                self.command_subscriber.close()
            except:
                pass

        if self.command_thread:
            self.command_thread.join(timeout=2)

        self.executor.shutdown(wait=False)
        logger.info("Resource reporter stopped")

    def update_job_stats(self, stats):
        """Cập nhật số liệu về job processing"""
        self.job_stats = stats

    # Chức năng 2: Async Report Event (không đồng bộ)
    def async_report_event(self, data):
        """
        Gửi báo cáo sự kiện không đồng bộ

        Args:
            data: Dict chứa thông tin sự kiện cần báo cáo theo định dạng:
                {
                    "status": int,         # Mã trạng thái
                    "error_code": int,     # Mã lỗi
                    "error_message": str,  # Thông báo lỗi
                    "result": dict,        # Kết quả xử lý
                    "stats_data": dict,    # Dữ liệu thống kê
                    "task_id": str         # ID của task
                }
        """
        # Xác thực data theo yêu cầu
        required_fields = ["status", "error_code", "error_message", "task_id"]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field in event data: {field}")
                data[field] = None if field != "error_code" else 0

        # Chuẩn bị payload
        event_payload = {
            "consumer_id": self.consumer_id,
            "time_callback": datetime.now().isoformat(),
            "ip": self.ip,
            "group_consumer": self.group_consumer,
            "data": data
        }

        # Gửi async
        self.executor.submit(self.send_event, event_payload)

    # Chức năng 3: Command Listener
    def setup_command_listener(self):
        """Thiết lập listener cho các lệnh từ PubSub với xác thực thích hợp"""
        if not all([self.command_project_id, self.command_subscription]):
            logger.warning("Command listener not started: missing project_id or subscription")
            return False

        try:
            from google.cloud import pubsub_v1

            # Các tùy chọn xác thực - PubSub client sẽ tự động sử dụng một trong những cách sau:
            # 1. Credentials file chỉ định qua biến môi trường GOOGLE_APPLICATION_CREDENTIALS
            # 2. Default credentials từ gcloud CLI nếu đã đăng nhập
            # 3. Metadata server credentials nếu chạy trên Google Cloud (GKE, Compute Engine, Cloud Run, etc.)

            # Tùy chọn xác thực tường minh (nếu cần)
            credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

            if credentials_path and os.path.exists(credentials_path):
                logger.info(f"Using credentials from: {credentials_path}")
                # Không cần làm gì thêm vì PubSub client sẽ tự động đọc từ biến môi trường
            else:
                logger.info("No explicit credentials file provided, using default authentication")
                # Sẽ sử dụng xác thực mặc định (gcloud hoặc metadata server)

            # Tạo subscriber client
            self.command_subscriber = pubsub_v1.SubscriberClient()
            self.command_subscription_path = self.command_subscriber.subscription_path(
                self.command_project_id, self.command_subscription
            )

            logger.info(
                f"Command listener set up successfully for project: {self.command_project_id}, subscription: {self.command_subscription}")
            return True

        except Exception as e:
            logger.error(f"Failed to setup command listener: {e}")
            return False

    def command_listener_loop(self):
        """Thread để lắng nghe các lệnh từ PubSub"""
        if not self.setup_command_listener():
            return

        logger.info(f"Starting command listener for consumer_id: {self.consumer_id}")

        def command_callback(message):
            try:
                # Lấy thông tin từ message
                data = json.loads(message.data.decode('utf-8'))
                attributes = message.attributes if message.attributes else {}

                # Kiểm tra xem message có dành cho consumer này không
                target_consumer = attributes.get('target_consumer')
                if target_consumer and target_consumer != 'all' and target_consumer != self.consumer_id:
                    # Message không dành cho consumer này
                    logger.debug(f"Ignoring command for consumer: {target_consumer}")
                    message.nack()
                    return

                # Lấy command từ data
                command = data.get('command')
                if not command:
                    logger.warning(f"Received message without command: {data}")
                    message.ack()
                    return

                logger.info(f"Processing command: {command} from target: {target_consumer or 'unspecified'}")

                # Xử lý các lệnh
                if command == "shutdown":
                    self._handle_shutdown_command(data)
                elif command == "restart":
                    self._handle_restart_command(data)
                else:
                    logger.warning(f"Unknown command: {command}")

                # Xác nhận đã xử lý
                message.ack()

            except Exception as e:
                logger.error(f"Error processing command: {e}")
                message.ack()  # Vẫn xác nhận để tránh xử lý lặp lại

        # Thiết lập flow control (số lượng message tối đa xử lý đồng thời)
        flow_control = pubsub_v1.types.FlowControl(max_messages=10)

        # Đăng ký callback mà không sử dụng filter
        streaming_pull_future = self.command_subscriber.subscribe(
            self.command_subscription_path,
            callback=command_callback,
            flow_control=flow_control
        )

        logger.info(f"Command listener started for consumer {self.consumer_id}")

        # Chạy cho đến khi bị dừng
        try:
            streaming_pull_future.result()
        except Exception as e:
            logger.error(f"Exception in command listener: {e}")
            if self.running:  # Chỉ thử lại nếu vẫn đang chạy
                logger.info("Restarting command listener in 5 seconds...")
                time.sleep(5)
                self.start_command_listener()

    def _handle_shutdown_command(self, data):
        """Xử lý lệnh shutdown"""
        reason = data.get('reason', 'Received shutdown command')
        logger.info(f"Shutdown command received: {reason}")

        # Báo cáo sự kiện shutdown
        self.async_report_event({
            "status": 200,
            "error_code": 0,
            "error_message": "",
            "result": {"action": "shutdown", "reason": reason},
            "stats_data": {},
            "task_id": str(uuid.uuid4())
        })

        # Gọi callback nếu được đăng ký
        if self.on_shutdown_callback:
            try:
                self.on_shutdown_callback(reason)
            except Exception as e:
                logger.error(f"Error in shutdown callback: {e}")

        # Dọn dẹp và thoát
        self.stop()
        logger.info("Exiting process due to shutdown command")
        # Thoát với mã thoát khác 0 để container/orchestrator biết cần restart
        sys.exit(42)

    def _handle_restart_command(self, data):
        """Xử lý lệnh restart"""
        reason = data.get('reason', 'Received restart command')
        logger.info(f"Restart command received: {reason}")

        # Báo cáo sự kiện restart
        self.async_report_event({
            "status": 200,
            "error_code": 0,
            "error_message": "",
            "result": {"action": "restart", "reason": reason},
            "stats_data": {},
            "task_id": str(uuid.uuid4())
        })

        # Xử lý tương tự shutdown nhưng với mã thoát khác
        if self.on_shutdown_callback:
            try:
                self.on_shutdown_callback(reason)
            except Exception as e:
                logger.error(f"Error in shutdown callback: {e}")

        self.stop()
        logger.info("Exiting process due to restart command")
        sys.exit(43)

    def register_shutdown_callback(self, callback):
        """Đăng ký callback được gọi khi nhận lệnh shutdown"""
        self.on_shutdown_callback = callback

    def start_command_listener(self):
        """Bắt đầu command listener thread"""
        if self.command_thread and self.command_thread.is_alive():
            logger.warning("Command listener already running")
            return False

        if not all([self.command_project_id, self.command_subscription]):
            logger.warning("Command listener not started: missing project_id or subscription")
            return False

        self.command_thread = threading.Thread(target=self.command_listener_loop, daemon=True)
        self.command_thread.start()
        return True
