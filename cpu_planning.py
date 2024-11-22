from utils import load_processes, clear_screen
from process import calculate_statistics, execute_process, finalize_process
from memory_management import worst_fit, initialize_partitions
from visualization import display_memory_table, display_ready_queue, display_waiting_queue
from collections import deque

def assign_to_waiting_processes(waiting_queue, ready_queue, partitions, current_time, max_ready_queue_size=5):
    for process in list(waiting_queue):
        # Verificar el límite de procesos en ready_queue
        if len(ready_queue) >= max_ready_queue_size:
            # print(f"  * Límite alcanzado. Proceso {process.process_id} permanece en lista de espera.")
            break

        # Intentar asignar memoria
        partition = worst_fit(partitions, process)
        if partition:
            # Verificar que el proceso no esté ya en la ready_queue
            if process.process_id not in [p.process_id for p in ready_queue]:
                partition.process_id = process.process_id
                partition.internal_fragmentation = partition.size - process.size
                process.assigned_partition = partition
                waiting_queue.remove(process)
                ready_queue.append(process)
                print(
                    f"  * Proceso {process.process_id} ha sido asignado a la cola de listos.")

def update_waiting_queue(waiting_queue, processes, current_time, max_waiting_size=5):
    for process in list(processes):
        if process.arrival_time <= current_time and len(waiting_queue) < max_waiting_size:
            waiting_queue.append(process)
            processes.remove(process)

def synchronize_ready_queue(ready_queue, partitions, current_process):
    # Obtener IDs de los procesos asignados en las particiones
    active_process_ids = {
        partition.process_id for partition in partitions if partition.process_id is not None}

    # Filtrar procesos activos que no están duplicados
    synchronized_queue = [
        proc for proc in ready_queue if proc.process_id in active_process_ids]

    # Si hay un proceso en ejecución, colocarlo al frente y evitar duplicados
    if current_process and current_process.process_id in active_process_ids:
        synchronized_queue = [current_process] + [
            proc for proc in synchronized_queue if proc.process_id != current_process.process_id]

    return synchronized_queue

def simulate(file_name):
    processes = load_processes(file_name)
    partitions = initialize_partitions()
    ready_queue = deque()  # Procesos en memoria listos para ejecutar
    waiting_queue = deque()  # Procesos esperando asignación de memoria
    current_process = None
    quantum = 3
    quantum_counter = 0
    current_time = 0

    print("\n\t---I N I C I O  D E  L A  S I M U L A C I O N---")

    assign_to_waiting_processes(
        waiting_queue, ready_queue, partitions, current_time)

    # Bucle principal de la simulación
    while True:
        print(f"\n\t---TIEMPO: {current_time}---")

        # Actualizar las colas
        update_waiting_queue(waiting_queue, processes, current_time)
        assign_to_waiting_processes(
            waiting_queue, ready_queue, partitions, current_time)

        # Ejecutar el proceso actual
        if current_process is None and ready_queue:
            current_process = ready_queue.popleft()
            if current_process.start_time is None:
                current_process.start_time = current_time

        if current_process:
            current_process, quantum_counter, finished = execute_process(
                current_process, quantum_counter, quantum, ready_queue, current_time)

            # Si el proceso terminó, liberar memoria y actualizar estado
            if finished:
                finalize_process(current_process, partitions, current_time)
                current_process = None
                quantum_counter = 0

            # Si el quantum se agota, mover el proceso al final de la cola
            elif quantum_counter == quantum:
                print(
                    f"  * Proceso {current_process.process_id} ha agotado su tiempo en CPU.")

                # Mover el proceso al final de la cola de listos
                ready_queue.append(current_process)

                # Liberar la CPU
                # current_process = None
                quantum_counter = 0

                # Asignar el siguiente proceso de la cola de listos
                if ready_queue:
                    current_process = ready_queue.popleft()
                    if current_process.start_time is None:
                        current_process.start_time = current_time

        # Incrementar el tiempo
        current_time += 1

        # Sincronizar la cola de listos con las particiones y el proceso en CPU
        ready_queue = deque(synchronize_ready_queue(
            list(ready_queue), partitions, current_process))

        # Verificar la condición de salida
        if all(process.finished for process in processes) and not ready_queue and not waiting_queue and current_process is None:
            break

        # Mostrar tablas
        display_memory_table(partitions)
        display_ready_queue(ready_queue)
        if waiting_queue:
            display_waiting_queue(waiting_queue)
        current_process = None
        input("Presiona Enter para continuar...")
        clear_screen()

    print("\n\t---F I N  D E  L A  S I M U L A C I O N---")
    calculate_statistics(processes)