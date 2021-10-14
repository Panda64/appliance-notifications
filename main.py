# main.py
import RPi.GPIO as GPIO
import time
import threading
import logging
import sys
import os
from twilio.rest import Client

GPIO.setmode(GPIO.BCM)

vlightPin = 4
u1lightPin = 24
u2lightPin = 25
u3lightPin = 26
u4lightPin = 13
button1Pin = 17
button2Pin = 27
button3Pin = 22
button4Pin = 23
vsensorPin = 6

GPIO.setup(u1lightPin, GPIO.OUT)
GPIO.setup(u2lightPin, GPIO.OUT)
GPIO.setup(u3lightPin, GPIO.OUT)
GPIO.setup(u4lightPin, GPIO.OUT)
GPIO.setup(vlightPin, GPIO.OUT)

GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vsensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(u1lightPin, False)
GPIO.output(u2lightPin, False)
GPIO.output(u3lightPin, False)
GPIO.output(u4lightPin, False)
GPIO.output(vlightPin, False)

current_user = None
vibrating = False
appliance_active = False
last_vibration_time = time.time()
start_vibration_time = last_vibration_time
cycle_start = None
begin_seconds = 10
end_seconds = 20
verbose = True
twilio_account_sid = ''
twilio_auth_token = ''
client = Client(twilio_account_sid, twilio_auth_token)


def short_beep(pin):
    GPIO.output(pin, True)
    time.sleep(0.25)
    GPIO.output(pin, False)
    
def long_beep(pin):
    GPIO.output(pin, True)
    time.sleep(1)
    GPIO.output(pin, False)
    
def greet_user1():
    short_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(1.5)
    #############
    short_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(1.5)
    #############
    long_beep(u1lightPin)
    time.sleep(0.5)
    short_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(1.5)
    #############
    short_beep(u1lightPin)
    time.sleep(0.5)
    long_beep(u1lightPin)
    time.sleep(0.5)
    short_beep(u1lightPin)
    time.sleep(0.5)
    short_beep(u1lightPin)
    time.sleep(1.5)
    #############
    short_beep(u1lightPin)
    time.sleep(1.5)
    #############
    long_beep(u1lightPin)
    time.sleep(0.5)
    short_beep(u1lightPin)
    
def greet_user2():
    short_beep(u2lightPin)
    time.sleep(0.5)
    short_beep(u2lightPin)
    time.sleep(1.5)
    #############
    long_beep(u2lightPin)
    time.sleep(0.5)
    long_beep(u2lightPin)
    time.sleep(0.5)
    short_beep(u2lightPin)
    time.sleep(1.5)
    #############
    long_beep(u2lightPin)
    time.sleep(0.5)
    long_beep(u2lightPin)
    time.sleep(0.5)
    short_beep(u2lightPin)
    time.sleep(1.5)
    #############
    short_beep(u2lightPin)
    time.sleep(0.5)
    short_beep(u2lightPin)
    
def greet_user3():
    short_beep(u3lightPin)
    time.sleep(1.5)
    #############
    long_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    time.sleep(1.5)
    #############
    short_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    time.sleep(1.5)
    #############
    short_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    time.sleep(1.5)
    #############
    long_beep(u3lightPin)
    time.sleep(0.5)
    long_beep(u3lightPin)
    time.sleep(0.5)
    long_beep(u3lightPin)
    time.sleep(1.5)
    #############
    long_beep(u3lightPin)
    time.sleep(0.5)
    short_beep(u3lightPin)
    
def greet_user4():
    long_beep(u4lightPin)
    time.sleep(0.5)
    long_beep(u4lightPin)
    time.sleep(1.5)
    #############
    short_beep(u4lightPin)
    time.sleep(0.5)
    long_beep(u4lightPin)
    time.sleep(1.5)
    #############
    short_beep(u4lightPin)
    time.sleep(0.5)
    long_beep(u4lightPin)
    time.sleep(0.5)
    short_beep(u4lightPin)
    time.sleep(1.5)
    #############
    short_beep(u4lightPin)
    time.sleep(0.5)
    short_beep(u4lightPin)
    time.sleep(1.5)
    #############
    long_beep(u4lightPin)
    time.sleep(0.5)
    long_beep(u4lightPin)
    time.sleep(0.5)
    long_beep(u4lightPin)
    
def vibrated(x):
    global vibrating
    global last_vibration_time
    global start_vibration_time
    
    logging.debug('Vibrated')
     
    last_vibration_time = time.time()
    
    if not vibrating:
        start_vibration_time = last_vibration_time
        vibrating = True
            
def send_appliance_active_message():
    global appliance_active
    global cycle_start
    
    cycle_start = time.time()
    
    message = client.messages \
                    .create(
                        body="",
                        from_='',
                        to=''
                    )
    logging.debug(message.sid)
    
    appliance_active = True
    GPIO.output(vlightPin, True)

def send_appliance_inactive_message():
    global appliance_active
    global current_user
    
    message = client.messages \
                    .create(
                        body="",
                        from_='',
                        to=''
                    )
    logging.debug(message.sid)
    
    appliance_active = False
    GPIO.output(vlightPin, False)
    
    GPIO.output(current_user, False)
    current_user = None

def check():
    global vibrating
    global current_user
    
    current_time = time.time()
    logging.debug(f'Checking at {current_time}')
    
    delta_vibration = last_vibration_time - start_vibration_time
    
    if vibrating and delta_vibration > begin_seconds and current_user and not appliance_active:
        send_appliance_active_message()
        
    if (not vibrating and appliance_active and current_time - last_vibration_time > end_seconds) or (current_time - cycle_start > 7200):
        send_appliance_inactive_message()
    
    vibrating = current_time - last_vibration_time < 3
    threading.Timer(2, check).start()

def user_selected(user_light_pin):
    global current_user
    
    if not appliance_active:
        previous_user = current_user
        current_user = user_light_pin
        
        if previous_user:
            GPIO.output(previous_user, False)
        
        if user_light_pin == u1lightPin:
            greet_user1()
        elif user_light_pin == u2lightPin:
            greet_user2()
        elif user_light_pin == u3lightPin:
            greet_user3()
        elif user_light_pin == u4lightPin:
            greet_user4()
        else:
            return 'Invalid User Number!'
        
        if current_user == user_light_pin:
            time.sleep(1)
            GPIO.output(current_user, True)
            expire(current_user)
    
def expire(user):
    global current_user
    
    time.sleep(20)
    
    if not appliance_active:
        GPIO.output(user, False)
        
        if current_user == user:
            current_user = None
    

logging.basicConfig(format='%(message)s', level=logging.INFO)

if verbose:
    logging.getLogger().setLevel(logging.DEBUG)

GPIO.add_event_detect(vsensorPin, GPIO.RISING, callback=vibrated, bouncetime=2100)
GPIO.add_event_detect(button1Pin, GPIO.FALLING, callback=lambda x: user_selected(u1lightPin))
GPIO.add_event_detect(button2Pin, GPIO.FALLING, callback=lambda x: user_selected(u2lightPin))
GPIO.add_event_detect(button3Pin, GPIO.FALLING, callback=lambda x: user_selected(u3lightPin))
GPIO.add_event_detect(button4Pin, GPIO.FALLING, callback=lambda x: user_selected(u4lightPin))


threading.Timer(2, check).start()            