#!/usr/bin/env python

import socket
import sys
import checksum
from datetime import datetime

def main(argv): 
  TCP_IP = 'gaia.cs.umass.edu'
  TCP_PORT = 20000
  BUFFER_SIZE = 1024
  ID=argv[1]
  loss=argv[2]
  corrupt=argv[3]
  maxd=argv[4]
  tout=argv[5]
  
  now = datetime.now()
  print("Haoyu Guan "+str(now))
  message = "HELLO S "+loss+" "+corrupt+" "+maxd+" "+ID

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((TCP_IP, TCP_PORT))
  s.send(message.encode())
  data = s.recv(BUFFER_SIZE).decode()
  message=data.split()
  while(message[0]=="WAITING"):
    data = s.recv(BUFFER_SIZE).decode()
    message=data.split()
  if (message[0]=="ERROR"):
    print(data)
  if (message[0]=="OK"):
    now = datetime.now()
    print(str(now)+" channel has been established.")
    seq="0"
    f = open("./declaration.txt", "r")
    ttpack=0
    ttmsg=""
    ttrec=0
    ttcor=0
    touttime=0
    for i in range(0,10):
      c=f.read(20)
      msg=seq+" 0 "+c+" "
      ttmsg=ttmsg+c
      check=checksum.checksum(msg)
      msg=msg+check
      datarecieve=False
      gosend=True
      while (not datarecieve):
        if (gosend):
          s.send(msg.encode())
          
          
          ttpack+=1
        try:
          s.settimeout(float(tout))
          data = s.recv(30).decode()
          ttrec+=1
          
          if(checksum.checksum_verifier(data)):
            datarecieve=True
            
            ack=data[2]
            if (ack!=seq):
              datarecieve=False
              gosend=False
          else:
            ttcor+=1
            datarecieve=False
            gosend=False
          if(datarecieve and (seq=="0")):
            seq="1"
          elif(datarecieve and (seq=="1")):
            seq="0"  
        except socket.timeout:
          gosend=True
          touttime+=1
          datarecieve=False
          
    now = datetime.now()
    print(ttmsg)
    print("Haoyu Guan finish at "+str(now)+" file checksum: "+checksum.checksum(ttmsg))
    print("total number of packets sent "+str(ttpack)+"\ntotal number of packets received "+str(ttrec)+"\nnumber of times a corrupted message was received "+str(ttcor)+"\nnumber of timeouts "+str(touttime))
  
  
  
  
  s.close()

  

if __name__ == "__main__":
  main(sys.argv)