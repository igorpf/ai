# -*- coding: utf-8 -*-
from .State import State
from random import randint
from parser import parse_weights
import numpy
import math
import random
import datetime, time
import operator
import os
import sys
import random as rand

class Controller:

	def __init__(self, load, state):
		self.features = dict()
		self.best_performance = 0
		self.initialize_parameters(load, state)
		self.params_buffer = []

	def initialize_parameters(self, load, state):
		self.state = state
		if load == None:
			self.parameters = numpy.random.normal(0, 1, 4*len(self.compute_features()))
			print self.parameters
		else:
			self.parameters = parse_weights(4*len(self.compute_features()), load)

	def output(self, episode, performance):
		print "Performance do episodio #%d: %f" % (episode, performance)

		if episode > 0 and episode % 10 == 0:
			if not os.path.exists("./params"):
				os.makedirs("./params")
			output = open("./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'), "w+")
			for parameter in self.parameters:
				output.write(str(parameter) + "\n")

	#FUNCAO A SER COMPLETADA. Deve utilizar os pesos para calcular as funcoes de preferencia Q para cada acao e retorna
	#1 caso a acao desejada seja direita, 2 caso seja esquerda, 3 caso seja nula, e 4 caso seja atirar
	def take_action(self, state):
		self.compute_features()
		features = self.features

		indexes = iter([i for i in range(len(self.parameters))])
		#enemy_not_on_sight, prox, prox_arrow
		qLeft = features['enemy_not_on_sight'] * self.parameters[indexes.next()] + features['prox'] * self.parameters[indexes.next()]+ features['prox_arrow'] * self.parameters[indexes.next()]+ features['enemy_close'] * self.parameters[indexes.next()]
		qRight = features['enemy_not_on_sight'] * self.parameters[indexes.next()] + features['prox'] * self.parameters[indexes.next()]+ features['prox_arrow'] * self.parameters[indexes.next()]+ features['enemy_close'] * self.parameters[indexes.next()]
		qShoot = features['enemy_not_on_sight'] * self.parameters[indexes.next()] + features['prox'] * self.parameters[indexes.next()]+ features['prox_arrow'] * self.parameters[indexes.next()]+ features['enemy_close'] * self.parameters[indexes.next()]
		qNoAction = features['enemy_not_on_sight'] * self.parameters[indexes.next()] + features['prox'] * self.parameters[indexes.next()]+ features['prox_arrow'] * self.parameters[indexes.next()]+ features['enemy_close'] * self.parameters[indexes.next()]

		q = [qLeft, qRight, qShoot, qNoAction]
		maxQ = max(q)
		if  maxQ == qLeft:
			return 2
		elif maxQ == qRight:
			return 1
		elif maxQ == qShoot:
			return 4
		elif maxQ == qNoAction:
			return 3

	#FUNCAO A SER COMPLETADA. Deve calcular features estados
	def compute_features(self):
		self.features['prox'] = (1 / self.state.dist_enemy) * self.state.enemy_sight 			#Calcula proximidade do inimigo - General
		self.features['enemy_not_on_sight'] = 1 - self.state.enemy_sight                        #Caso inimigo não esteja no campo de visão, incentiva a procurá-lo - General
		self.features['prox_arrow'] = (1 / self.state.dist_arrow) * self.state.arrow_sight  	# Calcula proximidade de um tiro do inimigo - Defense
		self.features['enemy_close'] = (1 / (0.25*self.state.dist_enemy))                       #tentar evitar colisões quando ele persegue o inimigo
		#Todo: feature pra escapar da bala
		return self.features
	#FUNCAO A SER COMPLETADA. Deve atualizar a propriedade self.parameters
	def update(self, episode, performance):
		#print "Params", self.parameters, "\n Buffer: ", self.params_buffer
		l = list()
		range = 0.5
		scale = 0.1
		for p in self.parameters: #gera aleatoriamente novos parametros para a próxima iteração
			l += [p + (scale * (rand.random() - range))]
		if performance > self.best_performance:
			self.params_buffer = self.parameters  # guarda o que aprendeu até agora
			self.best_performance = performance
		else: #se não ganhou, volta pro que tinha de melhor até agora
			self.parameters = self.params_buffer

		self.parameters = l  # troca os parametros
