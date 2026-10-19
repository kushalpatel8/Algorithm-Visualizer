def fibonacci(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    yield dp, [0, 1]
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        yield dp, [i, i-1, i-2]