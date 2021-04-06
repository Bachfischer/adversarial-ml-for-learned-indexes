import numpy as np
import csv
import random
from enum import Enum

class Distribution(Enum):
	BINOMIAL = 0
	EXPONENTIAL = 1
	LOGNORMAL = 2
	NORMAL = 3
	POISSON = 4
	RANDOM = 5

def get_data(distribution, size):
	data = []
	if distribution == Distribution.RANDOM:
		data = random.sample(range(2, size * 2), size)
	elif distribution == Distribution.BINOMIAL:
		data = np.random.binomial(100, 0.5, size)
	elif distribution == Distribution.POISSON:
		data = np.random.poisson(6, size)
	elif distribution == Distribution.EXPONENTIAL:
		data = np.random.exponential(10, size)
	elif distribution == Distribution.LOGNORMAL:
		data = np.random.lognormal(0, 2, size)
	else:
		data = np.random.normal(1000, 100, size)
	return data

def get_sorted_data(distribution, size):
	data = get_data(distribution, size)
	data.sort()
	return data

def generate_data(distribution, data_size, filename):
	data = get_sorted_data(distribution, data_size)

	multiplicant = 1
	if distribution == Distribution.EXPONENTIAL:
		multiplicant = 10000000
	elif distribution == Distribution.LOGNORMAL:
		multiplicant = 10000

	data_path = "./data/" + filename + ".csv"
	with open(data_path, 'w') as csv_file:
		csv_writer = csv.writer(csv_file)
		for index, number in enumerate(data):
			csv_writer.writerow([int(number * multiplicant), index+1])

if __name__ == "__main__":
	# generate_data(Distribution.BINOMIAL, data_size = 50, filename = "binomial_50")
	# generate_data(Distribution.EXPONENTIAL, data_size = 50, filename = "exponential_50")
	# generate_data(Distribution.LOGNORMAL, data_size = 50, filename = "lognormal_50")
	# generate_data(Distribution.NORMAL, data_size = 50, filename = "normal_50")
	# generate_data(Distribution.POISSON, data_size = 50, filename = "poisson_50")
	generate_data(Distribution.RANDOM, data_size = 50, filename = "random_50")
