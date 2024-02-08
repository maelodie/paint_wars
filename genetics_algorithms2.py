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
from paintwars_arena import *

rob = 0
arena_index = 3

# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *AVANT* CETTE LIGNE =-=-=-=-=-=-=-=-=-=

simulation_mode = 2 # Simulation mode: realtime=0, fast=1, super_fast_no_render=2 -- pendant la simulation, la touche "d" permet de passer d'un mode à l'autre.

posInit = (70,400) # position initiale du robot (centre de la carte)

# ___________ Variables pour stocker les paramètres_____________#
param = [1,0,1,-1,-1,-1,1,1] # premier paramètre généré aléatoirement 
bestParam = [] # variable contenant le meilleur paramètre parmi ceux qui vont être générés

# ________________ Paramètres d'évaluation ______________________#
evaluations = 500 * 3 # nombre d'évaluations : 500 évaluations pour connaître la carte et 3 évaluations par comportement pour l'orientation 
orientationEval = 0 # compteur permettant de vérifier toutes les 3 itérations le score obtenu par un comportement dans différentes orientations 
positions = [(64, 232), (64,288), (64, 344), (64, 400), (64, 456), (64, 512), (64, 568), (64, 624),
             (736, 232), (736,288), (736, 344), (736, 400), (736, 456), (736, 512), (736, 568), (736, 624)]
#_____________ Paramètres pour l'algorithme génétique ___________#
mu = 5
lamda = 20
parents = []
population = dict()
parent = []
parent = param.copy() # contient les paramètres du comportement du parent (parent du comportement)
scoreParent = 0 # contient le score du parent après expérimentation des 3 évaluations (avec oritentation)
eval1 = True # permet de savoir si c'est la première évaluation. Si c'est le cas, on n'effectue pas encore la comparaison enfant vs parent (l'enfant n'a pas encore été testé)

#____________ Calcul du score pour la distance ___________________#
distanceList = [] # liste permettant de faire la somme des distances obtenues pour calculer le score des comportements après 3 itérations 
bestScoreDistance = 0 # distance la plus grande entre le centre de la carte et une distance quelconque (score)

#______ Calcul du score pour la couverture de l'environnement______#
bestScoreCouverture = 0
scoreCouverture = 0
score_couverture_list = []
score_passage = 0
areneCopy = get_arena(arena_index).copy()

#____________ Calcul du score pour la vitesse et la rotation _____ #
score_vitesse_iteration = []
score_list = []
bestScoreVitesse = 0

def step(robotId, sensors, position):
    global evaluations, param, bestParam
    global orientationEval, positions
    global distanceList, bestScoreDistance
    global parent, scoreParent, eval1
    global score_vitesse_iteration, bestScoreVitesse, score_list
    global bestScoreCouverture, scoreCouverture, arenaCopy, score_couverture_list, score_passage
    bestIteration = 0 

    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
    if evaluations > 0: # on effectue des evaluations fixes puis une exploitation du meilleur paramètre après épuisement du nombre d'évaluations
        if rob.iterations % 400 == 0:    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
            if rob.iterations > 0:
                # On compare la distance la plus longue
                scoreDistance = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) ) # distance parcourue entre le milieu et un point quelconque avec les paramètres comportementparam précédents
                distanceList.append(scoreDistance) # on ajoute la distance effectuée à pendant 3 itération à une liste dont on va calculer la distance totale

                # On compare la vitesse de translation et la vitesse de rotation sur les itérations
                scoreVitesse = score_vitesse(score_vitesse_iteration)
                score_vitesse_iteration.clear()
                score_list.append(scoreVitesse) 
                
                # On compare le score de couverture sur l'environnement:
                scoreCouverture = score_couverture(areneCopy, position, robotId)
                score_couverture_list.append(scoreCouverture)

                if orientationEval % 3 == 0 and orientationEval != 0: # `orientationEval` permet d'évaluer un comportement 3 fois avec différentes orientations (ou positions) et on ne compte pas la première itération parce que la liste de distances est encore vide
                    finalScoreVitesse = sum(score_list) # on fait d'abord la somme des distances parcourues avec les 3 évaluations
                    score_list.clear() # on efface le contenu de la liste pour le prochain comportement
                    
                    finalScoreCouverture = sum(score_couverture_list)
                    score_couverture_list.clear()

                    finalScoreDistance = sum(distanceList)
                    distanceList.clear()

                    if bestScoreVitesse < finalScoreVitesse and bestScoreCouverture < finalScoreCouverture and bestScoreDistance < finalScoreDistance: 
                        bestScoreVitesse = finalScoreVitesse
                        bestScoreCouverture = finalScoreCouverture
                        bestScoreDistance = finalScoreDistance
                        bestParam = param.copy()
                        bestIteration = rob.iterations 
                        saveParams(bestIteration, bestScoreVitesse, bestParam) 

                    print(
                        'iteration:\t', rob.iterations,
                        'parent:\t', parent,
                        'enfant:\t', param,
                        'score Vitesse:\t', finalScoreVitesse,
                        'score Couverture:\t', finalScoreCouverture
                    )

                    score = finalScoreCouverture + finalScoreVitesse

                    if eval1: # si c'est la première initialisation, on initialise le score du parent à celui qu'on a obtenu
                        scoreParent = score # le score du parent est le premier score
                        eval1 = False # on met l'évaluation à False car ce n'est plus la première itération

                    if score > scoreParent and score != scoreParent: # si le score de l'enfant est supérieur au score du parent, le parent est remplacé par l'enfant
                        scoreParent = score # le nouveau scoreParent est le score de l'enfant 
                        parent = param.copy() # l'enfant devient le nouveau parent et le parent est archivé

                    # Dans tous les cas, on génère les enfants tq:
                    param = parent.copy() # l'enfant est une copie du parent avec un mutation
                    param[random.randint(0, len(param) - 1)] = random.randint(-1, 1) # on initialise la valeur de l'enfant à celle du parent avec une mutation parmi ses éléments 
                            
                else: # ici, on tombe dans le cas d'évaluation d'orientation du comportement (on ne change pas le paramètre mais on change l'orientation que l'on évalue avec le même paramètre)
                    orientation = random.randint(0, 360) # l'orientation est un entier aléatoire comprise entre 0 et 360
                    rob.controllers[robotId].set_absolute_orientation(orientation) # on l'oriente au nombre tiré aléatoirement

                    pos = random.choice(positions)
                    x, y = pos[0], pos[1]
                    rob.controllers[robotId].set_position(x, y) # on place le robot à son point d'initiation
            # incrémentation / désincrémentation des paramètres
            evaluations -= 1
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

    score_vitesse_append(translation, rotation, score_vitesse_iteration)
    env_passage(areneCopy, position, robotId)
    

    return translation, rotation

def score_vitesse_append(translation, rotation, score_vitesse_iteration):
    score_vitesse_iteration.append(translation * (1 - abs(rotation)))

def score_vitesse(score_vitesse_iteration):
    return sum(score_vitesse_iteration)

def env_passage(arene, position, robotId):
    x = int(position[0] // len(arene))
    y = int(position[1] // len(arene[0]))
    
    if x >= len(arene) :
        x = len(arene) - 1
    if y >= len(arene[0]):
        y = len(arene[0]) - 1

    arene[x][y] = -1 * robotId
    
def score_couverture(arene, position, robotId):
    score = 0
    width_arene = len(arene)
    height_arene = len(arene[0])

    for k in range(width_arene * height_arene):
        i = k // width_arene
        j = k % width_arene

        if arene[i][j] <= 0:
            score += 1

    return score

def generate_child(parents, population, k, mu, lamda):
    """
        k : nombre de mutation
    """
    nb_enfants = lamda / mu # nombre d'enfants par parent
    indexes = [random.randint(0, len(parents[0]-1))] # k indices aléatoires où il faut changer la valeur pour la mutation

    for parent in parents:
        for _ in range(nb_enfants):
            for i in indexes:
                child = parent.copy()
                child[i] = random.randint(-1,1) 
                population[child] = 0

    return parents, population

def saveParams(bestIteration, bestDistance, bestParam):
    with open("best_params.txt", "w") as file:
        file.write("Meilleurs paramètres:\n")
        file.write("Distance: " + str(bestDistance) + "\n")
        file.write("Paramètre: " + str(bestParam) + "\n")
        file.write("Iteration: " + str(bestIteration) + "\n")

# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *APRES* CETTE LIGNE =-=-=-=-=-=-=-=-=-=

number_of_robots = 1  # 8 robots identiques placés dans l'arène

arena = get_arena(arena_index)

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
