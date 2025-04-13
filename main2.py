import matplotlib.pyplot as plt
from typing import List, Tuple


class DiskRequest:
    def __init__(self, track, arrival_time=0, deadline=float('inf')):
        self.track = track
        self.arrival_time = arrival_time
        self.deadline = deadline


class DiskScheduler:
    def __init__(self, total_tracks: int = 200):
        self.total_tracks = total_tracks
        self.current_position = 53  # Set the initial head position at 53
        self.requests = []

    def calculate_seek_time(self, from_track, to_track):
        """Calculate the seek time (absolute distance) between two tracks"""
        return abs(to_track - from_track)

    def plot_movements(self, algorithm_name: str, movements: List[int], total_movement: int):
        """Plot the head movements for visualization, showing arrows for movement"""
        plt.figure(figsize=(10, 6))

        # Plot head movement as blue circles and connecting lines
        plt.plot(range(len(movements)), movements, 'b-o', label="Track Visited")

        # Add arrows to indicate head movement direction
        for i in range(1, len(movements)):
            plt.arrow(i - 1, movements[i - 1], i, movements[i] - movements[i - 1],
                      head_width=0.1, head_length=3, fc='red', ec='red', length_includes_head=True)

        plt.title(f'{algorithm_name} Disk Scheduling\nTotal head movement: {total_movement} tracks')
        plt.xlabel('Request Sequence')
        plt.ylabel('Track Number')
        plt.grid(True)
        plt.legend()
        plt.show()

    def fcfs(self) -> Tuple[List[int], int]:
        """First Come First Serve scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position

        for request in self.requests:
            pos = request.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos

        self.plot_movements("FCFS", movements, total_movement)
        return movements, total_movement

    def sstf(self) -> Tuple[List[int], int]:
        """Shortest Seek Time First scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position
        remaining_requests = self.requests.copy()

        while remaining_requests:
            closest = min(remaining_requests, key=lambda x: self.calculate_seek_time(current_pos, x.track))
            pos = closest.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos
            remaining_requests.remove(closest)

        self.plot_movements("SSTF", movements, total_movement)
        return movements, total_movement

    # def scan(self) -> Tuple[List[int], int]:
    #     """SCAN (Elevator) scheduling"""
    #     movements = [self.current_position]
    #     total_movement = 0
    #     current_pos = self.current_position
    #     remaining_requests = sorted(self.requests, key=lambda x: x.track)

    #     greater = [r for r in remaining_requests if r.track >= current_pos]
    #     lesser = [r for r in remaining_requests if r.track < current_pos]

    #     for request in greater:
    #         pos = request.track
    #         movements.append(pos)
    #         total_movement += self.calculate_seek_time(current_pos, pos)
    #         current_pos = pos

    #     for request in reversed(lesser):
    #         pos = request.track
    #         movements.append(pos)
    #         total_movement += self.calculate_seek_time(current_pos, pos)
    #         current_pos = pos

    #     self.plot_movements("SCAN", movements, total_movement)
    #     return movements, total_movement
    def scan(self) -> Tuple[List[int], int]:
        """Left-first SCAN (Elevator) scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position
        remaining_requests = sorted(self.requests, key=lambda x: x.track)

        greater = [r for r in remaining_requests if r.track >= current_pos]
        lesser = [r for r in remaining_requests if r.track < current_pos]

        # Move left first (toward 0)
        for request in reversed(lesser):  # highest to lowest
            pos = request.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos

        # If head is not already at track 0, go to 0 (end of disk in left direction)
        if current_pos != 0:
            movements.append(0)
            total_movement += self.calculate_seek_time(current_pos, 0)
            current_pos = 0

        # Then move right (start of greater list)
        for request in greater:
            pos = request.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos

        self.plot_movements("SCAN (Left-first)", movements, total_movement)
        return movements, total_movement

    def c_scan(self) -> Tuple[List[int], int]:
        """C-SCAN scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position
        remaining_requests = sorted(self.requests, key=lambda x: x.track)

        greater = [r for r in remaining_requests if r.track >= current_pos]
        lesser = [r for r in remaining_requests if r.track < current_pos]

        for request in greater:
            pos = request.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos

        if lesser:
            movements.append(0)
            total_movement += self.calculate_seek_time(current_pos, 0)
            current_pos = 0

        for request in lesser:
            pos = request.track
            movements.append(pos)
            total_movement += self.calculate_seek_time(current_pos, pos)
            current_pos = pos

        self.plot_movements("C-SCAN", movements, total_movement)
        return movements, total_movement

    def edf(self) -> Tuple[List[int], int]:
        """Earliest Deadline First scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position

        # Sort requests by deadline (earliest first)
        sorted_requests = sorted(self.requests, key=lambda x: x.deadline)

        for request in sorted_requests:
            movements.append(request.track)
            total_movement += self.calculate_seek_time(current_pos, request.track)
            current_pos = request.track

        self.plot_movements("EDF", movements, total_movement)
        return movements, total_movement

    def fd_scan(self) -> Tuple[List[int], int]:
        """Feasible Deadline SCAN scheduling"""
        movements = [self.current_position]
        total_movement = 0
        current_pos = self.current_position

        remaining_requests = sorted(self.requests, key=lambda x: x.track)

        feasible_requests = [r for r in remaining_requests if
                             self.calculate_seek_time(current_pos, r.track) <= r.deadline]

        greater = [r for r in feasible_requests if r.track >= current_pos]
        lesser = [r for r in feasible_requests if r.track < current_pos]

        for request in greater:
            movements.append(request.track)
            total_movement += self.calculate_seek_time(current_pos, request.track)
            current_pos = request.track

        for request in reversed(lesser):
            movements.append(request.track)
            total_movement += self.calculate_seek_time(current_pos, request.track)
            current_pos = request.track

        self.plot_movements("FD-SCAN", movements, total_movement)
        return movements, total_movement


# Example usage
def main():
    # Create a disk scheduler with a specific initial head position at 53
    scheduler = DiskScheduler(200)

    # Define the request queue with deadlines
    scheduler.requests = [
        DiskRequest(98, deadline=25),
        DiskRequest(183, deadline=30),
        DiskRequest(37, deadline=35),
        DiskRequest(122, deadline=40),
        DiskRequest(14, deadline=45),
        DiskRequest(124, deadline=50),
        DiskRequest(65, deadline=55),
        DiskRequest(67, deadline=60)
    ]

    # Test each algorithm with visualization
    print("FCFS:")
    movement, sequence = scheduler.fcfs()
    print(f"Total head movement: {sequence} tracks\n")

    print("SSTF:")
    movement, sequence = scheduler.sstf()
    print(f"Total head movement: {sequence} tracks\n")

    print("SCAN:")
    movement, sequence = scheduler.scan()
    print(f"Total head movement: {sequence} tracks\n")

    print("C-SCAN:")
    movement, sequence = scheduler.c_scan()
    print(f"Total head movement: {sequence} tracks\n")

    print("EDF:")
    movement, sequence = scheduler.edf()
    print(f"Total head movement: {sequence} tracks\n")

    print("FD-SCAN:")
    movement, sequence = scheduler.fd_scan()
    print(f"Total head movement: {sequence} tracks\n")


if __name__ == "__main__":
    main()