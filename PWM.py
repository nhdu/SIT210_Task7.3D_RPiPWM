import RPi.GPIO as GPIO     # Importing RPi library to use the GPIO pins
import time  # Importing sleep from time library
led_pin = 26  # Initializing the GPIO pin 26 for LED
GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)   # Declaring pin 26 as output pin
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

pwm = GPIO.PWM(led_pin, 100)    # Created a PWM object
pwm.start(0) # Started PWM at 0% duty cycle


try:
    while 1:
        dis = distance()
        print("Distance to object = %.1f cm" % dis)
        if (dis < 5):
            pwm.ChangeDutyCycle(100)
        elif (dis >= 5 and dis < 8):
            pwm.ChangeDutyCycle(75)
        elif (dis >= 8 and dis < 11):
            pwm.ChangeDutyCycle(50)
        elif (dis >= 11 and dis < 20):
            pwm.ChangeDutyCycle(25)
        else:
            pwm.ChangeDutyCycle(0)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass        # Go to next line
pwm.stop()      # Stop the PWM
GPIO.cleanup()  # Make all the output pins LOW