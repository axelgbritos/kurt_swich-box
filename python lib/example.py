'''
Ejemplo de uso de la caja de switches KURT usando la libreria kurt_sw_module.py

Esta version del dispositivo tiene 6 switches frontales y una salida externa de 5V en la parte trasera. (ver especificaciones tecnicas)
Los switches frontales se numeran del 1 al 6 y la salida trasera es el switch 7 (ext_5v).
'''

import kurt_sw_module as box
import sys
import time

PRINT_RESPONSE = True

#Conexion con el instrumento. Configurar manualmente el puerto COM.
ser = box.connect("COM8")

if ser is None:
    print("CONNECTION ERROR")
    sys.exit(1)

#Consultar identificacion. 
print(box.identify(ser))

#Abrir todos los switches.
box.open_all(ser)

print("---TEST: Cerrar secuencialmente los switches.")
for i in range(1, 8):
    response = box.close_switch(ser, i)
    if PRINT_RESPONSE:
        print(response)
    time.sleep(1)

print("---TEST: Abrir secuencialmente los switches.")
for i in range(1, 8):
    response = box.open_switch(ser, i)
    if PRINT_RESPONSE:
        print(response)
    time.sleep(1)

    
print("---Alternar switch 1, 5 y 7(ext_5v).")

box.toggle_switch(ser, 1)
box.toggle_switch(ser, 5)
box.toggle_switch(ser, 7)

# Sino se imprime la respuesta conviene limpiar buffer de entrada para evitar que impriman mensajes anteriores.
ser.flushInput()

print(box.status(ser))

# Desconectar el instrumento al terminar de usarlo para liberar el puerto.
box.disconnect(ser)