def linear_search(arr, target):
    for i in range(len(arr)):
        yield i, False
        if arr[i] == target:
            yield i, True
    yield -1, False