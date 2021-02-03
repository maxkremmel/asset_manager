#Wertpapier Klasse
class Security:
    
    def __init__(self, ISIN, bdate, num, curPrice, name):
        self.ISIN = ISIN
        self.bdate = bdate
        self.num = num
        self.curPrice = curPrice
        self.name = name
    
