import tkinter as tk
from PN532 import PN532
import RPi.GPIO as GPIO
import sys
import os
import time
import threading


def callbackPN532(tag, id):
        print('Found tag: {}, id: {}'.format(tag, id))
        pn532.close()


pn532 = PN532('tty:AMA0', 'A0000001020304', callbackPN532)

class FullScreenApp(object):
    
    
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
        master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        #master.bind('<Escape>',self.toggle_geom)            
    
     
class App(threading.Thread):
    
    

    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        Listening = False
        #Initialize SR-04 Stuff
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = 7
        PIN_ECHO = 11
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        print ("Waiting for sensor to settle")
        time.sleep(2)
        while True:
            
            print ("Calculating distance")

            GPIO.output(PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.00001)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print ("Distance:",distance,"cm")
            
            if distance < 25:
                Listening = True
                listen = pn532.listen()
            else:
                Listening = False
                pn532.close()
            
            
            '''
            listen = pn532.listen()
            if not listen:
                break
            if counter > 100:
                pn532.close()
                counter = 0
                print("Restarting")
                pn532 = PN532('tty:AMA0', 'A0000001020304', callbackPN532)
            
        pn532.close()'''



def term():
    pn532.close()
    win.destroy()
    exit()

# Window Setup
win = tk.Tk() 
win.title("Medical ID") 
win.resizable(False,False)
win.bind("<Escape>", lambda x: term())
FullScreenApp(win)

# Label
titleLbl = tk.Label(win, text = "Medical ID\n__________________")
labelfont = ('Ariel', 40, 'bold')
titleLbl.config(font=labelfont)
titleLbl.config(fg='#03adfc')

#2nd Label
label2 = tk.Label(win, text = "Scan Phone Here\n...")
label2.config(font=labelfont)


fName = "Yousif" 
label3 = tk.Label(win, text = "Data Transfer Complete!\nWelcome " + fName)
label3.config(font=labelfont)


def nfcScan():
    label2.destroy()
    simBtn.destroy()
    label3.pack(pady=300)
    win.after(5000,refresh) 

def refresh():
    pn532.close()
    python = sys.executable
    os.execl(python, python, * sys.argv)

simBtn = tk.Button(text = "Simulate Scan", command = nfcScan) 


APP = App(win)
titleLbl.pack()
simBtn.pack()
label2.pack(pady=300)

win.mainloop() 
 
