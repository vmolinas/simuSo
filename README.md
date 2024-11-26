# Simulación de Planificación de Procesos y Gestión de Memoria

Este proyecto implementa una **simulación de planificación de procesos y gestión de memoria**. Está diseñado para emular el comportamiento de un sistema operativo en la asignación y ejecución de procesos, aplicando técnicas de gestión de memoria y planificación de la CPU.

## Funcionalidades

1. **Carga y Validación de Procesos**:
   - Los procesos se cargan desde un archivo externo validando que cumplan con las reglas predefinidas (formato, valores numéricos, tamaño máximo, y unicidad de IDs).

2. **Gestión de Memoria**:
   - Utiliza el algoritmo *Worst Fit* para asignar memoria a los procesos.
   - Control de fragmentación interna y liberación de particiones al finalizar un proceso.

3. **Planificación de CPU**:
   - Implementación de un sistema de colas (*ready queue* y *waiting list*).
   - Planificación basada en *Round Robin* con un quantum configurable.
   - Estadísticas por proceso: tiempo de espera, turnaround, tiempo de inicio y finalización.

4. **Visualización en Tiempo Real**:
   - Tabla de memoria mostrando el estado de las particiones.
   - Cola de procesos listos para ejecución.

5. **Interactividad**:
   - El avance de la simulación se realiza de forma interactiva (pausado por cada tick de tiempo).

## Tecnologías y Herramientas

- **Lenguaje**: Python.
- **Estructuras**: Gestión de procesos, particiones y estadísticas mediante clases y métodos.
- **Entrada/Salida**: Archivo externo para cargar procesos y visualización por consola.

## Uso

1. Prepara un archivo de entrada con los procesos en el formato:  
   `id,size,arrival_time,burst_time`.

2. Ejecuta la simulación con el comando:  
   ```bash
   python main.py <nombre_archivo>
