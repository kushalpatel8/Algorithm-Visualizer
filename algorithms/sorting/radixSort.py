def radix_sort(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            idx = (arr[i] // exp) % 10
            count[idx] += 1
            yield arr, [i]
        
        for i in range(1, 10):
            count[i] += count[i - 1]
            
        i = n - 1
        while i >= 0:
            idx = (arr[i] // exp) % 10
            output[count[idx] - 1] = arr[i]
            count[idx] -= 1
            i -= 1
            
        for i in range(n):
            arr[i] = output[i]
            yield arr, [i]
            
        exp *= 10
            