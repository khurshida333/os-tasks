def second_chance_page_replacement(pages, frame_size):
    from collections import deque

    queue = deque()
    reference_bits = {}
    in_memory = set()
    page_faults = 0

    for page in pages:
        if page in in_memory:
            # Page hit - set reference bit to 1 (but don't modify queue)
            reference_bits[page] = 1
            print(f"Page {page}: Hit   | Memory: {list(queue)}, Ref bits: {reference_bits}")
        else:
            page_faults += 1
            if len(queue) >= frame_size:
                # Find the first page with ref_bit=0
                replaced = False
                while not replaced:
                    candidate = queue[0]
                    if reference_bits[candidate] == 0:
                        # Remove the candidate
                        queue.popleft()
                        in_memory.remove(candidate)
                        del reference_bits[candidate]
                        replaced = True
                    else:
                        # Give a second chance (set ref_bit=0 and move to end)
                        reference_bits[candidate] = 0
                        queue.popleft()
                        queue.append(candidate)

            # Add the new page
            queue.append(page)
            in_memory.add(page)
            reference_bits[page] = 1
            print(f"Page {page}: Fault | Memory: {list(queue)}, Ref bits: {reference_bits}")

    print(f"\nTotal Page Faults: {page_faults}")
    return page_faults


# Test run
pages = [1, 2, 3, 4, 1, 2, 5, 3, 2, 1, 4, 5]
frame_size = 4
second_chance_page_replacement(pages, frame_size)