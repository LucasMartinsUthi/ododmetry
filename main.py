#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
left_motor.stop_action = "hold"
right_motor.stop_action = "hold"

tank = MoveTank(OUTPUT_A, OUTPUT_B)
steering = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()
radio = Radio()

gyro_sensor_in3 = GyroSensor(INPUT_1)
pen_in5 = Pen(INPUT_3)

motorC = LargeMotor(OUTPUT_C) # Magnet

# Here is where your code starts
wheel_dim = 5.6
robot_dm = 15.2

velocidade = 70

robot_odo = robot_dm / wheel_dim

walk_kp = 2

def rotate(num):
    degrees = num*robot_odo
    tank.on_for_degrees(velocidade, -velocidade, degrees)
    
    left_motor.wait_while('running', 5000)
    
    tank.stop()
    # aplicar kalman
    
    
def walk(dis_cm, angle):
    wheel_circ = 2 * math.pi * (wheel_dim / 2)
    degrees = (dis_cm / wheel_circ) * 360
    target = left_motor.position + degrees
    # tank_drive.on_for_degrees(velocidade, velocidade, degrees)
    
    while left_motor.position <= target:
        # print("Angle:", angle)
        # print("Gyro:", gyro_sensor_in3.angle)
        e = (angle - gyro_sensor_in3.angle) * walk_kp
        
        # print("Erro:", e)
        
        steering.on(e, velocidade)
        
    # aplicar kalman
    left_motor.reset()
    right_motor.reset()
    
    
contador = 0

pen_in5.down()


while True:
    direcao = (90 * contador)
    print(direcao)
    
    walk(50, direcao)
    time.sleep(0.5)
    rotate(90)
    time.sleep(0.5)
    
    contador += 1
    
    
# print(motorA.count_per_m)
# while True:
    # print(gyro_sensor_in3.angle)
    # print(gyro_sensor_in3.rate)
    # time.sleep(0.3)
    
        
    
    

