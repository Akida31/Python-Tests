import random, time, sys, os

print("\n\nHallo und willkommen zu der weltberühmten Quizshow von Fuison!")
time.sleep(2)
print("\nDie Regeln:")
time.sleep(1)
print("Du startest mit 1000 Punkten!")
time.sleep(1.8)
print("Für jede richtige Antwort bekommst du 100 Punkte!")
time.sleep(1.8)
print("Für jede falsche Antwort bekommst du 50 Punkte abzug!")
time.sleep(1.8)
print('\nWenn du aufhören willst schreibe "#stop" oder wenn du faul bist einfach nur "#"\n')
time.sleep(2)

#setup
i = 0
questions = []
answera = []
answerb = []
answerc = []
answerd = []
right = []
numberofquestions = 0 # ----------------------
points = 1000



#start
while i < 3:
    if i == 1:
        countquestions = numberofquestions#-------------------------
        i = 2
    elif i == 2:
        poi = 0
        if countquestions == 0:
            time.sleep(1)
            print("\nLeider sind die Fragen alle schon gestellt worden!\n")
            time.sleep(2)
            print("Bis zum nächsten Mal!")
            time.sleep(2)
            sys.exit()
        while poi == 0:
            number = random.randint(1,numberofquestions)#-------------------
            number -= 1
            if questions[number] != "":
                poi = 1
                time.sleep(1)
                print(questions[number])
                time.sleep(2)
                print("\n")
                print("a) " + answera[number])
                time.sleep(0.8)
                print("b) " + answerb[number])
                time.sleep(0.8)
                print("c) " + answerc[number])
                time.sleep(0.8)
                print("d) " + answerd[number])
                print("\n")
                joi = 0
                while joi == 0:
                    answer = input()
                    if "#" in answer:
                        sys.exit()
                    elif "a" in answer:
                        answer1 = "a"
                        joi = 1
                    elif "b" in answer:
                        answer1 = "b"
                        joi = 1
                    elif "c" in answer:
                        answer1 = "c"
                        joi = 1
                    elif "d" in answer:
                        answer1 = "d"
                        joi = 1
                    else:
                        print("\nIch habe dich nicht verstanden!")
                        time.sleep(1.5)
                        print("Bitte gib deine Antwort nochmal ein!\n")
                        time.sleep(2)


                if answer1 == right[number]:
                    time.sleep(0.5)
                    print("\nrichtig\n\n")
                    points += 100
                else:
                    time.sleep(0.5)
                    print("\nfalsch")
                    time.sleep(1)
                    points -= 50
                    print("Richtige Antwort: " + right[number] + "\n\n")
                    time.sleep(1)
                time.sleep(1)
                print("Punkte: " + str(points) + "                  Fragen: " + str(numberofquestions - countquestions + 1) +  "\n\n\n")
                time.sleep(3)
                

                #delete question
                questions[number] = ""
                answera[number] = ""
                answerb[number] = ""
                answerc[number] = ""
                answerd[number] = ""
                right[number] = ""
                countquestions -= 1

    if i == 0:
        i = 1
        questions.append("Wer ist der reichste Mensch der Welt?")
        answera.append("Bill Gates")
        answerb.append("Jeff Bezos")
        answerc.append("Mark Zuckerberg")
        answerd.append("Steve Jobs")
        right.append("b")
        numberofquestions = 1
        questions.append("Welches Jahr ist gerade?")
        answera.append("1010")
        answerb.append("2019")
        answerc.append("5072")
        answerd.append("2018")
        right.append("d")
        numberofquestions = 2
        questions.append("Wann wurde Rom gegründet?")
        answera.append("123 v. Chr.")
        answerb.append("476 n. Chr.")
        answerc.append("123 n. Chr.")
        answerd.append("753 v. Chr.")
        right.append("d")
        numberofquestions = 3
