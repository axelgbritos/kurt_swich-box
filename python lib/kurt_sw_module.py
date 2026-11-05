"""
kurt_sw_module.py
Libreria de control de la caja de conmutación KURT a traves de puerto serie.

Axel G. Britos - Instituto Nacional de Tecnologia Industrial (INTI) - Argentina

V0.1 - 08/2026.

Notas de version:
    * 0.1 - 08/2026: Release inicial.

    
Pendiente:
Hacer funcionar prog_set().
"""

import serial
import time

def connect(port):
    '''
    Conexion con el instrumentos via puerto serie. Por defecto utiliza la configuracion 9600-8-N-1.

    Parameters
    ----------
    port: str, puerto serie a conectar (ejemplo: "COM3")

    Returns
    -------
    ser: serial conection object. 
    '''
    ser = serial.Serial()
    if ser.is_open:
        ser.close()
    ser.port = port
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1

    ser.dtr = False
    ser.rts = False
    try:
        ser.open()
    except:
        ser.close()
        return None
    ser.reset_input_buffer()
    return ser

def disconnect(ser):
    '''
    Desconecta el instrumento y cierra la conexion serie.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    '''
    ser.close()

def identify(ser):
    '''
    Eso, identifica el dispositivo.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: Nombre del dispositivo + software version.
    '''
    ser.write(f"IDN?\n".encode("ascii"))
    time.sleep(0.5)
    response = ser.read(ser.in_waiting).decode("ascii", errors="replace").strip()
    return response

 
def get_switch(ser,SWn):
    '''
    Obtiene el estado de un switch especifico.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    SWn: int, switch number.

    Returns
    -------
    str: Estado del switch n (SWn OPEN/CLOSE).
    '''
    ser.write(f"SW{SWn}?\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def open_switch(ser,SWn):
    '''
    Abre un switch especifico.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    SWn: int, switch number.

    Returns
    -------
    str: Estado del switch n(SWn OPEN/CLOSE).
    '''
    ser.write(f"SW{SWn} RESET\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response


def close_switch(ser,SWn):
    '''
    Cierra un switch especifico.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    SWn: int, switch number.

    Returns
    -------
    str: Estado del switch n (SWn OPEN/CLOSE).
    '''
    ser.write(f"SW{SWn} SET\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def toggle_switch(ser,SWn):
    '''
    Invierte el estado de un switch especifico.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    SWn: int, switch number.

    Returns
    -------
    str: Estado del switch n (SWn OPEN/CLOSE).
    '''
    ser.write(f"SW{SWn} TGL\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response


def trg_config(ser,trg_mode):
    '''
    Configura el trigger externo.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    trg_mode: bool, True = Habilitar trigger, False = Desactivar trigger.

    Returns
    -------
    str: Estado del trigger externo (TRG ON/OFF).
    '''
    if trg_mode:
        ser.write("TRG ON\n".encode("ascii"))
    else:
        ser.write("TRG OFF\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.read(ser.in_waiting).decode("ascii", errors="replace").strip()
    return response


def open_all(ser):
    '''
    Abre todos los switches.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: "OPEN".
    '''
    ser.write("OPEN\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def stop(ser):
    '''
    Abre todos los switches, deshabilita el trigger y reinicia la secuencia. 
    El trigger externo debe ser habilitado nuevamente luego de este comando.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: "STOP".
    '''
    ser.write("STOP\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def status(ser):
    '''
    Obtiene el estado de los switches, del trigger y de la secuencia.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    tuple: (state, trigger, step)
        state: list of int, estado de los switches (0=abierto, 1=cerrado).
        trigger: int, estado deltrigger externo (0=off, 1=on).
        step: list of int, posicion en la lista de estados ([actual, total]).
    '''
    ser.write("STATE?\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.read(ser.in_waiting).decode("ascii", errors="replace").strip()

    lines = response.splitlines()

    # Estado de los switches
    state = lines[0].replace("STATE:", "").strip().split()
    state = [int(bit) for bit in state]

    # Estado del trigger
    trigger = 1 if "TRG ON" in lines[1] else 0

    # Estado del step
    step_text = lines[2].replace("STEP", "").strip()
    step = [int(value) for value in step_text.split("/")]

    return state, trigger, step

'''
def prog_set(ser, state_list, clear=False): 
    
    #---Esta funcion no esta lista todavia--- NO USAR.
    #Configura una lista de estados programados.
    
    time.sleep(0.1)
    if clear:
        prog_clear(ser)
    ser.write("PROG START\n".encode("ascii"))
    time.sleep(0.1)

    for state in state_list:
        pattern = "".join("1" if v else "0" for v in state)
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            ser.write((pattern + "\n").encode("ascii"))
            time.sleep(0.1)
            confirmation = ser.readline().decode("ascii",errors="replace").strip()
            print(confirmation)
            attempts += 1
            if not confirmation.startswith("ERR"):
                break

        if confirmation.startswith("ERR"):
            ser.write("PROG END\n".encode("ascii"))
            return confirmation
        
    ser.write("PROG END\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response
'''

def prog_edit_n(ser,n, state):
    '''
    Modifica el estado especifico en la posicion n de lista de estados programados.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    n: int, posicion a modificar.
    state: list of int, switch status (0=abierto, 1=cerrado).

    '''
    pattern = "".join("1" if v else "0" for v in state)
    ser.write(f"PROG {n}\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    if response == f"PROG {n}":
        pattern = "".join("1" if v else "0" for v in state)
        ser.write(pattern+"\n".encode("ascii"))
        time.sleep(0.1)
        response = ser.readline().decode("ascii", errors="replace").strip()
        if response.startswith(str(n)):
            return response
    else:
        return response


def prog_get(ser):
    '''
    Obtiene la lista de estados programados.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    tuple: (prog_count, states)
        prog_count: int, numero de estados programados.
        states: lista int con los estados programados. (0=cerrado, 1=abierto).
    '''
    ser.write("PROG?\n".encode("ascii"))
    time.sleep(0.1)
    count = ser.readline().decode("ascii",errors="replace").strip()

    try:
        prog_count = int(count)
    except ValueError:
        prog_count = -1
    states = []
    for _ in range(prog_count):
        line = ser.readline().decode(
            "ascii",
            errors="replace"
        ).strip()
        if ":" not in line:
            continue
        index, pattern = line.split(":", 1)
        pattern = pattern.replace("\t", "")
        state = [int(bit) for bit in pattern]
        states.append(state)
    return prog_count, states

def prog_clear(ser):
    '''
    Limpia la lista de estados programados.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: "PROG CLEAR".
    '''
    ser.write("PROG CLEAR\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response


def next_status(ser):
    '''
    Salta al estado siguiente en la lista de estados programados.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: 
        "STEP n/m": Donde n es el estado actual y m es el total de estados.
        "ERR CMD": No hay estados programados.
    '''
    ser.write("NEXT\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def prev_status(ser):
    '''
    Salta al estado anteior en la lista de estados programados.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().

    Returns
    -------
    str: 
        "STEP n/m": Donde n es el estado actual y m es el total de estados.
        "ERR CMD": No hay estados programados.
    '''
    ser.write("PREV\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

def goto_status(ser, step):
    '''
    Establece el estado de los switches al estado programado en la posicion n.

    Parameters
    ----------
    ser: serial conection object. Crear con la funcion connect().
    step: int, posicion en la lista de estados.

    Returns
    -------
    str: 
        "STEP n/m": Donde n es el estado actual y m es el total de estados.
        "ERR CMD": No hay estados programados o el numero de estados esta fuera de rango.
    '''
    ser.write(f"GOTO {step}\n".encode("ascii"))
    time.sleep(0.1)
    response = ser.readline().decode("ascii", errors="replace").strip()
    return response

