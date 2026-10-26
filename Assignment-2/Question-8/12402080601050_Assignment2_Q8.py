
MOD = 1000000007

n, m = map(int, input().split())
grid = [input().split() for _ in range(n)]

dp = [[None] * m for _ in range(n)]
ways = [[0] * m for _ in range(n)]

if grid[0][0] != "X":
    dp[0][0] = int(grid[0][0])
    ways[0][0] = 1

for i in range(n):
    for j in range(m):
        if grid[i][j] == "X" or (i == 0 and j == 0):
            continue

        score = int(grid[i][j])
        candidates = []

        if i > 0 and dp[i-1][j] is not None:
            candidates.append((dp[i-1][j], ways[i-1][j]))

        if j > 0 and dp[i][j-1] is not None:
            candidates.append((dp[i][j-1], ways[i][j-1]))

        if i > 0 and j > 0 and dp[i-1][j-1] is not None:
            candidates.append((dp[i-1][j-1], ways[i-1][j-1]))

        if candidates:
            best = max(x[0] for x in candidates)
            dp[i][j] = best + score
            ways[i][j] = sum(
                count for value, count in candidates if value == best
            ) % MOD

if dp[n-1][m-1] is None:
    print("IMPOSSIBLE")
else:
    print(dp[n-1][m-1], ways[n-1][m-1])
