# simulador.py

import sys
from collections import deque

class Partition:
    def __init__(self, id_partition, start_address, size):
        self.id_partition = id_partition
        self.start_address = start_address
        self.size = size
        self.process_id = None  # Proceso asignado a la partición
        self.internal_fragmentation = 0

    def is_free(self):
        return self.process_id is None

    def __str__(self):
        return (f"Partición {self.id_partition}: "
                f"Dirección de inicio = {self.start_address}K, "
                f"Tamaño = {self.size}K, "
                f"Proceso asignado = {self.process_id}, "
                f"Fragmentación interna = {self.internal_fragmentation}K")

class Process:
    def __init__(self, process_id, size, arrival_time, burst_time):
        self.process_id = process_id
        self.size = size
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # Para el algoritmo Round Robin
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_time = None
        self.finish_time = None
        self.assigned_partition = None
        self.finished = False

    def __str__(self):
        return (f"Proceso {self.process_id}: "
                f"Tamaño = {self.size}K, "
                f"Arribo = {self.arrival_time}, "
                f"Irrupción = {self.burst_time}")

def load_processes(file_name):
    processes = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.strip() == "" or line.startswith("#"):
                    continue  # Ignorar líneas vacías o comentarios
                process_data = line.strip().split(',')
                if len(process_data) != 4:
                    print(f"Formato incorrecto en la línea: {line.strip()}")
                    continue
                process_id = int(process_data[0].strip())
                size = int(process_data[1].strip())
                arrival_time = int(process_data[2].strip())
                burst_time = int(process_data[3].strip())
                processes.append(Process(process_id, size, arrival_time, burst_time))
    except FileNotFoundError:
        print(f"Archivo {file_name} no encontrado.")
        sys.exit(1)
    return processes

def initialize_partitions():
    # Dirección de inicio acumulativa
    partitions = []
    current_address = 0
    # Partición para el Sistema Operativo
    partitions.append(Partition(0, current_address, 100))
    current_address += 100
    # Partición para trabajos grandes
    partitions.append(Partition(1, current_address, 250))
    current_address += 250
    # Partición para trabajos medianos
    partitions.append(Partition(2, current_address, 150))
    current_address += 150
    # Partición para trabajos pequeños
    partitions.append(Partition(3, current_address, 50))
    current_address += 50
    return partitions

def worst_fit(partitions, process):
    worst_partition = None
    max_size = -1
    for partition in partitions:
        if partition.is_free() and partition.size >= process.size:
            if partition.size > max_size:
                max_size = partition.size
                worst_partition = partition
    return worst_partition

def update_ready_queue(ready_queue, processes, current_time):
    for process in processes:
        if process.arrival_time == current_time:
            if len([p for p in ready_queue if not p.finished]) < 5:
                ready_queue.append(process)
                print(f"Tiempo {current_time}: Proceso {process.process_id} ha llegado y se ha añadido a la cola de listos.")
            else:
                print(f"Tiempo {current_time}: Proceso {process.process_id} ha llegado pero la multiprogramación está al límite.")

def calculate_statistics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    completed_processes = 0

    for process in processes:
        if process.finished:
            completed_processes += 1
            total_turnaround_time += process.turnaround_time
            total_waiting_time += process.waiting_time

    if completed_processes == 0:
        avg_turnaround_time = 0
        avg_waiting_time = 0
        throughput = 0
    else:
        avg_turnaround_time = total_turnaround_time / completed_processes
        avg_waiting_time = total_waiting_time / completed_processes
        total_time = max([p.finish_time for p in processes if p.finished], default=1)
        throughput = completed_processes / total_time

    print("\n--- Informe Estadístico ---")
    print(f"Tiempo de retorno promedio: {avg_turnaround_time:.2f}")
    print(f"Tiempo de espera promedio: {avg_waiting_time:.2f}")
    print(f"Rendimiento del sistema: {throughput:.2f} trabajos por unidad de tiempo")

def display_memory_table(partitions):
    print("\nTabla de particiones de memoria:")
    for partition in partitions:
        print(partition)

def display_ready_queue(ready_queue):
    print("\nCola de procesos listos:")
    if not ready_queue:
        print("Vacía")
    else:
        for process in ready_queue:
            if not process.finished:
                print(f"Proceso {process.process_id}")

def simulate(file_name):
    processes = load_processes(file_name)
    partitions = initialize_partitions()
    ready_queue = deque()
    current_time = 0
    multiprogramming_limit = 5
    cpu_queue = deque()
    current_process = None
    quantum = 3
    quantum_counter = 0

    total_processes = len(processes)
    print("\n--- Inicio de la Simulación ---")
    while True:
        # Llegada de nuevos procesos
        update_ready_queue(ready_queue, processes, current_time)

        # Asignar memoria a los procesos en la cola de listos
        for process in list(ready_queue):
            if process.assigned_partition is None:
                partition = worst_fit(partitions, process)
                if partition:
                    partition.process_id = process.process_id
                    partition.internal_fragmentation = partition.size - process.size
                    process.assigned_partition = partition
                    cpu_queue.append(process)
                    ready_queue.remove(process)
                    print(f"Tiempo {current_time}: Proceso {process.process_id} asignado a la Partición {partition.id_partition}.")

        # Mostrar el estado actual de la memoria y la cola de listos
        display_memory_table(partitions)
        display_ready_queue(ready_queue)

        # Si no hay procesos en la CPU y hay procesos en la cola de CPU, asignar uno
        if current_process is None and cpu_queue:
            current_process = cpu_queue.popleft()
            if current_process.start_time is None:
                current_process.start_time = current_time
            print(f"Tiempo {current_time}: Proceso {current_process.process_id} está corriendo en la CPU.")

        # Ejecutar el proceso actual
        if current_process:
            current_process.remaining_time -= 1
            quantum_counter += 1

            # Verificar si el proceso ha terminado
            if current_process.remaining_time == 0:
                current_process.finish_time = current_time + 1
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                current_process.finished = True
                # Liberar la partición de memoria
                for partition in partitions:
                    if partition.process_id == current_process.process_id:
                        partition.process_id = None
                        partition.internal_fragmentation = 0
                        break
                print(f"Tiempo {current_time + 1}: Proceso {current_process.process_id} ha finalizado.")
                current_process = None
                quantum_counter = 0

            # Verificar si el quantum ha expirado
            elif quantum_counter == quantum:
                print(f"Tiempo {current_time + 1}: Quantum expirado para el Proceso {current_process.process_id}.")
                cpu_queue.append(current_process)
                current_process = None
                quantum_counter = 0

        # Incrementar el tiempo
        current_time += 1

        # Verificar condición de finalización
        all_finished = all(p.finished for p in processes)
        if all_finished:
            break

    calculate_statistics(processes)
    print("\n--- Fin de la Simulación ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python simulador.py <archivo_procesos.txt>")
        sys.exit(1)
    archivo_procesos = sys.argv[1]
    simulate(archivo_procesos)
