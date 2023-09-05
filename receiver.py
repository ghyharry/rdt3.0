#!/usr/bin/env python

import socket
import sys
import checksum
import time
from datetime import datetime

def main(argv): 
  TCP_IP = 'gaia.cs.umass.edu'
  TCP_PORT = 20000
  BUFFER_SIZE = 1024
  ID=argv[1]
  loss=argv[2]
  corrupt=argv[3]
  maxd=argv[4]

  now = datetime.now()
  print("Haoyu Guan "+str(now))
  message = "HELLO R "+loss+" "+corrupt+" "+maxd+" "+ID

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
    ack="1"
    
    ttpack=0
    ttmsg=""
    ttrec=0
    ttcor=0
    cout=0
    datarecieve=False
    while(len(ttmsg)<200 and cout<100):
      cout+=1
      try:
        s.settimeout(20)
        data = s.recv(30).decode()
        
        if(len(data)<5):
          break
      except socket.timeout:
        break
      
      ttrec+=1
      if(checksum.checksum_verifier(data)):
        datarecieve=True
        seq=data[0]
        if(ack!=seq):
          word=data[4:24]
          ttmsg+=word
        ack=seq
      else:
        ttcor+=1
        datarecieve=False
        c="                    "
        msg="  "+ack+" "+c+" "
        
        check=checksum.checksum(msg)
        msg=msg+check
        
        s.send(msg.encode())
        
        ttpack+=1
      if (datarecieve):
        

        c="                    "
        msg="  "+ack+" "+c+" "
        
        check=checksum.checksum(msg)
        msg=msg+check
        
        s.send(msg.encode())
        
        ttpack+=1
      

    now = datetime.now()
    print(ttmsg)
    print("Haoyu Guan "+str(now)+" "+checksum.checksum(ttmsg))
    print("total number of packets sent "+str(ttpack)+"\ntotal number of packets received "+str(ttrec)+"\nnumber of times a corrupted message was received "+str(ttcor))
  
  
  
  

  time.sleep(5)
  s.close()

  

if __name__ == "__main__":
  main(sys.argv)