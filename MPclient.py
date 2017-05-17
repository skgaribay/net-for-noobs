from socket import *
import select, sys
servName = raw_input('Enter server host: ')
servPort = int(raw_input('Enter port: '))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servName, servPort))
clientSocket.settimeout(2)

	
try:
	while 1:
		sockList = [sys.stdin, clientSocket]
		read_sockets, write_sockets, error_sockets = select.select(sockList, [], [])
	
		for s in read_sockets:
			if s == clientSocket:
				resp = s.recv(4096)
				if not resp:
					print '**you got DISCONNECTED**'
					clientSocket.close()
					sys.exit()
				else:
					print resp
					sys.stdout.flush()
					
			else:
				msg = raw_input('')
				clientSocket.send(msg)
				sys.stdout.flush
				if msg.lower() == '/quit':
					clientSocket.close()
					print 
					print '**client closed**'
					sys.exit()

		
except KeyboardInterrupt:
	clientSocket.send('/quit')
	clientSocket.close()
	print
	print '**client closed**'	
	sys.exit()
		

		
