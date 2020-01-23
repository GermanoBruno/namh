class Step():
	def __init__(self, current, number, winType, char, stepText):
		'''
		# Inicializador da classe step
		# recebe:
			# numero atual e total de wins da missao
			# tipo de win condition
			# lista do nome do personagem
			# texto na integra
		# produz:
			# porcentagem de conclusao do step
			# texto do nome do personagem
		'''
		self.current = current
		self.number = number
		self.winType = winType
		self.stepText = stepText
		self.char = char
		self.charText = ''
		self.percent = float(self.current)/float(self.number)
		for charName in self.char:
			self.charText = self.charText + ' ' + charName
		if self.charText[-1] == '.':
			self.charText = self.charText[:-1]
		self.charText = self.charText[1:]

	def printStep(self):
		# printa o texto do step
		print(self.stepText)

	def printResume(self):
		# printa uma forma resumida do texto do step
		if self.winType == 'r':
			print(self.current + '/' + self.number + ' in a row ' + self.charText)
		else:
			print(self.current + '/' + self.number + ' ' + self.charText)

class Mission():
	def __init__(self, title, rank, status, url, preReq, steps=[], charUnlock=''):
		'''
		# Inicializador da classe mission
		# recebe:
			# titulo da missao
			# rank necessario para faze-la
			# status atual da missao (bloqueada, desbloqueada ou completa)
			# url da missao
			# pre requisitos da missao
			# passos da missao (se desbloqueada)
			# personagem a desbloquear (se desbloqueada) 
		'''
		self.title = title 		# done
		self.rank = rank 		# string
		self.status = status 	#
		#-1 completed, 0 locked, 1 unlocked
		self.url = url 			#
		self.preReq = preReq 	# list of strings
		# if status == 1
		self.steps = steps
		self.charUnlock = charUnlock

	def readMission(self, steps, charUnlock):
		# acho que tá inutil, a checar
		self.steps = steps
		self.charUnlock = charUnlock

	def printMission(self):
		# printa a missao formatada
		if self.charUnlock != '':
			for step in self.steps:
				step.printStep()
			print("\tTo unlock " + self.charUnlock + '\n\n')