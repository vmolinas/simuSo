def update_ready_queue(ready_queue, waiting_list, processes, current_time):
    print(f"\nTiempo {current_time}: Verificando procesos que llegan.")

    # Crear una lista para almacenar los procesos que no han terminado
    active_processes = []
    for p in ready_queue:
        if not p.finished:
            active_processes.append(p)

    if len(active_processes) < 5:
        # Añadir procesos de la lista de espera hasta llenar la cola de listos a 5
        while waiting_list and len(active_processes) < 5:
            process = waiting_list.pop(0)
            ready_queue.append(process)
            active_processes.append(process)
            print(f"Tiempo {current_time}: Proceso {process.process_id} (esperando) se ha añadido a la cola de listos.")

    # Revisar los procesos que llegan en el tiempo actual y añadirlos a la cola de listos o a la lista de espera
    for process in processes:
        if process.arrival_time == current_time and not process.finished:
            if len(active_processes) < 5:
                ready_queue.append(process)
                active_processes.append(process)
                print(f"Tiempo {current_time}: Proceso {process.process_id} ha llegado y se ha añadido a la cola de listos (Tamaño: {process.size}K).")
            else:
                waiting_list.append(process)
                print(f"Tiempo {current_time}: Proceso {process.process_id} ha llegado pero la multiprogramación está al límite. Se ha añadido a la lista de espera.")
        else:
            print(f"Tiempo {current_time}: Proceso {process.process_id} aún no llega o ya ha terminado (Llega en {process.arrival_time}, Estado terminado: {process.finished}).")