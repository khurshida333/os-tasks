import random

def random_page_replacement(pages, frame_size):
    from collections import deque

    memory = deque()
    in_memory = set()
    page_faults = 0

    for page in pages:
        if page in in_memory:
            print(f"Page {page}: Hit   | Memory: {list(memory)}")
        else:
            page_faults += 1
            if len(memory) >= frame_size:
                # Remove a random page
                victim = random.choice(list(memory))
                memory.remove(victim)
                in_memory.remove(victim)
                print(f"Removed page {victim} to insert page {page}")
            memory.append(page)
            in_memory.add(page)
            print(f"Page {page}: Fault | Memory: {list(memory)}")

    print(f"\nTotal Page Faults: {page_faults}")
    return page_faults

# Example test
pages = [1, 2, 3, 4, 1, 2, 5, 3, 2, 1, 4, 5]
frame_size = 4
random_page_replacement(pages, frame_size)
