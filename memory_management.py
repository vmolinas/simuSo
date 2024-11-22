from partition import Partition

def initialize_partitions():
    partitions = []
    current_address = 0

    partitions.append(Partition(0, current_address, 100))  # Partición SO
    current_address += 100
    partitions.append(Partition(1, current_address, 50))  # Partición Procesos Pequeños
    current_address += 50
    partitions.append(Partition(2, current_address, 150))  # Partición Procesos Medianos
    current_address += 150
    partitions.append(Partition(3, current_address, 250))  # Partición Procesos Grandes
    current_address += 250

    return partitions

def worst_fit(partitions, process):
    worst_partition = None
    max_size = -1
    
    for partition in partitions:
        # Ignorar la partición 0 porque está reservada para el sistema operativo
        if partition.id_partition == 0:
            continue

        if partition.is_free() and partition.size >= process.size:
            if partition.size > max_size:
                max_size = partition.size
                worst_partition = partition

    if worst_partition:
        print(f"  * Proceso {process.process_id} asignado a la Partición {worst_partition.id_partition} con tamaño {worst_partition.size}KB.")

    return worst_partition

def release_memory(partitions, process):
    for partition in partitions:
        if partition.process_id == process.process_id:
            print(f"\n  * Liberando la partición {partition.id_partition} ocupada por el Proceso {process.process_id}.")
            partition.process_id = None
            partition.internal_fragmentation = 0
            break