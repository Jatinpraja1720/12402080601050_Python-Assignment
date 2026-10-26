
import re
from collections import defaultdict, deque

X, T = map(int, input().split())
n = int(input())

pattern = r"(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)"

logs = []

for _ in range(n):
    line = input().strip()
    match = re.match(pattern, line)

    if match:
        time, user, ip, status = match.groups()
        h, m = map(int, time.split(":"))
        minutes = h * 60 + m
        logs.append((minutes, time, user, ip, status))

failures = defaultdict(deque)
suspicious = {}

for minutes, time, user, ip, status in logs:

    if status == "FAIL":
        failures[user].append((minutes, ip))

        while failures[user] and minutes - failures[user][0][0] > T:
            failures[user].popleft()

    elif status == "SUCCESS":
        q = failures[user]

        while q and minutes - q[0][0] > T:
            q.popleft()

        count = sum(1 for _, fail_ip in q if fail_ip != ip)

        if count >= X and user not in suspicious:
            suspicious[user] = time

for user in sorted(suspicious):
    print(user, suspicious[user])
