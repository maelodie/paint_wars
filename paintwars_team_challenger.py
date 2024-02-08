# Projet "robotique" IA&Jeux 

# Binome:
#  Prénom Nom: Jules MAZLUM         | 28605659
#  Prénom Nom: Maeva RAMAHATAFANDRY | 21104443
import math
from braitenberg import *
from layers import * 
from paintwars_config import *

def get_team_name():
    return "Mario and Luigi" # à compléter (comme vous voulez)

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors

 # Initialisation de la bibliothèque de comportement

avancer = Avancer() # Comportement avancer tout droit
loveWall = LoveWall()
hateWall = HateWall()

avoidAlly = AvoidAlly()
seekAlly = SeekAlly()

avoidEnemy = AvoidEnemy()
seekEnemy = SeekEnemy()


def step(robotId, sensors):
    #initialisation des variables
    sensors = get_extended_sensors(sensors)
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)
    param =  [1, 0, 1, 1, -1, -1, 1, 1]
    translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
    rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );

    translation, rotation = braitenberg_avoider(sensors)
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation

"""def strategie_map0(robotId, sensors):
    if robotId%8 == 3 or robotId%8 == 4:


        translation, rotation = 

    return translation, rotation"""
librarie1 = Subsomption()
librarie1.addLayer(avoidAlly)
librarie1.addLayer(avancer)

librarie1.activate(sensors)