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

posInit = (400,400) # position initiale du robot (centre de la carte)

# ___________ Variables pour stocker les paramètres_____________#
param = [random.randint(-1, 1) for _ in range(0, 8)] # premier paramètre généré aléatoirement 
bestParam = [] # variable contenant le meilleur paramètre parmi ceux qui vont être générés
bestDistance = 0 # distance la plus grande entre le centre de la carte et une distance quelconque (score)

# ___________ Paramètres d'évaluation _____________#
evaluations = 0 # nombre d'évaluations : 500 évaluations pour connaître la carte et 3 évaluations par comportement pour l'orientation 
orientationEval = 0 # compteur permettant de vérifier toutes les 3 itérations le score obtenu par un comportement dans différentes orientations 
distanceList = [] # liste permettant de faire la somme des distances obtenues pour calculer le score des comportements après 3 itérations 


def step(robotId, sensors, position):
    global evaluations, param, bestParam, bestDistance, orientationEval, distanceList
    bestIteration = 0 

    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
    if evaluations < 500 * 3: # on effectue des evaluations fixes puis une exploitation du meilleur paramètre après épuisement du nombre d'évaluations
        if rob.iterations % 400 == 0:    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
            if rob.iterations > 0:

                print(rob.iterations)

                dist = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) ) # distance parcourue entre le milieu et un point quelconque avec les paramètres comportementparam précédents
                distanceList.append(dist) # on ajoute la distance effectuée à pendant 3 itération à une liste dont on va calculer la distance totale
                if orientationEval % 3 == 0 and orientationEval != 0: # `orientationEval` permet d'évaluer un comportement 3 fois avec différentes orientations (ou positions) et on ne compte pas la première itération parce que la liste de distances est encore vide
                    score = sum(distanceList) # on fait d'abord la somme des distances parcourues avec les 3 évaluations
                    distanceList.clear() # on efface le contenu de la liste pour le prochain comportement
                        
                    if bestDistance < score: # si le score actuel est meilleur que le score enregistré comme le meilleur
                        bestDistance = score # le meilleur score est remplacé par le score actuel
                        bestParam = param.copy() # le meilleur paramètre est celui du comportement actuel
                        bestIteration = rob.iterations # on stocke l'itération pendant laquelle le meilleur paramètre a été trouvé
                        saveParams(bestIteration, bestDistance, bestParam) # on enregistre la meilleure itération, la meilleure distance et le meilleur paramètre dans un fichier

                    param = [random.randint(-1, 1) for _ in range(0, 8)] # on génère un nouveau paramètre seulement toutes les 3 itérations
                    plot(evaluations//3, score, bestDistance, 1)
                    
                else: # ici, on tombe dans le cas d'évaluation d'orientation du comportement (on ne change pas le paramètre mais on change l'orientation que l'on évalue avec le même paramètre)
                    orientation = random.randint(0, 360) # l'orientation est un entier aléatoire comprise entre 0 et 360
                    rob.controllers[robotId].set_position(posInit[0], posInit[1]) # on place le robot à son point d'initiation
                    rob.controllers[robotId].set_absolute_orientation(orientation) # on l'oriente au nombre tiré aléatoirement
            
            # incrémentation / désincrémentation des paramètres
            evaluations += 1
            orientationEval += 1
    
    # ici, on tombe dans le cas d'exploitation des paramètres trouvées. Toutes les 1000 itérations, on affiche l'état de l'expérience et optionnellement remettre le robot au centre de la carte 
    else:
        param = bestParam.copy() # Utilisation des meilleurs paramètres
        dist = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) ) # calcul de la distance parcourue grâce au paramètre
        if rob.iterations % 1000 == 0:
            print("Itération ", rob.iterations,  ": \tscore: ",  dist,  "\n")
            #reset
            #orientation = random.randint(0, 360)
            #rob.controllers[robotId].set_position(posInit[0], posInit[1])
            #rob.controllers[robotId].set_absolute_orientation(orientation)

    # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
    translation = math.tanh ( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"] );
    rotation = math.tanh ( param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"] );

    return translation, rotation

def saveParams(bestIteration, bestDistance, bestParam):
    with open("best_params.txt", "w") as file:
        file.write("Meilleurs paramètres:\n")
        file.write("Distance: " + str(bestDistance) + "\n")
        file.write("Paramètre: " + str(bestParam) + "\n")
        file.write("Iteration: " + str(bestIteration) + "\n")

# pour utiliser : "python plot.py graph1.csv 0 1"
def plot(generation, score, bestscore, i):
    name = "graph"+str(i)+".csv"

    with open(name, "a") as file:
        file.write(str(generation) + ",")
        file.write(str(score) + ",")
        file.write(str(bestscore))
        file.write("\n")

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
