import socket                        # Needed to communicate hosts
import sqlite3                    # Needed to access local database
import yahooDataObject    # Needed to access Yahoo data
import time                            # For sleep
import main


class MasterProgram:

    
    def __init__(self):
        self._objList = [yahooDataObject.yahooDataObject('GOOG'), 
                                            yahooDataObject.yahooDataObject('AAPL'),
                                            yahooDataObject.yahooDataObject('IBM'),
                                            yahooDataObject.yahooDataObject('MSFT'),
                                            yahooDataObject.yahooDataObject('TOSHBF'),
                                            yahooDataObject.yahooDataObject('SNE'),
                                            yahooDataObject.yahooDataObject('2357.TW'),
                                            yahooDataObject.yahooDataObject('LNVGY'),
                                            yahooDataObject.yahooDataObject('ITX.MC'),
                                            yahooDataObject.yahooDataObject('SAN'),
                                            yahooDataObject.yahooDataObject('FB'),
                                            yahooDataObject.yahooDataObject('IDR.MC')]
        self._port = 12345                                # Port for communication, private.
        self._slaveConnected = False             # Tells if there is a slave connected
        self._listSock = socket.socket()    # Listener socket
        self._connSock = socket.socket()    # Connection socket
        self._host = socket.gethostname() # Get local machine name
        self._failCounter = 0                            # Counts the number of failed attempts
        

    def initConnection(self):
        self._listSock = socket.socket()
        self._listSock.settimeout(5.0) # Five seconds of timeout
        self._listSock.bind((self._host, self._port))
        self._listSock.listen(5) # Start receiving requests

    def doWork(self):
        conn = sqlite3.connect('tablaProyecto.db') # Create connection
        c = conn.cursor() # Create cursor
        # c.execute('''DROP TABLE IF EXISTS stocks''')        
        c.execute('CREATE TABLE if not EXISTS stocks (symbol text, last text, xdate text, change text, high text, low text, vol text, send text)')

        
        while True:
            # Update database 
            
            
            for obj in self._objList:
                c = conn.cursor()
                obj.updateYahooStockQuoteWeb()
                valores = obj.D
                
                query = 'INSERT INTO stocks (symbol, last, xdate, change, high, low, vol, send) VALUES (:symbol, :last, :date, :change, :high, :low, :vol, 1);'
                c.execute(query, valores)
                print c.fetchall()
                conn.commit()
            
            search = self._connSock.recv(1024)
            # Update data objects
            c = conn.cursor()
            valores = c.execute('SELECT %s FROM stocks', search)
                
        
            # Check for any new connection attempt
            if self._slaveConnected is False:
                try:
                    self._connSock.addr = self._listSock.accept()
                    self._connSock.settimeout(5.0) # Five seconds of timeout
                    self._slaveConnected = True
                    self._connSock.setblocking(0)  # This socket is non-blocking
                    print "Connected to a slave"
                    
                except socket.timeout:
                    self._slaveConnected = False
                    print "Couldnt connect to any slave"

            
            # Send data
            if self._slaveConnected is True:
                try:
                    self._connSock.send(valores)
                    main.wait = True
                    self._failCounter = 0
                    print "Packet sent"
                except (socket.timeout, socket.error):
                    self._failCounter += 1
                    if self._failCounter == 10:
                        self._failCounter = 0
                        self._slaveConnected = False
                        self._listSock.close()    # Restart the socket
                        self._connSock.close()    # Restart the socket
                        self.initConnection()
                        print "Restarting socket"

            conn.close()
        
