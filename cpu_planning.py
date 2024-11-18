from utils import load_processes
from process import *
from memory_management import *
from visualization import *
from collections import deque

def update_ready_queue(ready_queue, processes, partitions, current_time, max_queue_size=5):
    # Contar los procesos ya asignados a memoria (no están libres)
    processes_in_memory = sum(1 for partition in partitions if partition.process_id is not None)

    for process in list(processes):
        # Solo considerar procesos que llegan en el tiempo actual
        if process.arrival_time <= current_time and not process.finished:
            # Verificar si hay espacio en la cola de listos, considerando los procesos en memoria
            if len(ready_queue) + processes_in_memory < max_queue_size:
                ready_queue.append(process)
                processes.remove(process)
                print(f"Tiempo {current_time}: Proceso {process.process_id} añadido a la cola de listos.")

def assign_memory_to_processes(ready_queue, partitions, cpu_queue, current_time):
    for process in list(ready_queue):
        # Intentar asignar memoria solo si el proceso no tiene ya una partición asignada
        if process.assigned_partition is None:
            partition = worst_fit(partitions, process)
            if partition:
                partition.process_id = process.process_id
                partition.internal_fragmentation = partition.size - process.size
                process.assigned_partition = partition
                cpu_queue.append(process)
                ready_queue.remove(process)
                print(f"Tiempo {current_time}: Proceso {process.process_id} asignado a la Partición {partition.id_partition}.")

def assign_to_waiting_processes(waiting_list, ready_queue, partitions, current_time, max_ready_queue_size=5):
    for process in list(waiting_list):
        # Verificar el límite de procesos en ready_queue
        if len(ready_queue) >= max_ready_queue_size:
            print(f"Tiempo {current_time}: Límite alcanzado. Proceso {process.process_id} permanece en lista de espera.")
            break

        # Intentar asignar memoria
        partition = worst_fit(partitions, process)
        if partition:
            partition.process_id = process.process_id
            partition.internal_fragmentation = partition.size - process.size
            process.assigned_partition = partition
            waiting_list.remove(process)
            ready_queue.append(process)
            print(f"Tiempo {current_time}: Proceso {process.process_id} asignado a memoria.")
            display_ready_queue(ready_queue)
            display_memory_table(partitions)
            input("Presiona Enter para continuar...")  # Pausa después de asignar memoria

def execute_process(current_process, quantum_counter, quantum, cpu_queue, current_time):
    if current_process:
        current_process.remaining_time -= 1
        quantum_counter += 1

        # Verificar si el proceso ha terminado
        if current_process.remaining_time == 0:
            return current_process, 0, True  # Proceso terminado

    return current_process, quantum_counter, False  # Proceso sigue ejecutándose

def finalize_process(current_process, partitions, current_time):
    print(f"\nTiempo {current_time}: Proceso {current_process.process_id} ha terminado.")
    current_process.finish_time = current_time + 1
    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
    current_process.finished = True  # Asegúrate de marcar como finalizado
    release_memory(partitions, current_process)

    print(f"Proceso {current_process.process_id}: Start={current_process.start_time}, Finish={current_process.finish_time}, Turnaround={current_process.turnaround_time}, Waiting={current_process.waiting_time}")


def update_waiting_list(waiting_list, processes, current_time, max_waiting_size=5):
    for process in list(processes):
        if process.arrival_time <= current_time and len(waiting_list) < max_waiting_size:
            waiting_list.append(process)
            processes.remove(process)
            print(f"Tiempo {current_time}: Proceso {process.process_id} añadido a la lista de espera.")

def simulate(file_name):
    processes = load_processes(file_name)
    partitions = initialize_partitions()
    ready_queue = deque()  # Procesos en memoria listos para ejecutar
    waiting_list = deque()  # Procesos esperando asignación de memoria
    current_process = None
    quantum = 3
    quantum_counter = 0
    current_time = 0

    print("\n--- Inicio de la Simulación ---")

    while True:
        # Mostrar el estado actual al inicio de cada ciclo
        print(f"\n*** TIEMPO: {current_time} ***")
        display_ready_queue(ready_queue)
        display_memory_table(partitions)
        if current_process:
            print(f"Proceso en ejecución: {current_process.process_id} (Tiempo restante: {current_process.remaining_time})")
        else:
            print("Ningún proceso está ejecutándose actualmente en la CPU.")

        input("Presiona Enter para continuar...")  # Pausa en cada ciclo

        # Mover procesos que han llegado a la lista de espera
        update_waiting_list(waiting_list, processes, current_time)

        # Asignar memoria a los procesos en la lista de espera
        assign_to_waiting_processes(waiting_list, ready_queue, partitions, current_time)

        # Ejecutar el proceso actual
        if current_process is None and ready_queue:
            current_process = ready_queue.popleft()
            if current_process.start_time is None:
                current_process.start_time = current_time
            print(f"Tiempo {current_time}: Proceso {current_process.process_id} está corriendo en la CPU.")

        if current_process:
            current_process, quantum_counter, finished = execute_process(current_process, quantum_counter, quantum, ready_queue, current_time)

            # Si el proceso terminó, liberar memoria
            if finished:
                finalize_process(current_process, partitions, current_time)
                current_process = None
                quantum_counter = 0


            # Si el quantum se agota, mover al final de la cola
            elif quantum_counter == quantum:
                ready_queue.append(current_process)
                current_process = None
                quantum_counter = 0

        # Incrementar el tiempo
        current_time += 1

        # Verificar la condición de salida
        if all(process.finished for process in processes) and not ready_queue and not waiting_list and current_process is None:
            break

    print("\n--- Fin de la Simulación ---")
    calculate_statistics(processes)