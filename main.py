#!/bin/python2.7

import slave
import master
import socket

def testRole():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for send
    try:
        s.connect((host, port)) # Connet the socket
        return s
    except socket.error:
        print "Couldn't find a server"
        return False
""" ########## The main py starts here ######### """

""" First thing to do is check if initializate the connection """
wait = False

role = testRole()

if role is not False: # If it's a slave
    print "I'm a slave"
    prog = slave.SlaveProgram(role)
    prog.initConnection()
    prog.doWork()
#    print "Becoming a master"

print "I'm a master"
prog = master.MasterProgram()
prog.initConnection()
prog.doWork()
