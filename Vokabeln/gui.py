#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, os, math, sys, random
try:
    from tkinter import *
    import _thread
except:
    quit()

def popupdestroy():
    global popup
    popup.destroy()
    popup.quit()
def popupmsg(msg, size = None):
    global popup
    popup = Tk()
    popup.wm_title("WARNING")
    label = Label(popup, text=msg)
    if size != None:
        label.config(font=("Courier", size))
    label.pack(side=TOP, fill=X, pady=10)
    B1 = Button(popup, text="Okay", command = popupdestroy)
    B1.pack()
    popup.mainloop()
    
    

def voc_lesen():
    global eingabe, loginfenster
    loginfenster = Tk()
    loginfenster.title("FuVoc - Lektion wählen")
    #loginfenster.geometry('550x140+100+100')
    label = Label(loginfenster,text="Bitte die Nummer der Lektion eingeben.", font="Courier")
    eingabe = Entry(loginfenster)
    butt = Button(loginfenster, font='Courier', text='Go!')
    butt.bind("<ButtonRelease-1>", test)
    eingabe.bind("<Return>", test)
    label.pack(side=TOP, fill = BOTH)
    eingabe.pack(side=TOP, fill = BOTH)
    butt.pack(side=TOP, fill = BOTH)
    loginfenster.mainloop()
    
    
def test(event):
    global eingabe, loginfenster, Lektion
    Lektion = str(eingabe.get())
    lektion = "Lektion_" + Lektion + ".pancake"
    alllekt = os.listdir()
    if lektion in alllekt:
        loginfenster.destroy()
        read()
    else:
        msg = "Lektion " + Lektion + " nicht vorhanden"
        popupmsg(msg)
    
def read():
    global Lektion, words,freevocs
    lektion = "Lektion_" + Lektion + ".pancake"
    wordd = open(lektion, "r")
    words = []
    linie = 0
    for line in wordd:
        if linie == 0:
            linie = 1
            freevocs = [0]
        else:
            words.append(line[:len(line)-1].split(","))
            freevocs.append(int(freevocs[-1])+1)
    del freevocs[-1]
        
    wordd.close()
    newvoc()

def newvoc():
    global freevocs
    if len(freevocs) > 0:
        numb = random.randint(0,len(freevocs)-1)
        frage(numb)
    else:
        popupmsg("Alle Vokabeln wurden abgefragt")
        quit()


def testword(number):
    global words, eingabe2,fenster,freevocs
    eingaben = []
    for elem in eingabe2:
        eingaben.append(str(elem.get()))
    liste = words[number][2:]
    ueber = liste[len(liste)-1].split(".")
    ueber2 = eingaben[len(eingaben)-1]
    if ueber2 in ueber:
        xy = True
    else:
        xy = False
    if liste[:len(liste)-2] == eingaben[:len(liste)-2] and xy:
        fenster.destroy()
        del freevocs[number]
    else:
        text = ""
        nummer = 0
        while nummer < len(liste)-1:
            text = text + "\n" + str(Text[nummer]) + ":   " + str(liste[nummer])
            nummer +=1
        text = text + "\nÜbersetzung:   " + str(liste[nummer])
        popupmsg("Richtig wäre:" + str(text),20)
        fenster.destroy()
    newvoc()

def frage(number):#wort
    global Lektion, words,eingabe2, fenster, Text
    liste = words[number]
    wortart = liste[0]
    fenster = Tk()
    fenster.title("FuVoc")
    label = Label(fenster,text=liste[1], font="Courier")
    label.pack(side=TOP, fill = BOTH)
    if wortart == "nomen":
        Text = ["Genitiv Sg.","Genus","Genitiv Plural","Übersetzung 2"]
    elif wortart == "verb":
        Text = ["1.Pers.Sg.Präsens","1.Pers.Sg.Perfekt","PPP","Übersetzung"]
    nummber = 2
    eingabe2 = []
    while nummber < len(liste):
        if liste[nummber] != "":
            if nummber == len(liste) -1:
                label2 = Label(fenster,text="Übersetzung", font="Courier")
            else:
                label2 = Label(fenster,text=Text[nummber-2], font="Courier")
            eingabe2.append(Entry(fenster))
            label2.pack(side=TOP, fill = BOTH)
            eingabe2[len(eingabe2)-1].pack(side=TOP, fill = BOTH)
            
        nummber += 1
    sendenbut = Button(fenster,text="Überprüfen", font="Courier")
    func = lambda number, zi = number: testword(zi)
    eingabe2[len(eingabe2)-1].bind("<Return>", func)
    sendenbut.bind("<ButtonRelease-1>", func)
    sendenbut.pack()
    fenster.mainloop()
        
voc_lesen()
