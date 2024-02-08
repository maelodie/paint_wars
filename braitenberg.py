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