def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k: return
    currSum = sum(arr[:k])
    maxSum = currSum
    yield 0, k - 1, currSum, maxSum
    
    for i in range(1, n - k + 1):
        currSum = currSum - arr[i - 1] + arr[i + k + 1]
        maxSum = max(currSum, maxSum)
        yield i, i + k - 1, currSum, maxSum
    