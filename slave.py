import socket                        # Needed to communicate hosts
import time                            # For sleep
import main


class SlaveProgram:
    def __init__(self, a_socket):
        self.obj_list = ["GOOGL","AAPL","IBM","MSFT","TOSBF","SNE","2357.TW",
                         "LNVGY","ITX.MC","SAN","FB","IDR.MC"]
        self._port = 12345                               # Port for communication, private.
        self._connStat = True                            # Connection status
        self._connSock = a_socket                 # Connects with the master
        self._failCounter = 0                     # Counts the number of failed attempts
        
    def initConnection(self):
        self._listSock = socket.socket()
        self._listSock.settimeout(5.0) # Five seconds of timeout
        self._listSock.bind((self._host, self._port))
        self._listSock.listen(5) # Start receiving requests
        
    def doWork(self):
        self._connSock.settimeout(10.0) # Ten seconds timeout
        self._connSock.setblocking(0)        # Non-blocking socket

        while self._connStat is True:     # While there is a Master

            # Receive data from server
            try:
                for i in self._obj_list:
                    self._connSock.send(self._obj_list[i])
                    print "Waiting master..."
                    
                    if(main.wait==False):
                        pass
                    else:
                        myData = self._connSock.recv(1024) 
                        main.wait = False
                        self._objList[0].updateYahooStockQuoteStr(myData)
                        self._failCounter = 0
            except (socket.timeout, socket.error):
                time.sleep(4) # Four seconds of sleep
                self._failCounter += 1
                print self._failCounter
                if self._failCounter == 10:
                    self._connStat = False
                    self._connSock.close()

        # Update objects

        # Update database



        
