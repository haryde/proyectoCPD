import urllib2    #Needed to access Yahoo webpage

class yahooDataObject:
    """ Class to get values from Yahoo in different formats """

    """ Object constructor """
    def __init__(self, a_symbol):
        
        # Name of the object. Defines where to search
        self.symbol = a_symbol 
        # String formated data
        self.s = ""
        # Dictionary formated data
        self.D = {}

        self.updateYahooStockQuoteWeb()

    """ Returns a string, containing the values obtained from Yahoo """
    """ Also returns a dict, suitable to easily insert it in the DB """
    def updateYahooStockQuoteWeb(self):
        url = "http://download.finance.yahoo.com/d/" \
        "quotes.csv?s=%s&f=sl1d1c1hgvt" % self.symbol
    
        f = urllib2.urlopen(url)
        s = f.read() 
        f.close()

        s = s.strip() # Convierte 'f' en caracteres  
        self.s = s.replace('"','') # Reemplaza las dobles comillas

        try:
            L = self.s.split(',') # Reemplaza los espacios por ','
        
            self.D['symbol'] = L[0]
            self.D['last'] = L[1]
            self.D['date'] = L[2]
            self.D['change'] = L[3]
            self.D['high'] = L[4]
            self.D['low'] = L[5]
            self.D['vol'] = L[6]
            self.D['time'] = L[7]
        except IndexError:
            self.D = {}

    """ Updates the object data using a string value """
    def updateYahooStockQuoteStr(self, string):

        self.s = string
        try:
            L = self.s.split(',')
        
            self.D['symbol'] = L[0]
            self.D['last'] = L[1]
            self.D['date'] = L[2]
            self.D['change'] = L[3]
            self.D['high'] = L[4]
            self.D['low'] = L[5]
            self.D['vol'] = L[6]
            self.D['time'] = L[7]
        except IndexError:
            self.D = {}
        

# Google, Apple, IBM, Microsoft, Toshiba Corp., Sony Corp., AsusTek Inc., Lenovo, Inditex, Banco Santander, Facebook, Indra Sistemas
