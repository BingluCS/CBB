import sys
import psutil
import mpi4py
#from mpi4py import MPI
import time
import subprocess
def cpu_idle_stat():
    core_cnt = psutil.cpu_count()
    percore_stat = psutil.cpu_times_percent(interval=0.01, percpu=True)
    total_idle = 0
    print('### Idle utilization in CPU power. 1 means a whole core is idle ###')
    for i in range(core_cnt):
        print('    >> Core {}, idle utilization, {}'.format(i, percore_stat[i].idle))
        total_idle += percore_stat[i].idle
        print('>>>> All core, aggregated idle utilization, {}'.format(total_idle))

    return total_idle/100


def get_cpu_utilization(duration):
    start_time = time.time()
    end_time = start_time + duration

    cpu_utilization = []

    while time.time() < end_time:
        utilization = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_utilization.append(utilization)

    return cpu_utilization

def save_cpu_utilization_data(cpu_utilization_data, filename):
    with open(filename, 'w') as file:
        for utilization in cpu_utilization_data:
            file.write(','.join(map(str, utilization)) + '\n')



# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# num = subprocess.run("hostname", capture_output=True, text=True).stdout.strip()
# print(num[9:])
cpu_utilization_data = get_cpu_utilization(int(sys.argv[1]))
save_cpu_utilization_data(cpu_utilization_data, sys.argv[2])
