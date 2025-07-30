from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # numero del priceso
size = comm.Get_size()  # total de procesos

# Verificacion del comunicador (comm)
if len(sys.argv) != 2:
    if rank == 0:
        print("Uso correcto: python estadisticas_mpi.py <tamaño_arreglo>")
    sys.exit()

N = int(sys.argv[1]) #tamaño del arreglo

if N % size != 0: # N (arreglo) debe ser divisible entre el número de procesos (size)
    if rank == 0:
        print("El tamaño del arreglo debe ser divisible entre el número de procesos")
    sys.exit()


data = None
if rank == 0: # Proceso 0 (genera los números aleatorios)
    data = np.random.uniform(0, 100, N) #números entre 0-100
    print(f"Proceso {rank}: se generó un arreglo con {N} números aleatorios.") #Indica el total, antes de repartir

# MPI_Bcast: envía el tamaño del arreglo a los demás
N = comm.bcast(N, root=0)

local_n = N // size # Repartir cantidad de números entre los procesos

# Crear arreglo vacío donde cada proceso va a recibir su parte
sub_arreglo = np.empty(local_n, dtype='d')

# MPI_Scatter: reparte los datos entre los procesos
comm.Scatter(data, sub_arreglo, root=0)
print(f"Proceso {rank}: recibió {len(sub_arreglo)} números.")

# Resultados de cada proceso
min_local = np.min(sub_arreglo)
max_local = np.max(sub_arreglo)
sum_local = np.sum(sub_arreglo)
avg_local = sum_local / local_n
print(f"Proceso {rank}: min = {min_local:.2f}, max = {max_local:.2f}, promedio = {avg_local:.2f}")

# MPI_Reduce: calcula estadísticas globales
min_global = comm.reduce(min_local, op=MPI.MIN, root=0)
max_global = comm.reduce(max_local, op=MPI.MAX, root=0)
sum_global = comm.reduce(sum_local, op=MPI.SUM, root=0)

# También juntamos todos los arreglos para reconstruir el arreglo original (opcional pero útil si ocupamos todo)
data_reconstruida = None
if rank == 0:
    data_reconstruida = np.empty(N, dtype='d')

#MPI_Gather reconstruye el arreglo completo en el proceso 0
comm.Gather(sub_arreglo, data_reconstruida, root=0)

#Resultados globales solo en el proceso 0
if rank == 0:
    avg_global = sum_global / N
    print("\n=== Resultados globales ===")
    print(f"Min global: {min_global:.2f}")
    print(f"Max global: {max_global:.2f}")
    print(f"Promedio global: {avg_global:.2f}")


