#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, time
import RPi.GPIO as GPIO
import os

# GPIO Setup for buttons (example GPIO pins)
START_BUTTON = 17
STOP_BUTTON = 27
RESET_BUTTON = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize LCD
lcd = Adafruit_CharLCD()
lcd.begin(16, 2)  # 16x2 LCD display

# Global timer variables
timer_running = False
start_time = 0
preset_time = 10  # Example scenario time in seconds
elapsed_time = 0

# Helper function to display messages on LCD
def update_lcd(line1, line2=""):
    lcd.clear()
    lcd.message(line1[:16] + "\n" + line2[:16])

# Play audio cues
def play_audio(file):
    os.system(f"aplay {file}")  # Assumes .wav files and `aplay` is available

# Timer controls
def start_timer():
    global timer_running, start_time
    if not timer_running:
        timer_running = True
        start_time = time()
        play_audio("start.wav")  # Add your audio file

def stop_timer():
    global timer_running, elapsed_time
    if timer_running:
        timer_running = False
        elapsed_time += time() - start_time
        play_audio("stop.wav")

def reset_timer():
    global timer_running, start_time, elapsed_time
    timer_running = False
    elapsed_time = 0
    play_audio("reset.wav")

# Main loop
try:
    while True:
        # Handle button inputs
        if GPIO.input(START_BUTTON) == GPIO.LOW:
            start_timer()
        elif GPIO.input(STOP_BUTTON) == GPIO.LOW:
            stop_timer()
        elif GPIO.input(RESET_BUTTON) == GPIO.LOW:
            reset_timer()

        # Update LCD display
        if timer_running:
            current_time = time() - start_time + elapsed_time
        else:
            current_time = elapsed_time

        remaining_time = max(preset_time - current_time, 0)
        update_lcd(f"Time Left:", f"{remaining_time:.1f}s")

        # Timer finished
        if timer_running and remaining_time <= 0:
            stop_timer()
            update_lcd("Time's Up!")
            play_audio("end.wav")
            sleep(3)

        sleep(0.1)

except KeyboardInterrupt:
    update_lcd("Goodbye!")
    GPIO.cleanup()
