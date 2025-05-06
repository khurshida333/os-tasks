def opt(pages, frame_size):
    memory = []
    page_faults = 0

    for index, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frame_size:
                memory.append(page)  # Simply add if space is available
            else:
                # Check which page in memory is either:
                # 1. Not used again in the future (replace it)
                # 2. Used farthest in the future (replace the farthest one)
                # 3. If multiple not used, replace the oldest (FIFO)
                
                replace_index = 0
                farthest_next_use = -1
                no_future_use_found = False

                for i, mem_page in enumerate(memory):
                    # Check if this page appears again in the future
                    if mem_page not in pages[index+1:]:
                        replace_index = i
                        no_future_use_found = True
                        break
                    else:
                        # Find when it will be used next
                        next_use = pages[index+1:].index(mem_page)
                        if next_use > farthest_next_use:
                            farthest_next_use = next_use
                            replace_index = i

                # Replace the selected page
                memory[replace_index] = page

            page_faults += 1
            print(f"Page {page}: Fault, Memory: {memory}")
        else:
            print(f"Page {page}: Hit,   Memory: {memory}")

    print(f"\nTotal Page Faults: {page_faults}")

pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] 
frame = 4
opt(pages, frame)