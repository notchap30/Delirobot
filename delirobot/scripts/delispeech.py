#! /usr/bin/python3
import time
import pyttsx3
from pickle import FALSE
from gtts import gTTS
import os
from yaml import compose_all
from yaml.composer import ComposerError
import speech_recognition as sr
import actionlib
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

voice = sr.Recognizer()
working = False
# listen1 = False
# listen2 = False
# askforroom = False
# readytodeli = 0
# numroom = 0
# getroom1 = False

def deli_speak(mytext):
    rospy.loginfo(mytext)
    synthesizer = pyttsx3.init()
    synthesizer.say(mytext) 
    synthesizer.runAndWait() 
    synthesizer.stop()

def deli_listen_speak():
    txt_voice = ""
    try:
        with sr.Microphone() as source:
            voice.adjust_for_ambient_noise(source, duration=0.5)
            audio_listen = voice.listen(source, timeout=7.0)

            txt_voice = voice.recognize_google(audio_listen)
            txt_voice = txt_voice.lower()
            # print("Recieve: " + txt_voice)
            rospy.loginfo(txt_voice + ". I have recieve command.")
            return txt_voice

    except sr.UnknownValueError:
        rospy.loginfo("Please say again.")
        # print("Please say again.")

    except sr.RequestError as e:
        rospy.loginfo("Could not request results; {0}".format(e))
        # print("Could not request results; {0}".format(e))

def deli_listen():
    return input('Please Enter\n')

def howmanyroom(command):
    if command == "1":
        deli_speak("Ok one room")
        return 1, False, True
    elif command == "2":
        deli_speak("Ok two room")
        return 2, False, True
    elif command == "cancel":
        deli_speak("Ok cancel")
        return 0, False, False
    else:
        return 0, True, True

def whatshouldido(command):
    if command == "upper open":
        deli_speak("Upper lid open")
    elif command == "upper close":
        deli_speak("Upper lid close")
    elif command == "lower open":
        deli_speak("Lower lid open")
    elif command == "lower close":
        deli_speak("Lower lid close")
    elif command == "bigbox":
        deli_speak("I fold the plate for the big box")
    elif command == "smallbox":
        deli_speak("plate down")

def roomnumber(numroom):
    correct=False
    check= False
    room1 = "base"
    room2 = "base"
    deli_speak("What room is it?")
    if numroom == 1:
        while not correct:
            room1=deli_listen()
            deli_speak("room1 is "+room1+" is that correct?")
            check = True
            while check:
                command=deli_listen()
                if command == "correct":
                    correct=True
                    check = False
                if command == "inccorrect":
                    correct=False
                    check = False
        return room1, room2
    elif numroom == 2:
        while not correct:
            room1=deli_listen()
            deli_speak("room1 is "+room1+" is that correct?")
            check = True
            while check:
                command=deli_listen()
                if command == "correct":
                    correct=True
                    check = False
                if command == "inccorrect":
                    correct=False
                    check = False
        correct = False
        deli_speak("room2, What room is it?")
        while not correct:
            room2=deli_listen()
            deli_speak("room2 is "+room2+" is that correct?")
            check = True
            while check:
                command=deli_listen()
                if command == "correct":
                    correct=True
                    check = False
                if command == "inccorrect":
                    correct=True
                    check = False
        return room1, room2

        
def checkpassword(roomnum):
    deli_speak("I'm at room "+roomnum+" please speak the password")
    password = "123"
    passincorrect = True
    while (passincorrect):
        command = deli_listen_speak()
        if command == password:
            deli_speak("password is correct please grab your box. If you are finish please say yes")
            notfinish = True
            while (notfinish):
                command = deli_listen_speak()
                if command == "yes":
                    notfinish = False
            deli_speak("Thankyou. Good bye")
            passincorrect = False

def gotoroom(room, frombase):
    if frombase == True:
        setgoal(0,-8,0,1)
    if room=="101":
        setgoal(2,-8.3,0,1)
        rospy.loginfo("Node sent")
    if room=="102":
        setgoal(4,-7.8,0,1)
        rospy.loginfo("Node sent")
    if room=="103":
        setgoal(8,-8.3,0,1)
        rospy.loginfo("Node sent")
    if room=="104":
        setgoal(10,-7.8,0,1)
        rospy.loginfo("Node sent")
    if room=="105":
        setgoal(14,-8.3,0,1)
        rospy.loginfo("Node sent")
    if room=="106":
        setgoal(16,-8.3,0,1)
        rospy.loginfo("Node sent")
    if room=="107":
        setgoal(18,-7.8,0,1)
        rospy.loginfo("Node sent")
    if room=="108":
        setgoal(18,-8.3,0,1)
        rospy.loginfo("Going back")
    elif room=="base":
        rospy.loginfo("Going back")
        setgoal(0,-8,0,1)
        setgoal(0.1,0.1,0.1,0.0)
        deli_speak("Deli back to base")


def setgoal(x,y,z,w):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        rospy.loginfo("Action Finish")
    time.sleep(5)   


def base_command():
    room1 = ""
    room2 = ""
    numroom = 0
    waitingforroomcommand=True
    readytodeli = False
    while (waitingforroomcommand):
        command = deli_listen()
        numroom,waitingforroomcommand,robotisnotready, = howmanyroom(command)
    while (robotisnotready):
        deli_speak("What should I do?")
        command = deli_listen()
        whatshouldido(command)
        if command == "ready":
            room1, room2= roomnumber(numroom)
            robotisnotready = False
            readytodeli = True
            deli_speak("Deli is ready going to "+room1+ " then "+room2)
    working_command(room1,room2)

def working_command(room1,room2):
    deli_speak("Deli start working")
    passincorrect = True
    gotoroom(room1,True)
    checkpassword(room1)
    gotoroom(room2,False)
    if room2 != "base":
        checkpassword(room2)
        gotoroom("base",False)


if __name__ == '__main__':
    rospy.init_node('movebase_client_py')
    rospy.loginfo("start")
    
    # setgoal(0,-5,0,0)
    while(True):
        command = deli_listen()
        if command == "delilisten":
            deli_speak("Im listening")
            command = deli_listen_speak()
        if command == "delistop":
            break
        if command == "delibase":
            gotoroom("base",False)
        if  command == "hey":
            deli_speak("Hi. Please let me help you. How many room do you want?")
            base_command()
