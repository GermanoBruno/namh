''' organizacao do codigo
	# operacoes possiveis:
	# definir current team
	# inserir nova missao
	# 

	#mods
		# modificacao: ter todas as missoes salvas, marcar as missoes como completas ou não, e ter as limitacoes para cada uma
		# modificacao: pegar nivel e xp do site

	# Formato missao:
		#	linha 1: 			personagem a ser desbloquado
		#	linhas seguintes:	numero wins, n ou r(normal, row), personagem
		# e.g.: 
			#	Naruto Uzumaki (S)
			#	2 r naruto
			#	8 n naruto
			#	0
		# steps como dictionaries
		#	step.number = 2
		#	step.win_type = r
		#	step.char = 'naruto'
		# missoes como lista de steps
		#

	# to do:
		# classe step
			# criar DONE
		# classe mission
			# criar DONE
		# BD
			# criar arquivo DONE
			# atualizar lista de chars DONE
			# criar missoes para cada char
			# xp e nível (scraping)
			# mudar charList pra classe
		# logicas
			# inserir missao
			# result de partida (scraping?)
		# current team
		#
		#
		#
		#
		#
'''

'''
	1. Ver Missoes
		1. Todas
			Display todas as missoes atuais
		2. Time atual
			Display missoes com os personagens usados
	2. Mudar Time Atual
		Muda o time atual
	3. Times Favoritos
		Display times favoritados pelo user
	4. META Teams
		Display meta teams de acordo com os bonecos habilitados (criar tabela de acordo com a sessão)
	5. Inspecionar Time
		Mostra o time inimigo, com os textos das habilidades
		Pode ser aprimorado pra mostrar jogabilidade basica dos bonecos (playing with/playing against)
	0. Sair


'''


#from bd import *
from classes import *
from webScrape import *
from bd import *

import operator


def modificarTimeAtual(charList):
	timeAtual = ['', '', '']
	while timeAtual[0] not in charList:
		timeAtual[0] = input("Qual o primeiro membro da equipe?\n")
	while (timeAtual[1] not in charList) and timeAtual[1] != timeAtual[0]:
		timeAtual[1] = input("Qual o segundo membro da equipe?\n")
	while (timeAtual[2] not in charList) and ((timeAtual[2] != timeAtual[0]) and (timeAtual[2] != timeAtual[1])):
		timeAtual[2] = input("Qual o terceiro membro da equipe?\n")
	return timeAtual

def atualizarMissoes(session):
	missionListList = acharMissao(session)
	# Tentar sort pelo nome
	for missionList in missionListList:
		for mission in missionList:
			mission.printMission()
			#printar "Para habilitar + nome do personagem" depois de todo step set

def missoesPorPersonagem(session):
	missionListList = acharMissao(session)
	allSteps = []
	for missionList in missionListList:
		for mission in missionList:
			if mission.charUnlock != '':
				for step in mission.steps:
					allSteps.append(step)
	allSteps.sort(key=operator.attrgetter('charText'))
	for step in allSteps:
		step.printResume()

def missoesMaisConcluidas(session):
	missionListList = acharMissao(session)
	allSteps = []
	for missionList in missionListList:
		for mission in missionList:
			if mission.charUnlock != '':
				for step in mission.steps:
					allSteps.append(step)
	allSteps.sort(key=operator.attrgetter('percent'))
	for step in allSteps:
		step.printResume()

def missoesPorTipo(session):
	missionListList = acharMissao(session)
	allSteps = []
	for missionList in missionListList:
		for mission in missionList:
			if mission.charUnlock != '':
				for step in mission.steps:
					allSteps.append(step)
	allSteps.sort(key=operator.attrgetter('winType'))
	for step in allSteps:
		step.printResume()

def missoesParaTime(session, time):
	missionListList = acharMissao(session)
	for missionList in missionListList:
		for mission in missionList:
			if mission.charUnlock != '':
				# fazer if pra ver se o char do step esta no time
				for step in mission:
					if step.charText in bdcharList():
						a=1
		


logSuccess = 0
print("  Bem vindo :)\n\n\n  Realize seu login\n")
while logSuccess == 0:
	nick = input("Digite o login\n")
	senha = input("Digite a senha\n")
	sessao, logSuccess = login(nick, senha)
	if logSuccess == 0:
		print("Credenciais invalidas, tente novamente\n\n")

print("\n\n\n\n\n\nQual operacao deseja realizar?")
print("  1. Atualizar missoes (agrupa por missoes)")
print("  2. Organizar missoes por personagem")
print("  3. Organizar por proximidade de conclusao")
print("  4. Organizar por tipo de missao (in a row/normal)")
# implementar
#print("  5. Organizar missoes por time")
#print("  6. Mudar Time Atual")
op = input("  0. Sair do programa\n")
sortByChar = 0
ordem = 'personagem'
timeAtual = []

while(op != '0'):
	if op == '1':
		# atualizar missoes
		# e.g. 
		#	q w (quick game, win)
		# ou
		#	r w 64 (ladder game, win, 64 xp)
		atualizarMissoes(sessao)
	elif op == '2':
		# Sort por personagem
		missoesPorPersonagem(sessao)
	elif op == '3':
		# Missoes disponiveis com o time atual
		missoesMaisConcluidas(sessao)
	elif op == '4':
		missoesPorTipo(sessao)
	elif op == '5':
		# Missoes disponiveis com o time atual
		if timeAtual == []:
			print("Time não especificado\n")
			timeAtual = modificarTimeAtual(listaPersonagens())
		missoesParaTime(sessao, timeAtual)
	elif op == '6':
		timeAtual = modificarTimeAtual(listaPersonagens())
	else:
		print("Entrada invalida")
	print("\n\n\n\n\n\nQual outra operacao deseja realizar?")
	print("  1. Atualizar missoes")
	print("  2. Organizar missoes por personagem")
	print("  3. Organizar por proximidade de conclusao")
	print("  4. Organizar por tipo de missao (in a row/normal)")
	# implementar
	#print("  5. Organizar missoes por time")
	#print("  6. Mudar Time Atual")
	op = input("  0. Sair do programa\n")

print("Até breve :)\n")