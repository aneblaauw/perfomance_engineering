
    
def createSimpleSchedule(problem):
            # First create the straight forward schedule
            # iterates through the jobs and returns a schedule of the different jobs
            schedule = []
            for job in problem.jobs:
                for i in range(len(job.operations)):
                    schedule.append((job.id, i))
            
            return schedule

def possibleSchedule(schedule, problem):
    # checks if a schedule is accepted according to the problem
    print('Checks if schedule is possible')
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