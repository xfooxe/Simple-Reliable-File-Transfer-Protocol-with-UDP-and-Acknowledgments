import Functions

''' RDT function from Receiver to receiver the file.'''
def RdtReceivePkt (sock,bufferSize,seqNum2,P_Drop=0):
    receiveSuccess = 0                                                                  
    while (not(receiveSuccess)):                                                        

        data, address = sock.recvfrom(bufferSize+100)                                       #Packet has been received from the Sender
        if (Functions.lossProbability(P_Drop)):                                             #If lossProbability is true, it starts to Drop packet intentionally.
            print ("DATA PACKET DROPPED\n")
            receiveSuccess=0                                                              

        else:                                                                               #If lossProbability is False, then no dropped packet.
            seqNum,checksum,dataPkt=Functions.unpackData(data)                            


            checksum2 = Functions.checksum(dataPkt)                                      

            if ((checksum2 == checksum) and (seqNum == seqNum2)):                           #if packet did not loss and has the correct and expect seqNum then sends Ack with new seqNum 
                    Ack = seqNum2                                                           
                    Ack = b'ACK' + str(Ack).encode("UTF-8")                                 
                    SenderAck = Functions.MakePkt("6500",address[1],seqNum,Functions.checksum(Ack),Ack,"ACK")     #receiver sends SeqNum, checksum, Ack
                    print("\tSequence Number: {0}\n\tReceiver sequence: {1}\n\tChecksum from Sender: {2}\n\tChecksum for Received File: {3}\n".format(seqNum,seqNum2,checksum,checksum2))
                    seqNum2 = 1-seqNum                                                      #update seqNum for next iteration.
                    receiveSuccess = 1                                                  

            elif ((checksum2 != checksum) or (seqNum != seqNum2)):                          #if packet did loss  or has wrong seqNum then sends ack with previous seqNum that will lead the sender to resend the packet.
                    Ack = 1 - seqNum2                                                       
                    Ack = b'ACK' + str(Ack).encode("UTF-8")                                 
                    SenderAck = Functions.MakePkt("6500",address[1],1 - seqNum2,Functions.checksum(Ack),Ack,"ACK")   #Receiver sends SeqNum, checksum, Ack
                    print("\Receiver Requested to Resend the Packet")
                    print("\n\tSequence Number: {0}\n\tReceiver sequence: {1}\n\tChecksum from Sender: {2}\n\tChecksum for Received File: {3}\n".format(seqNum,seqNum2,checksum,checksum2))
                    receiveSuccess = 0  
            
            sock.sendto(SenderAck,address)                                                 #sending Ack packet to the sender

    return dataPkt,address,seqNum2                                                       



def senderHandShaking(sock,receiver_address):
        
    # Send the SYN message to the receiver
    sock.sendto(b'SYN', receiver_address)

    # Receive the SYN-ACK message from the receiver
    data, receiver_address = sock.recvfrom(1024)
    if data == b'SYN-ACK':
        print("[HandShaking]")
        print("\tReceived SYN-ACK from", receiver_address)
        print()

        # Send the ACK message to the receiver
        sock.sendto(b'ACK', receiver_address)

        # Start the file transfer process
        # ...
    else:
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