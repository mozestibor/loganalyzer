from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    hostname: str
    service_name: str  # A te regexedben ez a 'process'
    message: str
    raw_line: str
    pid: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        # Szép kiíratás stringként
        return f"[{self.timestamp}] {self.service_name}: {self.message}"