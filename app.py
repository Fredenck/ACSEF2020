# Raspberry Pi3 Traffic Control Front End (server) Program
# Using Flask Web Server and Python

import RPi.GPIO as GPIO
import time

from subprocess import call, check_output
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

#global variables
#requested mode: '','Normal_Traffic','Stops_Sign','Power_Down'
reqMod = ''
#progress: ''(complete), 'Switch to '
proGress = ''
#message: 'Select a button..', 'Wait to complete, or select a button', 'Wait IO program to start..'
myText = ''
#Network: IP address:
myNetworkIP = ''

#status GPIO; must be consistent with io program
iReq=12
oAuto=17
oMan1=27
oMan2=22
oStdby=23

def getNetworkIP():
    global myNetworkIP
    
    binaryIP=check_output(["hostname", "-I"])
    if binaryIP==b'\n':
        myNetworkIP="not connected"
    else:
        strIP=binaryIP.decode()
        myIP=strIP.split(" ")[0]
        #connected, extract Network
        binaryNetwork=check_output(["iwgetid"])
        strNetwork=binaryNetwork.decode()
        myNetwork=strNetwork.split('"')[1]
        myNetworkIP = myNetwork+': '+myIP
    return

#config GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([oAuto,oMan1,oMan2,oStdby,iReq], GPIO.OUT)
GPIO.output([oAuto,oMan1,oMan2,oStdby,iReq], 0)

def chkStatGPIO():
    global reqMod
    global proGress
    global myText
    myText = ': select a button'
    reqMod = ''
        
    if GPIO.input(iReq)==1:
        proGress = 'Switch to '
        myText = ': wait to complete, or select a button'
    else:
        proGress = ''
    # initial start default to 'Power_Down' mode by io program
    if GPIO.input(oAuto)==1:
        reqMod = 'Auto'
    else:
        if GPIO.input(oMan1)==1:
            reqMod = 'Manual1'
        else:
            if GPIO.input(oMan2)==1:
                reqMod = 'Manual2'
            else:
                if GPIO.input(oStdby)==1:
                    reqMod = 'Standby'
                else:
                    myText = 'Wait IO program to start'
    return
    
#interactive web page
#This section create hardware interrupt and update webpage
# redirect(): go to the function
# render_template(): bring the web page to the front and update parameters
@app.route('/')
def update():
    global reqMod
    global proGress
    global myText
    global myNetworkIP
    
    #update
    chkStatGPIO()
    getNetworkIP()
    
    templateData = {'rMode':reqMod,'prog':proGress,'note': myText,'ipAddr':myNetworkIP}
    return render_template('operate.html', **templateData )

@app.route('/<selected>')
def operate(selected):
    global reqMod
    
    if reqMod != '' and reqMod != 'Shutdown':
        if selected == "Auto" and reqMod != 'Auto':
            GPIO.output([oAuto,oMan1,oMan2,oStdby,iReq],[1,0,0,0,1])

        if selected == "Manual1" and reqMod != 'Manual1':
            GPIO.output([oAuto,oMan1,oMan2,oStdby,iReq],[0,1,0,0,1])
        if selected == "Manual2" and reqMod != 'Manual2':
            GPIO.output([oAuto,oMan1,oMan2,oStdby,iReq],[0,0,1,0,1])
        if selected == "Standby" and reqMod != 'Standby':
            GPIO.output([oAuto,oMan1,oMan2,oStdby,iReq],[0,0,0,1,1])
    
    if selected == "Shutdown":
        GPIO.cleanup()
        call("sudo shutdown -h now", shell=True)        

    return redirect(url_for('update'))


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
    #host ='0.0.0.0' allows access from network