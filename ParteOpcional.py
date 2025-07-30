# ParteOpcional.py
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    if rank == 0:
        print("Este programa necesita exactamente 2 procesos.")
    exit()

N = 10000  # número de repeticiones

latencias_ida_vuelta = []
latencias_unidireccional = []
ancho_bandas_MBps = []

# Tamaños de mensaje en bytes: 1B, 1KB, 1MB
tamanos = [1, 1024, 1024*1024]


for tam in tamanos: # probar cada tamano
    mensaje = np.zeros(tam, dtype='b')

    comm.Barrier()  # sincronizar antes de empezar a medir

    if rank == 0:
        start_time = MPI.Wtime()

        for _ in range(N):
            comm.Send(mensaje, dest=1, tag=0)
            comm.Recv(mensaje, source=1, tag=0)

        end_time = MPI.Wtime()
        total_time = end_time - start_time

        latencia_promedio = (total_time / N) * 1e6  # microsegundos ida y vuelta
        latencia_unidireccional = latencia_promedio / 2
        latencias_ida_vuelta.append(latencia_promedio)
        latencias_unidireccional.append(latencia_unidireccional)

        # Ancho de banda estimado en MB/s = (tam bytes * 2 viajes * N) / total_time en segundos
        # Se multiplica por 2 porque el mensaje va y vuelve (ida y vuelta)
        ancho_banda = (tam * 2 * N) / (total_time * 1024 * 1024)
        ancho_bandas_MBps.append(ancho_banda)

        print(f"\nTamaño mensaje: {tam} bytes")
        print(f"Latencia promedio ida y vuelta: {latencia_promedio:.2f} μs")
        print(f"Latencia estimada unidireccional: {latencia_unidireccional:.2f} μs")
        print(f"Ancho de banda estimado: {ancho_banda:.2f} MB/s")

    elif rank == 1:
        for _ in range(N):
            comm.Recv(mensaje, source=0, tag=0)
            comm.Send(mensaje, dest=0, tag=0)

# Proceso 0 grafica los resultados
if rank == 0:
    plt.figure(figsize=(10,6))

    # Eje X en KB para mejor visualizacion
    x_kb = [t/1024 for t in tamanos]

    plt.subplot(2,1,1)
    plt.plot(x_kb, latencias_ida_vuelta, marker='o')
    plt.xscale('log')
    plt.xlabel('Tamaño del mensaje (KB)')
    plt.ylabel('Latencia ida y vuelta (μs)')
    plt.title('Latencia promedio vs tamaño de mensaje')
    plt.grid(True)

    plt.subplot(2,1,2)
    plt.plot(x_kb, ancho_bandas_MBps, marker='o', color='orange')
    plt.xscale('log')
    plt.xlabel('Tamaño del mensaje (KB)')
    plt.ylabel('Ancho de banda estimado (MB/s)')
    plt.title('Ancho de banda estimado vs tamaño de mensaje')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
