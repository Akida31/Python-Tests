

import time, os, sys, random
def vokabeln():
    datei = input("\nWelche Lektion möchtest du lernen?\n")
    datei = "L" + datei
    try:
        xk = open(datei, "r")
    except:
        print("ERROR. File does not exist!")
        sys.exit()

    anzahl = 1
    wortart = [""] * anzahl
    lat = [""] * anzahl
    stern = [""] * anzahl
    plus = [""] * anzahl
    apostro = [""] * anzahl
    minus = [""] * anzahl
    frg1 = [""] * anzahl
    frg2 = [""] * anzahl
    frg3 = [""] * anzahl
    frg4 = [""] * anzahl

    nummer = 0


    for linie in xk:
        
    ##    if wortart[nummer] == "" and lat[nummer] == "" and stern[nummer] == "" and plus[nummer] == "" and apostro[nummer] == "" and minus[nummer] == "" and frg1[nummer] == "":
    ##        nummer += 0
    ##    else:
    ##        nummer += 1
        if linie[0] == "?":
            if linie[1] == "1":
                frg1[nummer] = linie[2 : (len(linie)-1)]
            elif linie[1] == "2":
                frg2[nummer] = linie[2 : (len(linie)-1)]
            elif linie[1] == "3":
                frg3[nummer] = linie[2 : (len(linie)-1)]
            elif linie[1] == "4":
                frg4[nummer] = linie[2 : (len(linie)-1)]
        elif linie[0] == '"':
            if "ome" in linie:
                wortart[nummer] = "Nomen"
            elif "erb" in linie:
                wortart[nummer] = "Verb"
            elif "prä" in linie:
                wortart[nummer] = "Präposition"
            elif "jekti" in linie:
                wortart[nummer] = "Adjektiv"
        elif linie[0] == "#":
            lat[nummer] = linie[1 : (len(linie)-1)]
        elif linie[0] == "*":
            stern[nummer] = linie[1 : (len(linie)-1)]
        elif linie[0] == "+":
            plus[nummer] = linie[1 : (len(linie)-1)]
        elif linie[0] == "'":
            apostro[nummer] = linie[1 : (len(linie)-1)]
        elif linie[0] == "-":
            minus[nummer] = linie[1 : (len(linie)-1)] 
                
        elif linie[0] == "1":
            nummer += 1
            wortart.append("")
            lat.append("")
            stern.append("")
            plus.append("")
            apostro.append("")
            minus.append("")
            frg1.append("")
            frg2.append("")
            frg3.append("")
            frg4.append("")

    xk.close()
    richtig = 0
    falsch = 0
    words_there = 1
    while words_there > 0:
        words_there = 0
        pkt = 0
        number = random.randint(0,len(lat)-1)
        if wortart[number] == "Nomen":                   
            print("\n\nLatein:                   " + lat[number])
            form1 = input("Genitiv Sg.:              ")
            if form1 == stern[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + stern[number])
                pkt -= 1
            form1 = input("Genus:                    ")
            if form1 == plus[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + plus[number])
                pkt -= 1
            if apostro[number] != "":
                form1 = input("Genitiv Pl.:              ")
                if form1 == apostro[number]:
                    pkt += 0
                else:
                    print("FALSCH. Richtige Antwort:      " + apostro[number])
                    pkt -= 1
            form1 = input("Übersetzung:              ")
            if form1 == frg1[number] or frg2[number] or frg3[number] or frg4[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + frg1[number] + ", " + frg2[number] + ", " + frg3[number] + ", " + frg4[number] + ", ")
                pkt -= 1

        elif wortart[number] == "Verb":
            print("\n\nLatein:                   " + lat[number])
            form1 = input("1. Pers. Sg. Präsens:     ")
            if form1 == stern[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + stern[number])
                pkt -= 1
            form1 = input("1. Pers. Sg. Präteritum:  ")
            if form1 == plus[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + plus[number])
                pkt -= 1
            if apostro[number] != "":
                form1 = input("PPP:                      ")
                if form1 == apostro[number]:
                    pkt += 0
                else:
                    print("FALSCH. Richtige Antwort:      " + apostro[number])
                    pkt -= 1
            form1 = input("Übersetzung:              ")
            if form1 == frg1[number] or frg2[number] or frg3[number] or frg4[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + frg1[number] + ", " + frg2[number] + ", " + frg3[number] + ", " + frg4[number] + ", ")
                pkt -= 1
        elif wortart[number] == "Adjektiv":
            print("\n\nLatein:                   " + lat[number])
            form1 = input("Genitiv Sg.:     ")
            if form1 == stern[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + stern[number])
                pkt -= 1
##            form1 = input("1. Pers. Sg. Präteritum:  ")
##            if form1 == plus[number]:
##                pkt += 0
##            else:
##                print("FALSCH. Richtige Antwort:      " + plus[number])
##                pkt -= 1
##            if apostro[number] != "":
##                form1 = input("PPP:                      ")
##                if form1 == apostro[number]:
##                    pkt += 0
##                else:
##                    print("FALSCH. Richtige Antwort:      " + apostro[number])
##                    pkt -= 1
            form1 = input("Übersetzung:              ")
            if form1 == frg1[number] or frg2[number] or frg3[number] or frg4[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + frg1[number] + ", " + frg2[number] + ", " + frg3[number] + ", " + frg4[number] + ", ")
                pkt -= 1
        elif wortart[number] == "Präposition":
            print("\n\nLatein:                   " + lat[number])
            form1 = input("mit welchem Fall:     ")
            if form1 == stern[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + stern[number])
                pkt -= 1
##            form1 = input("1. Pers. Sg. Präteritum:  ")
##            if form1 == plus[number]:
##                pkt += 0
##            else:
##                print("FALSCH. Richtige Antwort:      " + plus[number])
##                pkt -= 1
##            if apostro[number] != "":
##                form1 = input("PPP:                      ")
##                if form1 == apostro[number]:
##                    pkt += 0
##                else:
##                    print("FALSCH. Richtige Antwort:      " + apostro[number])
##                    pkt -= 1
            form1 = input("Übersetzung:              ")
            if form1 == frg1[number] or frg2[number] or frg3[number] or frg4[number]:
                pkt += 0
            else:
                print("FALSCH. Richtige Antwort:      " + frg1[number] + ", " + frg2[number] + ", " + frg3[number] + ", " + frg4[number] + ", ")
                pkt -= 1
        if pkt == 0:
            richtig += 1
        else:
            falsch += 1
        wortart.pop(number)
        lat.pop(number)
        stern.pop(number)
        plus.pop(number)
        apostro.pop(number)
        minus.pop(number)
        frg1.pop(number)
        frg2.pop(number)
        frg3.pop(number)
        frg4.pop(number)

        for kj in lat:
            if kj == "":
                words_there += 0
            else:
                words_there += 1

    print("\n\nDas waren alle Vokablen!")
    print("Richtig: " + str(richtig) + "\nFalsch: " + str(falsch))
    quest = input("Möchtest du eine andere Lektion lernen?\n")
    quest.lower()
    if "ja" in quest:
        vokabeln()
    else:
        quit()
vokabeln()
