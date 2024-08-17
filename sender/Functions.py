import math
import random
import struct

'''  This function gets the file size '''
def FileSize(file):
    file.seek(0,2)                                                  #Moves the file pointer to the end of the file
    fileSize = file.tell()                                          #gets file size
    file.seek(0,0)                                                  #Moves the file pointer the the beginning of the file
    return fileSize                                                 


''' This function gets how many chunk the program need to transfer the file '''
def chunkTimes(fileSize, bufferSize):
    ChunkTimes = (fileSize / (bufferSize-12))                       #Filesize is divided by bufferSize (512-12) 12 bytes is the headers for the packet
    chunk = math.ceil(ChunkTimes)                                    
    return (chunk)                                                   


'''This function updates the sequence number from and to 0 or 1'''
def UpdateSeqNum(seqNum):
    return 1-seqNum                                                


'''This function find the Checksum of the data'''
def checksum(data):
    checksum = 0                                             
    for i in range(0,len(data),2):                                  #Loop starts from 0 to data length for 2 times.
        first2bits = data[i : (i+2)]                                #taking 16 bits (2 bytes) value from 512 bytes
        if len(first2bits) == 1:
            twoByteInteger = struct.unpack("!B",first2bits)[0]       #If len(data)=1 it has to be unpacked with standard size 1
        elif len(first2bits) == 2:
            twoByteInteger = struct.unpack("!H",first2bits)[0]       #If len(data)=2 it has to be unpacked with standard size 2
        checksum = checksum + twoByteInteger                         #checksum addition
        while (checksum>>16)==1:                                     #loop goes on until condition becomes 'false'
            checksum = (checksum & 0xffff) + (checksum >>16)         #Wrapup function
    return checksum                                                  #returns checksum for the data in integer


'''This function finds id the drop loss has to be done or not'''
def lossProbability(DropProb=0):
    DataLoss = False                                                #DataLoss has been initial as 'False'
    Random_Num = random.random()                                    #This generates a random probability value (0.00 to 1.00)
    if (Random_Num < (DropProb)):                                 
        DataLoss = True                                             #If condition is 'True' it corrupts data
    return DataLoss                                           


'''This Function makes packet (source port : destination port : Sequence number : checksum : header size : data size : packet type : data -> together forms a packet)'''
def MakePkt(source,dest,seqNums,chksums,data,typeData):
    if typeData=="Data":
        packetType=1
    elif typeData=="Handshaking":
        packetType=2
    elif typeData=="ACK":
        packetType=3
    headerSize=12
    dataSize=len(data)
    packet_header = f"{source}:{dest}:{chksums}:{seqNums}:{headerSize}:{dataSize}:{packetType}".encode()     #pack the header components between each one ":"
    packet = packet_header +b":"+ data                                                               
    return struct.pack(""+str(len(packet))+"s",packet)                                               #Pack header + data to transfer the packet


'''This Function Extracts Sequence number,checksum, data from packet'''
def unpackData(packet):
    packet = struct.unpack(""+str(len(packet))+"s", packet)             
    packet_data = packet[0].split(b":", 7)                          #split the packet components 
    chcksum = packet_data[2]
    sequence_number = packet_data[3]
    data = packet_data[7]
    return int(sequence_number.decode()),int(chcksum.decode()),data         #return the sequence number, checksum , data 



''' Function to calculate throughput and delay statistics'''
def calculate_statistics(file_size, transfer_time):
    throughput = file_size / transfer_time
    delay = transfer_time / file_size
    return throughput, delay


