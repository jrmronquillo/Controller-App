                                       

#import stbt 
import socket    # used for TCP/IP communication
import smtplib   # used to send email report
import time      # used to insert current date in email report
import sys

rack = sys.argv[1]
key = sys.argv[2]

if sys.argv[1] == "A00":
        rack = "00-80-A3-A2-D9-13"
elif sys.argv[1] == "A01":
        rack = "00-80-A3-A9-E3-68"
elif sys.argv[1] == "A02":
        rack = "00-80-A3-A9-E3-6A"
elif sys.argv[1] == "A03":
        rack = "00-80-A3-A9-E3-7A"
elif sys.argv[1] == "A04":
        rack = "00-80-A3-A9-DA-67"
elif sys.argv[1] == "A05":
        rack = "00-80-A3-A9-E3-79"
elif sys.argv[1] == "A06":
        rack = "00-80-A3-A9-E3-78"
elif sys.argv[1] == "A07":
        rack= "00-80-A3-9E-67-37"
elif sys.argv[1] == "A08":
        rack = "00-80-A3-9D-86-D5"
elif sys.argv[1] == "A09":
        rack = "00-80-A3-9D-86-CF"
elif sys.argv[1] == "A10":
        rack = "00-80-A3-9E-67-27"
elif sys.argv[1] == "A11":
        rack = "00-80-A3-9E-67-34"
elif sys.argv[1] == "A12":
        rack = "00-80-A3-9E-67-35"
elif sys.argv[1] == "B04":
        rack = "00-20-4A-BD-C5-1D"
elif sys.argv[1] == "B05":
        rack = "00-80-A3-9D-86-D2"
elif sys.argv[1] == "B06":
        rack = "00-80-A3-9E-67-3B"
elif sys.argv[1] == "B07":
        rack = "00-80-A3-9E-67-36"
elif sys.argv[1] == "B08":
        rack = "00-80-A3-9E-67-32"
elif sys.argv[1] == "B09":
        rack = "00-80-A3-9D-86-D6"
elif sys.argv[1] == "B10":
        rack = "00-80-A3-9D-86-D3"
elif sys.argv[1] == "B11":
        rack = "00-80-A3-9D-86-D1"
elif sys.argv[1] == "B12":
        rack = "00-80-A3-9D-86-D0"
else:
        print "Invalid Rack number inputted for first argument"

if sys.argv[3] == "record":
        f=open('scriptTest.py', 'a')
        f.write(rack)
        f.write(key)
        f.write('\n')
        f.close()
        get_frame()
        save_frame(get_frame(), "$picture")
        print "Screenshot saved to '$picture'"

else:
        print "Recording parameter not set, not recording"


print rack
print key
slot = "1-16"
#def jKeyPress(rack, key, slot):
#Prepare 3-byte control message for transmission
TCP_IP = '10.23.223.36'
TCP_PORT = 40000
BUFFER_SIZE = 1024
MESSAGE = 'MAC="' + rack + '" dataset="RC71" signal="' + key + '" output="' + slot + '" \n'
#Open socket, send message, close scoket
p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p.connect((TCP_IP, TCP_PORT))
p.send(MESSAGE)
data = p.recv(BUFFER_SIZE)
p.close()
print "Return Data: " + str(data) + key
#jKeyPress("00-80-A3-A9-C3-7A", "menu", "1-16")

