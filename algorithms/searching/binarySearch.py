def binary_search(arr, target):
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        yield mid, False, lo, hi
        if arr[mid] == target:
            yield mid, True, lo, hi
            return
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    yield -1, False, lo, hi