# Tarea 3 -  Medición de latencia y comunicación colectiva

## Descripción

Se implementan dos programas en Python usando mpi4py:

- **Parte A:** Cálculo de mínimo, máximo y promedio global de un arreglo usando MPI_Bcast, MPI_Scatter y MPI_Reduce.
- **Parte B:** Medición de latencia punto a punto entre dos procesos usando MPI_Send y MPI_Recv.

---

## Requisitos previos

- Python 3
- Virtual Environment (opcional)
- Instalar mpi4py

---

## Archivos

- `ParteA.py`: operaciones colectivas
- `ParteB.py`: medición de latencia

---

## Instrucciones para ejecutar

### Parte A - Operaciones colectivas

Ejecutar con N procesos (N debe ser divisible entre el número de procesos):

(Desde la terminal en el directorio con el archivo)
  mpirun -np 4 python estadisticas_mpi.py 1000000

### Parte B - Medición de latencias

Ejecutar con 2 procesos:

(Desde la terminal en el directorio con el archivo)
  mpirun -np 2 python latencia_mpi.py

  
