from abc import ABC, abstractmethod
from typing import List, Optional
from process import Process
from collections import deque

class Scheduler(ABC):

    
    def __init__(self):
        self.current_time = 0
        self.ready_queue: List[Process] = []
        self.completed_processes: List[Process] = []
        
    @abstractmethod
    def schedule(self, processes: List[Process]) -> None:

        pass
    
    def get_statistics(self) -> dict:

        if not self.completed_processes:
            return {
                "avg_waiting_time": 0,
                "avg_turnaround_time": 0,
                "max_waiting_time": 0
            }
            
        avg_waiting = sum(p.waiting_time for p in self.completed_processes) / len(self.completed_processes)
        avg_turnaround = sum(p.turnaround_time for p in self.completed_processes) / len(self.completed_processes)
        max_waiting = max(p.waiting_time for p in self.completed_processes)
        
        return {
            "avg_waiting_time": avg_waiting,
            "avg_turnaround_time": avg_turnaround,
            "max_waiting_time": max_waiting
        }

class FCFSScheduler(Scheduler):

    
    def schedule(self, processes: List[Process]) -> None:
        processes = sorted(processes, key=lambda x: x.arrival_time)
        self.current_time = 0
        
        for process in processes:

            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
                
            process.waiting_time = self.current_time - process.arrival_time
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            self.completed_processes.append(process)

class SJFScheduler(Scheduler):

    def schedule(self, processes: List[Process]) -> None:
        remaining_processes = sorted(processes, key=lambda x: x.arrival_time)
        self.current_time = 0
        
        while remaining_processes or self.ready_queue:
            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                self.ready_queue.append(remaining_processes.pop(0))
            
            if not self.ready_queue:
                self.current_time = remaining_processes[0].arrival_time
                continue
                

            self.ready_queue.sort(key=lambda x: x.burst_time)
            current_process = self.ready_queue.pop(0)
            
            current_process.waiting_time = self.current_time - current_process.arrival_time
            self.current_time += current_process.burst_time
            current_process.completion_time = self.current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            self.completed_processes.append(current_process)

class RoundRobinScheduler(Scheduler):

    
    def __init__(self, time_quantum: int):
        super().__init__()
        self.time_quantum = time_quantum
        self.context_switch_penalty = 1
        
    def schedule(self, processes: List[Process]) -> None:
        remaining_processes = sorted(processes, key=lambda x: x.arrival_time)
        ready_queue = deque()
        self.current_time = 0
        

        process_map = {
            p.id: Process(
                p.id, p.burst_time, p.arrival_time,
                remaining_time=p.burst_time
            ) for p in processes
        }
        
        while remaining_processes or ready_queue:

            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                ready_queue.append(process_map[remaining_processes.pop(0).id])
                
            if not ready_queue:
                self.current_time = remaining_processes[0].arrival_time
                continue
                
            current_process = ready_queue.popleft()
            time_slice = min(self.time_quantum, current_process.remaining_time)
            

            self.current_time += time_slice
            current_process.remaining_time -= time_slice
            

            if ready_queue or remaining_processes:
                self.current_time += self.context_switch_penalty
            

            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            else:
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                self.completed_processes.append(current_process)