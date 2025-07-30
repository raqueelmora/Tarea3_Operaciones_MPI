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
  
  mpirun -np 4 ./mpi_env/bin/python ParteA.py 1000000

### Parte B - Medición de latencias

Ejecutar con 2 procesos:

(Desde la terminal en el directorio con el archivo)
 
  mpirun -np 2 python latencia_mpi.py

## Resultados y Análisis


### Parte A - Operaciones colectivas

Proceso 0: se genero un arreglo con 1000000 numeros aleatorios.
Proceso 1: recibio 250000 numeros.
Proceso 2: recibio 250000 numeros.
Proceso 1: minimo = 0.00, maximo = 100.00, promedio = 50.02
Proceso 0: recibio 250000 numeros.
Proceso 3: recibio 250000 numeros.
Proceso 2: minimo = 0.00, maximo = 100.00, promedio = 49.97
Proceso 0: minimo = 0.00, maximo = 100.00, promedio = 50.04
Proceso 3: minimo = 0.00, maximo = 100.00, promedio = 50.04

Resultados globales:
Minimo global: 0.00
Maximo global: 100.00
Promedio global: 50.02

A partir de estos resultados, se puede ver una distribución equitativa de los numeros totales. Fueron 4 procesos para 1 millón de números, lo cual significa 250k números para cada proceso. En caso de que el los números no se pudieran dividir en 4, el programa no permitiría proceder. Según iban terminando la tarea de distribuir números y encontrar el minimo, máximo y promedio, los resultados se iban imprimiendo. Se desraca que incluso antes de que se pudieran distribuir los numeros al proceso 0 y 3, el proceso 1 ya había sacado las estadísticas de su conjunto de números. 

Es importante notar que el rango de los números es de 0-100, y dado de que cada proceso recibió 250k números, es casi imposible que 0 y 100 no salieran de mínimo y máximo. Con menos muchos números aleatorios y un rango más amplio (ej: 0-10000), quizá cada proceso muestre un mínimo y máximo diferente. En este caso, todos los procesos definitivamente recibieron el número 0 y el número 100 probablemente varias veces. Además dado que el rango es tan pequeño, era de esperar que el promedio sería cerca a 50. Sería muy díficil que con un arreglo de números aleatorios, salgan muchos números sobre o debajo de 50 como para jalar el promedio lejos del 50. Esto se ve en los resultados globales y también en cada proceso, indicando que la repartición de los números sí fue equitativa. 



  
