from socket import *
from datetime import datetime
import select, sys
	
def broadcast(sock, msg):#send to all except server and sender
	for s in connections:
		if s != servSocket and s != sock:
			try:
				s.send(msg.rstrip('\n'))
			except:
				s.close()
				connections.remove(s)
				del usernames[s]
				del userData[s]

def command(msg, sock):
	commands = ['quit', 'name', 'whois', 'time', 'help']
	cmdLine = msg[1:].split()
	cmdLine[0] = cmdLine[0].lower()
	
	if cmdLine[0] in commands:
		if cmdLine[0] == 'name':
			nameHolder = usernames[sock]
			if cmdLine[1] in usernames.values():
				resp = 'SERVER: ' + cmdLine[1] + ' is already in use'
				sock.send(resp.rstrip('\n'))
				
			else:
				usernames[sock] = cmdLine[1]
				resp = '**' + nameHolder + ' changed their username to ' +cmdLine[1] + '**' 
				broadcast(sock, resp)
			
		elif cmdLine[0] == 'help':
			for i in commands:
				resp = ' /' + i
				sock.send(resp)
	
		elif cmdLine[0] == 'time':
			resp = 'SERVER: [%s:%s:%s.%s]' % (datetime.now().hour, datetime.now().minute, datetime.now().second, datetime.now().microsecond)
			sock.send(resp.rstrip('\n'))
			
		elif cmdLine[0] == 'quit':
			connections.remove(sock)
			resp = '**' + usernames[sock] + ' is now OFFLINE**'
			broadcast(sock, resp)
			del usernames[sock]
			del userData[sock]
			sock.close()
			
		elif cmdLine[0] == 'whois':
			if cmdLine[1] in usernames.values():
				for s in usernames:
					if usernames[s] == cmdLine[1]:
						resp = 'SERVER: ' + cmdLine[1] + ' is ' + str(userData[s]) 
						sock.send(resp.rstrip('\n'))
						
			else:
				resp = cmdLine[1] + ' is not connected to this server'
				sock.send(resp.rstrip('\n'))
			
		else:
			resp = 'functionality not available'
			sock.send(resp.rstrip('\n'))
			
	else:
		resp = '**command not recognized**'
		sock.send(resp.rstrip('\n'))

servPort = int(raw_input('Enter port: '))
servSocket = socket(AF_INET, SOCK_STREAM)
servSocket.bind(('', servPort))
servSocket.listen(10)
print 'Server is ready on port ' + str(servPort)

connections = []
usernames = {}
userData = {}

connections.append(servSocket)


try:
	while 1:
		read_sockets, write_sockets, error_sockets = select.select(connections, [], [])
	
		for s in read_sockets:
			if s == servSocket:
				connSock, addr = servSocket.accept()
				connections.append(connSock)
				usernames[connSock] = str(addr)
				userData[connSock] = addr
				resp = '**[%s | %s] is now ONLINE**' % addr
				connSock.send('SERVER: You are now connected to the chat server\ntype /help for a list of usable commands')
				broadcast(connSock, resp)
			
			else:
				try:
					msg = s.recv(4096)
					if msg:
						if msg == '/':
							s.send('SERVER: usage is /<command>')	
						elif msg[0] == '/':
							command(msg, s)
						else:
							resp =  '%s: %s' % (usernames[s], msg)
							print resp
							broadcast(s, resp)
					
				except:
					resp = '**[%s | %s] is now OFFLINE**' % userData[s]
					broadcast(s, resp)
					s.close()
					connections.remove(s)
					del usernames[s]
					del userData[s]
					continue
					
except KeyboardInterrupt:
	servSocket.close()
	print '\n**server closed**'
	sys.exit()
