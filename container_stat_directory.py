import os
import time

def read_int_from_file(path):
    with open(path, 'r') as file:
        data = file.read().strip()
        #print(f"Read from {path}: {data}")  # Debug output
        if data.isdigit():
            return int(data)
        return 0

def read_cpu_usage_usec(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if "usage_usec" in line:
            _, value = line.split()
            #print(f"CPU usage_usec from {path}: {value}")  # Debug output
            return int(value)
    return 0

def get_cpu_usage_percent(container_cgroup_path, interval=1):
    cpu_stat_path = os.path.join(container_cgroup_path, 'cpu.stat')
    cpu_usage_start = read_cpu_usage_usec(cpu_stat_path)

    time.sleep(interval)

    cpu_usage_end = read_cpu_usage_usec(cpu_stat_path)
    cpu_delta = cpu_usage_end - cpu_usage_start
    print(f"CPU usage delta: {cpu_delta}")  # Debug output

    # Correct total CPU time available calculation:
    # Assuming 1 CPU for simplicity in the calculation. Adjust based on actual allocated CPUs.
    total_cpu_time_available = 1 * interval * 1e9  # nanoseconds for 1 CPU

    cpu_percentage = (cpu_delta / total_cpu_time_available) * 100
    return cpu_percentage


def get_memory_usage_percent(container_cgroup_path):
    memory_usage_path = os.path.join(container_cgroup_path, 'memory.current')
    memory_max_path = os.path.join(container_cgroup_path, 'memory.max')

    memory_usage = read_int_from_file(memory_usage_path)
    memory_max = read_int_from_file(memory_max_path)

    if memory_max == 0:  # Avoid division by zero if memory.max is not set or returned zero
        return 0

    return (memory_usage / memory_max) * 100

# Main execution
if __name__ == "__main__":
    container_cgroup_path = '/sys/fs/cgroup/system.slice/docker-85bc37ab47ea44e9c6b40dc1925e46cb06b4d0a16dbfa264f762a9304ae7fde9.scope'
    cpu_usage_percent = get_cpu_usage_percent(container_cgroup_path)
    memory_usage_percent = get_memory_usage_percent(container_cgroup_path)

    print(f"Container CPU usage: {cpu_usage_percent:.2f}%")
    print(f"Container memory usage: {memory_usage_percent:.2f}%")
