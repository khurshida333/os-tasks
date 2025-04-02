import random
import math
from typing import List, Tuple
from process import Process
from scheduler import FCFSScheduler, SJFScheduler, RoundRobinScheduler

class Simulation:
    def __init__(
        self,
        num_sequences: int = 20,
        processes_per_sequence: int = 10,
        max_burst_time: int = 20,
        arrival_rate: float = 2.0
    ):
        self.num_sequences = num_sequences
        self.processes_per_sequence = processes_per_sequence
        self.max_burst_time = max_burst_time
        self.arrival_rate = arrival_rate
        
    def generate_burst_time(self) -> int:

        u = random.random()
        return max(1, int(-self.max_burst_time / 3 * math.log(u)))
        
    def generate_arrival_times(self, num_processes: int) -> List[int]:

        times = []
        current_time = 0
        for _ in range(num_processes):

            u = random.random()
            interval = int(-1/self.arrival_rate * math.log(u))
            current_time += interval
            times.append(current_time)
        return times
        
    def generate_sequence(self, sequence_id: int) -> List[Process]:
        arrival_times = self.generate_arrival_times(self.processes_per_sequence)
        
        return [
            Process(
                id=sequence_id * 1000 + i,
                burst_time=self.generate_burst_time(),
                arrival_time=arrival_times[i],
                remaining_time=0
            )
            for i in range(self.processes_per_sequence)
        ]
        
    def run(self) -> dict:

        schedulers = {
            "FCFS": FCFSScheduler(),
            "SJF": SJFScheduler(),
            "RR-2": RoundRobinScheduler(time_quantum=2),
            "RR-4": RoundRobinScheduler(time_quantum=4)
        }
        
        results = {name: [] for name in schedulers.keys()}
        
        for i in range(self.num_sequences):
            sequence = self.generate_sequence(i)
            
            for name, scheduler in schedulers.items():

                sequence_copy = [
                    Process(
                        id=p.id,
                        burst_time=p.burst_time,
                        arrival_time=p.arrival_time,
                        remaining_time=p.burst_time
                    )
                    for p in sequence
                ]
                
                scheduler.schedule(sequence_copy)
                stats = scheduler.get_statistics()
                results[name].append(stats)
                

        final_results = {}
        for name, stats_list in results.items():
            avg_stats = {
                key: sum(stat[key] for stat in stats_list) / len(stats_list)
                for key in stats_list[0].keys()
            }
            final_results[name] = avg_stats
            
        return final_results
if __name__ == "__main__":
    sim = Simulation(
        num_sequences=100,
        processes_per_sequence=20,
        max_burst_time=30,
        arrival_rate=3.0
    )

    results = sim.run()
    print(results)
