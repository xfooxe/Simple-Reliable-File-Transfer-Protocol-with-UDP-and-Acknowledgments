# Simple-Reliable-File-Transfer-Protocol-with-UDP-and-Acknowledgments

To set up a network between hosts and test the code:
1. Determine the network configuration: connect the hosts using wi-fi (may use localhost or ethernet).
2. Assign IP addresses and port numbers: Assign IP addresses so that the machine can figure it out. Assign a port number 6000 for the sender and 6500 for the receiver that will be used forthe communication. The sender will write in the command line the IP address and port number  of the receiver and the filename.
3. Split the file into 500-bit for file data and 12 for the header. Assign a sequence number to each packet to ensure that the receiver can reassemble the file correctly.
4. Configure packet dropping probability: Determine the packet dropping probability, which determines the likelihood of dropping a packet during transmission. We will assume that it is  0 , 0.1 , 0.3 loss probability for both the sender and receiver and another scenario when sender only is 0.6. also when receiver only in 0.6.
5. Firstly output handshaking mechanism, ensuring that both the sender and receiver follow the same protocol.
6. New file will be created in receiver device where the received data will be written. 
7. The sender has transmitted metadata about the file being sent, with the file size contains number of chunks(each chunk is 500byte). 
8. Break the file into smaller chunks and send them sequentially from the sender to the receiver. In the receiver code, ensuring that the data chunks are received with correct sequence numberand written to the new file correctly and check for ack loss or packet loss.
9. Measure time delay and file size: measure the time delay between sending and receiving data. And calculate the size of the transferred file


![image](https://github.com/user-attachments/assets/46b0b34a-68c3-4992-bfee-2d1448fe3d33)

![image](https://github.com/user-attachments/assets/a782e14b-61c5-4b43-b9dd-88d430a728f6)

![image](https://github.com/user-attachments/assets/5477c41f-ccd1-405e-a13b-9a1870cc13fa)

![image](https://github.com/user-attachments/assets/51278a72-e674-4216-a313-8dd1198ce7ee)



