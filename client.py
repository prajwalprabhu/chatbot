import socket
import json
import threading
from time import sleep
c=socket.socket()
name=input("Enter Your Name")
ip=socket.gethostname()

message="""
		{
		"info":{
		"name":"",
		"IP":""

		},
		"message":"Connected"
		}

		"""


data=json.loads(message)
data["info"]["name"]=name
data["info"]["IP"]=ip
str_data=json.dumps(data)

def send(conn):
	while 1:
		
		global data
		msg=input("Your message")
		if not msg=='':
			data["message"]=msg
			
			str_data=json.dumps(data)
			conn.send(str_data.encode())


def listen(conn):
	while 1:
		data=conn.recv(1024).decode()
		if not len(data)==0:
			
			sdata=json.loads(data)
			name=sdata["info"]["name"]
			msg=sdata["message"]
			print(f"\n{name} : {msg}")





c.connect(('localhost',9999))
c.send(str_data.encode())
sleep(1)
c.send(str_data.encode())
listen=threading.Thread(target=listen,args=[c])
listen.start()
send=threading.Thread(target=send,args=[c])
send.start()
