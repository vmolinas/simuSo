import sys
import os
from process import Process

def validate_processes_file(file_name):
    errors = []  # Lista para acumular errores encontrados
    ids = set()  # Conjunto para verificar IDs únicos
    line_num = 0  # Contador de línea

    try:
        with open(file_name, 'r') as file:
            for line in file:
                line_num += 1
                if line.strip() == "" or line.startswith("#"):
                    continue  # Ignorar líneas vacías o comentarios

                process_data = line.strip().split(',')
                if len(process_data) != 4:
                    errors.append(f"  ***Error en línea {line_num}: Formato incorrecto (se esperaban 4 campos, encontrados {len(process_data)}).")
                    continue

                try:
                    process_id = int(process_data[0].strip())
                    size = int(process_data[1].strip())
                    arrival_time = int(process_data[2].strip())
                    burst_time = int(process_data[3].strip())
                except ValueError:
                    errors.append(f"  ***Error en línea {line_num}: Valores no numéricos encontrados.")
                    continue

                # Verificar IDs únicos
                if process_id in ids:
                    errors.append(f"  ***Error en línea {line_num}: ID duplicado {process_id}.")
                else:
                    ids.add(process_id)

                # Verificar que el tamaño no exceda 250K
                if size > 250:
                    errors.append(f"  ***Error en línea {line_num}: Tamaño {size}K excede el máximo permitido de 250K.")

        if errors:
            print("  ***Errores encontrados en el archivo de procesos:")
            for error in errors:
                print(error)
            return False
        else:
            return True

    except FileNotFoundError:
        print(f"  ***Archivo {file_name} no encontrado.")
        sys.exit(1)

def load_processes(file_name):
    if not validate_processes_file(file_name):
        print("  ***Error en la validación del archivo de procesos. Corrige los errores e intenta nuevamente.")
        sys.exit(1)

    processes = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.strip() == "" or line.startswith("#"):
                    continue
                process_data = line.strip().split(',')
                process_id = int(process_data[0].strip())
                size = int(process_data[1].strip())
                arrival_time = int(process_data[2].strip())
                burst_time = int(process_data[3].strip())
                processes.append(Process(process_id, size, arrival_time, burst_time))
    except FileNotFoundError:
        print(f"  ***Archivo {file_name} no encontrado.")
        sys.exit(1)

    # Ordenar los procesos por tiempo de arribo (arrival_time)
    processes.sort(key=lambda process: process.arrival_time)

    return processes

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')