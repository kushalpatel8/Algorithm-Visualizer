def tim_sort(arr):
    n = len(arr)
    min_run = 16
    
    # Sort individual subarrays of size min_run using insertion sort
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                yield arr, [j + 1, i]
            arr[j + 1] = key
            yield arr, [j + 1, i]
            
    # Merge sorted runs
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(left + 2 * size - 1, n - 1)
            
            if mid < right:
                len1 = mid - left + 1
                len2 = right - mid
                left_arr = arr[left:mid + 1]
                right_arr = arr[mid + 1:right + 1]
                
                i = 0
                j = 0
                k = left
                while i < len1 and j < len2:
                    if left_arr[i] <= right_arr[j]:
                        arr[k] = left_arr[i]
                        i += 1
                    else:
                        arr[k] = right_arr[j]
                        j += 1
                    k += 1
                    yield arr, [k, left, right]
                    
                while i < len1:
                    arr[k] = left_arr[i]
                    i += 1
                    k += 1
                    yield arr, [k, left, right]
                    
                while j < len2:
                    arr[k] = right_arr[j]
                    j += 1
                    k += 1
                    yield arr, [k, left, right]
                    
        size = 2 * size