"""Supply chain on blockchain."""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Block:
    index: int
    timestamp: str
    data: Dict
    previous_hash: str
    hash: str = ""

class SupplyChain:
    """Blockchain-based supply chain tracker."""
    
    def __init__(self):
        self.chain = [self._create_genesis_block()]
        self.pending_data = []
    
    def _create_genesis_block(self) -> Block:
        """Create the first block."""
        return Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={"message": "Genesis Block"},
            previous_hash="0",
            hash=self._hash_block(0, "0", {})
        )
    
    def _hash_block(self, index: int, prev_hash: str, data: Dict) -> str:
        """Calculate block hash."""
        block_string = json.dumps({
            'index': index,
            'previous_hash': prev_hash,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_event(self, product_id: str, event_type: str, location: str, 
                  metadata: Dict = None) -> Block:
        """Add a supply chain event."""
        data = {
            'product_id': product_id,
            'event_type': event_type,
            'location': location,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=data,
            previous_hash=self.chain[-1].hash,
            hash=""
        )
        new_block.hash = self._hash_block(new_block.index, new_block.previous_hash, data)
        
        self.chain.append(new_block)
        return new_block
    
    def get_product_history(self, product_id: str) -> List[Dict]:
        """Get full history for a product."""
        return [
            block.data for block in self.chain 
            if block.data.get('product_id') == product_id
        ]
    
    def verify_chain(self) -> bool:
        """Verify blockchain integrity."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != self._hash_block(current.index, current.previous_hash, current.data):
                return False
            if current.previous_hash != previous.hash:
                return False
        
        return True
