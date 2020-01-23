''' organizacao do codigo
	# operacoes possiveis:
		# display de missoes atuais
			# diferentes sorts
	# definir current team


	# to do:
		# achar metodo para encontrar missoes do seu time
			# criar classe char com propriedade "possible names"
			# passar no db pra achar alguem dessa categoria
		# gui
			# pygame ou qt?
		# current team
			# possivel pegar do js?

'''

'''
	1. Ver Missoes
		1. Todas
			Display todas as missoes atuais (sorts variados)
		2. Time atual
			Display missoes com os personagens usados (sorts variados)
	2. Mudar Time Atual
		Muda o time atual (possivel por scraping do js?)
	3. Times Favoritos
		Display times favoritados pelo user
	4. META Teams
		Display meta teams de acordo com os bonecos habilitados (criar tabela de acordo com a sessão)
	5. Inspecionar Time
		Mostra o time inimigo, com os textos das habilidades
		Pode ser aprimorado pra mostrar jogabilidade basica dos bonecos (playing with/playing against)
	0. Sair


'''

from classes import *
from webScrape import *
from bd import *

import operator

from getpass import getpass

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
	# Printa missoes separadas, cada uma com seus steps e o personagem desbloqueado
	missionListList = acharMissao(session)
	for missionList in missionListList:
		for mission in missionList:
			mission.printMission()

def missoesPorPersonagem(session):
	# Printa missoes sort pelo nome do personagem
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
	# Printa missoes sort pelo nivel de conclusao
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
	# Printa missoes sort pelo tipo de missao ("in a row" ou não)
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

'''
# a ser implementado
def missoesParaTime(session, time):
	missionListList = acharMissao(session)
	for missionList in missionListList:
		for mission in missionList:
			if mission.charUnlock != '':
				# fazer if pra ver se o char do step esta no time
				for step in mission:
					if step.charText in bdcharList():
						a=1
'''

logSuccess = 0
print("\n\n\n           Bem vindo ao NAMH\n\n")
while logSuccess == 0:
	nick = input("Digite o login:\n")
	senha = getpass(prompt='Digite a senha\n')
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
		# sort padrao
		atualizarMissoes(sessao)
	elif op == '2':
		# Sort por personagem
		missoesPorPersonagem(sessao)
	elif op == '3':
		# Missoes disponiveis com o time atual
		missoesMaisConcluidas(sessao)
	elif op == '4':
		missoesPorTipo(sessao)
	else:
		print("Entrada invalida")
	'''
	a ser implementado
	elif op == '5':
		# Missoes disponiveis com o time atual
		if timeAtual == []:
			print("Time não especificado\n")
			timeAtual = modificarTimeAtual(listaPersonagens())
		missoesParaTime(sessao, timeAtual)
	elif op == '6':
		timeAtual = modificarTimeAtual(listaPersonagens())
	'''
	print("\n\n\n\n\n\nQual outra operacao deseja realizar?")
	print("  1. Atualizar missoes")
	print("  2. Organizar missoes por personagem")
	print("  3. Organizar por proximidade de conclusao")
	print("  4. Organizar por tipo de missao (in a row/normal)")
	# a ser implementado
	#print("  5. Organizar missoes por time")
	#print("  6. Mudar Time Atual")
	op = input("  0. Sair do programa\n")

print("Até breve :)\n")