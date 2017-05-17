from socket import *
import select, sys


def host():#server protocol, called when hosting a chat
	servPort = int(raw_input('Enter port: '))
	servSocket = socket(AF_INET, SOCK_STREAM)
	servSocket.bind(('', servPort))
	servSocket.listen(1)	#program is one-to-one only
	print 'Waiting for a connection...'
	peerSocket , addr = servSocket.accept()
	resp = 'You are now in a chat with ' + user
	peerSocket.send(resp)
	msg = peerSocket.recv(4096)
	print msg
	
	try: 
		while 1:
			socketList = [sys.stdin, peerSocket]
			read_sockets, write_sockets, error_sockets = select.select(socketList, [], [])
			for sock in read_sockets:
				if sock == peerSocket:
					resp = sock.recv(4096)
					if not resp:	#handles sudden disonnection
						print '\n**you got DISCONNECTED**'
						servSocket.close()
						sys.exit()
						
					else:
						print resp
						sys.stdout.flush()
					
				else:
					msg = raw_input('')
					if msg.lower() == '/quit':	#exit protocol
						peerSocket.send(user + ' left the chat')	#informs peer that user has left
						print '\n**chat closed**'
						servSocket.close
						sys.exit()
						
					peerSocket.send(user + ': ' + msg.rstrip('\n'))	#as per class protocol, all messages must not have a trailing new line
					sys.stdout.flush()
					
	except KeyboardInterrupt:
		print '\n**chat closed**'
		servSocket.close
		sys.exit()
		
				
def client():#client protocol, called when joining a chat
	servName = raw_input('Enter server host: ')
	servPort = int(raw_input('Enter port: '))
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((servName, servPort))
	clientSocket.send('You are now in chat with ' + user)
	
	try:
		while 1:
			sockList = [sys.stdin, clientSocket]
			read_sockets, write_sockets, error_sockets = select.select(sockList, [], [])
	
			for s in read_sockets:
				if s == clientSocket:
					resp = s.recv(4096)
					if not resp:	#handles sudden disconnection
						print '\n**you got DISCONNECTED**'
						clientSocket.close()
						sys.exit()
					else:
						print resp
						sys.stdout.flush()
					
				else:
					msg = raw_input('')
					if msg.lower() == '/quit':	#exit protocol
						clientSocket.send(user + ' left the chat')
						clientSocket.close()
						print '\n**chat closed**'
						sys.exit()
					
					clientSocket.send(user + ': ' + msg.rstrip('\n'))
					sys.stdout.flush()
	

		
	except KeyboardInterrupt:
			clientSocket.close()
			print '\n**chat closed**'
			sys.exit()
	
	
user = raw_input('Username: ')
print 'What would you like to do?\n(1) Host a chat session\n(2) Join a chat session\n(3) Quit'
choice = '0'

while choice not in {'1', '2', '3'}:	#main menu, handles error in choices
	choice = raw_input('>: ')
	if choice == '1':
		host()
	
	elif choice == '2':
		client()
	
	elif choice == '3':
		print 'App closed'
		sys.exit()
	
	else:
		print 'Please input 1, 2, or 3'


