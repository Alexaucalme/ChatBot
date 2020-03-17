import os
from chatterbot import *
from chatterbot.trainers import *

def Quitter():
	Clear()
	os.sys.exit()

def Clear():
	os.system('clear')
Clear()

print('\n###############')
print('### ChatBot ###')
print('###############\n')

chatbot = ChatBot('Denist',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	logic_adapters=[
	    {
	        'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Je suis désolé, mais je ne comprends pas.',
            'maximum_similarity_threshold': 0.90
        }
    ])

conversation = [ 'Bonjour',
		'Salut !',
		'Comment vas-tu ?',
		'Je vais bien.',
		'Interessant...',
		'Merci.',
		'De rien'
				]

trainer = ListTrainer(chatbot)
trainer.train(conversation)

print()
print('Bonjour ! Pose moi une question : ')

def Question():
	Question = input('\n> ')
	if Question == 'bisous':
		Quitter()
	return Question

def Reponse():
	Reponse = chatbot.get_response(Question())
	print()
	return Reponse


while True:
	print(Reponse())
