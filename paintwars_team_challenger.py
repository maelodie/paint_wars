# Projet "robotique" IA&Jeux 

# Binome:
#  Prénom Nom: Jules MAZLUM         | 28605659
#  Prénom Nom: Maeva RAMAHATAFANDRY | 21104443

from paintwars_config import *
import math
# ______________ COMPORTEMENTS BRAITENBERG ____________________ #
def braitenberg_avoider(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = ((-1) * sensors["sensor_back_left"]["distance"] + (1) * sensors["sensor_back_right"]["distance"] +
                (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"] +
                (-1) * sensors["sensor_front"]["distance"] + (1) * sensors["sensor_back"]["distance"] + 
                (-1) * sensors["sensor_left"]["distance"] + (1) * sensors["sensor_right"]["distance"] 
             )
    return translation, rotation

def braitenberg_loveWall(sensors):
    translation = 100 * sensors["sensor_front"]["distance"]
    rotation = ((1) * sensors["sensor_front_left"]["distance_to_wall"] + (-1) * sensors["sensor_front_right"]["distance_to_wall"]+
                (1) * sensors["sensor_left"]["distance_to_wall"] + (-1) * sensors["sensor_right"]["distance_to_wall"]+
                (1) * sensors["sensor_back_left"]["distance_to_wall"] + (-1) * sensors["sensor_back_right"]["distance_to_wall"]
                )
    return translation, rotation

def braitenberg_hateWall(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = ((-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"]["distance"]  +
                (-1) * sensors["sensor_front"]["distance_to_wall"] + (1) * sensors["sensor_back"]["distance"] 
                )
    return translation, rotation

def braitenberg_loveBot(sensors):
    translation = (100) * sensors["sensor_front"]["distance"]
    rotation = ((1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance_to_robot"]+
                (1) * sensors["sensor_left"]["distance_to_robot"] + (-1) * sensors["sensor_right"]["distance_to_robot"]+
                (1) * sensors["sensor_back_left"]["distance_to_robot"] + (-1) * sensors["sensor_back_right"]["distance_to_robot"]
                )
    return translation, rotation

def braitenberg_hateBot(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = ((-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]+
                (-1) * sensors["sensor_left"]["distance_to_robot"] + (1) * sensors["sensor_right"]["distance_to_robot"]+
                (-1) * sensors["sensor_back_left"]["distance_to_robot"] + (1) * sensors["sensor_back_right"]["distance_to_robot"]
                )
    return translation, rotation


#__________________________ SUBSOMPTION ______________________________________ #
class Layer:
    def __init__(self, behavior_name):
        self.behavior_name = behavior_name
        self.translation = 0
        self.rotation = 0

    def activate(self, sensors, parametre_sensor, robotId):
        pass

    def set_behavior(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation
    
    def get_attributes(self):
        return self.translation, self.rotation
    
    def get_behavior_name(self):
        return self.behavior_name
      
class Subsomption():
    def __init__(self):
        self.layers = []
        self.current_layer = None
    
    def addLayer(self, layer):
        self.layers.append(layer)

    def activate(self, sensors, parametre_sensor, robotId):
        for layer in self.layers:
            self.current_layer = layer
            layer.activate(sensors, parametre_sensor, robotId)
            if layer.activate(sensors, parametre_sensor, robotId):
                return
    
    def get_attributes(self):
        if self.current_layer is not None:
            return self.current_layer.get_attributes()
    
    def get_current_layer(self):
        if self.current_layer is not None:
            return self.current_layer.get_behavior_name()


class LoveEnemy(Layer):
    def __init__(self):
        super().__init__("LoveEnemy")

    def activate(self, sensors, parametre_sensor, robotId):
        if ((sensors["sensor_front"]["isRobot"] and not sensors["sensor_front"]["isSameTeam"]) or
        (sensors["sensor_front_right"]["isRobot"] and not sensors["sensor_front_right"]["isSameTeam"]) or
        (sensors["sensor_right"]["isRobot"] and not sensors["sensor_right"]["isSameTeam"]) or
        (sensors["sensor_back_right"]["isRobot"] and not sensors["sensor_back_right"]["isSameTeam"]) or
        (sensors["sensor_back"]["isRobot"] and not sensors["sensor_back"]["isSameTeam"]) or
        (sensors["sensor_back_left"]["isRobot"]and not sensors["sensor_back_left"]["isSameTeam"]) or
        (sensors["sensor_left"]["isRobot"]and not sensors["sensor_left"]["isSameTeam"] ) or
        (sensors["sensor_front_left"]["isRobot"] and not sensors["sensor_front_left"]["isSameTeam"])):
            translation, rotation = braitenberg_loveBot(sensors)
            self.set_behavior(translation, rotation)
            return True
        
        return False
    
class HateAlly(Layer):
    def __init__(self):
        super().__init__("HateAlly")

    def activate(self, sensors, parametre_sensor, robotId):
        if ((sensors["sensor_front"]["isRobot"] and sensors["sensor_front"]["isSameTeam"]) or
        (sensors["sensor_front_right"]["isRobot"] and sensors["sensor_front_right"]["isSameTeam"]) or
        (sensors["sensor_right"]["isRobot"] and sensors["sensor_right"]["isSameTeam"]) or
        (sensors["sensor_back_right"]["isRobot"] and sensors["sensor_back_right"]["isSameTeam"]) or
        (sensors["sensor_back"]["isRobot"] and sensors["sensor_back"]["isSameTeam"]) or
        (sensors["sensor_back_left"]["isRobot"] and sensors["sensor_back_left"]["isSameTeam"]) or
        (sensors["sensor_left"]["isRobot"] and sensors["sensor_left"]["isSameTeam"]) or
        (sensors["sensor_front_left"]["isRobot"] and sensors["sensor_front_left"]["isSameTeam"])):
            translation, rotation = braitenberg_hateBot(sensors)
            self.set_behavior(translation, rotation)
            return True
        return False
    
class HateWall(Layer):
    def __init__(self):
        super().__init__("HateWall")

    def activate(self, sensors, parametre_sensor, robotId):
        if ((sensors["sensor_front"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_front"]["isRobot"]) or
        (sensors["sensor_front_right"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_front_right"]["isRobot"]) or
        (sensors["sensor_right"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_right"]["isRobot"]) or
        (sensors["sensor_back_right"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_back_right"]["isRobot"]) or
        #(sensors["sensor_back"]["distance_to_wall"] < 1 and sensors["sensor_back"]["isRobot"]) or
        (sensors["sensor_back_left"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_back_left"]["isRobot"]) or
        (sensors["sensor_left"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_left"]["isRobot"]) or
        (sensors["sensor_front_left"]["distance_to_wall"] < parametre_sensor and not sensors["sensor_front_left"]["isRobot"])):
            translation, rotation = braitenberg_hateWall(sensors)
            self.set_behavior(translation, rotation)
            return True
        return False
    
class Explore1(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param = [1, 1, 1, 1, -1, -1, 1, 1]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore2(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param = [1, 1, 1, 1, 0, -1, 1, 0]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore3(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param = [1, 1, 1, 1, 0, 1, -1, 0]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore4(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param = [1, 1, 1, 1, 1, -1, -1, 1]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
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

