import time, os, sys, random
try:
	joh = open("quiz.py", "r")
	read_text = ""
	for kohl in joh:
		if "numberofquestions" in kohl:
			read_text = kohl[28]
	joh.close()
except:
	print("ERROR 271")
	time.sleep(0.5)
	print("Datei  nicht vorhanden!")
	sys.exit()
print("Willkommen im Bearbeitungsmodus für das Quizspiel von Fusion\n")
time.sleep(2)
frage = input("Wie heißt deine Frage?\n")
time.sleep(0.8)
antworta = input("\nAntwort a:\n")
time.sleep(0.8)
antwortb = input("\nAntwort b:\n")
time.sleep(0.8)
antwortc = input("\nAntwort c:\n")
time.sleep(0.8)
antwortd = input("\nAntwort d:\n")
time.sleep(0.8)
i = 0
while i == 0:
	richtig = input("\nRichtige Antwort?\n")
	if richtig == "a" or richtig == "b" or richtig == "c" or richtig == "d":
		i = 1
	else:
		print("Das ist keine Antwort!")
		time.sleep(1)
		print("Nimm dieses Erstellen ernst!")
		time.sleep(2)

try:
	opn = open("version1.py", "a")
	opn.write('\n        question.append("' + frage +'")')
	opn.write('\n        answera.append("' + antworta +'")')
	opn.write('\n        answerb.append("' + antwortb +'")')
	opn.write('\n        answerc.append("' + antwortc +'")')
	opn.write('\n        answerd.append("' + antwortd +'")')
	opn.write('\n        right.append("' + richtig +'")')
	read_text = str(int(read_text) + 1)
	opn.write('\n        numberofquestions' + ' = ' + read_text)
	opn.close()
	time.sleep(2)
	print("\nFrage wurde erfolgreich hinzugefügt!")
except:
    print("ERROR 178")
    time.sleep(1)
    print("Datei kann nicht beschrieben werden!")
