from memory_management import release_memory

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
    
def finalize_process(current_process, partitions, current_time):
    current_process.finish_time = current_time + 1
    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
    current_process.finished = True
    release_memory(partitions, current_process)

    print(f"\t---Proceso {current_process.process_id}: "
          f"  * Inicio={current_process.start_time}, Finalizado={current_process.finish_time}")

def execute_process(current_process, quantum_counter, quantum, cpu_queue, current_time):
    if current_process:
        # Imprimir el estado del proceso en la CPU y el quantum
        print(f"\n\t---PROCESADOR---")
        print(f"  * Proceso {current_process.process_id} está corriendo en la CPU.")
        print(f"  * Quantum usado: {quantum_counter + 1}/{quantum}")

        # Reducir el tiempo restante del proceso y actualizar el quantum
        current_process.remaining_time -= 1
        quantum_counter += 1

        # Verificar si el proceso ha terminado
        if current_process.remaining_time == 0:
            print(f"  * Proceso {current_process.process_id} ha terminado su ejecución.")
            return current_process, 0, True

    return current_process, quantum_counter, False

def calculate_statistics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    completed_processes = 0

    for process in processes:
        if process.finished:
            completed_processes += 1
            total_turnaround_time += process.turnaround_time
            total_waiting_time += process.waiting_time

    if completed_processes > 0:
        avg_turnaround_time = total_turnaround_time / completed_processes
        avg_waiting_time = total_waiting_time / completed_processes
        total_time = max([p.finish_time for p in processes if p.finished], default=1)
        throughput = completed_processes / total_time
    else:
        avg_turnaround_time = 0
        avg_waiting_time = 0
        throughput = 0

    print("\n---INFORME ESTADISTICO---")
    print(f"  * Tiempo de retorno promedio: {avg_turnaround_time:.2f}")
    print(f"  * Tiempo de espera promedio: {avg_waiting_time:.2f}")
    print(f"  * Rendimiento del sistema: {throughput:.2f} trabajos por unidad de tiempo")