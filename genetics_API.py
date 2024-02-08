import random
import math
# _______________________________ Calcul des scores _______________________________ #
# Calcul du score pour la vitesse

def score_vitesse_append(translation, rotation, score_vitesse_iteration):
    score_vitesse_iteration.append(translation * (1 - abs(rotation)))

def score_vitesse(score_vitesse_iteration):
    return sum(score_vitesse_iteration)

# Calcul du score pour la couverture de l'environnement
def env_passage(arene, position, robotId):
    x = int(position[0] // len(arene))
    y = int(position[1] // len(arene[0]))
    
    if x >= len(arene) :
        x = len(arene) - 1
    if y >= len(arene[0]):
        y = len(arene[0]) - 1

    arene[x][y] = -1 * robotId
    
def score_couverture(arene):
    score = 0
    width_arene = len(arene)
    height_arene = len(arene[0])

    for k in range(width_arene * height_arene):
        i = k // width_arene
        j = k % width_arene

        if arene[i][j] <= 0:
            score += 1

    return score

def calculate(distanceList, score_couverture_list, score_list, score_vitesse_iteration, position, areneCopy, posInit):
    # évaluation de la distance
    scoreDistance = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) ) # distance parcourue entre le milieu et un point quelconque avec les paramètres comportementparam précédents
    distanceList.append(scoreDistance) # on ajoute la distance effectuée à pendant 3 itération à une liste dont on va calculer la distance totale

    # On compare la vitesse de translation et la vitesse de rotation sur les itérations
    scoreVitesse = score_vitesse(score_vitesse_iteration)
    score_vitesse_iteration.clear()
    score_list.append(scoreVitesse) 
    
    # On compare le score de couverture sur l'environnement:
    scoreCouverture = score_couverture(areneCopy)
    score_couverture_list.append(scoreCouverture)
    
    return distanceList, score_list, score_couverture_list

def evaluate(arena, orientationEval, robotId, posInit, posEvaluation, rob, param, score_list, score_couverture_list, distanceList, final_couverture_list, final_distance_list, final_vitesse_list):
    if orientationEval % 3 == 0 and orientationEval != 0:
        finalScoreVitesse = sum(score_list) # on fait d'abord la somme des distances parcourues avec les 3 évaluations
        final_vitesse_list.append(finalScoreVitesse)
        score_list.clear() # on efface le contenu de la liste pour le prochain comportement
        
        finalScoreCouverture = sum(score_couverture_list)
        final_couverture_list.append(finalScoreCouverture)
        score_couverture_list.clear()

        finalScoreDistance = sum(distanceList)
        final_distance_list.append(finalScoreDistance)
        distanceList.clear()
        

        if posEvaluation % 2 == 0 and posEvaluation != 0:
            finalPosDistance = sum(final_distance_list)
            final_distance_list.clear()

            finalPosVitesse = sum(final_vitesse_list) 
            final_vitesse_list.clear()

            finalPosCouverture = sum(final_couverture_list)
            final_couverture_list.clear()

            if bestScoreVitesse > finalPosVitesse and bestScoreCouverture < finalPosCouverture and bestScoreDistance < finalPosDistance:
                bestScoreVitesse = finalPosVitesse
                bestScoreCouverture = finalPosCouverture
                bestScoreDistance = finalPosDistance

                bestParam = param.copy()

                bestIteration = rob.iterations 
                saveParams(bestIteration, bestScoreVitesse, bestParam) 
                print(
                        'iteration:', rob.iterations,
                        '\tenfant: ', param,
                        '\tscore Vitesse: ', finalPosVitesse,
                        '\tscore Couverture: ', finalPosCouverture,
                        '\score Distance: ', finalPosDistance
                    )

        else:
            x = random.randint(0, len(arena) - 1) 
            y = random.randint(0, len(arena[0]) - 1)
            rob.controllers[robotId].set_position(x, y) # on place le robot à son point d'initiation
    else:
        orientation = random.randint(0, 360) # l'orientation est un entier aléatoire comprise entre 0 et 360
        rob.controllers[robotId].set_absolute_orientation(orientation) # on l'oriente au nombre tiré aléatoirement
    
    return finalPosDistance + finalPosVitesse + finalPosCouverture
     
# _____________________Etapes d'optimisation stochastique de la population___________________ #

# Etape 1 : Variation et génération de la population candidate
def generate_child(parents, population, k, mu, lamda):
    nb_enfants = lamda / mu # nombre d'enfants par parent
    indexes = [random.randint(0, len(parents[0]-1))] # k indices aléatoires où il faut changer la valeur pour la mutation

    for parent in parents:
        for _ in range(nb_enfants):
            for i in indexes:
                child = parent.copy()
                child[i] = random.randint(-1,1) 
                population[child] = 0
        population[parent] = 0
    return parents, population

# Etape 2 : Sélection des meilleurs candidats
def selection(parents, population, k, mu, lamda):
    sorted_population = dict(sorted(population.items(), key=lambda item: item[1], reverse=True)) # on trie la liste de la population en fonction de leur score
    parents = list(sorted_population.items())[:5] # on retourne les 5 meilleurs score 
    return parents

# _______________________________ Fonctions utilitaires________________________ #

# Sauvegarde des meilleurs paramètres 
def saveParams(bestIteration, bestDistance, bestParam):
    with open("best_params.txt", "w") as file:
        file.write("Meilleurs paramètres:\n")
        file.write("Distance: " + str(bestDistance) + "\n")
        file.write("Paramètre: " + str(bestParam) + "\n")
        file.write("Iteration: " + str(bestIteration) + "\n")