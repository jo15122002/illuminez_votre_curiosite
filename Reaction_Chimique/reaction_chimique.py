import time
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard import Exceptions
from smartcard.System import readers
from smartcard.CardConnection import CardConnection
from smartcard.Card import Card

class MyObserver(CardObserver):
    def __init__(self):
        self.cards = []
        self.scannedCards = []
        self.rightPairs = ["169E4059", "B66640C1"]

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.cards.append(card)
    
    def checkPairs(self):
        if set(self.scannedCards) == set(self.rightPairs):
            return "Bravo !"
        else:
            return "Raté !"

    def get_uid(self):
        connection = readers()[0].createConnection()
        connection.connect()
        uid_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        uid_response, sw1, sw2 = connection.transmit(uid_command)
        uid = toHexString(uid_response).replace(" ", "")
        return uid

if __name__ == '__main__':
    cardmonitor = CardMonitor()
    observer = MyObserver()
    cardmonitor.addObserver(observer)

    while(True):
        print("Attente d'une carte...")

        while not observer.cards:
            time.sleep(0.1)

        card = observer.cards[0]
        observer.cards = []

        #print(observer.get_uid())

        uid = observer.get_uid()
        
        #uid = toHexString(card.atr)
        observer.scannedCards.append(uid)

        #print("Len : " + str(len(observer.scannedCards)))

        if(len(observer.scannedCards) == 2):
            #print("2 cartes scannées !")
            print(observer.checkPairs())
            observer.scannedCards = []
        
        print("Carte détectée : " + uid)
