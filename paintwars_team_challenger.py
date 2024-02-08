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

explorer1 = Explore1()
explorer2 = Explore2()
explorer3 = Explore3()
explorer4 = Explore4()

library1 = Subsomption()
library1.addLayer(hateAlly)
library1.addLayer(loveEnemy)
library1.addLayer(hateWall)
library1.addLayer(explorer1)

library2 = Subsomption()
library2.addLayer(hateAlly)
library2.addLayer(loveEnemy)
library2.addLayer(hateWall)
library2.addLayer(explorer2)

library3 = Subsomption()
library3.addLayer(hateAlly)
library3.addLayer(loveEnemy)
library3.addLayer(hateWall)
library3.addLayer(explorer3)

library4 = Subsomption()
library4.addLayer(hateAlly)
library4.addLayer(loveEnemy)
library4.addLayer(hateWall)
library4.addLayer(explorer4)

def step(robotId, sensors):
    global arenaIndexSelector
    #initialisation des variables
    sensors = get_extended_sensors(sensors)
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)

    if robotId%8 == 0 or robotId%8 == 4 :
        library1.activate(sensors, 1, robotId)
        translation, rotation = library1.get_attributes()

    if robotId%8 == 1 or robotId%8 == 5 :
        library2.activate(sensors, 1, robotId)
        translation, rotation = library2.get_attributes()

    if robotId%8 == 2 or robotId%8 == 6 :
        library3.activate(sensors, 1, robotId)
        translation, rotation = library3.get_attributes()

    if robotId%8 == 3 or robotId%8 == 7 :
        library4.activate(sensors, 1, robotId)
        translation, rotation = library4.get_attributes()

    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation