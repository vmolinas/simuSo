def display_memory_table(partitions):
    print("\nTABLA DE PARTICIONES DE MEMORIA:")
    print("+----------------+----------------+------------+--------------------+------------------+")
    print("| ID Partición   | Dirección Ini  | Tamaño     | Proceso Asignado   | Fragmentación    |")
    print("+----------------+----------------+------------+--------------------+------------------+")

    for partition in partitions:
        if partition.id_partition == 0:
            process_display = "SISTEMA OPERATIVO"
            fragmentation_display = "-"
        else:
            process_display = f"Proceso {partition.process_id}" if partition.process_id else "Libre"
            fragmentation_display = f"{partition.internal_fragmentation} KB" if partition.internal_fragmentation > 0 else "0 KB"

        print(f"| {str(partition.id_partition).ljust(15)}"
              f"| {str(partition.start_address).ljust(15)}"
              f"| {str(partition.size).ljust(11)}"
              f"| {process_display.ljust(19)}"
              f"| {fragmentation_display.ljust(16)} |")
    
    print("+----------------+----------------+------------+--------------------+------------------+")

def display_ready_queue(ready_queue):
    print("\nCOLA DE LISTOS:")
    print("+------------+------------+--------------+------------------+------------------+")
    print("| Proceso ID | Tamaño (K) | Tiempo Arribo| Tiempo Irrupción | Tiempo Restante  |")
    print("+------------+------------+--------------+------------------+------------------+")

    for process in ready_queue:
        print(f"| {str(process.process_id).ljust(10)} "
              f"| {str(process.size).ljust(10)} "
              f"| {str(process.arrival_time).ljust(12)} "
              f"| {str(process.burst_time).ljust(16)} "
              f"| {str(process.remaining_time).ljust(16)} |")
    print("+------------+------------+--------------+------------------+------------------+")