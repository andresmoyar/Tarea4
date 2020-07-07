#B54889 Andrés Moya Ramírez
#Tarea3-Modelos Andrés Moya R. B54889
from scipy import stats
from scipy import signal
from scipy import integrate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

#Parte2 - potencia promedio de la señal modulada generada.

# Potencia instantánea
pin = senal**2

# Potencia promedio (W)
potpro = integrate.trapz(pin, t) / (N * T)
print("La potencia promedio:\n",potpro)
#Parte 3 - Simular un canal ruidoso del tipo AWGN

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


#Parte 4 - Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.
# Relación señal-a-ruido deseada
# Antes del canal ruidoso
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
#Parte 5 - Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.
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

#Parte 6 - Graficar BER versus SNR.
plt.figure(5)
plt.plot(SNR,BERfull)
plt.grid(True)
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
plt.title('BER vs SNR')
plt.show()
