import Functions                                                    #Import from function.py all methods may be needed
import rdt                                                 #To Send/Receive function
import time                                                         #To Calculate time for statistic
import socket
import struct
import sys
import os

start = time.time()                                      #To find the start time

sender_IP = ""                                          #IP address is what the device in have
Sender_port = 6000                                       #Port Number is assigned to 6500

'''Get the IP address, port number, file name from the command-line.'''
UDP_IP = sys.argv[1]                   
UDP_PORT = int(sys.argv[2])                        
fileName = sys.argv[3]
bufferSize = 512                                        #Set to 512. packet size is 512 with sequence number 1 byte, checksum 2 bytes,........... data 500 bytes.
address = (UDP_IP,UDP_PORT)


'''The packet dropping probability and can be set from 0-0.99'''
DropProb = 0.3
print("loss probability: ",DropProb)                                                        


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)                #Socket with IPV4, UDP
sock.bind(("",Sender_port))                                              #Set the sender port to 6000
print("The sender {0}:{1} is sending a message......".format(sender_IP,Sender_port))

"""read the data from file to send"""
file = open(fileName,'rb')                                            #open test file to transfer it to the receiver


'''HandShaking'''
rdt.senderHandShaking(sock,address)

'''Exchange metadata'''
print("[MetaData]")
fileSize = os.path.getsize(fileName)                               
chunk = Functions.chunkTimes(fileSize,bufferSize)                     #Finding the chunks value to many times to transfer the file
chunkBytes = struct.pack("!I", chunk)                                  #Convert chunk from integer to byte to send metadata
print("\tFile has been Extracted \n\tFile size: {0} \n\tNo. of chunk to send the entire file: {1}\n".format(fileSize,chunk))
seqNum = 0                                                            #Sequence Number is set to 0 initially
seqNum = rdt.RdtSendPkt(sock,address,seqNum,chunkBytes)      #sending the file size to Receiver(handshaking)


'''start sending the file in chunks'''
print("\n\n[Data]")
print('File Transfer Starts!')


'''Sending the splitter file chunk to the receiver for chunk times'''
for i in range(0,chunk):                                             
    print("\nChunk :",i+1)                                           
    textPkt = file.read(bufferSize-12)                                        #Read the file for 500 bytes at a time.
    if(i>= (chunk-2)):                                                       #Make sure corruption is not made at last sent chunk, if not sender or receiver waiting for ack/data.
        DropProb=0                                                            #Packet Dropping probability manually set to zero (No corruption) if true.
    seqNum = rdt.RdtSendPkt(sock,address,seqNum,textPkt,DropProb)    #rdtSend to send the packet
    i=i+1                                                                     

file.close()                                                        #File closed
sock.close()                                                        #Socket Closed


''' Calculate statistics '''
end = time.time()                                                  
ElapsedTime = end - start                                        

throughput, delay = Functions.calculate_statistics(fileSize, ElapsedTime)   #Function that calculate the throughput and the delay time

# Print the statistics
print("\nStatistics results: ")
print("\tDelay Time: {:.2f} seconds".format(ElapsedTime))
print("\tThroughput: {:.2f} bytes/second".format(throughput))
