"""Alert management."""

from typing import List, Callable
from datetime import datetime

class AlertManager:
    """Manage system alerts and notifications."""
    
    def __init__(self):
        self.handlers = []
        self.alert_history = []
    
    def add_handler(self, handler: Callable[[str], None]):
        """Add an alert handler."""
        self.handlers.append(handler)
    
    def send_alert(self, message: str, severity: str = 'warning'):
        """Send an alert through all handlers."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity
        }
        self.alert_history.append(alert)
        
        for handler in self.handlers:
            try:
                handler(message)
            except:
                pass
