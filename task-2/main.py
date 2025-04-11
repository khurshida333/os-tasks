import matplotlib.pyplot as plt
from disk_scheduling import fcfs, sstf, scan, cscan, edf, fd_scan


def visualize(results):
    plt.figure(figsize=(10, 6))

    for algorithm, (total_movement, seek_sequence) in results.items():
        plt.plot(seek_sequence, range(len(seek_sequence)), marker='o', linestyle='-', label=f"{algorithm} ({total_movement} moves)")

    plt.xlabel("Cylinder Number")
    plt.ylabel("Order of Execution")
    plt.title("Disk Scheduling Algorithms Visualization")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    print("Disk Scheduling Simulation")

    disk_size = 200
    start = 53
    requests = [
        {'sector': 98, 'deadline': 10},
        {'sector': 183, 'deadline': 20},
        {'sector': 37, 'deadline': 5},
        {'sector': 122, 'deadline': 15},
        {'sector': 14, 'deadline': -1},  
        {'sector': 124, 'deadline': -1},
        {'sector': 65, 'deadline': -1},
        {'sector': 67, 'deadline': -1}
    ]

   
    results = {}

    
    results["FCFS"] = fcfs([r['sector'] for r in requests], start)
    results["SSTF"] = sstf([r['sector'] for r in requests], start)
    results["SCAN"] = scan([r['sector'] for r in requests], start, disk_size)
    results["C-SCAN"] = cscan([r['sector'] for r in requests], start, disk_size)
    results["EDF"] = edf(requests, start)
    results["FD-SCAN"] = fd_scan(requests, start, disk_size)

    
    for algorithm, (total_movement, seek_sequence) in results.items():
        print(f"\n{algorithm}:")
        print(f"Seek Sequence: {seek_sequence}")
        print(f"Total Head Movements: {total_movement}")

    
    visualize(results)

if __name__ == "__main__":
    main()

# 98,183,37,122,14,124,65,67

# 0,14,37
# 53->37->14->0->65->67->98->122->124->183

# 53