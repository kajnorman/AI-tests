import network
import time
from machine import Pin, PWM
import socket
import machine

#machine.freq(200000000)

#print (machine.freq())

SSID = 'ITEK'
PASSWORD = 'SECRETSECRET'
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait for the connection to establish
while not wifi.isconnected():
    pass
print(wifi.ifconfig())
print('Connected to Wi-Fi')
# Define the server address and port
server_ip = '10.100.0.183'  # 178 er Jonas   Change this to the IP of your server
server_port = 12345 # Change this to the port your server is listening on
# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)


gy53_signal = Pin(2, Pin.IN,Pin.PULL_DOWN)

servo = PWM(Pin(6))
servo.freq(50)
vandret = 4300
width = vandret
servo.duty_u16(width)
time.sleep(1)
sp = 2000#2800
pv = 0
oldpv=0
mvavgpv=0
oldmvavgpv=0
print("rebooting")
data = b'0.0'

#  to go into fast mode measure the gy53 must have the serial comand : 0xA5 0x51 0xF6



while True:
    while gy53_signal.value() == True:
        pass
    while gy53_signal.value() == False:
        pass
    starttime = time.ticks_us()
    while gy53_signal.value() == True:
        pass
    endtime = time.ticks_us()
    olderpv = oldpv
    oldpv=pv
    pv = endtime-starttime

    oldermvavgpv = oldmvavgpv
    oldmvavgpv = mvavgpv
    mvavgpv = (pv+oldpv+olderpv)/3
    flpv=(mvavgpv-2500)/2500.0
    float_string = "{:.2f}".format(flpv)  # Formats to two decimal places
    print(float_string)

#    message = "Hello, server!"
#    client_socket.sendto(message.encode(), (server_ip, server_port))
    client_socket.sendto(float_string.encode(), (server_ip, server_port))
    print("sent")
    # Receive data from the server
#    data, server_address = client_socket.recvfrom(1024)
    try:
        data = client_socket.recv(20)
      #  print(server_address)
        print(f"m: {data.decode()}")
    except Exception as e:
        print (e)
        print("no data")
    #time.sleep(0.01)
    width = 4500 - int(float(data) * 2500)
    print (width)


    if (width>7000):
        width=7000
    if (width<2000):
        width = 2000
    servo.duty_u16(int(width))


# Close the socket
client_socket.close()




while True:

    d = mvavgpv - oldermvavgpv  #filtered d
    print (pv)
    #print(d)
    vandret =4300
#    width=    (2*(pv-1000)) + d* 2
    width=  vandret  +   ((mvavgpv-sp)) + d * 6

