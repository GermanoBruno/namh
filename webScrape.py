import requests
from bs4 import BeautifulSoup
from classes import *
from bd import *

rankList = bdRankList()

def login(nick, password):
	# Request e checagem de sucesso
	s = requests.Session()
	req = s.get('https://naruto-arena.net')
	if req.status_code == 200:
		content = req.content

		# armazena o conteudo do site e busca o token
		soup = BeautifulSoup(content, 'html.parser')
		tag = soup.find(name='input', attrs={'name':'_token'})

		# armazena o token e cria payload
		token = tag['value']
		payload = {'_token' : token, 'login' : nick, 'password' : password, 'submit2' : 'Login'}

		# posta o request
		post = s.post('https://naruto-arena.net/login', payload)

		# atualiza o conteudo do site pós tentativa de login e busca o formulario de logout (so disponivel quando login sucesso)
		content = post.content
		soup = BeautifulSoup(content, 'html.parser')
		tag = soup.find(name='form', attrs={'action':'https://naruto-arena.net/logout'})

		# Debugger de login
		if tag == None :
			success = 0
		else:
			success = 1

		return s, success

def listaPersonagens():
	req = requests.get('https://naruto-arena.net/characters-and-skills')

	if req.status_code == 200:
		print('Foi\n')
		content = req.content

		soup = BeautifulSoup(content, 'html.parser')
		tag = soup.find_all(name='div', attrs={'class':'description'})

		stringList = []
		for i in tag:
			string = i.find(name='h2')
			#print(string.contents[0])
			stringList.append(string.contents[0].lower())
		return stringList
	else:
		print('Request Failed, personagens nao baixados')

def lerMissoes(url, session):
	req = session.get(url, allow_redirects=False)
	if req.status_code == 200:
		content = req.content
		soup = BeautifulSoup(content, 'html.parser')
		# Procura a imagem de lista (indicando step da missao)
		tag = soup.find_all(name = 'div', attrs={'class':'floatleft'})
		#sprint(tag)
		linkList = []
		missionList = []
		for box in tag:
			# Inicializa as variaveis para os valores padrao
			missionUrl = None
			preReq = []
			stepList = []
			charUnlock = ''
			# Procura o titulo da missao
			title = box.find_next(name = 'h5').contents[0]
			# Seleciona a div(box) que contem a missao
			box = box.find(name = 'div', attrs={'class':'bg2'})
			# Verifica se a missao esta completa
			rankText = box.find_next(name='font')
			rank = rankText.contents[0]
			if rank not in rankList:
				rank = ''
				status = -1
			elif rankText['class'][0] == 'error':
				# Se missao nao completa, verifica se o rank nao e compativel com o atual
				status = 0
				texts = box.find_all(name='font')
				# Pega a lista de missoes necessarias para realizar a missao (preReq)
				for text in texts:
					missionSearch = text.contents
					for mission in missionSearch:
						if (mission not in rankList) and (mission != 'You do not meet the requirements to do this mission.'):
							preReq.append(mission)
			else:
				texts = box.find_all(name='font')
				# Setta status como 1, se não for missao unlocked, vai mudar
				status = 1
				# Pega a lista de missoes necessarias para realizar a missao (preReq)
				for text in texts:
					missionSearch = text.contents
					for mission in missionSearch:
						if (mission not in rankList) and (mission != 'You do not meet the requirements to do this mission.'):
							preReq.append(mission)
						if text['class'][0] == 'nothing':
							# Inicialmente parecendo estar completa, chegamos no "you do not...", portanto: missao locked
							status = 0
				if status == 1:
					missionUrl = box.find_next(name='a')['href']
					# Pega a missionUrl entra na missão e coleta Steps e charUnlock
					req = session.get(missionUrl)
					content = req.content
					soup = BeautifulSoup(content, 'html.parser')
					# Busca dos steps
					# Procura a imagem de lista (indicando step da missao)
					missionSteps = soup.find_all(name = 'img', attrs={'src':'../images/pres/preli.gif'})
					for step in missionSteps:
						# coloca em uma lista o texto de missões
						strText = str(step.find_next(string=True))
						# Retira tab e newline do nome
						strText = strText.strip('\n\t')
						# Retira o Win no começo do step
						if(strText != ''):
							stepWords = strText.strip('Win ').split(' ')
							stepWords[-2] = stepWords[-2][:-1]
							currentWins = stepWords[-1].strip('(').split('/')[0]
							totalWins = strText.split(' ')[1]
							if stepWords[4] == 'row':
								char = stepWords[6:-1]
								newStep = Step(currentWins, totalWins, 'r', char, strText)
							else:
								char = stepWords[3:-1]
								newStep = Step(currentWins, totalWins, 'n', char, strText)
							stepList.append(newStep)
					# Busca do char a ser desbloqueado
					charUnlock = soup.find(name='div', attrs={'class': 'floatleft'})
					charUnlock = charUnlock.find_all(name='br')
					charUnlock = charUnlock[-3].contents[0].strip('\n\t')
				missionList.append(Mission(title, rank, status, missionUrl, preReq, stepList, charUnlock))
		return(missionList)
	else:
		print('Request failed')

def acharMissao(session):
	# a partir da tela de missões, entrar em cada sub secao e verificar as missoes por fazer
	req = session.get('https://naruto-arena.net/ninja-missions', allow_redirects=False)
	if req.status_code == 200:
		content = req.content
		soup = BeautifulSoup(content, 'html.parser')
		# Procura a imagem de lista (indicando step da missao)
		tag = soup.find_all(name = 'div', attrs={'class':'infolink'})
		linkList = []
		missionListList = []
		for link in tag:
			link = link.find_next(name = 'a')['href']
			linkList.append(link)
		for link in linkList:
			missionListList.append(lerMissoes(link, session))
	return missionListList