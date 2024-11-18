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

    print("\n--- Informe Estadístico ---")
    print(f"Tiempo de retorno promedio: {avg_turnaround_time:.2f}")
    print(f"Tiempo de espera promedio: {avg_waiting_time:.2f}")
    print(f"Rendimiento del sistema: {throughput:.2f} trabajos por unidad de tiempo")