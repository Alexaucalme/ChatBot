import os
#import chatbotProcess
from ymlProcess import *
from chatterbot import *
from chatterbot.trainers import *

# Fonction pour quitter le programme
def Quitter():
	Clear()
	os.sys.exit()

# Fonction pour effacer la console
def Clear():
	os.system('clear')

# On efface la console
Clear()

print('\n###############')
print('### ChatBot ###')
print('###############\n')

# Création du ChatBot
chatbot = ChatBot('Denis',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	logic_adapters=[
	    {
	        'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Je suis désolé, mais je ne comprends pas.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)

# On créé le trainer permettant d'entrainer le ChatBot grâce à des listes
trainer = ListTrainer(chatbot)

ListeFichiers = ['french/botprofile.yml',
					'french/conversations.yml',
					'french/food.yml',
					'french/greetings.yml',
					'french/trivia.yml',
					'english/ai.yml',
					'english/botprofile.yml',
					'english/computers.yml',
					'english/conversations.yml',
					'english/emotion.yml',
					'english/food.yml',
					'english/gossip.yml',
					'english/greetings.yml',
					'english/health.yml',
					'english/history.yml',
					'english/humor.yml',
					'english/literature.yml',
					'english/money.yml',
					'english/movies.yml',
					'english/politics.yml',
					'english/psychology.yml',
					'english/science.yml',
					'english/sports.yml',
					'english/trivia.yml',
					]

print("\nEntraînement des paires de questions/réponses:")
for i in ListeFichiers:
	print('\n' + i + '...\n')
	pairs = FormattagePairs(ymlProcess(i))
	for pair in pairs:
		trainer.train(pair)

# Test de l'entrainement
print(chatbot.get_response("Quelle est ton chef ?"))
print(chatbot.get_response("Qu'est ce qui te derange ?"))

print()
print('Bonjour ! Pose moi une question : ')

# Fonction attendant une question de l'utilisateur
def Question():
	Question = input('\n--> ')
	if Question == 'exit':
		Quitter()
	return Question

# Fonction retournant la réponse du bot à l'utilisateur
def Reponse():
	Reponse = chatbot.get_response(Question())
	print()
	return Reponse

# On lance le ChatBot
while True:
	print(Reponse())
