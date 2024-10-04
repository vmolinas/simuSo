class Partition:
    def __init__(self, id_partition, start_address, size):
        self.id_partition = id_partition
        self.start_address = start_address
        self.size = size
        self.process_id = None  # Proceso asignado a la partición
        self.internal_fragmentation = 0

    def is_free(self):
        return self.process_id is None

class Process:
    def __init__(self, process_id, size, arrival_time, burst_time):
        self.process_id = process_id
        self.size = size
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # Para el algoritmo Round Robin
        self.waiting_time = 0
        self.turnaround_time = 0
        self.finished = False

def load_processes(file_name):
    processes = []
    with open(file_name, 'r') as file:
        for line in file:
            process_data = line.strip().split(',')
            process_id = int(process_data[0])
            size = int(process_data[1])
            arrival_time = int(process_data[2])
            burst_time = int(process_data[3])
            processes.append(Process(process_id, size, arrival_time, burst_time))
    return processes

def initialize_partitions():
    return [
        Partition(1, 0, 250),  # Trabajo grande
        Partition(2, 250, 150),  # Trabajo mediano
        Partition(3, 400, 50),  # Trabajo pequeño
    ]

def worst_fit(partitions, process):
    worst_partition = None
    for partition in partitions:
        if partition.is_free() and partition.size >= process.size:
            if worst_partition is None or partition.size > worst_partition.size:
                worst_partition = partition
    return worst_partition


def round_robin(queue, quantum=3):
    current_time = 0
    while queue:
        process = queue.pop(0)
        if process.remaining_time > quantum:
            current_time += quantum
            process.remaining_time -= quantum
            queue.append(process)
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            process.finished = True
        # Actualizar tiempos de espera y retorno
        process.turnaround_time = current_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time


def update_ready_queue(ready_queue, processes, current_time):
    for process in processes:
        if process.arrival_time <= current_time and process not in ready_queue and not process.finished:
            ready_queue.append(process)


def calculate_statistics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    completed_processes = 0

    for process in processes:
        if process.finished:
            completed_processes += 1
            total_turnaround_time += process.turnaround_time
            total_waiting_time += process.waiting_time

    avg_turnaround_time = total_turnaround_time / completed_processes
    avg_waiting_time = total_waiting_time / completed_processes
    throughput = completed_processes / max([process.turnaround_time for process in processes])

    print(f"Tiempo de retorno promedio: {avg_turnaround_time}")
    print(f"Tiempo de espera promedio: {avg_waiting_time}")
    print(f"Rendimiento del sistema: {throughput} trabajos por unidad de tiempo")


def simulate(file_name):
    processes = load_processes(file_name)
    partitions = initialize_partitions()
    ready_queue = []
    current_time = 0
    multiprogramming_limit = 5

    while processes or ready_queue:
        update_ready_queue(ready_queue, processes, current_time)

        if len(ready_queue) > multiprogramming_limit:
            ready_queue = ready_queue[:multiprogramming_limit]

        # Asignación de memoria a procesos listos
        for process in ready_queue:
            partition = worst_fit(partitions, process)
            if partition:
                partition.process_id = process.process_id
                partition.internal_fragmentation = partition.size - process.size

        round_robin(ready_queue)

        # Actualizar el tiempo y liberar particiones
        current_time += 1
        for partition in partitions:
            if partition.process_id and partition.process_id in [p.process_id for p in ready_queue if p.finished]:
                partition.process_id = None
                partition.internal_fragmentation = 0

    calculate_statistics(processes)