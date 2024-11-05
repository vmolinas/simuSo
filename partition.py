class Partition:
    def __init__(self, id_partition, start_address, size):
        self.id_partition = id_partition
        self.start_address = start_address
        self.size = size
        self.process_id = None  # Proceso asignado a la partición
        self.internal_fragmentation = 0

    def is_free(self):
        return self.process_id is None

    def __str__(self):
        return (f"Partición {self.id_partition}: "
                f"Dirección de inicio = {self.start_address}K, "
                f"Tamaño = {self.size}K, "
                f"Proceso asignado = {self.process_id}, "
                f"Fragmentación interna = {self.internal_fragmentation}K")