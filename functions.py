import os

# Función para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
