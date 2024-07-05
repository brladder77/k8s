import docker

def get_docker_sdk_stats(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    stats = container.stats(stream=False)  # Get a snapshot of the current stats

    cpu_stats = stats['cpu_stats']
    cpu_delta = cpu_stats['cpu_usage']['total_usage']
    system_cpu_delta = cpu_stats['system_cpu_usage']
    num_cpus = cpu_stats['online_cpus']

    memory_stats = stats['memory_stats']
    memory_usage = memory_stats['usage']
    memory_limit = memory_stats['limit']

    # Calculations might need to be adjusted based on how Docker computes percentages
    cpu_percentage = (cpu_delta / system_cpu_delta) * num_cpus * 100
    memory_percentage = (memory_usage / memory_limit) * 100

    return cpu_percentage, memory_percentage

# Example usage
container_name = '85bc37ab47ea44e9c6b40dc1925e46cb06b4d0a16dbfa264f762a9304ae7fde9'
cpu_usage, memory_usage = get_docker_sdk_stats(container_name)
print(f"CPU Usage: {cpu_usage:.2f}%")
print(f"Memory Usage: {memory_usage:.2f}%")
