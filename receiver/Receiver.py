import Functions                                                    #Import from function.py all methods may be needed
import rdt                                                          #To Send/Receive function
import time                                                         #To Calculate time for statistic
import socket
import struct

start = time.time()                    #To find the start time

'''Importing IP address, port number, Buffer size'''
UDP_IP = ""                             #IP address is what the device in have
UDP_PORT = 6500                         #Port Number is assigned to 6500
bufferSize = 512                        #bufferSize is set to 512. packet size is 512 with sequence number 1 byte, checksum 2 bytes, data 500 bytes.
addr = ("",UDP_PORT)


'''The packet dropping probability and can be set from 0-0.99'''
DropProb = 0.3                                                              


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)                      #Socket with IPV4, UDP
sock.bind(addr)                                                             #Binding the socket
print("The Receiver {0}:{1} is waiting for a message......".format(addr[0],addr[1]))

'''HandShaking'''
rdt.recHandShaking(sock)


'''Create new file to write the transferred file '''
newFile = open('Received File.txt', 'wb')                                   #opening a new file to copy the transferred text


'''Receiving the metadata'''
print("[MetaData]")
seqNum = 0                                                                 #Sequence Number is set to 0 initially
ChunksTimes,address,seqNum = rdt.RdtReceivePkt(sock,bufferSize,seqNum) 

Chunks= struct.unpack("!I", ChunksTimes)[0]                                     #changing chunks from byte to integer.
print ("Number of chunks to receive the entire file: ", Chunks)


'''Start receiving the data in chunks'''
print("\n\n[Data]")
print('File receive Starts....\n')                            #Start Receiving File from Client.


for i in range(0,Chunks):                                                           #Transferred text packet in the new file.
    print("Chunk :",i+1)                                                   
    if(i>= (Chunks-2)):                                                            #Make sure corruption is not made at last sent chunk, if not sender or receiver waiting for ack/data.
        DropProb=0                                                                 #Packet Dropping probability manually set to zero (No corruption) if true.
    textPkt,address,seqNum = rdt.RdtReceivePkt(sock,bufferSize,seqNum,DropProb)   #Receiving the packet
    newFile.write(textPkt)                                                         #If packet received successful, It writes to the file
    i=i+1                                                                   

'''File Received from Client at the end of Loop'''

ReceivedFileSize = Functions.FileSize(newFile)                                 #Calculating Received text file size

newFile.close()                                                                   #file closed
sock.close()                                                                      #socket closed


'''Statics time delay and file size'''
end = time.time()                                                           
Elapsed_time = end -  start  
print ("Server: File has been Received\n\tReceived File size: {0}".format(ReceivedFileSize))
print("\tTime taken in Seconds: {:.2f}seconds".format(Elapsed_time))

