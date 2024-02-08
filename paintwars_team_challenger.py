# Projet "robotique" IA&Jeux 

# Binome:
#  Prénom Nom: Jules MAZLUM         | 28605659
#  Prénom Nom: Maeva RAMAHATAFANDRY | 21104443

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

loveEnemy = LoveEnemy()
hateAlly = HateAlly()
hateWall = HateWall()
explorer = Explore()

library = Subsomption()
library.addLayer(hateAlly)
library.addLayer(loveEnemy)
library.addLayer(hateWall)
library.addLayer(explorer)

def step(robotId, sensors):
    global arenaIndexSelector
    #initialisation des variables
    sensors = get_extended_sensors(sensors)
    
    library.activate(sensors, 1, robotId)
    translation, rotation = library.get_attributes()

    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation