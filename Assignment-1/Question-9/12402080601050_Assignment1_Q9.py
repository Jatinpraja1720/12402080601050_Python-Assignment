import heapq

w, n = map(int, input().split())

jobs = []

for i in range(n):
    arrival, job_id, priority, duration, resources = input().split()

    jobs.append((
        int(arrival),
        i,
        job_id,
        int(priority),
        int(duration),
        int(resources)
    ))

jobs.sort()

workers = [(0, i + 1) for i in range(w)]
heapq.heapify(workers)

waiting_time = 0
result = []
ready = []

i = 0
current_time = 0

while i < n or ready:

    while i < n and jobs[i][0] <= current_time:
        arrival, order, job_id, priority, duration, resources = jobs[i]

        heapq.heappush(
            ready,
            (-priority, arrival, order, job_id, duration, resources)
        )
        i += 1

    if not ready:
        current_time = jobs[i][0]
        continue

    free_time, worker_id = heapq.heappop(workers)

    if free_time > current_time:
        current_time = free_time

        while i < n and jobs[i][0] <= current_time:
            arrival, order, job_id, priority, duration, resources = jobs[i]

            heapq.heappush(
                ready,
                (-priority, arrival, order, job_id, duration, resources)
            )
            i += 1

    priority, arrival, order, job_id, duration, resources = heapq.heappop(ready)

    start = max(current_time, free_time)
    finish = start + duration

    waiting_time += start - arrival

    result.append((start, job_id, worker_id, finish))
    heapq.heappush(workers, (finish, worker_id))

    current_time = start


for start, job_id, worker_id, finish in sorted(result):
    print(job_id, "W" + str(worker_id), start, finish)

print("AVG_WAIT", round(waiting_time / n, 2))
