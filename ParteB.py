from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # número del proceso
size = comm.Get_size()  # total de procesos

# Asegurarse de que solo haya 2 procesos a la hora de correr en la terminal
if size != 2:
    if rank == 0:
        print("Este programa necesita exactamente 2 procesos.")
    exit()


N = 10000 # número de veces que se va a enviar el mensaje
mensaje = np.zeros(1, dtype='b')  # b = entero de 1 byte

# Proceso 0 envía y recibe el mensaje N veces
if rank == 0:
    start_time = MPI.Wtime()  # tiempo inicial

    for i in range(N): # recordar que N es cantidad de veces que se manda y se recibe el mensaje 
        comm.Send(mensaje, dest=1, tag=0)     # MPI_Send: proceso 0 envia 1 byte a proceso 0
        comm.Recv(mensaje, source=1, tag=0)   # MPI_Recv: proceso 0 recibe respuesta de proceso 1

    end_time = MPI.Wtime()  # tiempo final
    total_time = end_time - start_time

    # Calcular latencias (después de completar las N transmisiones de ida y vuelta )
    latencia_promedio = (total_time / N) * 1e6  # en microsegundos
    latencia_unidireccional = latencia_promedio / 2

    print(f"Mensaje de 1 byte transmitido {N} veces.")
    print(f"Latencia promedio por mensaje (ida y vuelta): {latencia_promedio:.2f} microsegundos")
    print(f"Latencia estimada unidireccional: {latencia_unidireccional:.2f} microsegundos")

# Proceso 1 recibe el mensaje y lo devuelve
elif rank == 1:
    for i in range(N):
        comm.Recv(mensaje, source=0, tag=0)   # MPI_RCV:ecibir mensaje de proceso 0 
        comm.Send(mensaje, dest=0, tag=0)     # MPI_Send:enviar de vuelta a proceso 0
