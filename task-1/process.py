from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:

    id: int
    burst_time: int  #
    arrival_time: int
    remaining_time: int  # For SRTF
    waiting_time: int = 0
    turnaround_time: int = 0
    completion_time: Optional[int] = None
    
    def __str__(self) -> str:
        return f"Process {self.id} (burst={self.burst_time}, arrival={self.arrival_time})"