import random

# Genera 2 millones de números aleatorios entre 0 y 1
def generar_datos(ruta_archivo, cantidad=2_000_000):
    with open(ruta_archivo, 'w') as f:
        for i in range(cantidad):
            if i > 0:
                f.write("#")
            f.write(f"{random.randint(0, 2_000_000)}")

if __name__ == "__main__":
    generar_datos("datos_generados.txt")
