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
La modulacion BPSK(Bits Phase Shift Keying) lo que hace es el método de desplazamiento de dos símbolos, tiene un bit de información cada uno. Tiene inmunidad la mayor inmunidad al ruido respecto al resto de la familia de phase shift ya que posee una diferencia máxima. Su velocidad de modulación es la más baja de este tipo. Para crear la señal portadora se hace la señal senosoidal de amplitud unitaria y se le agrega una frecuencia de 5000Hz para 10 mil bits con 50 puntos para su muestreo. La onda modulada debería cambiar de dirección cada vez que hay un 1 en los datos y con 0 no debería reaccionar.  
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
La señal modulada obtenidad,con su período en x, es la siguiente 

<img src="https://github.com/andresmoyar/Tarea4/blob/master/BPSK.png">

La señal portadora es la siguiente

<img src="https://github.com/andresmoyar/Tarea4/blob/master/Onda.png">

## Parte 2-Calcular la potencia promedio de la señal modulada generada.
Para calcular la potencia promedio de la señal modulada se debe utilizar la fórmula para potencia instántanea y potencia promedio, son las siguientes:
<img src="https://render.githubusercontent.com/render/math?math=P(T)=(1/2T)*\int_{-T}^{T}x^2(t)dt=A{x^2(t)}">
<img src="https://render.githubusercontent.com/render/math?math=P(T)=(1/2T)*\int_{-T}^{T}E[X^2(t)]dt=A{E[X^2(t)]}">
Para obtener el resultado para este caso se hace el siguiente código:
```python
# Potencia instantánea
pin = senal**2

# Potencia promedio (W)
potpro = integrate.trapz(pin, t) / (N * T)
print("La potencia promedio:\n",potpro)
```
La potencias promedio obtenida es 0.24500049000096372 W

## Parte 3 - Simular un canal ruidoso del tipo AWGN
Para simular el canal ruidoso, se debe obtener la relación señal a ruido 
<img src="https://render.githubusercontent.com/render/math?math=SNR_{dB}=10log_{10}(Ps/Pn)">
Se debe obtener la potencia del ruido y de la señal. Esta SNR debe estar en el rango de -2 a 3 dB.
```python

# Relación señal-a-ruido deseada
SNR = range(-2,3)
Rxfull=[] # Guarda el ruido RX de cada SNR en una lista para usarlo posteriormente en la parte 5.
for i in SNR: 
  pn=0
  # Potencia del ruido para SNR y potencia de la señal dadas
  pn =pn+potpro / (10**(i / 10))
  # Desviación estándar del ruido
  sigma = np.sqrt(pn)
  # Crear ruido (pn = sigma^2)
  ruido = np.random.normal(0, sigma, senal.shape)
  # Simular "el canal": señal recibida
  Rx = senal + ruido
  Rxfull.append(Rx) 
  # Visualización de los primeros bits recibidos
  plt.figure(2)
  plt.plot(Rx[0:20*P])
for j in range(len(Rxfull)):   
    Rx =Rxfull[j]
    plt.plot(Rx[0:20*P])# Visualización  del ruido en el rango de SNR de los primeros bits recibidos
    print("\nCon valores de  SNR={}dB.Provoca el ruido de por=\n{}\n".format(SNR[j],Rxfull[j]))
```
Cada uno de estos se almacena para obtener la señal con ruido para cada uno. La señal con ruido es la siguiente:

<img src="https://github.com/andresmoyar/Tarea4/blob/master/snr.png">


## Parte 4 - Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.
 Aquí se debe graficar espectral de potencia de la señal antes y después cuando se modela con el canal ruidoso.
 Para ello se hace el siguiente código de Python. Aplicando el método de Welch para obtener la gráfica usando la frecuencia y la densidad espectral.
 ```python
 fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Densidad espectral de potencia [V^2/Hz]')
plt.show()
# Después del canal ruidoso
fw, PSD = signal.welch(Rx, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia  [Hz]')
plt.ylabel('Densidad espectral de potencia [V^2/Hz]')
plt.show()
```
La gráfica sin ruido es la siguiente 

<img src="https://github.com/andresmoyar/Tarea4/blob/master/DensidadvsFrecuencia.png">
La gráfica con ruido es la siguiente 

<img src="https://github.com/andresmoyar/Tarea4/blob/master/densidadvsfrecuenciadespues.png">

## Parte 5 - Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.
En el siguiente código se muestra como demodulary decodificar la señal. Además el BER para cada SNR que se encontró en las parte 3. Primero se debe hacer la energía, luego se hace un arreglo para almacenar la tasa de errores. Para la parte de decodificar se debe recorrer la lista de ruido anterior y para ella se usa la energía en el intervalo de operación después se hace los casos de que cada vez que la energía de esto es mayor a la pseudo-energía, se hace almacena un 1 y si esta no se cumple(es ortogonal) se almacena un 0, luego el error se muestra restando del original estos bits almacenados. El conteo BER se hace promediando por el total del número de bits. Luego se almacena los BER en un arreglo para mostrar el caso para cada SNR. 

Para la demodulación y decodificación se usa la siguiente fórmula:


<img src="https://render.githubusercontent.com/render/math?math=g(t)h(t)=\int_{0}^{T}g(t)h(t)dt">

 ```python
# Pseudo-energía de la onda original (esta es suma, no integral)
Es = np.sum(sin**2)

# Inicialización del vector de bits recibidos
bit=np.shape(arr)
bitsRx = np.zeros(bit)
#total de ber
BERfull=[] 
# Decodificación de la señal por detección de energía
for i in range(len(Rxfull)): # Recorrer la lista obtenida del ruido Rx de cada SNR de la parte 3
    Rx=Rxfull[i]
    for k,b in enumerate(arr):
      Ep = np.sum(Rx[k*P:(k+1)*P] * sin)
      
      if Ep > Es/2:
        bitsRx[k] = 1
      else:
        bitsRx[k] = 0

    err = np.sum(np.abs(arr - bitsRx))
    BER = err/N
    BERfull.append(BER)
    print('El ruid de SNR= {}dB ,la senal decodificada tiene  errores de {}en {} bits con la siguiente tasa de error {}.'.format(SNR[i],err, N,BER))

```

Esto da lo siguiente para cada SNR:

El ruido de SNR= -2dB ,la señal decodificada tiene  errores de 235.0 en 10000 bits con la siguiente tasa de error 0.0235.

El ruido de SNR= -1dB ,la señal decodificada tiene  errores de 163.0 en 10000 bits con la siguiente tasa de error 0.0163.

El ruido de SNR= 0dB ,la señal decodificada tiene  errores de 93.0 en 10000 bits con la siguiente tasa de error 0.0093.

El ruido de SNR= 1dB ,la señal decodificada tiene  errores de 34.0 en 10000 bits con la siguiente tasa de error 0.0034.

El ruido de SNR= 2dB ,la señal decodificada tiene  errores de 22.0 en 10000 bits con la siguiente tasa de error 0.0022.

## Parte 6 - Graficar BER versus SNR.
En esta parte se debe graficar los arreglos de SNR y de BER para mostrar la comparación según el decibel y la tasa de errores. Al ser todo derivado de algo aleatorio(ruido) cada vez que se corre el programa puede dar distinto, pero cuando se probo el resultado es el siguiente:

<img src="https://github.com/andresmoyar/Tarea4/blob/master/BERvsSNR.png">
