import serial

ser = serial.Serial('COM4')

while True:
    print ser.read_all()