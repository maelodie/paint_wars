from braitenberg import *
import math

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
            param = [1, 0, 1, 1, -1, -1, 1, 1]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore2(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param = [1, 1, 1, 1, -1, 0, 0, 1]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore3(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param =  [1, 1, 1, 1, -1, 0, 1, 0]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True
    
class Explore4(Layer):
    def __init__(self):
        super().__init__("Avancer")

    def activate(self, sensors, parametre_sensor, robotId):  
            param =  [1, 1, 1, 1, -1, 0, 1, 0]
            translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
            rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );
            self.set_behavior(translation, rotation)
            return True