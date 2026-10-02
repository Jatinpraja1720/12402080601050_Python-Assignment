'''
Problem Statement: Simulate a job scheduler where each job has job_id, priority, duration and required resource count. Multiple worker
threads execute jobs. Higher priority jobs must be processed first; jobs with same priority use earlier arrival order. The program must
maintain thread-safe job assignment and produce a final execution report.
'''

import heapq

w, n = map(int, input().split())

jobs = []

for i in range(n):

    arrival, job_id, priority, duration, resources = input().split()

    arrival = int(arrival)
    priority = int(priority)
    duration = int(duration)
    resources = int(resources)

    jobs.append(
        (arrival, job_id, priority, duration, resources, i)
    )

jobs.sort()

workers = []

for i in range(w):
    heapq.heappush(workers, (0, i + 1))

waiting = []
completed = []

time = 0
index = 0

while index < n or waiting:

    if not waiting and index < n and time < jobs[index][0]:
        time = jobs[index][0]

    while index < n and jobs[index][0] <= time:
        arrival, job_id, priority, duration, resources, order = jobs[index]

        heapq.heappush(
            waiting,
            (-priority, arrival, order, job_id, duration, resources)
        )

        index += 1

    worker_time, worker_id = heapq.heappop(workers)

    if worker_time > time:
        time = worker_time

        while index < n and jobs[index][0] <= time:
            arrival, job_id, priority, duration, resources, order = jobs[index]

            heapq.heappush(
                waiting,
                (-priority, arrival, order, job_id, duration, resources)
            )

            index += 1

    if not waiting:
        heapq.heappush(workers, (worker_time, worker_id))
        continue

    priority, arrival, order, job_id, duration, resources = heapq.heappop(waiting)

    start_time = max(time, worker_time)
    finish_time = start_time + duration

    waiting_time = start_time - arrival

    completed.append(
        (job_id, worker_id, start_time, finish_time, waiting_time)
    )

    heapq.heappush(workers, (finish_time, worker_id))

    time = start_time

completed.sort(key=lambda x: x[2])

total_wait = 0

for job_id, worker_id, start_time, finish_time, waiting_time in completed:

    print(job_id, "W" + str(worker_id), start_time, finish_time)

    total_wait += waiting_time

if n > 0:
    average = total_wait / n
else:
    average = 0

print(f"AVG_WAIT {average:.2f}")
