def quick_sort(arr, lo, hi):
    if lo < hi:
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr, [i, j, hi]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        yield arr, [i + 1, hi]
        
        pi = i + 1
        yield from quick_sort(arr, lo, pi - 1)
        yield from quick_sort(arr, pi + 1, hi)