"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""
import requests
import serial
import numpy as np
import struct

# Define the IP address and Port of the Server.
ip_address = "127.0.0.1"
port = "8000"

# Make the request
r = requests.get("http://" + ip_address + ":" + port)

# Move the response to another variable
response = r.json()
# Print the response

#Parametros para el puerto serial
nombre_puerto = 'COM10'
baudios = 9600
timeout = 1

#inicializar puerto comunicacion serial
port = serial.Serial(nombre_puerto, baudios, timeout = timeout)

print(response)

def posicionColores():
    posicion_pelotas = []
    for i in range(len(response)):
        if response[i][2] == 'CYAN':        #CRUSHI
            posicion_cian = response[i][0]
            posicion_cian[1] = posicion_cian[1] + response[i][1] #Se le suma el radio del color cian
        elif response[i][2] == 'YELLOW':    #OTRO CARRO
            posicion_amarillo = response[i][0]
        else:
            posicion_pelotas.append(response[i][0])

    vector_pelotas = []
    vector_pelotas.append(100*np.subtract(posicion_pelotas,posicion_cian))

    distancia_pelotas = []
    for i in range(len(posicion_pelotas)):
        distancia_pelotas.append([np.sqrt((vector_pelotas[0][i][0])**2+(vector_pelotas[0][i][1])**2),i])

    distancias_ordenadas = sorted(distancia_pelotas)    # Se ordenan de menor a mayor las distancias de las pelotas
    num = distancias_ordenadas[0][1]
    pelota_cercana = [int(vector_pelotas[0][num][0]),int(vector_pelotas[0][num][1])]    # (posicion x, posicion y) de la pelota mas cercana
    return(pelota_cercana)

def conversion(pelota_cercana): #Funcion para convertir la distancia en 1 byte
    if np.abs(pelota_cercana[0]) > 127:
        if pelota_cercana[0] < -127:
            pelota_cercana[0] = 0
        else:
            pelota_cercana[0] = 255
    if np.abs(pelota_cercana[1]) > 127:
        if pelota_cercana[1] < -127:
            pelota_cercana[1] = 0
        else:
            pelota_cercana[1] = 255
    else:
        pelota_cercana[0] = pelota_cercana[0] + 127
        pelota_cercana[1] = pelota_cercana[1] + 127
    return pelota_cercana

def mandarBluetooth(distancia):
    print(distancia)
    send = bytearray([distancia[0], distancia[1]])
    port.write(send)

pelota_cercana = posicionColores()
distancia = conversion(pelota_cercana)
mandarBluetooth(distancia)