import tkinter as tk
from PN532 import PN532
from Crypto.Cipher import AES
from AESED import AESCBC

import RPi.GPIO as GPIO
import sys
import os
import time
import threading
import base64
import re
import codecs
import requests
import json



timeSinceLast = None
pn532 = None

def callbackPN532(tag, id):
        print('Found tag: {}, id: {}'.format(tag, id)) 
        pn532.close()
        
        identifier = id.split(":")
        r = requests.post("https://medicalidou.com/login.php", data={'email': identifier[0]})
        data = json.loads(r.text)
        
        name = data["MID_Name"].split(":")
        AES_inst = AESCBC(identifier[1], name[1])
        nameDec = AES_inst.decrypt(name[0])
        
        nfcScan(nameDec)
        
        
        if(":" in id):
            os.system('python3 tagtool.py --device "tty:AMA0" format tt2')
            





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
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

            TRIG = 7
            ECHO = 11
            maxTime = 0.04

            while True:
                GPIO.setup(TRIG,GPIO.OUT)
                GPIO.setup(ECHO,GPIO.IN)

                GPIO.output(TRIG,False)

                time.sleep(0.01)

                GPIO.output(TRIG,True)

                time.sleep(0.00001)

                GPIO.output(TRIG,False)

                pulse_start = time.time()
                timeout = pulse_start + maxTime
                while GPIO.input(ECHO) == 0 and pulse_start < timeout:
                    pulse_start = time.time()

                pulse_end = time.time()
                timeout = pulse_end + maxTime
                while GPIO.input(ECHO) == 1 and pulse_end < timeout:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = round(pulse_duration * 17150, 2)

                print(distance)
                
                
                if distance < 25:
                    currentTime = round(time.time() * 1000)
                    time.sleep(3)
                    while round(time.time() * 1000) < (currentTime + 6000): 
                        listen = pn532.listen()
                else:
                    pn532.close()
        except:
            GPIO.cleanup()
            
            
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

label3 = None

def clearName():
    label3.destroy()
    label2 = tk.Label(win, text = "Scan Phone Here\n...")
    label2.config(font=labelfont)
    label2.pack(pady=300)
    

def nfcScan(name):
    
    label3 = tk.Label(win, text = "Data Transfer Complete!\nWelcome " + name)
    label3.config(font=labelfont)
    
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
 