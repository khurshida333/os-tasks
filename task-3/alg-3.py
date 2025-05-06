def lru_page_replacement(pages, frame_size):
    memory = []
    page_faults = 0

    for page in pages:
        if page in memory:
            # Page hit: move the page to the end (most recently used)
            memory.remove(page)
            memory.append(page)
            print(f"Page {page}: Hit,   Memory: {memory}")
        else:
            # Page fault
            if len(memory) < frame_size:
                memory.append(page)
            else:
                # Remove the least recently used page (front of the list)
                memory.pop(0)
                memory.append(page)
            page_faults += 1
            print(f"Page {page}: Fault, Memory: {memory}")

    print(f"\nTotal Page Faults: {page_faults}")

# Test it
pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
frame = 4
lru_page_replacement(pages, frame)
