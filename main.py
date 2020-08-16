import socket
import threading
import json
from time import sleep
s=socket.socket()
s.bind(('localhost',9999))
s.listen()
IP=socket.gethostname()
conn_list=[]
conn_name={}
def listen(conn,addr):
	while 1:
		
		print(type(conn))
		data=conn.recv(1024).decode()
		jdata=json.loads(data)
		msg=jdata["message"]

		for connn in conn_list:
			sdata=json.dumps(jdata)
			if not connn==conn:
				connn.send(sdata.encode())
		if msg=="!DISCONNECT":
			conn.close()
			i=conn_list.index(conn)
			conn_list.pop(i)
			quit()



def client_handle(conn,addr):
	conn=conn
	data=conn.recv(1024).decode()
	data=json.loads(data)
	name=data["info"]['name']
	conn_name[name]=conn
	data=json.dumps(data)
	
	listen_thread=threading.Thread(target=listen,args=[conn,addr])
	listen_thread.start()
	

def start(s):
	while 1:
		print("[STARTING SERVER]")
		sleep(1)
		print(f"[STARTED] In {IP}")
		conn,addr=s.accept()
		conn_list.append(conn)
		print(f"[CONNECTED]:{addr}")
		client_thread=threading.Thread(target=client_handle,args=[conn,addr])
		client_thread.start()
start(s)
