import time
from deap import base, creator, tools
import pandas as pd
from Manduca_Multisite_EAG_Analysis.Floral_VOC_Analysis.Floral_GA_Opt.Classification.EAG_Classifier_Library import TT_Split, PCA_Constructor
from EAG_DataProcessing_Library import butter_bandpass_filter
import random
def create_individual():
    print('creating individual')
    return {
        'lowcut': random.uniform(.00001, 1),
        'highcut': random.uniform(1.001, 5),
        'order': random.randint(1, 4)}

def apply_filter_to_dataframe(dataframe, lowcut, highcut, fs=1000, order=1):
    print('applying filter to dataframe')
    # creates a new DataFrame with the same structure as the input DataFrame
    filtered_dataframe = pd.DataFrame(columns=dataframe.columns, index=dataframe.index)

    # iterates over the rows of the input DataFrame
    for index, row in dataframe.iterrows():
        # applies the butterworth bandpass filter to the current row
        filtered_row = butter_bandpass_filter(row, lowcut, highcut, fs, order)

        # stores the filtered row in the new DataFrame
        filtered_dataframe.loc[index] = filtered_row

    return filtered_dataframe

from itertools import combinations

def GA_EVAL(individual, data):
    buttered_df = apply_filter_to_dataframe(dataframe=data.iloc[:,:-3],
                                            lowcut=individual['lowcut'],
                                            highcut=individual['highcut'],
                                            order=individual['order'])
    buttered_df = pd.concat([buttered_df, data.iloc[:,-3:]], axis=1)
    print('Finding the principal components.. ')
    pca_df, _, _ = PCA_Constructor(buttered_df.iloc[:, :-3], 10)
    PCA_DF = pd.concat([pca_df, buttered_df.iloc[:, -3:]], axis=1)

    # Calculate the variance of each class
    class_variances = PCA_DF.groupby('label').var() # replace 'class' with your actual class column name

    # Calculate the total variance for each class
    class_variance_sums = class_variances.sum(axis=1)

    # Calculate the absolute difference in variance for each pair of classes
    pairs = combinations(class_variance_sums.index, 2)
    variance_differences = [abs(class_variance_sums[a] - class_variance_sums[b]) for a, b in pairs]

    # Sum up all the differences to get the fitness value
    fitness_value = sum(variance_differences)

    return fitness_value,

def dict_mutate(individual, mu, sigma, indpb):
    for key in individual:
        if random.random() < indpb:
            individual[key] += random.gauss(mu, sigma)
            individual['lowcut'] = max(.00001, min(1., individual['lowcut']))
            individual['highcut'] = max(1.01, min(5., individual['highcut']))
            individual['order'] = int(round(max(1, min(4, individual['order']))))
            print(individual)
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
            o['lowcut'] = max(.00001, min(1, o['lowcut']))
            o['highcut'] = max(1.01, min(5, o['highcut']))
            o['order'] = int(round(max(1, min(4, o['highcut']))))
    return o1, o2

# Register the custom initialization function in the toolbox
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def main(data, POPULATION_SIZE, TOURNAMENT_SIZE, CROSS_PROB, MUT_PROB, G):
    # Register the custom initialization function in the toolbox
    #print('initializing.....')
    toolbox.register("evaluate", GA_EVAL)
    toolbox.register("mate", dict_mate, eta=20.0, indpb=CROSS_PROB)
    toolbox.register("mutate", dict_mutate, mu=0, sigma=1, indpb=MUT_PROB)
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    hof = tools.HallOfFame(1)
    #print('populating.....')
    population = toolbox.population(n=POPULATION_SIZE)
    # perform evaluation of each individual in the population
    #print('initial evaluation of the population')
    fitnesses = list(map(toolbox.evaluate, population, [data] * len(population)))
    #print('initial evaluation of the population')
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        #fitnesses = list(executor.map(lambda ind_data: toolbox.evaluate(*ind_data), zip(population, [data] * len(population))))

    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    # get all the fitnesses in the population
    fits = [ind.fitness.values[0] for ind in population]
    ...
    EvolutionStats = {'Generation': [], 'Population': [], 'Mean Fitness': [], 'Max Fitness': [], 'Min Fitness': [],
                      'Fitness STD': []}
    # perform the evolution for G generations (G is set as an argument for the main function)
    g = 0
    max_fitnesses = []
    no_improvement = 0
    MAX_NO_IMPROVEMENT = 15  # change this to the number of generations without improvement you want to tolerate
    while g < G:
        max_fitness = round(max(fits))
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

    return hof[0], EvolutionStats


start = time.time()

LLL_df = pd.read_csv('Cov_health_QC_T_1.csv', index_col=0)
print('first split')
train_features, test_features, train_labels, test_labels =TT_Split(LLL_df)
# Get the indices of the train_features DataFrame
train_indices = train_features.index
# Select the corresponding rows from the LLL_df
train_labels_df = LLL_df.iloc[:,-3:].loc[train_indices]
# Concatenate train_features and train_labels_df
df = pd.concat([train_features, train_labels_df], axis=1)
params, statistics=main(data=df, POPULATION_SIZE=100, TOURNAMENT_SIZE=3, CROSS_PROB=.5, MUT_PROB=.25, G=150)

buttered_df = apply_filter_to_dataframe(dataframe=LLL_df.iloc[:, :-3],
                                            lowcut=params['lowcut'],
                                            highcut=params['highcut'],
                                            order=params['order'])
print('here are the parameters:', params)
print(' here are the statistics:', statistics)

end = time.time()
total_time = end - start
print("\n"+ str(total_time))

STATSDF=pd.DataFrame(statistics)
BDF = pd.concat([buttered_df, LLL_df.iloc[:,-3:]], axis=1)
PDF = pd.DataFrame.from_dict(params, orient='index').T


PDF.to_csv('Cov_health_QC1_BestParams.csv')
BDF.to_csv('Cov_health_QC1_finalDF.csv')
STATSDF.to_csv('Cov_health_Q1_STATS.csv')
print('the entire code has finished')

## from here I need to decide how I will proceed... Do I reprocess my data? no I think I return the best
## data frame right?