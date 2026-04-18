"""System resource monitoring."""

import psutil
import time
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SystemMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict
    load_average: List[float]
    processes: int

class SystemMonitor:
    """Monitor system health and resources."""
    
    def __init__(self, interval: int = 60):
        self.interval = interval
        self.history = []
        self.running = False
    
    def get_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage('/').percent,
            network_io={
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            },
            load_average=list(psutil.getloadavg()),
            processes=len(psutil.pids())
        )
    
    def check_thresholds(self, metrics: SystemMetrics, thresholds: Dict) -> List[str]:
        """Check metrics against thresholds."""
        alerts = []
        
        if metrics.cpu_percent > thresholds.get('cpu', 80):
            alerts.append(f"CPU usage high: {metrics.cpu_percent}%")
        
        if metrics.memory_percent > thresholds.get('memory', 85):
            alerts.append(f"Memory usage high: {metrics.memory_percent}%")
        
        if metrics.disk_percent > thresholds.get('disk', 90):
            alerts.append(f"Disk usage high: {metrics.disk_percent}%")
        
        return alerts
    
    def start_monitoring(self, callback=None):
        """Start continuous monitoring."""
        self.running = True
        
        while self.running:
            metrics = self.get_metrics()
            self.history.append(metrics)
            
            if callback:
                callback(metrics)
            
            time.sleep(self.interval)
