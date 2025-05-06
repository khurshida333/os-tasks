def fifo_page_replacement(pages, frame_size):
    memory = []
    page_faults = 0
    old_index = 0  # Keeps track of which frame to replace

    for index, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frame_size:
                memory.append(page)
            else:
                memory[old_index] = page #Replace the oldest page 
                old_index = (old_index + 1) % frame_size #(0 + 1) % 4 = 1, (1 + 1) % 4 = 2, (2 + 1) % 4 = 3, (3 + 1) % 4 = 0 (wraps around)
            page_faults += 1
            print(f"Page {page}: Fault, Memory: {memory}")
        else:
            print(f"Page {page}: Hit,   Memory: {memory}")

    print(f"\nTotal Page Faults: {page_faults}")

pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] 
frame = 4
fifo_page_replacement(pages, frame)
