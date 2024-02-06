# UE IA & JEUX - L3, SU
# TP "comportement réactif"
#
# Nicolas Bredeche
# 2021-03-31

from pyroborobo import Pyroborobo, Controller, AgentObserver, WorldObserver, CircleObject, SquareObject, MovableObject
# from custom.controllers import SimpleController, HungryController
import numpy as np
import random
import math

import paintwars_arena

rob = 0

# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *AVANT* CETTE LIGNE =-=-=-=-=-=-=-=-=-=

simulation_mode = 2 # Simulation mode: realtime=0, fast=1, super_fast_no_render=2 -- pendant la simulation, la touche "d" permet de passer d'un mode à l'autre.

# Initialisation des paramètres
posInit = (400,400) # position initiale

# Liste contenant les paramètres optimaux
param = []
bestParam = []

# score
bestDistance = 0

# population
dicoPopulation = [] # liste contenant les paramètres sur les individus générés
premier_individu = [random.randint(-1, 1) for _ in range(0, 8)] # ancêtre de la population généré au hasard
dicoPopulation.append(premier_individu)
nbGeneration = 500 # nombre d'individus générés 
individu_actuel = premier_individu.copy()
meilleurIndividu = premier_individu.copy()
bestDistance = 0

def step(robotId, sensors, position):
    # Import des variables globales
    global nbGeneration, individu_actuel, meilleurIndividu, bestDistance,  dicoPopulation
    
    if nbGeneration == 500:
        bestDistance = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) )

    if nbGeneration > 0:
        if rob.iterations % 400 == 0: # 1 comportement toutes les 400 itérations
            print(rob.iterations)
            individu_actuel = meilleurIndividu.copy()
            individu_actuel[random.randint(0, len(meilleurIndividu)-1)] = random.randint(-1, 1)
            if individu_actuel not in dicoPopulation:
                if rob.iterations > 0:
                    
                    dist = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) )

                    if bestDistance < dist:
                        bestDistance = dist
                        dicoPopulation.append(meilleurIndividu)
                        meilleurIndividu = individu_actuel.copy()
                        print("Meilleur individu: ", meilleurIndividu)
                        print("hi its me")

                    else:
                        dicoPopulation.append(individu_actuel)
            nbGeneration -= 1
    else:
        param = meilleurIndividu.copy() # Utilisation des meilleurs paramètre
        dist = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) )
        
        if rob.iterations % 1000 == 0:
            print("Itération ", rob.iterations,  ": \tscore: ",  dist,  "\n")

            #reset
            #rob.controllers[robotId].set_position(posInit[0], posInit[1])
            #rob.controllers[robotId].set_absolute_orientation(90)

    # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
    param = meilleurIndividu.copy()
    translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
    rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );

    return translation, rotation

def saveParams(bestIteration, bestDistance, bestParam):
    with open("best_params.txt", "w") as file:
        file.write("Meilleurs paramètres:\n")
        file.write("Distance: " + str(bestDistance) + "\n")
        file.write("Paramètre: " + str(bestParam) + "\n")
        file.write("Iteration: " + str(bestIteration) + "\n")

# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *APRES* CETTE LIGNE =-=-=-=-=-=-=-=-=-=

number_of_robots = 1  # 8 robots identiques placés dans l'arène

arena = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

offset_x = 36
offset_y = 36
edge_width = 28
edge_height = 28


class MyController(Controller):

    def __init__(self, wm):
        super().__init__(wm)

    def reset(self):
        return

    def step(self):

        sensors = {}

        sensors["sensor_left"] = {"distance": self.get_distance_at(0)}
        sensors["sensor_front_left"] = {"distance": self.get_distance_at(1)}
        sensors["sensor_front"] = {"distance": self.get_distance_at(2)}
        sensors["sensor_front_right"] = {"distance": self.get_distance_at(3)}
        sensors["sensor_right"] = {"distance": self.get_distance_at(4)}
        sensors["sensor_back_right"] = {"distance": self.get_distance_at(5)}
        sensors["sensor_back"] = {"distance": self.get_distance_at(6)}
        sensors["sensor_back_left"] = {"distance": self.get_distance_at(7)}

        translation, rotation = step(self.id, sensors, self.absolute_position)

        self.set_translation(translation)
        self.set_rotation(rotation)

    def check(self):
        # print (self.id)
        return True


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class MyAgentObserver(AgentObserver):
    def __init__(self, wm):
        super().__init__(wm)
        self.arena_size = Pyroborobo.get().arena_size

    def reset(self):
        super().reset()
        return

    def step_pre(self):
        super().step_pre()
        return

    def step_post(self):
        super().step_post()
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class MyWorldObserver(WorldObserver):
    def __init__(self, world):
        super().__init__(world)
        rob = Pyroborobo.get()

    def init_pre(self):
        super().init_pre()

    def init_post(self):
        global offset_x, offset_y, edge_width, edge_height, rob

        super().init_post()

        for i in range(len(arena)):
            for j in range(len(arena[0])):
                if arena[i][j] == 1:
                    block = BlockObject()
                    block = rob.add_object(block)
                    block.soft_width = 0
                    block.soft_height = 0
                    block.solid_width = edge_width
                    block.solid_height = edge_height
                    block.set_color(164, 128, 0)
                    block.set_coordinates(offset_x + j * edge_width, offset_y + i * edge_height)
                    retValue = block.can_register()
                    # print("Register block (",block.get_id(),") :", retValue)
                    block.register()
                    block.show()

        counter = 0
        for robot in rob.controllers:
            x = 260 + counter*40
            y = 400
            robot.set_position(x, y)
            counter += 1

    def step_pre(self):
        super().step_pre()

    def step_post(self):
        super().step_post()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Tile(SquareObject):  # CircleObject):

    def __init__(self, id=-1, data={}):
        super().__init__(id, data)
        self.owner = "nobody"

    def step(self):
        return

    def is_walked(self, id_):
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class BlockObject(SquareObject):
    def __init__(self, id=-1, data={}):
        super().__init__(id, data)

    def step(self):
        return

    def is_walked(self, id_):
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def main():
    global rob

    rob = Pyroborobo.create(
        "config/paintwars.properties",
        controller_class=MyController,
        world_observer_class=MyWorldObserver,
        #        world_model_class=PyWorldModel,
        agent_observer_class=MyAgentObserver,
        object_class_dict={}
        ,override_conf_dict={"gInitialNumberOfRobots": number_of_robots, "gDisplayMode": simulation_mode}
    )

    rob.start()

    rob.update(1000000)
    rob.close()

if __name__ == "__main__":
    main()
