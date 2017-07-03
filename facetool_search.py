#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

token = \
''

verbose = False

import requests, facebook, os, sys, random, time, json

reload(sys)
sys.setdefaultencoding('utf8')


graph = facebook.GraphAPI(token)

sleep = 2
comments_limit = 400
ids = []

CE = '\033[0;0m'
C0 = '\033[30m'
C1 = '\033[31m'
C2 = '\033[32m'
C3 = '\033[33m'
C4 = '\033[34m'
C5 = '\033[35m'
C6 = '\033[36m'
C7 = '\033[37m'

calendar = time.strftime('%d_%m')
if not os.path.exists(calendar):
		os.mkdir(calendar)

json_folder = os.path.abspath('JSON'+'/'+calendar)
if not os.path.exists(json_folder):
	os.makedirs(json_folder)
	

def wait(min):
	for x in range(min * 10):
		os.system("clear")
		load = ["Carregando", "Carreg4ndo", "Carr3gando", "Ca r3gando", "Carre and0", "C4rRegand0", " 4rreGando", "carregaNDo", "Carr$*#ndo"]
		print random.choice(load), random.choice(["\\", "-", "/"]), "\n", str(random.randrange(1000)) + "%", C0 + "[" + "#" * x + "]"+ CE
		#print load[random.randrange(len(load)):] + load[:random.randrange(len(load))]
		time.sleep(0.05)

def search(word):
	sdata = requests.get('https://graph.facebook.com/search?q='+ word +'&type=group&access_token='+ token)
	sdata = sdata.json()

	for sgroup in sdata['data']:
		if sgroup['privacy'] == 'OPEN':
			os.system('clear')
			print '\n'+ C3 +'[#]'+ CE +' CHECANDO GRUPO: '+ C3 + sgroup['name'] +''+ CE +' ['+ sgroup['id'] +']'
			try:
				get_info(sgroup['id'], word)
			except Exception, e:
				if verbose:
					print '\n'+ C1 + str(e) +''+ CE +'\n'		
				pass

def get_id(group):
	if not group.isalpha():
		print '\n'+ C3 +'[#]'+ CE +' Procurando ID do grupo...'
		time.sleep(sleep)
		print C2 +'[+]'+ CE +' Encontrado:', str(group)
		return group
	
	group = 'https://www.facebook.com/groups/'+group

	print '\n'+ C3 +'[#]'+ CE +' Verificando privacidade do grupo...'

	try:
		gid = requests.get(group).text.split('group_id')[1].split(',')[0].lstrip('u\'":')
	except Exception, e:
		print '\n'+ C1 +'[!]'+ CE +' GRUPO FECHADO. Não foi possível continuar.'
		if verbose:
			print '\n'+ C1 + str(e) + CE +'\n'
		return False

	print C2 +'[+]'+ CE +' Grupo ABERTO. Continuando...'		

	print '\n'+ C3 +'[#]'+ CE +' Procurando ID do grupo...'
	time.sleep(sleep)
	
	#gid = gid.text.split('"id":"')[1].split('"}')[0]
	
	print C2 +'[+]'+ CE +' Encontrado:', str(gid)
	return gid




def get_post(id, word, info):
	
	# info = graph.get_object(id=id, fields='name,feed.limit(200){comments.limit(200)}')

	group_name = info['feed']['data'][0]['to']['data'][0]['name']

	print C2 +'[+]'+ CE +' GRUPO: '+ C2 + group_name +''+ CE +'\n'

	print C2 +'[+]'+ CE +' Procurando postagens com a PALAVRA-CHAVE:'+ C1 , word, CE +''

	time.sleep(2)

	x = 0
	i = 0

	for post in info['feed']['data']:
		cond = []
		try:
			for s in word.split():
				if s.upper() in post['message'].upper().split():
					cond.append(True)
				else:
					cond.append(False)
			if False not in cond:
				i += 1

		except Exception, e:
			if verbose:
				print '\n'+ C1 + str(e) +''+ CE +'\n'
			pass

	if i < 1:
		print '\n'+ C1 +'[!]'+ CE +' NÃO ENCONTRAMOS NENHUM RESULTADO. PRESSIONE '+ C1 +'ENTER'+ CE +' PARA CONTINUAR.\n'
		time.sleep(1)
		os.system('clear')
		return

	for post in info['feed']['data']:
		cond = []
		try:
			for s in word.split():
				if s.upper() in post['message'].upper().split():
					cond.append(True)
				else:
					cond.append(False)
			if False not in cond:
				os.system('clear')

				x += 1

				try:
					MESSAGE = post['message'].replace('\n', ' ')
				except:
					MESSAGE = 'SEM MENSAGEM'
				
				try:
					AUTOR = post['from']['name']
				except:
					AUTOR = 'SEM AUTOR'

				try:
					created_time = '{}/{}/{} ás {}'.format(post['created_time'].split('T')[0].split('-')[2], post['created_time'].split('T')[0].split('-')[1], post['created_time'].split('T')[0].split('-')[0], post['created_time'].split('T')[1].split('+')[0])
				except:
					created_time = 'SEM DATA'

				try:
					LIKES = str(len(post['likes']['data']))
				except:
					LIKES = 0

				try:
					LINK = post['actions'][0]['link']
				except:
					LINK = 'SEM LINK'


				print C3 +'[#]'+ CE +' POSTAGENS ENCONTRADAS: '+ C3 +'['+ str(x) +' de '+ str(i) +']'+ CE +'\n'

				print C2 +'[+]'+ CE +' AUTOR:'+ C3, AUTOR, CE +'POSTADO:'+ C3, created_time, CE +'CURTIDAS:'+ C3, LIKES, CE +'\n'
				
				print C2 +'[+]'+ CE +' MENSAGEM:'+ C4, MESSAGE, ''+ CE +'\n'
				
				print C2 +'[+]'+ CE +' LINK:'+ C3, LINK, ''+ CE +''

				if x == i:
					break
				raw_input('\n'+ C1 +'[>]'+ CE +' Próximo:'+ C1 +' ENTER '+ CE +'')
				

		except Exception, e:
			if verbose:
				print '\n'+ C1 + str(e) +''+ CE +'\n'
			pass

	raw_input('\n'+ C1 +'[!]'+ CE +' FIM, PRESSIONE '+ C1 +'ENTER'+ CE +' PARA CONTINUAR.\n')

	os.system('clear')

	# # COMENTÁRIOS

	# info['feed']['data'][1]['comments']['data'][0]['id']

	# info['feed']['data'][1]['comments']['data'][0]['from']['id']
	# info['feed']['data'][1]['comments']['data'][0]['from']['mame']

	# info['feed']['data'][1]['comments']['data'][0]['message']
	# info['feed']['data'][1]['comments']['data'][0]['created_time']
	
	# info['feed']['data'][1]['comments']['data'][0]['like_count']
	# info['feed']['data'][1]['comments']['data'][0]['user_likes']

	# info['feed']['data'][1]['comments']['data'][0]['can_remove']



def get_info(id, word):
	print '\n'+ C3 +'[#]'+ CE +' Baixando informações...'
	info = graph.get_object(id=id, fields='email,name,owner,privacy,feed.limit(100),members.limit(10000)')
	print '\n'+ C2 +'[+]'+ CE +' INFORMAÇÕES COLETADAS!\n'
	time.sleep(1)
	
	try:
		owner = info['owner']['name']
	except:
		owner = False

	group_name = info['name'].replace('/', '_')

	print '\n'+ C2 +'[+]'+ CE +' GRUPO: '+ C3 + info['name'] +''+ CE +' USERS: '+ C3 + str(len(info['members']['data'])) +''+ CE +''
	# print C3 +'[#]'+ CE +' USERS: '+ C3 + str(len(info['members']['data'])) +''+ CE +''
 	
 	if word:
		group_folder = os.path.abspath(calendar+'/'+word+'/'+group_name)

	else:
		group_folder = os.path.abspath(calendar+'/1.GRUPOS/'+group_name)

	if not os.path.exists(group_folder):
		os.makedirs(group_folder)

	f = open(group_folder +'/1.INFORMACOES.txt', 'w')
	p = open(group_folder +'/2.PUBLICACOES.txt', 'w')
	x = open(group_folder +'/3.USUARIOS_ATIVOS.txt', 'w')
	u = open(group_folder +'/4.USUARIOS_TOTAL.txt', 'w')

	f.write('[#] PARSE DE GRUPO NO FACEBOOK\n\n')
	f.write('[+] Grupo: '+ info['name'] +'\n')
	f.write('[+] E-mail: '+ info['email'] +'\n')
	if owner:
		f.write('[+] Owner: '+ owner +' - http://www.facebook.com/'+ info['owner']['id']+'/\n')
	f.write('[+] Privacidade: '+ info['privacy'] +'\n\n')

	print '\n'+ C4+'[+]'+ CE +' COLETANDO: administradores...'
	for member in info['members']['data']:
		if member['administrator']:
			a = open(group_folder +'/5.ADMINISTRADORES.txt', 'w')
			a.write('[\'http://www.facebook.com/'+member['id']+'/\'] [\''+member['name']+'\']\n')
			a.close()
		else:
			u.write('[\'http://www.facebook.com/'+member['id']+'/\'] [\''+member['name']+'\']\n')

	time.sleep(sleep)
	
	print '\n'+ C4+'[+]'+ CE +' COLETANDO: posts...'
	for post in info['feed']['data']:
		p.write('[\''+post['id']+'\']'+'[\''+post['updated_time']+'\']\n')

	time.sleep(sleep)

	print '\n'+ C4+'[+]'+ CE +' COLETANDO: usuários ativos...'
	for posts in info['feed']['data']:
		try:
			for like in posts['likes']['data']:
				x.write('[\''+like['id']+'\'][\''+like['name']+'\']\n')
		except Exception, e:
			if verbose:
				print '\n'+ C1 + str(e) +''+ CE +'\n'
		
	time.sleep(sleep)

	f.close()
	p.close()
	u.close()
	x.close()

	os.system('clear')
	
	print	
	print C1 +'[$]'+ CE +' COMPLETO!'
	print C1 +'[$]'+ CE +' As informações do grupo foram salvas na pasta '+ C0 +'"'+ info['name'].replace('/', '_') +'"'+ CE +'\n'

def key_one(group, word, locate):
	# group = 'classificadosdevarginha'

	if group.isalpha():
		id = get_id(group)
	else:
		id = group
	
	json_file = json_folder +'/'+ id +'.JSON'
	
	if not os.path.isfile(json_file):
		# id_file = open(json_folder +'/'+ group +'.ID', 'w').write(id)
		print C3 +'[#]'+ CE +' Baixando informações...'
		api = requests.get('https://graph.facebook.com/'+ id +'?fields=feed.limit('+ str(comments_limit)+ ')&access_token='+ token).text
		print '\n'+ C2 +'[+]'+ CE +' INFORMAÇÕES COLETADAS!\n'
		time.sleep(1)

		json_str = json.dumps(api)
		data = json.loads(json_str)

		with open(json_folder +'/'+ id +'.JSON', 'w') as f:
			json.dump(data, f)

		with open(json_folder +'/'+ id +'.JSON', 'r') as f:
			data = json.load(f)

		info = json.loads(data)
		
	elif os.path.isfile(json_file):
		ids.append(group)
		if not locate:
			time.sleep(0.01)
			os.system('clear')
			return

		with open(json_folder +'/'+ id +'.JSON', 'r') as f:
			data = json.load(f)

		info = json.loads(data)


	else:
		print '\nALGO DEU ERRADO\n'

	# print '\n'+ C2 +'[+]'+ CE +' INFORMAÇÕES COLETADAS!'
	
	# time.sleep(2)
	# os.system('clear')

	if locate:
		try:
			get_post(id, word, info)
		except Exception, e:
			# print '\n'+ C1 +'[!]'+ CE +' Algo deu errado. Tente novamente OU tente outro grupo. \n'
			# time.sleep(2)
			os.system('clear')
			
			if verbose:
				print '\n'+ C1 + str(e), CE, '\n'

def pre_down():
	
	try:
		group = raw_input('\n'+ C1 +'[.]'+ CE +' Nome do GRUPO: '+ C1 )

		sdata = requests.get('https://graph.facebook.com/search?q='+ group +'&type=group&access_token='+ token)
		sdata = sdata.json()
	
		print '>>>>>>>>>>>>'

		x = 0
		j = 0

		for sgroup in sdata['data']:
			if sgroup['privacy'] == 'OPEN':
				j += 1

		for sgroup in sdata['data']:
			if sgroup['privacy'] == 'OPEN':
				x += 1
				os.system('clear')

				print '\n'+ C3 +'['+ str(x) +'/'+ str(j) +']'+ CE +' CHECANDO GRUPO: '+ C3 + sgroup['name'], CE +' ['+ sgroup['id'] +']'
				try:
					key_one(sgroup['id'], False, False)

				except Exception, e:
					if verbose:
						print '\n'+ C1 + str(e) +''+ CE +'\n'		
					pass
			
		# raw_input('\n'+ C2 +'[!]'+ CE +' FIM, PRESSIONE '+ C1 +'ENTER'+ CE +' PARA CONTINUAR.\n')

		back()
	
	except Exception, e:
		if verbose:
			print '\n'+ C1 + str(e) +''+ CE +'\n'
	except KeyboardInterrupt:
		print '\n\n' + C1 +'[!]'+ C0 +' INTERROMPIDO PELO USUÁRIO.\n'
		time.sleep(1)
		back()

def back():
	os.system('clear')

	print C3 +'[#]'+ CE +' O que deseja fazer?'
	print 
	print C2 +'[/]'+ CE +' 1. Voltar para menu principal'
	print C2 +'[/]'+ CE +' 2. Alterar PALAVRA-CHAVE da pesquisa'
	print C2 +'[/]'+ CE +' 3. Buscar por palavras chave nos bancos baixados'
	print 
	print C0 +'[/]'+ CE +' 5. Opções de varredura'
	print
	print C3 +'[/]'+ CE +' 0. Sair.'
	print
	
	back = raw_input(C1 +'[.]'+ CE +' Escolha uma opção: '+ C1 )

	if int(back) == 1:
		main()	
	elif int(back) == 2:
		pre_down()
	elif int(back) == 3:
		word = raw_input('\n'+ C1 +'[.]'+ CE +' Digite a PALAVRA-CHAVE: '+ C1 )
		os.system('clear')
		if ids:
			for id in ids:
				key_one(id, word, True)
		back()
	elif int(back) == 4:
		pass
	elif int(back) == 0:
		print '\n'+ C1 +'[#]'+ CE +' OBRIGADO, '+ C6 +'VOLTE SEMPRE!'+ CE +'\n'
		exit()
	else:
		print '\n'+ C1 +'[!]'+ CE +' OPÇÃO INVÁLIDA! Tente novamente...\n'
		time.sleep(2)
		back()

def start():
	os.system('clear')

	print C3 +'[#]'+ CE +' Parse de dados de grupos do Facebook:'
	print 

	print C7 +'[/]'+ CE +' 1. INFO de um só grupo. (Rápido)'
	print C7 +'[/]'+ CE +' 2. INFO de vários grupos por PALAVRA-CHAVE (Lento)'
	print
	print C2 +'[/]'+ CE +' 3. Procurar por posts contendo PALAVRAS-CHAVE no grupo'
	print C2 +'[/]'+ CE +' 4. Procurar por posts contendo PALAVRAS-CHAVE em vários grupos'
	print
	print C0 +'[/]'+ CE +' 5. Baixar BANCO de dados JSON'
	print
	opcao = raw_input(C1 +'[.]'+ CE +' Escolha uma opção: '+ C1 )

	if int(opcao) == 1:
		group = raw_input('\n'+ C3 +'[.]'+ CE +' Digite o NOME ou ID do grupo: '+ C1 )

		id = get_id(group)
		if id:
			try:
				get_info(id, False)
			except Exception, e:
				print '\n'+ C1 +'[!]'+ CE +' Algo deu errado. Tente novamente OU tente outro grupo. \n\n'+ C1 + str(e) +''+ CE +'\n'

	elif int(opcao) == 2:
		
		word = raw_input('\n'+ C1 +'[.]'+ CE +' Digite a PALAVRA-CHAVE: '+ C1 ).upper()
		
		search(word)

	elif int(opcao) == 3:
		group = raw_input('\n'+ C1 +'[.]'+ CE +' Digite o NOME ou ID do grupo: '+ C1 )
		word = raw_input('\n'+ C1 +'[.]'+ CE +' Digite a PALAVRA-CHAVE: '+ C1 )

		key_one(group, word)

	elif int(opcao) == 4:
		try:
			num_open = 0
			group = raw_input('\n'+ C1 +'[.]'+ CE +' Nome do GRUPO: '+ C1 )
			word = raw_input('\n'+ C1 +'[.]'+ CE +' Digite a PALAVRA-CHAVE: '+ C1 )

			os.system('clear')

			print '\n'+ C3 +'[#]'+ CE +' Baixando informações...'
			sdata = requests.get('https://graph.facebook.com/search?q='+ group +'&type=group&access_token='+ token)
			print '\n'+ C2 +'[+]'+ CE +' INFORMAÇÕES COLETADAS!\n'
			sdata = sdata.json()

			j = 0
			x = 0

			for sgroup in sdata['data']:
				if sgroup['privacy'] == 'OPEN':
					j += 1

			for sgroup in sdata['data']:
				if sgroup['privacy'] == 'OPEN':
					x += 1
					print '\n'+ C3 +'['+ str(x) +'/'+ str(j) +']'+ CE +' CHECANDO GRUPO: '+ C3 + sgroup['name'], CE +' ['+ sgroup['id'] +']\n'
					try:
						key_one(sgroup['id'], word, True)

					except Exception, e:
						if verbose:
							print '\n'+ C1 + str(e) +''+ CE +'\n'		
						pass
				if j < 1:
					print('\n'+ C1 +'[!]'+ CE +' NADA ENCONTRADO AQUI.\n')
					os.system('clear')

			main()
		except KeyboardInterrupt:
			back()

	elif int(opcao) == 5:
		try:
			pre_down()
		except KeyboardInterrupt:
			back()
			
def main():
	try:
		start()
	except Exception, e:
		if verbose:
			print '\n'+ C1 + str(e) +''+ CE +'\n'
	except KeyboardInterrupt:
		print '\n\n' + C1 +'[!] INTERROMPIDO PELO USUÁRIO!\n'+ CE

if __name__ == '__main__':
	wait(1)
	main()
