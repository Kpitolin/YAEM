#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import csv
import time

initial_bend_radius = 10000.0
initial_iris_size = 0.0
initial_phi1_angle = 0.0
initial_refractive_index = 1.35
genes_list = ["bend_radius", "iris_size", "𝚽1_angle", "refractive_index"]
characteristics_list = ["depth", "aperture", "r1", "viewing_angle"]
individual_list  = []

# Constants
I_square_root = numpy.exp(3)
omega = 1.5

# one time I/O operation

def retrieve_r1_list():

	r1_list = []
	with open("data/indice_refraction_facile.csv",'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader, None)
		for row in reader:
			r1_list.append(row)
	return r1_list

global_r1_list = retrieve_r1_list()



def create_individual(bend_radius = initial_bend_radius, iris_size = initial_iris_size, phi1_angle = initial_phi1_angle, refractive_index = initial_refractive_index):
	"""
	Returns an individual instance with the following attributes : 
	bend radius, iris size, 𝚽1 angle, refractive index
	"""
	return {"bend_radius":bend_radius, "iris_size":iris_size, "𝚽1_angle":phi1_angle, "refractive_index":refractive_index, "fitness" : -1.0}

def initialize_individual_population(population_size = 200):

	for i in range(population_size):
		indiv = create_individual()
		indiv["fitness"] = compute_individual_fitness(indiv)
		individual_list.append(indiv)

	return individual_list

def replace_random_individual(replacement_individual):
	index_of_individual_to_delete  = numpy.random.randint(0,len(individual_list))
	individual_list[index_of_individual_to_delete] = replacement_individual

def mutate_individual(individual):
	"""
	Mutates the individual by adding a random value (following a normal distribution) to each gene  (attribute)
	Reduce  so that individuals don't go to a "dead" zone. Put mutation ratio extra low, then increase it if evolution is too slow.  
	Mutation ratio corresponds to standard deviation
	Mutation ratio is the probability associated with mutation	

	Returns the mutated individual

	"""

# if (numpy.random.normal(10,5,1)[0])> 10:
	# for gene in genes_list:
	# 	individual[gene] += numpy.random.normal()
	individual["bend_radius"] += numpy.random.normal(0, 0.0010)
	if individual["bend_radius"] == omega / 2:
		individual["𝚽1_angle"] += numpy.random.normal(0, 0.00157)

	individual["iris_size"] += numpy.random.normal(0, 0.00075)
	individual["refractive_index"] += numpy.random.normal(0, 0.0002)


	return individual



# Comopute fitness just after mutation 
def run_tournament(population_size = 200, ratio = 0.02):

	"""
	We make a tournament with ratio % of population size
	Comment : compute_individual_fitness when the max is reproducing
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

		if individual_list[index]["fitness"] > value_of_max:
			value_of_max = individual_list[index]["fitness"]
			index_of_max = index

	print "max"
	print individual_list[index_of_max]

	individual_baby = run_individual_reproduction(individual_list[index_of_max])
	replace_random_individual(mutate_individual(individual_baby))

	if not is_individual_valid(individual_baby):
		individual_baby["fitness"] = 0.0
	else :
		print "bruh"
		individual_baby["fitness"] = compute_individual_fitness(individual_baby)
	

	

def run_individual_reproduction(parent_individual):
	"""
	Run the reproduction process for an individual : copies all genes from parent
	"""
	baby = {}

	for gene in genes_list:
		baby[gene] = parent_individual[gene]
	baby["fitness"] = -1.0
	return baby


def is_individual_valid(individual):

	characteristics = compute_individual_characteristics(individual)
	A = numpy.sqrt(numpy.exp(1) / ( 0.746 * I_square_root))
	if individual["bend_radius"] > 10000 or individual["bend_radius"] < omega / 2 \
	or individual["iris_size"] < 0 or individual["iris_size"] > omega / 2 \
	or individual["𝚽1_angle"] < 0 or individual["𝚽1_angle"] >= numpy.pi \
	or individual["refractive_index"] > 1.55 or individual["refractive_index"] < 1.35 :
		print "error 1"
		return False

	elif (not individual["𝚽1_angle"] == 0 and not individual["bend_radius"] == omega / 2):
		print "error 2"
		return False
	elif (not individual["𝚽1_angle"] == 0 and individual["iris_size"] > omega * numpy.cos(individual["𝚽1_angle"]) / 2 ):
		print "error 3"
		return False
	elif (individual["refractive_index"] == 1.35 and individual["𝚽1_angle"] == 0 and individual["iris_size"] > 1.0/2 * (omega - A)):
		print "error 4"
		return False
	elif (individual["refractive_index"] == 1.35 and not individual["𝚽1_angle"] == 0 and individual["iris_size"] > 1.0/2 * (omega *  numpy.cos(individual["𝚽1_angle"]) - A)):
		print "error 5"
		return False
	elif (not individual["refractive_index"] == 1.35 and  ((characteristics["depth"] > characteristics["r1"] * characteristics["aperture"] / 2) or characteristics["depth"] < characteristics["aperture"] / 2)):
		print "error 6"
		return False
	else:
		return True 


def retrieve_r1_list():

	r1_list = []
	with open("data/indice_refraction_facile.csv",'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader, None)
		for row in reader:
			r1_list.append(row)
	return r1_list

def find_r1(refractive_index):
	r1_list = global_r1_list
	r1 = 0

	for r1_values in r1_list:
		if refractive_index >= float(r1_values[1]) :
			r1 = float(r1_values[0])
	return r1

def compute_individual_characteristics(individual):
	individual_characteristics = {}
	

	if individual["bend_radius"] == omega / 2:
		individual_characteristics["depth"] = (omega / 2) * (1 + numpy.sin(individual["𝚽1_angle"]))
		individual_characteristics["aperture"] = omega * numpy.cos(individual["𝚽1_angle"]) - 2 * individual["iris_size"]
		individual_characteristics["r1"] = find_r1(individual["refractive_index"])
		if individual["refractive_index"] == 1.35:
			individual_characteristics["viewing_angle"] = 2 * numpy.arctan(individual_characteristics["aperture"] / 2 * individual_characteristics["depth"])

		elif individual["refractive_index"] > 1.35:

			A =  (numpy.square(individual_characteristics["r1"]) * individual_characteristics["aperture"]) / (2 * individual_characteristics["depth"])
			B = 1 + numpy.square(individual_characteristics["r1"]) - (A * individual_characteristics["aperture"] / (2 * individual_characteristics["depth"]))
			C = 1 + numpy.square(individual_characteristics["r1"])
			individual_characteristics["viewing_angle"] = 2 * numpy.arcsin((A-numpy.sqrt(B))/ C)

	elif individual["bend_radius"] > omega / 2:

		D = numpy.square(individual["bend_radius"]) - (numpy.square(omega) / 4)
		individual_characteristics["depth"] = individual["bend_radius"] - numpy.sqrt(D)
		individual_characteristics["aperture"] = omega - (2 * individual["iris_size"])
		individual_characteristics["r1"] = find_r1(individual["refractive_index"])

		if individual["refractive_index"] == 1.35:
			individual_characteristics["viewing_angle"] = 2 * numpy.arctan(individual_characteristics["aperture"] / 2 * individual_characteristics["depth"])

		elif individual["refractive_index"] > 1.35:

			A =  (numpy.square(individual_characteristics["r1"]) * individual_characteristics["aperture"]) / (2 * individual_characteristics["depth"])
			B = 1 + numpy.square(individual_characteristics["r1"]) - (A * individual_characteristics["aperture"] / (2 * individual_characteristics["depth"]))
			C = 1 + numpy.square(individual_characteristics["r1"])
			print "B"
			print B
			individual_characteristics["viewing_angle"] = 2 * numpy.arcsin((A-numpy.sqrt(B))/ C)


	return individual_characteristics


def compute_individual_fitness(individual):
	"""
	If object is invalid, fitness is 0, else , it depends on eye spatial resolution
	"""

	spatial_resolution = 0
	individual_characteristics = compute_individual_characteristics(individual)
	print individual_characteristics
	if individual["refractive_index"] == 1.35:
		spatial_resolution = 0.375 * (individual_characteristics["depth"] / individual_characteristics["aperture"]) * numpy.sqrt(numpy.log(0.746* numpy.square(individual_characteristics["aperture"]) * I_square_root))

	elif individual["refractive_index"] > 1.35:
		spatial_resolution = 1 / individual_characteristics["viewing_angle"]

	return spatial_resolution


if __name__ == "__main__":

	individual_list = initialize_individual_population(10)
	i = 0
	while i<50:	
		run_tournament(10, 1)
		i += 1
		


