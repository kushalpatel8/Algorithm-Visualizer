def merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        yield from merge_sort(arr, l, m)
        yield from merge_sort(arr, m + 1, r)
        
        # Merge logic
        n1 = m - l + 1
        n2 = r - m
        L = arr[l : m + 1]
        R = arr[m + 1 : r + 1]
        
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr, [k, l, r]
            
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr, [k, l, r]
            
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr, [k, l, r]