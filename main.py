from cpu_planning import simulate
import sys

# Llamada a la simulación con argumento del archivo
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python functions.py <archivo_procesos>")
        sys.exit(1)
    
    simulate(sys.argv[1])