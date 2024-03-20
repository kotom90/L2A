from mob_hp_bar_compare_pc import *
from keycode import Keycode

import serial
import time
import random
import threading
import keyboard

uart = serial.Serial("COM4", baudrate=9600)
time.sleep(2)

currentTarget = 1
numberOfTargets = 2
botStart = True
mobFullHPForLongTime = False
targetMobWasAttacked = False
shouldProvoke = True

noTargetForLongTime = False
targetWasFound = False

#If the time for buff pots has passed
timeToPressBuffPots = 0
#Find the Drop Icon position when starting, should pick a target first


def startBot():
    global botStart
    botStart = True

def stopBot():
    global botStart
    botStart = False

#Timers
def threadUseBuffPotsTimer():
    global timeToPressBuffPots
    time.sleep(60 * 20)
    timeToPressBuffPots = 1

def threadCheckMobFullHPForLongTime():
    #10 seconds count if mob was not attacked.
    global mobFullHPForLongTime
    global targetMobWasAttacked

    counter = 10
    while counter > 0:
        time.sleep(0.5)
        counter -= 1
        if targetMobWasAttacked == True:
            return
    mobFullHPForLongTime = True

def threadChecknoTargetForLongTime():
    #10 seconds count if mob was not attacked.
    global noTargetForLongTime
    global targetWasFound

    counter = 50
    while counter > 0:
        time.sleep(0.1)
        counter -= 1
        #reset counter if target was found
        if targetWasFound == True:
            counter = 50
    noTargetForLongTime = True

def startStopBot_hotkey_listener():
    keyboard.add_hotkey('alt+z', startBot)
    keyboard.add_hotkey('alt+x', stopBot)
    #keyboard.wait('esc')
    while True:
        time.sleep(1)


#Player actions
def hasTarget():
    return isDropIconVisible()

#searches for a new target when there is no target
def tryFindTarget():
    while findDropIcon() == False:
        pickNextTarget()
        time.sleep(0.5)

    
def sendKey(key):
    uart.write(bytes([key]))
    uart.flush()
    #print("Sent new KEY !!!")

def pickUp():
    time.sleep(0.1)
    for i in range(15):
        time.sleep(0.1)
        sendKey(Keycode.F6)
    time.sleep(0.1)

def sweep():
    time.sleep(0.1)
    for i in range(3):
        time.sleep(0.2)
        sendKey(Keycode.F5)
    time.sleep(0.1)

def spoil():
    time.sleep(0.1)
    for i in range(5):
        time.sleep(0.1)
        sendKey(Keycode.F4)
    time.sleep(0.1)

def attack():
    time.sleep(0.1)
    for i in range(5):
        time.sleep(0.1)
        sendKey(Keycode.F1)
    time.sleep(0.1)
    

def pickNextTarget():
    sendKey(Keycode.F2)

def useBuffPots():
    time.sleep(0.2)
    sendKey(Keycode.F10)
    time.sleep(0.3)
    sendKey(Keycode.F11)
    time.sleep(0.2)

def provokeTargets():
    sendKey(Keycode.F8)




def attackTarget():
    global currentTarget
    global timeToPressBuffPots
    global mobFullHPForLongTime
    global targetMobWasAttacked
    
    targetHP = getTargetHpPercentage()
    """while hasNoTarget() and botStart == True:
        pickNextTarget()
        time.sleep(0.5)
        print("NO TARGET!!")
        targetHP = getTargetHpPercentage()"""
    #if noTargetAttempts > 0:
    #print ("MOB HP IS ", getTargetHpPercentage())

    #Don't KS enemy mobs
    #if targetHP < 100:  
        #return
    time.sleep(0.1)

    #Use buff pots when the timer ends
    if timeToPressBuffPots == 1:
        useBuffPots()
        timeToPressBuffPots = 0
        potTimerThread = threading.Thread(target=threadUseBuffPotsTimer)
        potTimerThread.start()

    #start counting 10 second and set targetMobWasAttacked = True if not attacked in that time.
    checkMobFullHPForLongTimeThread = threading.Thread(target=threadCheckMobFullHPForLongTime)
    checkMobFullHPForLongTimeThread.start()

    mobFullHPForLongTime = False
    targetMobWasAttacked = False

    #Mob has full hp when targeted because we skip earlier mobs with less than 100 HP for KS.
    targetHP = 100

    #this is the lowest HP the target was at (for reattack while stunned).
    minimumTargetHp = 100 
    losingNoHpCounter = 20

    #We need the first hit to know whether the mob is in range to start the spoil
    firstHitAttacked = False

    attack()
    print("attacked next target")


    while targetHP > 0 and botStart == True:
        targetHP = getTargetHpPercentage()
        #if mob is attacked mark it for the 
        if targetHP < 100:
            targetMobWasAttacked = True
            if firstHitAttacked == False:
                spoil()
                firstHitAttacked = True
        
        #get the minimum hp the target was at and reset the counter when hp is lower.
        if targetHP < minimumTargetHp:
            minimumTargetHp = targetHP
            losingNoHpCounter = 20

        if targetHP >= minimumTargetHp:
            losingNoHpCounter -= 1
        print(losingNoHpCounter)
        #if the target has the same or more life for more than 40 x 0.2sec = 8sec attack again.
        if losingNoHpCounter == 0:
            attack()
            losingNoHpCounter = 20
        #exit loop if not attacking for more than 10 seconds after targeting
        if mobFullHPForLongTime == True:
            break
        time.sleep(0.2)

    #mob has 0 hp here after exiting loop
    sweep()
    pickUp()

def attackNextTarget():
    global targetWasFound
    global noTargetForLongTime
    global checkNoTargetForLongTimeThread
    global shouldProvoke

    targetWasFound = False
    pickNextTarget()
    time.sleep(0.5)
    #print("picked next target")

    #if target was found Attack it
    if hasTarget() == True:
        targetWasFound = True
        print("TARGET FOUND!!!")
        """if shouldProvoke:
            time.sleep(40)
            provokeTargets()
            shouldProvoke = False
            time.sleep(6)"""
        attackTarget()
        return

    if noTargetForLongTime:
        print("Stays for long without target!!!")
        shouldProvoke = True
        tryFindTarget()
        noTargetForLongTime = False
        checkNoTargetForLongTimeThread = threading.Thread(target=threadChecknoTargetForLongTime)
        checkNoTargetForLongTimeThread.start()


tryFindTarget()

potTimerThread = threading.Thread(target=threadUseBuffPotsTimer)
potTimerThread.start()

checkNoTargetForLongTimeThread = threading.Thread(target=threadChecknoTargetForLongTime)
checkNoTargetForLongTimeThread.start()

# Start the hotkey listener in a separate thread
startStopBot_hotkey_thread = threading.Thread(target=startStopBot_hotkey_listener)
startStopBot_hotkey_thread.start()

while 1:
    #print (botStart)
    #time.sleep(0.1)
    #print("bot start ", botStart)
    if botStart == 1:
        attackNextTarget()
    #print ("Cur target: ", currentTarget)
    #if currentTarget > numberOfTargets:
        #currentTarget = 1
    