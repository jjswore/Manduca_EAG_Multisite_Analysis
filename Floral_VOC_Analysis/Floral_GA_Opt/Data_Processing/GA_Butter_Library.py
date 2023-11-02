import time
from deap import base, creator, tools
import pandas as pd
from Floral_VOC_Analysis.Floral_GA_Opt.Classification.EAG_Classifier_Library import TT_Split, PCA_Constructor
from Floral_VOC_Analysis.Floral_GA_Opt.Data_Processing.EAG_DataProcessing_Library import butter_bandpass_filter
import random
import numpy as np
def create_individual():
    #print('creating individual')
    return {
        'lowcut_c1': random.uniform(.00001, 1),
        'highcut_c1': random.uniform(1.001, 6),
        'order_c1': random.randint(1, 4),
        'lowcut_c2': random.uniform(.00001, 1),
        'highcut_c2': random.uniform(1.001, 6),
        'order_c2': random.randint(1, 4)}

def apply_filter_to_dataframe(dataframe, lowcut, highcut, fs=1000, order=1):
    #print('applying filter to dataframe')
    # creates a new DataFrame with the same structure as the input DataFrame
    filtered_dataframe = pd.DataFrame(columns=dataframe.columns, index=dataframe.index)

    # iterates over the rows of the input DataFrame
    for index, row in dataframe.iterrows():
        # applies the butterworth bandpass filter to the current row
        filtered_row = butter_bandpass_filter(row, lowcut, highcut, fs, order)

        # stores the filtered row in the new DataFrame
        filtered_dataframe.loc[index] = filtered_row

    return filtered_dataframe

def GA_EVAL_FDR_MultiClass(individual, data, _scaling_memory=[None]):
    CH1 = data.iloc[:, :9000]
    CH2 = data.iloc[:, 9000:]
    #META = data.iloc[:, -3:]
    #CH1 = pd.concat([CH1, META], axis=1)

    CH1buttered_df = apply_filter_to_dataframe(dataframe=CH1.iloc[:, :-3],
                                            lowcut=individual['lowcut_c1'],
                                            highcut=individual['highcut_c1'],
                                            order=individual['order_c1'])

    CH2buttered_df = apply_filter_to_dataframe(dataframe=CH2.iloc[:, :-3],
                                            lowcut=individual['lowcut_c2'],
                                            highcut=individual['highcut_c2'],
                                            order=individual['order_c2'])

    buttered_df = pd.concat([CH1buttered_df,CH2buttered_df, data.iloc[:, -3:]], axis=1)

    pca_df, _, _ = PCA_Constructor(buttered_df.iloc[:, :-3], 2)
    PCA_DF = pd.concat([pca_df, buttered_df.iloc[:, -3:]], axis=1)

    # Calculate the overall mean of the data
    overall_mean = PCA_DF.iloc[:, :-3].mean()

    # Calculate the within-class scatter matrix
    S_W = sum([PCA_DF[PCA_DF['label'] == label].iloc[:, :-3].cov() * len(PCA_DF[PCA_DF['label'] == label])
               for label in PCA_DF['label'].unique()])

    # Calculate the between-class scatter matrix
    class_means = PCA_DF.groupby('label').mean()
    S_B = sum([(mean - overall_mean).values.reshape(-1, 1).dot((mean - overall_mean).values.reshape(1, -1)) * len(
        PCA_DF[PCA_DF['label'] == label])
               for label, mean in class_means.iterrows()])

    # Calculate Fisher's Discriminant Ratio for multiple classes
    FDR = np.linalg.det(S_B) / np.linalg.det(S_W)

    # If the scaling factor isn't already computed, calculate and store it
    if _scaling_memory[0] is None:
        _scaling_memory[0] = 10 ** (-np.floor(np.log10(np.abs(FDR))))
        #print(_scaling_memory[0])
    # Use the stored scaling factor to scale the FDR
    FDR_scaled = FDR * _scaling_memory[0]

    return FDR_scaled,

def dict_mutate(individual, mu, sigma, indpb):
    for key in individual:
        if random.random() < indpb:
            gauss_val = random.gauss(mu,sigma)
            #print('\n')
            #print('key:', key)
           # print('gauss va:', gauss_val)
            #print('individual before mutation', individual)
            individual[key] += gauss_val
            individual['lowcut_c1'] = max(.00001, min(1., individual['lowcut_c1']))
            individual['highcut_c1'] = max(1.01, min(6., individual['highcut_c1']))
            individual['order_c1'] = int(round(max(1, min(4, individual['order_c1']))))
            individual['lowcut_c2'] = max(.00001, min(1., individual['lowcut_c2']))
            individual['highcut_c2'] = max(1.01, min(6., individual['highcut_c2']))
            individual['order_c2'] = int(round(max(1, min(4, individual['order_c2']))))
            #print('after mutation', individual)
            #print('\n' )
    return individual,

def dict_mate(ind1, ind2, eta, indpb):
    ol = [o1, o2] = ind1.copy(), ind2.copy()
    for key in ind1:
        x1, x2 = o1[key], o2[key]
        rand = random.random()
        if rand <= indpb:
            beta = 2. * rand
        else:
            beta = 1. / (2. * (1. - rand))
        beta **= 1. / (eta + 1.)
        o1[key] = 0.5 * (((1 + beta) * x1) + ((1 - beta) * x2))
        o2[key] = 0.5 * (((1 - beta) * x1) + ((1 + beta) * x2))
        for o in ol:
            o['lowcut_c1'] = max(.00001, min(1, o['lowcut_c1']))
            o['lowcut_c2'] = max(.00001, min(1, o['lowcut_c2']))
            o['highcut_c1'] = max(1.01, min(6, o['highcut_c1']))
            o['highcut_c2'] = max(1.01, min(6, o['highcut_c2']))
            o['order_c1'] = int(round(max(1, min(4, o['order_c1']))))
            o['order_c2'] = int(round(max(1, min(4, o['order_c2']))))
    return o1, o2

def main(data, POPULATION_SIZE, TOURNAMENT_SIZE, CROSS_PROB, MUT_PROB, G):
    # Register the custom initialization function in the toolbox
    print('initializing.....')
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", dict, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", GA_EVAL_FDR_MultiClass)
    toolbox.register("mate", dict_mate, eta=20.0, indpb=CROSS_PROB)
    toolbox.register("mutate", dict_mutate, mu=0, sigma=1, indpb=MUT_PROB)
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    hof = tools.HallOfFame(1)
    print('populating.....')
    population = toolbox.population(n=POPULATION_SIZE)
    # perform evaluation of each individual in the population
    print('initial evaluation of the population')
    fitnesses = list(map(toolbox.evaluate, population, [data] * len(population)))
    #print('initial evaluation of the population')
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        #fitnesses = list(executor.map(lambda ind_data: toolbox.evaluate(*ind_data), zip(population, [data] * len(population))))

    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    # get all the fitnesses in the population
    fits = [ind.fitness.values[0] for ind in population]
    EvolutionStats = {'Generation': [], 'Population': [], 'Mean Fitness': [], 'Max Fitness': [], 'Min Fitness': [],
                      'Fitness STD': []}
    # perform the evolution for G generations (G is set as an argument for the main function)
    g = 0
    max_fitnesses = []
    no_improvement = 0
    MAX_NO_IMPROVEMENT = 15  # change this to the number of generations without improvement you want to tolerate
    while g < G:
        max_fitness = round(max(fits), 5)
        if max_fitnesses and max_fitness <= max(max_fitnesses):
            no_improvement += 1
        else:
            no_improvement = 0
        max_fitnesses.append(max_fitness)

        if no_improvement >= MAX_NO_IMPROVEMENT:
            print(f"Stopping early: Maximum fitness hasn't improved for {MAX_NO_IMPROVEMENT} generations.")
            break
    # print generation number
        g = g + 1
        #print(f' Generation: {g}')
        # select offspring from the population via the tournament. individuals with best accuracy
        # proceed to the offspring and next generation
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        #print('mating')
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CROSS_PROB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        #print('mutating')
        for mutant in offspring:
            if random.random() < MUT_PROB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # mutated and crossed over individuals will not have a fitness and need to be evaluated
        # only evaluated individuals that need evaluting and dont have a fitness (accuracy score)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fitnesses = list(map(toolbox.evaluate, invalid_ind, [data] * len(invalid_ind)))
        #with concurrent.futures.ThreadPoolExecutor() as executor:
            #fitnesses = list(executor.map(lambda ind_data: toolbox.evaluate(*ind_data), zip(invalid_ind, [data] * len(invalid_ind))))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        population[:] = offspring
        hof.update(population)
        fits = [ind.fitness.values[0] for ind in population]
        #calculate some statistics about the population
        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5
        print(f'----------GENERATION {g}----------')
        print(f'_Population Size_  _Mean Fitness_  _Max Fitness_  _Min Fitness_ _Fitness STD_')
        print(f'     {length}         {mean}    {max(fits)}    {min(fits)}     {std}')
        # Inside the loop for each generation:
        EvolutionStats['Generation'].append(g)
        EvolutionStats['Population'].append(length)
        EvolutionStats['Mean Fitness'].append(mean)
        EvolutionStats['Max Fitness'].append(max(fits))
        EvolutionStats['Min Fitness'].append(min(fits))
        EvolutionStats['Fitness STD'].append(std)
        print(f'best parameters found: {hof[0]}')
    print(f'best parameters found: {hof[0]}')

    return hof[0], EvolutionStats