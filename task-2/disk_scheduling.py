def fcfs(requests, start=53):
    seek_sequence = []
    total_movement = 0
    current = start

    for request in requests:
        movement = abs(request - current)
        total_movement += movement
        seek_sequence.append(request)
        current = request

    return total_movement, seek_sequence


def sstf(requests, start=53):
    requests = requests[:]  # Copy list 
    seek_sequence = []
    total_movement = 0
    current = start

    while requests:
        nearest_index = min(range(len(requests)), key=lambda i: abs(requests[i] - current))  
        nearest_request = requests.pop(nearest_index)

        movement = abs(nearest_request - current)
        total_movement += movement
        seek_sequence.append(nearest_request)
        current = nearest_request 

    return total_movement, seek_sequence


def scan(requests, start=53, disk_size=200, direction="left"):
    requests.sort()
    left = sorted([r for r in requests if r < start], reverse=True)
    right = [r for r in requests if r >= start]

    seek_sequence = []
    total_movement = 0
    current = start

    if direction == "left":
        left.append(0)
        scan_order = left + right
    else:
        right.append(disk_size - 1)
        scan_order = right + left

    for request in scan_order:
        movement = abs(request - current)
        total_movement += movement
        seek_sequence.append(request)
        current = request  

    return total_movement, seek_sequence


def cscan(requests, start=53, disk_size=200):
    requests.sort()
    left = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]

    seek_sequence = []
    total_movement = 0
    current = start

    right.append(disk_size - 1)
    scan_order = right + [0] + left 

    for request in scan_order:
        if current == disk_size - 1 and request == 0:
            seek_sequence.append(request)
            current = request 
            continue  

        movement = abs(request - current)
        total_movement += movement
        seek_sequence.append(request)
        current = request  

    return total_movement, seek_sequence

def edf(requests, start=53):
    # Sort by deadline current head position
    requests.sort(key=lambda x: (x['deadline'], abs(x['sector'] - start))) 
    #sort by deadline
    #if same deadline-->sort by (start - sector) ........ requires the least movement

    seek_sequence = []
    total_movement = 0
    head = start

    for request in requests:
        movement = abs(request['sector'] - head)
        total_movement += movement
        seek_sequence.append(request['sector'])
        head = request['sector']

    return total_movement, seek_sequence

def fd_scan(requests, start=53, disk_size=200):

    # Sort by deadline first, then by distance from head
    requests = sorted(requests,key=lambda x: (x['deadline'], abs(x['sector'] - current))) 

    seek_sequence = []
    total_movement = 0
    current = start 

    real_time_requests = [r for r in requests if r['deadline'] > 0] 
    normal_requests = [r for r in requests if r['deadline'] <= 0] 

    all_requests = real_time_requests + normal_requests

    for request in all_requests:
        movement = abs(request['sector'] - current)
        if movement <= request['deadline']:  
            total_movement += movement
            seek_sequence.append(request['sector'])
            current = request['sector']
        else:
            print(f"Request {request['sector']} with deadline {request['deadline']} rejected")

    return total_movement, seek_sequence
