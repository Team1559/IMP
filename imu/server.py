
import socket
import sys
import thread

host = "10.15.59.6"

port = 23


lock = thread.allocate_lock()


class Server(object):

	def __init__(self):

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.setblocking(1)
		host = socket.gethostname()
		self.s.bind(('',port))
		self.s.listen(5)


	def send(self):
		if self.c == None:
			return
		try:
			self.c.send("h",heading[0],",",heading[1],"z",z,"d",dist,"t",tid)
		except socket.error:
			pass


	def receive(self):
		if self.c == None:
			return
		try:
			r = self.c.recv(1024)
			print r
			return r
		except socket.error:
			pass


	def accept(self):
		try:
			self.c, ref = self.s.accept()
		except socket.error:
			self.c = None


	def close(self):
		if self.c == None:
			return
		self.c.close()


def startServer():
	thread.start_new_thread(run, ())


def run():
	s = Server()
	while 1:
		s.accept()
		#r = s.receive()
		with lock:
			s.send(cx)
			#if(r == "s"):
				#s.send(cx)
		s.close()


def putData(h,zr,d,t): #tid = target id, dist = diagonal distance
	global heading, z, dist, tid #tid-0 is boiler, tid-1 is peg
	with lock:
		heading = h
		z = zr
		dist = d
		tid = t
