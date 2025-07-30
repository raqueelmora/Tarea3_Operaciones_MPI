from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # # del proceso
size = comm.Get_size()  # total de procesos

# Verificacion si se paso el tamannio del arreglo por linea de comandos
if len(sys.argv) != 2:
    if rank == 0:
        print("Uso correcto: python estadisticas_mpi.py <tamaño_arreglo>")
    sys.exit()

# Tamannio del arreglo
N = int(sys.argv[1])

# Verificar que el tamannio sea divisible entre todos los procesos
if N % size != 0:
    if rank == 0:
        print("Error: el tamannio del arreglo debe ser divisible entre el numero de procesos")
    sys.exit()

# Proceso 0 (con numeros aleatorios)
data = None
if rank == 0:
    data = np.random.uniform(0, 100, N)
    print(f"Proceso {rank}: se genero un arreglo con {N} numeros aleatorios.")

# Reparticion del arreglo para cada proceso
local_n = N // size
sub_arreglo = np.empty(local_n, dtype='d')
comm.Scatter(data, sub_arreglo, root=0)
print(f"Proceso {rank}: recibio {len(sub_arreglo)} numeros.")

# Calculo de estadisticas locales segun cada proceso
min_local = np.min(sub_arreglo)
max_local = np.max(sub_arreglo)
avg_local = np.mean(sub_arreglo)
print(f"Proceso {rank}: minimo = {min_local:.2f}, maximo = {max_local:.2f}, promedio = {avg_local:.2f}")

# Reduccion resultados a proceso 0
min_global = comm.reduce(min_local, op=MPI.MIN, root=0)
max_global = comm.reduce(max_local, op=MPI.MAX, root=0)
sum_global = comm.reduce(np.sum(sub_arreglo), op=MPI.SUM, root=0)

# Resultado final proceso 0
if rank == 0:
    avg_global = sum_global / N
    print("\nResultados globales:")
    print(f"Minimo global: {min_global:.2f}")
    print(f"Maximo global: {max_global:.2f}")
    print(f"Promedio global: {avg_global:.2f}")
