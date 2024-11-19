from utils import load_processes, clear_screen
from process import calculate_statistics
from memory_management import worst_fit, release_memory, initialize_partitions
from visualization import display_memory_table, display_ready_queue
from collections import deque

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
            # print(f"Proceso {process.process_id} asignado a memoria.")

def execute_process(current_process, quantum_counter, quantum, cpu_queue, current_time):
    if current_process:
        current_process.remaining_time -= 1
        quantum_counter += 1

        # Verificar si el proceso ha terminado
        if current_process.remaining_time == 0:
            return current_process, 0, True

    return current_process, quantum_counter, False

def finalize_process(current_process, partitions, current_time):
    current_process.finish_time = current_time + 1
    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
    current_process.finished = True  # Esencial para las estadísticas
    release_memory(partitions, current_process)

    print(f"\nProceso {current_process.process_id}: "
          f"Inicio={current_process.start_time}, Finalizado={current_process.finish_time}")

def update_waiting_list(waiting_list, processes, current_time, max_waiting_size=5):
    for process in list(processes):
        if process.arrival_time <= current_time and len(waiting_list) < max_waiting_size:
            waiting_list.append(process)
            processes.remove(process)
            # print(f"Proceso {process.process_id} añadido a la lista de espera.")

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

    assign_to_waiting_processes(waiting_list, ready_queue, partitions, current_time)

    # Bucle principal de la simulación
    while True:
        print(f"\nTIEMPO: {current_time}")

        # Actualizar las colas
        update_waiting_list(waiting_list, processes, current_time)
        assign_to_waiting_processes(waiting_list, ready_queue, partitions, current_time)

        # Ejecutar el proceso actual
        if current_process is None and ready_queue:
            current_process = ready_queue.popleft()
            if current_process.start_time is None:
                current_process.start_time = current_time
            print(f"\nProceso {current_process.process_id} está corriendo en la CPU.")

        if current_process: current_process, quantum_counter, finished = execute_process(
                            current_process, quantum_counter, quantum, ready_queue, current_time)

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

        display_memory_table(partitions)
        display_ready_queue(ready_queue)
        input("Presiona Enter para continuar...")
        clear_screen()

    print("\n--- Fin de la Simulación ---")
    calculate_statistics(processes)