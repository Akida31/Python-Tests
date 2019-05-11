import random, time, os, sys
global zahlen
zahlen = ["a", "b", "c", "d", "e", "f"]
global zahlenc
zahlenc = ["a", "b", "c", "d", "e", "f"]
global geld
geld = 100

def eingabe_zahl():
	zahlen = ["", "", "", "", "", ""]
	i = 1
	m = 1
	while i < 6:
		print("Schreibe zwischen zwei Zahlen bitte ein Komma!")
		time.sleep(2.3)
		zahll = input("Auf welche Zahlen willst du tippen?\n") + ","
		zähl = [0, 0]
		for z in zahll:
			if "," == z or "." == z and i < 6:
				if zähl[1] > 0:
					if ((zähl[0]*10 + zähl[1]) < 50):
						zahlen[i] = zähl[0]*10 + zähl[1]
						i = i + 1
						zähl[1] = 0
						zähl[0] = 0
				elif zähl[1] == 0 and zähl[0] > 0:
					zahlen[i] = zähl[0]
					i = i + 1
					zähl[1] = 0
					zähl[0] = 0
			elif i < 6:
				if zähl[0] == 0:
					try:
						zähl[0] = int(z)
					except:
						z = z
				else:
					try:
						zähl[1] = int(z)
					except:
						z = z
			nie = 0
			for mett in zahlen:
				if mett == zahlen[i-1]:
					nie += 1
			if nie > 1:
				zahlen[i-1] = ""
				i -= 5
		print("\n\nFolgende Zahlen sind gewählt:\n" + str(zahlen[0]) + "   " + str(zahlen[1]) + "   " + str(zahlen[2]) + "   " + str(zahlen[3]) + "   " + str(zahlen[4]) + "   " + str(zahlen[5]) + "\n")
		time.sleep(2)
	global geld
	geld -= 1
	auslosung()

def eingabe_regel():
	print("\n\n\nHallo und willkommen zum Lottospiel 6 aus 49!")
	time.sleep(2)
	while True:
		print("\nWARNUNG: ")
		time.sleep(0.6)
		print("Glücksspiel kann süchtig machen!!!")
		time.sleep(2)
		print("\nKennst du die Regeln?")
		time.sleep(1.3)
		regeln = input()
		regeln = regeln.lower()
		if "ja" in regeln:
			time.sleep(1)
			print("Du hast " + str(geld) + " € auf deinem Konto!\n")
			time.sleep(1.4)
			print("Ein Los kostet 5 €")
			time.sleep(1)
			spielen = input("Möchtest du spielen?\n")
			spielen = spielen.lower()
			time.sleep(1)
			while True:
				if "ja" in spielen:
					eingabe_zahl()
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
def auslosung():
	print("Folgende Zahlen sind gezogen worden:")
	time.sleep(1.2)
	immi = 1
	while immi < 7:
		zahlenc[immi - 1] = random.randint(1,49)
		jiih = 0
		for miii in zahlenc:
			if miii == zahlenc[immi-1]:
				jiih += 1
		if jiih > 1:
			zahlenc[immi-1] = ""
			immi -= 1
		else:
			print(zahlenc[immi-1])
			time.sleep(0.7)
		immi += 1
	gewinn()
def gewinn():
	global geld
	richtig = 0
	for us in zahlen:
		if us in zahlenc:
			richtig += 1
			
	if richtig == 0:
		print("\n\nDu hast leider nichts gewonnen!!")
	elif richtig == 3:
		print("Du hast 3 Zahlen richtig getippt und deswegen gewinnst du 20 €")
		geld += 20
	elif richtig == 4:
		print("Du hast 4 Zahlen richtig getippt und deswegen gewinnst du 100 €")
		geld += 100
	elif richtig == 5:
		print("Du hast 5 Zahlen richtig getippt und deswegen gewinnst du 5.000 €")
		geld += 5000
	elif richtig == 6:
		print("\n\nDu hast alle Zahlen richtig getippt!!!\nDu gewinnst den Jackpot mit 1.000.000 € Gewinn!")
		time.sleep(2)
		print("Herzlichen Glückwunsch!!!")
		time.sleep(2)
		print("")
		geld += 1000000
	while True:
		apis = input("Möchtest du noch ein Spiel spielen?\n")
		if "ja" in apis:
			time.sleep(2)
			eingabe_regel()
		elif "nein" in apis:
			sys.exit()
		else:
			time.sleep(1.3)
			print("Das war leider zu undeutlich. :)")
			time.sleep(1)
	

eingabe_regel()
