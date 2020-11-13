
## TODO: Accommodate the fact that memory might be provided in megabytes (?)
def get_consumed_resources(jobid, runtime, job_data):

    executor_cores=int(job_data["executor_cores"])
    executor_memory=int(job_data["executor_memory"].strip('g'))
    driver_cores=int(job_data["driver_cores"])
    driver_memory=int(job_data["driver_memory"].strip('g'))
    num_executors=int(job_data["num_executors"])
    cpus = (num_executors * executor_cores) + driver_cores
    memory = driver_memory + (num_executors * executor_memory)
    return {'cpu_hours': cpus*(runtime/3600.0), 'memory_hours': memory*(runtime/3600.0)}