class Step():
	def __init__(self, current, number, winType, char, stepText):
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
		print(self.stepText)
	def printResume(self):
		if self.winType == 'r':
			print(self.current + '/' + self.number + ' in a row ' + self.charText)
		else:
			print(self.current + '/' + self.number + ' ' + self.charText)

class Mission():
	def __init__(self, title, rank, status, url, preReq, steps=[], charUnlock=''):
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
		self.steps = steps
		self.charUnlock = charUnlock

	def printMission(self):
		if self.charUnlock != '':
			for step in self.steps:
				step.printStep()
			print("\tTo unlock " + self.charUnlock + '\n\n')