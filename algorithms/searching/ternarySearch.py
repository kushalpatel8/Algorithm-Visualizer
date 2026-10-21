def ternary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3
        
        yield mid1, False, low, high
        if arr[mid1] == target:
            yield mid1, True, low, high
            return
            
        yield mid2, False, low, high
        if arr[mid2] == target:
            yield mid2, True, low, high
            return
            
        if target < arr[mid1]:
            high = mid1 - 1
        elif target > arr[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1
            
    yield -1, False, low, high