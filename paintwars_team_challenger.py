# Projet "robotique" IA&Jeux 
#
# Binome:
#  Prénom Nom: Jules MAZLUM
#  Prénom Nom: Maeva RAMAHATAFANDRY | 21104443

from braitenberg import *
from layers import * 

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

# subsomption 
# Construction de la bibliothèque de gestion des comportements en subsomption

behavior_lib = Subsomption() # Bibliothèque de comportements
avancer = Avancer() # Comportement avancer tout droit
hateWall = HateWall() # Comportement HateWall
loveBot = LoveBot() # Comportement lovebot

# Ajout de chaque comportement à la librairie
behavior_lib.addLayer(loveBot)
behavior_lib.addLayer(hateWall)
behavior_lib.addLayer(avancer)

def step(robotId, sensors):
    sensors = get_extended_sensors(sensors)

    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)

    parametre_sensor = 0.3 # sensibilité des senseurs
    behavior_lib.activate(sensors, parametre_sensor)
    translation, rotation = behavior_lib.get_attributes()
    
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation
