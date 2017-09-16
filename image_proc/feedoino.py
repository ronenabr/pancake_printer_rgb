#feedoino

import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


#x_speed[rpm], x_steps, y_speed, y_step

def move(x_speed, x_steps, y_speed, y_step):
    send_str = b'%d,%d,%d,%d\n' % (x_speed, x_steps, y_speed, y_step)
    print send_str
    ser.write(send_str)
    ser.flush()
    print ser.readline()
    print ser.readline()
    print ser.readline()

while True:
    res =  ser.readline()
    if not res:
        break

print "Header finished"
    

