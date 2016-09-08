from .State import State
from random import randint
import numpy
import math
import random
import datetime, time
import operator

class Controller:

	def __init__(self, load, state):
		self.initialize_parameters(load, state)

	def initialize_parameters(self, load, state):
		self.state = state
		if load == None:
			self.parameters = numpy.random.normal(0, 1, 4*len(self.compute_features()))
			print self.parameters
		else:
			params = open(load, 'r')
			weights = params.read().split("\n")
			self.parameters = [float(x.strip()) for x in weights[0:-1]]
			if len(self.parameters) != 4*len(self.compute_features()):
				print "Numero incorreto de pesos no arquivo informado"
				exit()
			print self.parameters

	def output(self, episode, performance):
		print "Performance do episodio #%d: %f" % (episode, performance)
	
		if episode > 0:
			output = open("./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'), "w+")
			for parameter in self.parameters:
				output.write(str(parameter) + "\n")

    #FUNCAO A SER COMPLETADA. Deve utilizar os pesos para calcular as funcoes de preferencia Q para cada acao e retorna
    #1 caso a acao desejada seja direita, 2 caso seja esquerda, 3 caso seja nula, e 4 caso seja atirar
	def take_action(self, state):

	#FUNCAO A SER COMPLETADA. Deve calcular features expandidas do estados
	def compute_features(self):

	#FUNCAO A SER COMPLETADA. Deve atualizar a propriedade self.parameters
	def update(self, episode, performance):