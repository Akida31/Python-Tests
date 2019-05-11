import random, time,sys
class Lotto():
    def __init__(self):
        self.zahlen = []
        self.geld = 100

    def eingabe_zahl(self):
        print("Schreibe zwischen zwei Zahlen bitte ein Komma!")
        time.sleep(2.3)
        input_zahl = input("Auf welche Zahlen willst du tippen?\n")
        zahl_list = input_zahl.replace(' ','').split(',')
        if len(zahl_list) == 1:
            zahl_list = input_zahl.split(' ')
        for zahl in zahl_list:
            try:
                if int(zahl) not in self.zahlen and 0 < int(zahl) < 50:
                    self.zahlen.append(int(zahl))
            except:
                    pass
        zahlstring = ""
        self.zahlen = sorted(self.zahlen[:6])
        for zahl in self.zahlen:
            zahlstring += "  " + str(zahl)
        print("\n\nFolgende Zahlen sind gewählt:\n" + zahlstring + "\n")
        time.sleep(2)
        if len(self.zahlen) < 6:
            self.eingabe_zahl()
        self.geld -= 5
        self.auslosung()

    def eingabe_regel(self):
        print("\n\n\nHallo und willkommen zum Lottospiel 6 aus 49!")
        time.sleep(2)
        while True:
            print("\nWARNUNG: ")
            time.sleep(0.6)
            print("Glücksspiel kann süchtig machen!!!")
            time.sleep(2)
            print("\nKennst du die Regeln?")
            time.sleep(1.3)
            regeln = input().lower()
            if "ja" in regeln:
                time.sleep(1)
                print("Du hast " + str(self.geld) + " € auf deinem Konto!\n")
                time.sleep(1.4)
                print("Ein Tippschein kostet 5 €")
                time.sleep(1)
                spielen = input("Möchtest du spielen?\n")
                spielen = spielen.lower()
                time.sleep(1)
                while True:
                    if "ja" in spielen:
                        self.eingabe_zahl()
                    elif "nein" in spielen:
                        sys.exit()
                    else:
                        print("Das konnte ich nicht verstehen!")
            elif "nein" in regeln:
                print("\n\nRegeln:")
                time.sleep(1)
                print("Du kannst in das Feld 6 Zahlen eintippen.")
                time.sleep(2)
                print("Diese Zahlen sind dann \"gesetzt\".")
                time.sleep(2)
                print("Der Computer erwürfelt durch Zufall auch 6 Zahlen.")
                time.sleep(1.8)
                print("Je mehr Zahlen übereinstimmen, desto höher der Gewinn!")
                time.sleep(2.3)
                print("\n           Die Gewinnquoten + Preisgelder sind:")
                time.sleep(3)
                print("6 Richtige: 1 zu 15.537.573  1.000.000 €")
                time.sleep(3)
                print("5 Richtige: 1 zu 60.223      5.000 €")
                time.sleep(3)
                print("4 Richtige: 1 zu 1.147       100 €")
                time.sleep(3)
                print("3 Richtige: 1 zu 63          20 €\n")
                time.sleep(4)
                
            else:
                time.sleep(1.2)
                print("Deine Antwort war leider zu unklar!")

    def auslosung(self):
        print("Folgende Zahlen sind gezogen worden:")
        time.sleep(1.2)
        zahlen_gelost = []
        while len(zahlen_gelost) < 6:
            zahl = random.randint(1,49)
            if zahl not in zahlen_gelost:
                zahlen_gelost.append(zahl)
                print(zahl)
                time.sleep(0.5)
        richtig = 0
        for zahl in self.zahlen:
            if zahl in zahlen_gelost:
                richtig += 1
			
        gewinn = [0,0,0,20,100,5000]
        if richtig < 4:
            print("\n\nDu hast leider nichts gewonnen!!")
        elif richtig == 6:
            print("\n\nDu hast alle Zahlen richtig getippt!!!\nDu gewinnst den Jackpot mit 1.000.000 € Gewinn!")
            time.sleep(2)
            print("Herzlichen Glückwunsch!!!")
            time.sleep(2)
            self.geld += 1000000
        else:
            print("Du hast {} Zahlen richtig getippt und deswegen gewinnst du {} €".format(richtig,gewinn[richtig]))
            self.geld += gewinn[richtig]
        self.again()

    def again(self):
        while True:
            apis = input("Möchtest du noch ein Spiel spielen?\n")
            if "ja" in apis:
                time.sleep(2)
                self.eingabe_regel()
            elif "nein" in apis:
                quit()
            else:
                time.sleep(1.3)
                print("Das war leider zu undeutlich. :)")
                time.sleep(1)
	
if __name__ == "__main__":
    lotto = Lotto()
    lotto.eingabe_regel()
