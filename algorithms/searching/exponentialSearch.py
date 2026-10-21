def exponential_search(arr, target):
    n = len(arr)
    if n == 0:
        yield -1, False, 0, 0
        return
        
    yield 0, False, 0, 0
    if arr[0] == target:
        yield 0, True, 0, 0
        return
        
    bound = 1
    while bound < n and arr[bound] < target:
        yield bound, False, bound // 2, min(bound, n - 1)
        bound *= 2
        
    low = bound // 2
    high = min(bound, n - 1)
    
    while low <= high:
        mid = (low + high) // 2
        yield mid, False, low, high
        if arr[mid] == target:
            yield mid, True, low, high
            return
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    yield -1, False, low, high