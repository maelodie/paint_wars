def braitenberg_avoider(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"] 
    return translation, rotation

def braitenberg_loveWall(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_wall"]
    rotation = (1) * sensors["sensor_front_left"]["distance_to_wall"] + (-1) * sensors["sensor_front_right"]["distance"] 
    return translation, rotation

def braitenberg_hateWall(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"]["distance"] 
    return translation, rotation

def braitenberg_loveBot(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance"] 
    return translation, rotation

def braitenberg_hateBot(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance"] 
    return translation, rotation