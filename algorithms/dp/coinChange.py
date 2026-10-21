def coin_change(coins, amount):
    n = len(coins)
    # 2D table: dp[i][w] is min coins using a subset of coins 0..i-1 to make amount w
    # 99 represents infinity for display purposes
    dp = [[0 if w == 0 else 99 for w in range(amount + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        coin = coins[i - 1]
        for w in range(1, amount + 1):
            if coin <= w:
                dp[i][w] = min(dp[i - 1][w], 1 + dp[i][w - coin])
            else:
                dp[i][w] = dp[i - 1][w]
            yield dp, (i, w)
