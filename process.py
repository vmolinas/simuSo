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

def complete_process(current_process, current_time):  
    current_process.finish_time = current_time  
    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time  
    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time  
    current_process.finished = True  

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