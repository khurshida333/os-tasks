import matplotlib.pyplot as plt
from simulation import Simulation


def main():

    sim = Simulation(
        num_sequences=100,
        processes_per_sequence=20,
        max_burst_time=30,
        arrival_rate=3.0
    )


    results = sim.run()

    schedulers = []
    avg_waiting_times = []
    avg_turnaround_times = []

    for scheduler_name, stats in results.items():
        schedulers.append(scheduler_name)
        avg_waiting_times.append(stats["avg_waiting_time"])
        avg_turnaround_times.append(stats["avg_turnaround_time"])

    print("\nCPU Scheduling Algorithms Simulation Results")
    print("=" * 50)
    for i in range(len(schedulers)):
        print(f"\n{schedulers[i]} Scheduler:")
        print(f"  Average Waiting Time: {avg_waiting_times[i]:.2f}")
        print(f"  Average Turnaround Time: {avg_turnaround_times[i]:.2f}")

    fig, ax = plt.subplots(figsize=(8, 5))

    bar_width = 0.3
    index = range(len(schedulers))

    plt.bar(index, avg_waiting_times, bar_width, label='Avg Waiting Time', color='blue')
    plt.bar([i + bar_width for i in index], avg_turnaround_times, bar_width, label='Avg Turnaround Time',
            color='orange')

    plt.xlabel("Scheduling Algorithm")
    plt.ylabel("Time (ms)")
    plt.title("CPU Scheduling Performance Comparison")
    plt.xticks([i + bar_width / 2 for i in index], schedulers)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()
