def display_memory_table(partitions):
    print("\n  TABLA DE PARTICIONES DE MEMORIA:")
    print("+----------------+---------------+----------+--------------------+-----------------+")
    print("|  ID Partición  |  Dir. Inicio  |  Tamaño  |  Proceso Asignado  |  Fragmentación  |")
    print("+----------------+---------------+----------+--------------------+-----------------+")

    for partition in partitions:
        partition_size = f"{partition.size} KB"
        if partition.id_partition == 0:
            process_display = "SISTEMA OPERATIVO"
            fragmentation_display = "-"
        else:
            process_display = f"Proceso {partition.process_id}" if partition.process_id else "Libre"
            fragmentation_display = f"{partition.internal_fragmentation} KB" if partition.internal_fragmentation > 0 else "0 KB"

        print(f"| {str(partition.id_partition).ljust(15)}"
              f"| {str(partition.start_address).ljust(14)}"
              f"| {partition_size.ljust(9)}"
              f"| {process_display.ljust(19)}"
              f"| {fragmentation_display.ljust(15)} |")
    
    print("+----------------+---------------+----------+--------------------+-----------------+")

def display_ready_queue(ready_queue):
    print("\n  COLA DE LISTOS:")
    print("+--------------+----------+-----------------+--------------------+-------------------+")
    print("|  Proceso ID  |  Tamaño  |  Tiempo Arribo  |  Tiempo Irrupción  |  Tiempo Restante  |")
    print("+--------------+----------+-----------------+--------------------+-------------------+")

    for process in ready_queue:
        process_size = f"{process.size} KB"
        print(f"| {str(process.process_id).ljust(12)} "
              f"| {process_size.ljust(8)} "
              f"| {str(process.arrival_time).ljust(15)} "
              f"| {str(process.burst_time).ljust(18)} "
              f"| {str(process.remaining_time).ljust(17)} |")
    print("+--------------+----------+-----------------+--------------------+-------------------+")

def display_waiting_queue(waiting_queue):
    print("\n  COLA DE ESPERA:")
    print("+--------------+----------+-----------------+--------------------+-------------------+")
    print("|  Proceso ID  |  Tamaño  |  Tiempo Arribo  |  Tiempo Irrupción  |  Tiempo Restante  |")
    print("+--------------+----------+-----------------+--------------------+-------------------+")

    for process in waiting_queue:
        process_size = f"{process.size} KB"
        print(f"| {str(process.process_id).ljust(12)} "
              f"| {process_size.ljust(8)} "
              f"| {str(process.arrival_time).ljust(15)} "
              f"| {str(process.burst_time).ljust(18)} "
              f"| {str(process.remaining_time).ljust(17)} |")
    print("+--------------+----------+-----------------+--------------------+-------------------+")

def display_statistics(estadisticas):
    if not estadisticas:
        print("No hay estadísticas para mostrar.")
        return

    print("\n  ESTADÍSTICAS DE PROCESOS:")
    print("+--------------+------------------+-----------------+------------------+-----------------------+")
    print("|  Proceso ID  |  Tiempo Llegada  |  Tiempo Espera  |  Tiempo Retorno  |  Tiempo Finalización  |")
    print("+--------------+------------------+-----------------+------------------+-----------------------+")

    # Inicializar variables para cálculo de promedios
    total_waiting_time = 0
    total_turnaround_time = 0

    # Imprimir las filas de datos
    for stat in estadisticas:
        print(f"| {str(stat['process_id']).ljust(12)} "
              f"| {str(stat['arrival_time']).ljust(16)} "
              f"| {str(stat['waiting_time']).ljust(15)} "
              f"| {str(stat['turnaround_time']).ljust(16)} "
              f"| {str(stat['finish_time']).ljust(21)} |")
        print("+--------------+------------------+-----------------+------------------+-----------------------+")

        # Acumular tiempos para cálculo de promedios
        total_waiting_time += stat['waiting_time']
        total_turnaround_time += stat['turnaround_time']

    # Calcular tiempos promedios
    average_waiting_time = total_waiting_time / len(estadisticas)
    average_turnaround_time = total_turnaround_time / len(estadisticas)

    # Imprimir los promedios
    print(f"\n  * Promedio de Tiempo de Espera: {average_waiting_time:.2f}")
    print(f"  * Promedio de Tiempo de Retorno: {average_turnaround_time:.2f}")