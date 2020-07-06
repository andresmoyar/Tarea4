# Tarea4
## IE0405-Modelos probabilísticos de señales y sistemas 
### Andrés Moya Ramírez B54889
### Universidad de Costa Rica
Es mi código fuente de la tarea 4 de modelos probabilísticos. Se encuentra el código fuente y las gráficas obtenidas.

Las librerías para hacer el código son las siguientes:
```python
#Tarea3-Modelos Andrés Moya R. B54889
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.optimize import curve_fit
```
## Parte 1-Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.
La modulacion BPSK(Bits Phase Shift Keying) lo que hace es el método de desplazamiento de dos símbolos, tiene un bit de información cada uno. 
### Código usado para obtener los parámetros de la mejor curva de ajuste
```python
arr = []
#con esto recorro los valores 
with open ('bits10k.csv','r') as X:
  filas=X.read().splitlines()
  #Hago un for para recorrer las filas
  for fila in filas:
    arr.append(int(fila))

#Parte 1 - Esquema de modulación BPSK para los bits presentados
#frecuencia de portadora 5 kHz y N=10 kbits
f=5000 #Hz
N= 10000
#Periodo
T=1/f #0,2 ms
#Numero de Puntos de muestreo
P=50
#Puntos de muestreo de cada periodo
tp=np.linspace(0,T,P)
#forma de onda de la portadora
sin=np.sin(2*np.pi*f*tp)
#Impresion
plt.plot(tp,sin)
plt.xlabel('Tiempo(s)')
plt.title('Onda portadora')
plt.figure(1)
plt.savefig('Onda.png')
#frecuencia de muestreo
fs= P/T #500 kHz
#linea temporal para toda la senal
t = np.linspace(0,N*T,N*P)
#Inicializador
senal= np.zeros(t.shape)
#Creacion de la senal modulada BPSK

for i,b in enumerate(arr):
    senal[i*P:(i+1)*P]=np.cos(np.dot(2 * np.pi * fs, T) + np.pi * (b - 1) + np.pi / 4)*sin
  
#Visualizacion
plt.figure()
plt.plot(senal[0:20*P])
plt.show()

```
