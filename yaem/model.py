import numpy

initial_bend_radius = 10000.0
initial_iris_size = 0.0
initial_phi1_angle = 0.0
initial_refractive_index = 1.35
genes_list = ["bend_radius", "iris_size", "phi1_angle", "refractive_index"]
individual_list  = []
 
def create_individual(bend_radius = initial_bend_radius, iris_size = initial_iris_size, phi1_angle = initial_phi1_angle, refractive_index = initial_refractive_index):
	"""
	Returns an individual instance with the following attributes : 
	bend radius, iris size, phi1 angle, refractive index
	"""
	return {"bend_radius":bend_radius, "iris_size":iris_size, "phi1_angle":phi1_angle, "refractive_index":refractive_index, "fitness" : -1.0}

def initialize_individual_population(population_size = 200):

	for i in range(population_size):
		individual_list.append(create_individual())
	return individual_list

def replace_random_individual(individual):

	index_of_individual_to_delete  = numpy.random.randint(0,len(individual_list))
	individual_list[index_of_individual_to_delete] = individual

def mutate_individual(individual):
	"""
	Mutates the individual by adding a random value (following a normal distribution) to each gene  (attribute)
	Returns the mutated individual
	"""
	for gene in genes_list:
		individual[gene] += numpy.random.normal()
	
	return individual


def run_tournament(population_size = 200, ratio = 0.02):

	"""
	We make a tournament with 2% of population size
	"""
	nb_of_participants = population_size * ratio

	participants_index_list = []
	while len(participants_index_list) < nb_of_participants:

		index = numpy.random.randint(0,len(individual_list))

		if index not in participants_index_list:
			participants_index_list.append(index)

	index_of_max = -1
	value_of_max = -1

	for index in participants_index_list:
		if individual_list[index]["fitness"] == -1:
			compute_individual_fitness(individual_list[index])
		if individual_list[index]["fitness"] > value_of_max:
			value_of_max = individual_list[index]["fitness"]
			index_of_max = index

	individual_baby = run_individual_reproduction(individual_list[index_of_max])
	replace_random_individual(mutate_individual(individual_baby))

	

	pass

# def run_individual_reproduction():
# 	"""
# 	"""
# 	pass

# def is_individual_valid():


# def compute_individual_fitness():
# 	"""
# 	"""
# 	pass


