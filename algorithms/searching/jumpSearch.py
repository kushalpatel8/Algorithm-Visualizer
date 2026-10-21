import math

def jump_search(arr, target):
    n = len(arr)
    step = max(1, int(math.sqrt(n)))
    prev = 0
    
    while prev < n and arr[min(step, n) - 1] < target:
        yield min(step, n) - 1, False, prev, min(step, n) - 1
        prev = step
        step += max(1, int(math.sqrt(n)))
        if prev >= n:
            yield -1, False, 0, n - 1
            return
            
    for i in range(prev, min(step, n)):
        yield i, False, prev, min(step, n) - 1
        if arr[i] == target:
            yield i, True, prev, min(step, n) - 1
            return
            
    yield -1, False, prev, min(step, n) - 1