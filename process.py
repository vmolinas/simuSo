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