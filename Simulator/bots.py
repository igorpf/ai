import AI
from random import randint

class Bots:
	
	#difficulty:
	#lazy_bot (sempre girando) -> 0
	#random_bot (comandos aleatorios) -> 1
	#normal_bot (mistura random e ninja) -> 2
	#ninja_bot (aimbot que sabe desviar) -> 3

	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.last_command = 5
		self.command_counter = 0
		self.last_distance = 0
		self.ninja_dodge = False

	def take_random_action(self):
		if self.command_counter < 30: #to not be a crazy bot -> change action after 1s
			self.command_counter += 1
			return self.last_command
		else:
			rand = randint(0,5)
			self.last_command = rand
			self.command_counter = 0
			return rand

	def take_ninja_action(self,state):
		if (state.dist_arrow < 150 or state.arrow_sight == True):
			if self.command_counter < 10: 
				self.command_counter += 1
				if self.command_counter == 10:
					self.ninja_dodge = True
				return self.last_command
			else:
				rand = randint(0,1)
				if rand == 0:
					return 1
				else:
					self.last_command = rand
					self.command_counter = 0
					return 2
		elif self.ninja_dodge == True:
			if self.command_counter < 10: 
				self.command_counter += 1
				if self.command_counter == 10:
					self.ninja_dodge = False
				return 5
		elif state.enemy_sight == True:
			return 4

		else:
			rand = randint(0,1)
			if rand == 1:
				rand = 2
			else:
				rand = 5
			self.last_command = rand
			self.command_counter = 0
			return rand


	def take_action(self,state):
		if self.difficulty == 0: #lazy_bot
			return 2 #2 - esquerda

		elif self.difficulty == 1: #random_bot
			return self.take_random_action()

		elif self.difficulty == 2: #normal_bot
			rand = randint(0,9)
			if rand < 5:
				return self.take_random_action()
			else:
				return self.take_ninja_action(state)
		else: #ninja_bot
			return self.take_ninja_action(state)
