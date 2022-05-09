
import random


def createSimpleSchedule(problem):
    # First create the straight forward schedule
    # iterates through the jobs and returns a schedule of the different jobs
    schedule = []
    for job in problem.jobs:
        for i in range(len(job.operations)):
            schedule.append((job.id, i))
    
    return schedule

def createBackwardsSchedule(problem):
    # The same approach as simple schedule, but starting with the job with the highest id
    schedule = []
    for i in range(len(problem.jobs) -1, -1, -1):
        job = problem.jobs[i]
        for j in range(len(job.operations)):
            schedule.append((job.id, j))
    
    return schedule

def createMixedSchedule(problem):
    # will make a schedule like the straight forward schedule, but mixes the different job ids
    job_schedules = []
    
    for job in problem.jobs:
        job_schedule = []
        for i in range(len(job.operations)):
            job_schedule.append((job.id, i))
        job_schedules.append(job_schedule)
    schedule = []

    while len(job_schedules) > 0:
        for job_schedule in job_schedules:
            schedule.append(job_schedule.pop(0))
            if len(job_schedule) == 0:
                job_schedules.remove(job_schedule)
    
    return schedule
        



def possibleSchedule(schedule, problem):
    # checks if a schedule is accepted according to the problem
    job_ids = problem.getJobs()
    job_count = {id:-1 for id in job_ids}
    possible = True
    for job in schedule:
        job_id = job[0]
        nr = job[1]
        if nr > job_count[job_id]:
            job_count[job_id] = nr
        else:
            possible = False
            break
    return possible       


def swapPositions(list, pos1, pos2):
    # Swap function
    new_list = list.copy()
    new_list[pos1], new_list[pos2] = new_list[pos2], new_list[pos1]
    return new_list


def create_random_benchmark(n_m, n_jobs, n_operations):
    total_operations = n_jobs * n_operations

    filename = 'mini_project_4/benchmark_4.txt'
    f = open(filename, "w")
    f.write('%s %s %s \n' % (n_m, n_jobs, total_operations))

    for i in range(n_jobs):
        s = str(n_operations) + ' '
        for j in range(n_operations):
            machine = random.randint(1, n_m)
            time = random.randint(1, 10) 
            print('Job %s: (%s, %s)'% (j, machine, time))
            s += '%s %s ' % (machine, time)
        s += '\n'
        f.write(s)
    
    f.close()

def translate_to_predict(schedule):
    # translate a schedule from [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (1, 2), (3, 1), (3, 2)]
    # to [1, 2, 3, 1, 2, 1, 3, 3]
    return [job_id for job_id, index in schedule]

def getAllSchedules(problem, set_size = 200):
    # creates an array of many possible  schedules
    schedules = []
    archive = []

    
    schedule1 = createSimpleSchedule(problem)
    new_schedules = createClosestNeighbours(schedule1, round(set_size/3), archive, problem)

    schedules = schedules + new_schedules


    schedule2 = createBackwardsSchedule(problem)
    new_schedules = createClosestNeighbours(schedule2, round(set_size/3), archive, problem)

    schedules = schedules + new_schedules

    schedule3 = createMixedSchedule(problem)
    new_schedules = createClosestNeighbours(schedule3, round(set_size/3), archive, problem)

    schedules = schedules + new_schedules

    return schedules


def getRandomSchedules(schedules, n):

    result = []
    for i in range(n):
        index = random.randint(0, len(schedules) -1)
        result.append(schedules.pop(index))
    
    return result


   


def createClosestNeighbours(schedule, size, archive, problem):
    schedules = [schedule]
    archive.append(schedule)
    while len(schedules) <size:
        for i in range(1, len(schedule)):
            neighbour = swapPositions(schedule, i-1, i)
            if neighbour not in archive:
                archive.append(neighbour)
                # check if this schedule is possible
                if possibleSchedule(neighbour, problem):
                    schedules.append(neighbour)
                    schedule = neighbour     
    return schedules


