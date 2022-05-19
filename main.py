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

velocidade_walk = 70
velocidade_turn = 40

robot_odo = robot_dm / wheel_dim

walk_kp = 2

def rotate(num):
    degrees = num*robot_odo
    tank.on_for_degrees(velocidade_turn, -velocidade_turn, degrees)
    
    left_motor.wait_while('running', 5000)
    
    tank.stop()
    # aplicar kalman
    
    
def walk(dis_cm, direction):
    wheel_circ = 2 * math.pi * (wheel_dim / 2)
    degrees = (dis_cm / wheel_circ) * 360
    target = left_motor.position + degrees
    # tank_drive.on_for_degrees(velocidade, velocidade, degrees)
    
    initial_pos = left_motor.position
    
    controle_velocidade = velocidade_walk
    while left_motor.position <= target:
        e = (direction - gyro_sensor_in3.angle) * walk_kp
        e = max(min(e, 100), -100)
        
        # derivada para a velocidade
        dist_from_target = target - left_motor.position
        dist_from_start = left_motor.position - initial_pos
        
        if(dist_from_target < 200):
            controle_velocidade = dist_from_target/200
            velocidade = max(velocidade_walk * controle_velocidade, 10)
            
        elif (dist_from_start < 200):
            controle_velocidade = dist_from_start/200
            velocidade = max(velocidade_walk * controle_velocidade, 10)
            
        else:
            velocidade = velocidade_walk
        
        steering.on(e, velocidade)
        
    # aplicar kalman
    tank.stop()
    
    
contador = 0

pen_in5.down()


while True:
    direcao = (90 * contador)
    print(direcao)
    
    walk(100, direcao)
    time.sleep(0.5)
    rotate(90)
    time.sleep(0.5)
    
    contador += 1
    
    
# print(motorA.count_per_m)
# while True:
    # print(gyro_sensor_in3.angle)
    # print(gyro_sensor_in3.rate)
    # time.sleep(0.3)
    
# TODO
# aplicar filtro de kalman
# valor do giroscopio tem que ser a mediana da pilha

    
    

