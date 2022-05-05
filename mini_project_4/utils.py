from models import Problem


def createFromBenchmark(filename):
        '''
        Task 4.
        Reads from txt file and creates a problem
        '''
        # TODO: fix filename path with sys.path eller noe
        try:
            with open(filename) as file:
                # line 1 -> create needed jobs and machines
                problem = Problem()
                lines = file.readlines()
                info = lines[0].split(' ')
                
                n_jobs = int(info[0])
                n_machines = int(info[1])
                for i in range(n_jobs):
                    job = Job(i+1)
                    problem.jobs.append(job)

                for i in range(n_machines):
                    machine = Machine(i+1)
                    problem.machines.append(machine)

                # line 2 -> end is operations
                for i in range(1, len(lines)):
                    job = problem.getJob(i)
                    info = lines[i].split(' ')
                    """
                    We know that from a line ['3', '3', '4', '2', '2', '1', '1\n']

                    [total operations, machine, time, machine, time, ...]

                    """
                    total_op = int(info[0])
                    for i in range(total_op): # 0,1,2
                        # if i =0, index = 1 and 2
                        # if i=1, index = 3 and 4
                        # if i=2, index = 5 and 6
                        # if i=3, index = 7 and 8

                        index1 = i*2 +1 # machine index
                        index2 =i*2 +2 # time index

                        machineid = int(info[index1])
                        timespan = int(info[index2])
                      
                        operation = Operation(problem.getMachine(machineid), timespan)
                        # add operation to the job
                        job.addOperation(operation)
                file.close()
            return problem
                
        except FileNotFoundError as fnf_error:
            print(fnf_error)
    
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
        