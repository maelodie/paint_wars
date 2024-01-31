from braitenberg import *

class Layer:
    def __init__(self, behavior_name, status):
        self.behavior_name = behavior_name
        self.translation = 0
        self.rotation = 0

    def activate(self, sensors, parametre_sensor):
        pass

    def set_behavior(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation
    
    def get_attributes(self):
        return self.translation, self.rotation
    
    def get_behavior_name(self):
        return self.behavior_name


class Avancer(Layer):
    def __init__(self):
        super().__init__("Avancer", False)

    def activate(self, sensors, parametre_sensor):
        if not (sensors["sensor_left"]["distance_to_wall"] < parametre_sensor or sensors["sensor_right"]["distance_to_wall"] < parametre_sensor or sensors["sensor_front"]["distance_to_wall"] < parametre_sensor):
            if not (sensors["sensor_left"]["distance_to_robot"] < parametre_sensor or sensors["sensor_right"]["distance_to_robot"] < parametre_sensor or sensors["sensor_front"]["distance_to_robot"] < parametre_sensor):
                translation = sensors["sensor_front"]["distance"]
                rotation = 0
                self.set_behavior(translation, rotation)
                return True
        return False
    



class HateWall(Layer):
    def __init__(self):
        super().__init__("HateWall", False)

    def activate(self, sensors, parametre_sensor):
        if sensors["sensor_left"]["distance_to_wall"] < parametre_sensor or sensors["sensor_right"]["distance_to_wall"] < parametre_sensor or sensors["sensor_front"]["distance_to_wall"] < parametre_sensor:
            translation, rotation = braitenberg_hateWall(sensors)
            self.set_behavior(translation, rotation)
            return True
        return False

class LoveBot(Layer):
    def __init__(self):
        super().__init__("Lovebot", False)

    def activate(self, sensors, parametre_sensor):
        if sensors["sensor_left"]["distance_to_robot"] < parametre_sensor or sensors["sensor_right"]["distance_to_robot"] < parametre_sensor or sensors["sensor_front"]["distance_to_robot"] < parametre_sensor:
            translation, rotation = braitenberg_loveBot(sensors)
            self.set_behavior(translation, rotation)
            return True
        return False
            

class Subsomption():
    def __init__(self):
        self.layers = []
        self.current_layer = None
    
    def addLayer(self, layer):
        self.layers.append(layer)

    def activate(self, sensors, parametre_sensor):
        for layer in self.layers:
            self.current_layer = layer
            layer.activate(sensors, parametre_sensor)
            if layer.activate(sensors, parametre_sensor):
                return
    
    def get_attributes(self):
        if self.current_layer is not None:
            return self.current_layer.get_attributes()
    
    def get_current_layer(self):
        if self.current_layer is not None:
            return self.current_layer.get_behavior_name()


