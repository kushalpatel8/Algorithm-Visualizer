def gnome_sort(arr):
    n = len(arr)
    idx = 0
    while idx < n:
        if idx == 0:
            idx += 1
        yield arr, [idx - 1, idx]
        if arr[idx] >= arr[idx - 1]:
            idx += 1
        else:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
            yield arr, [idx - 1, idx]
            idx -= 1