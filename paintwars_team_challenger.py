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

 # Initialisation de la bibliothèque de comportement

avancer = Avancer() # Comportement avancer tout droit
loveWall = LoveWall()
hateWall = HateWall()
seekEnemy = LoveBot()
avoidAlly = HateBot()
followAlly = LoveBot()
# librarie 1
behavior_lib = Subsomption() # Bibliothèque de comportements
behavior_lib.addLayer(seekEnemy)
behavior_lib.addLayer(hateWall)
behavior_lib.addLayer(avancer)

# librarie 2
behavior_lib2 = Subsomption() # Bibliothèque de comportements


def step(robotId, sensors):
    #initialisation des variables
    sensors = get_extended_sensors(sensors)
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)
    if robotId == 1:
        rotation = 0.5
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation

def subsomption_avancer_hatewall_lovebot(sensors, robotId):
   # Retrieve translation and rotation values
    parametre_sensor = 0.9 # sensibilité des senseurs
    behavior_lib.activate(sensors, parametre_sensor, robotId)
    translation, rotation = behavior_lib.get_attributes()

    return translation, rotation