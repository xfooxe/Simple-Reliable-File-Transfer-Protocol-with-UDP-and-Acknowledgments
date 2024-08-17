import Functions
import time
import socket

''' RDT function from Sender to send the file.'''
def RdtSendPkt(udpSock,addr,SeqNum,data,DropProb=0):
    sendSuccess = False                                                                                    
    packet = Functions.MakePkt("6000",addr[1],SeqNum,Functions.checksum(data),data,"Data") #Packet is created with the sequence number,checksum,data


    while (not(sendSuccess)):                                                           

        udpSock.sendto(packet,addr)                                                        #sending the packet to receiver
        print ("Sending the Packet...")
        startTime = time.time()                                                            # timer started
        
        
        udpSock.settimeout(1)                                                               #timeout after 1 second
        try:                                                                                
            print ("\tStart Timer")
            AckPkt,addr = udpSock.recvfrom(512)                                             #Sender received Ack packet
            udpSock.settimeout(None)                                                        #timer only for receive function 

            if (Functions.lossProbability(DropProb)):                                       #If lossProbability is true, it starts to Drop packet intentionally.
                print ("\tACKNOWLEDGEMENT PACKET DROPPED !!!")
                while(time.time() < (startTime + 1)):                                       #wait for approximately 1 second before retransmission. 
                            pass 
                print ("\tTIMED OUT !!! \n")
                sendSuccess = False                                                         

            else:                                                                           #If lossProbability is False, then no dropped packet.
                seqNmbr,senderChecksum,ackData=Functions.unpackData(AckPkt)            


                refrenceAck ="ACK"+str(SeqNum)                                              #Ack with equal to the sequence number.
                AckChecksum = Functions.checksum(ackData)                                 
                ackData = ackData.decode("UTF-8")                                      

                '''Comparing Ack''' 
                if (ackData != refrenceAck) or (AckChecksum != senderChecksum ):            #resend packet
                        print ("\tAck: {0}\n\tsequence number: {1}".format(ackData,SeqNum))
                        print("Resending the Packet")
                        sendSuccess = False                                                 #Resend the packet until success.
                        while(time.time() < (startTime + 0.03)):                            #wait little time
                            pass
                        print ("\tTIMED OUT 2!!! \n")


                elif (ackData == refrenceAck) and (AckChecksum == senderChecksum ):        #if packet did not being loss and has had ack then the send message has been done successfully 
                        print ("\tAck: {0} \n\tsequence number: {1}".format(ackData,SeqNum))
                        SeqNum = 1-SeqNum                                                  
                        sendSuccess = True                                                 
                        print ("\tStop Timer")

        except(socket.timeout):
            print ("\tTIMED OUT !!! \n")
            sendSuccess=False                                                               #exception after 1 second.

    return SeqNum                                                                         


def senderHandShaking(sock,receiver_address):
    succ = False
    while(not(succ)):
        # Send the SYN message to the receiver
        sock.sendto(b'SYN', receiver_address)
        sock.settimeout(1)
        try:
            
            # Receive the SYN-ACK message from the receiver
            data, receiver_address = sock.recvfrom(1024)
            sock.settimeout(None) 
            if data == b'SYN-ACK':
                print("[HandShaking]")
                print("\tReceived SYN-ACK from", receiver_address)
                print()

                # Send the ACK message to the receiver
                sock.sendto(b'ACK', receiver_address)
                succ=True

                # Start the file transfer process
                # ...
        except(socket.timeout):
            print("Invalid handshake message")
            exit()


def recHandShaking(sock):
            
    # Receive the SYN message from the Sender
    data, address = sock.recvfrom(1024)
    print("[HandShaking]")

    if data == b'SYN':
        print("\tReceived SYN from", address)

        # Send the SYN-ACK message to the sender
        sock.sendto(b'SYN-ACK', address)

        # Wait to receive the ACK message from the sender
        data, address = sock.recvfrom(1024)
        if data == b'ACK':
            print("\tReceived ACK from", address)
            print()
            # Start the file transfer process
            # ...
    else:
        print("Invalid handshake message")