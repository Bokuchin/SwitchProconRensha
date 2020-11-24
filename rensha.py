#!/usr/bin/env python3

import os
import threading
import time
import random


# Re-connect USB Gadget device
os.system('echo > /sys/kernel/config/usb_gadget/procon/UDC')
os.system('ls /sys/class/udc > /sys/kernel/config/usb_gadget/procon/UDC')

time.sleep(0.5)

gadget = os.open('/dev/hidg0', os.O_RDWR | os.O_NONBLOCK)
procon = os.open('/dev/hidraw4', os.O_RDWR | os.O_NONBLOCK)
mouse  = os.open('/dev/hidraw2', os.O_RDWR | os.O_NONBLOCK)
mouse_int = bytes([0,0,0,0,0,0,0,0])
val = None
def key_wari():
    global val
    while True:
        val = input()


def mouse_input():
    global mouse_int
    try:
        mouse_int = os.read(mouse, 128)
        #print('<<<', output_data.hex())
        #print(output_mouse.hex())
        #os.write(gadget, output_mouse)
    except BlockingIOError:
        pass
        #print("blockingioerror")
    except Exception as g:
        print(type(g))
        print(g)
        os._exit(1)



def procon_input():
    while True:
        try:
            input_data = os.read(gadget, 128)
            #print('>>>', input_data.hex())
            os.write(procon, input_data)
        except BlockingIOError:
            pass
        except:
            os._exit(1)

def convert(ou_dt_i, mo_in_i, weight, reflect):
    #global t_end
    mo_in_i = int.from_bytes(mo_in_i, byteorder='little', signed=True)
    ou_dt_i = int.from_bytes(ou_dt_i, byteorder='little', signed=True)
    #test
    '''if time.time() < t_end:
        mo_in_i = mo_in_i - 4'''

    merged_gy = ou_dt_i + mo_in_i * weight
    if merged_gy > 32767:
        merged_gy = 32767
    elif merged_gy < -32768:
        merged_gy = -32768
    else:
        pass
    merged_gy = merged_gy.to_bytes(2, byteorder='little', signed=True)

    return merged_gy

def replace_mouse(output_data, mouse_int):
    #a = output_data[0:13]
    global ti
    #mouse no click wo migi no button ni henkan
    ri_btn = 0
    le_btn = 0
    zr_btn = 0b10000000
    l_btn  = 0b01000000

    if (output_data[3] & zr_btn) and time.time() > ti + 0.02:#Lbutton ga 0x40 nara ZR wo osu
        ri_btn = 0b10000000
        ti = time.time()
    else:
        ri_btn = output_data[3] & 0b01111111
    if (output_data[5] & l_btn):
        ri_btn = output_data[3] | 0b10000000
    ri_btn = ri_btn.to_bytes(1, byteorder='little')
    #le_btn = (output_data[3] | le_btn).to_bytes(1, byteorder='little')

    a = output_data[0:3] + ri_btn + output_data[4:5] + output_data[5:6] + output_data[6:13]

    #kasokudo sensor ni tekitou ni atai wo ire naito setsuzoku ga kireru
    '''
    if int.from_bytes(mouse_int[2:4], byteorder="little") != 0:
        b = 256
    else:
        b=0
    if int.from_bytes(mouse_int[4:6], byteorder="little") != 0:
        b = 256
    else:
        b = 0
    d = bytes([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    if int.from_bytes(output_data[13:15], byteorder="little", signed=True) + b > 32767:
        ac0 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac0 = int.from_bytes(output_data[13:15], byteorder="little", signed=True) + b
        ac0 = ac0.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[15:17], byteorder="little", signed=True) + b > 32767:
        ac1 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac1 = int.from_bytes(output_data[15:17], byteorder="little", signed=True) + b
        ac1 = ac1.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[17:19], byteorder="little", signed=True) + b > 32767:
        ac2 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac2 = int.from_bytes(output_data[17:19], byteorder="little", signed=True) + b
        ac2 = ac2.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[25:27], byteorder="little", signed=True) + b > 32767:
        ac0_1 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac0_1 = int.from_bytes(output_data[25:27], byteorder="little", signed=True) + b
        ac0_1 = ac0_1.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[27:29], byteorder="little", signed=True) + b > 32767:
        ac1_1 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac1_1 = int.from_bytes(output_data[27:29], byteorder="little", signed=True) + b
        ac1_1 = ac1_1.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[29:31], byteorder="little", signed=True) + b > 32767:
        ac2_1 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac2_1 = int.from_bytes(output_data[29:31], byteorder="little", signed=True) + b
        ac2_1 = ac2_1.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[37:39], byteorder="little", signed=True) + b > 32767:
        ac0_2 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac0_2 = int.from_bytes(output_data[37:39], byteorder="little", signed=True) + b
        ac0_2 = ac0_2.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[39:41], byteorder="little", signed=True) + b > 32767:
        ac1_2 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac1_2 = int.from_bytes(output_data[39:41], byteorder="little", signed=True) + b
        ac1_2 = ac1_2.to_bytes(2, byteorder="little", signed=True)
    if int.from_bytes(output_data[41:43], byteorder="little", signed=True) + b > 32767:
        ac2_2 = (256).to_bytes(2, byteorder="little", signed=True)
    else:
        ac2_2 = int.from_bytes(output_data[41:43], byteorder="little", signed=True) + b
        ac2_2 = ac2_2.to_bytes(2, byteorder="little", signed=True)
    '''

    '''
    #mouse no ugoki wo gyro no ugoki ni henkan
    gy0_0 = convert(output_data[19:21], mouse_int[2:4], 250, False)#
    gy1_0 = convert(output_data[21:23], mouse_int[4:6], 0, False)#
    gy2_0 = convert(output_data[23:25], mouse_int[4:6], 0, False)#

    gy0_1 = convert(output_data[31:33], mouse_int[2:4], 250, False)#
    gy1_1 = convert(output_data[33:35], mouse_int[4:6], 0, False)#
    gy2_1 = convert(output_data[35:37], mouse_int[4:6], 0, False)#

    gy0_2 = convert(output_data[43:45], mouse_int[2:4], 250, False)#
    gy1_2 = convert(output_data[45:47], mouse_int[4:6], 0, False)#
    gy2_2 = convert(output_data[47:49], mouse_int[4:6], 0, False)#

    e = a+ac0+ac1+ac2 \
        +gy0_0+gy1_0+gy2_0 \
        +ac0_1+ac1_1+ac2_1 \
        +gy0_1+gy1_1+gy2_1 \
        +ac0_2+ac1_2+ac2_2 \
        +gy0_2+gy1_2+gy2_2 \
        +d
    '''
    e = a+output_data[13:63]#mouse no add wo kesita mono
    #print(int.from_bytes(gy1_0, byteorder='little'))
    #print(mouse_int.hex())
    return e

def procon_output():
    global mouse_int, val
    #flag = 0
    #gybuf0, gy_buf1 = bytes([0,0,0,0,0,0,0,0]), bytes([0,0,0,0,0,0,0,0])
    while True:
        try:
            output_data = os.read(procon, 128)
            mouse_input()

            if val == None :
                e = replace_mouse(output_data, mouse_int)
            elif val == "a":
                a = int.from_bytes(mouse_int[2:4], byteorder='little', signed=True)
                a = a + 200
                a = a.to_bytes(2, byteorder="little", signed=True)
                a = mouse_int[0:2] + a + mouse_int[4:]
                e = replace_mouse(output_data, a)
            elif val == "b":
                e = replace_mouse(output_data, mouse_int)
            else:
                print(f'"{val}"ga osare masita')


            #print(e.hex())
            os.write(gadget, e)#output_data
            mouse_int = bytes([mouse_int[0],mouse_int[1],0,0,0,0,mouse_int[6],mouse_int[7]])
        except BlockingIOError:
            pass
        except Exception as g:
            print(type(g))
            print(g)
            os._exit(1)

ti = time.time()
threading.Thread(target=key_wari).start()
threading.Thread(target=procon_input).start()
threading.Thread(target=procon_output).start()