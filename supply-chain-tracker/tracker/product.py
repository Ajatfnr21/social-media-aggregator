"""Product and shipment tracking."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class Shipment:
    shipment_id: str
    origin: str
    destination: str
    carrier: str
    status: str
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    events: List[Dict] = None

@dataclass  
class Product:
    product_id: str
    name: str
    manufacturer: str
    current_location: str
    status: str
    certifications: List[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'current_location': self.current_location,
            'status': self.status,
            'certifications': self.certifications or []
        }
