import os
import chatBotProcess
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

chatbot = ChatBot('Denis',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	logic_adapters=[
	    {
	        'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Je suis désolé, mais je ne comprends pas.',
            'maximum_similarity_threshold': 0.90
        }
    ],
	filters=[filters.get_recent_repeated_responses]
)

trainer = ListTrainer(chatbot)

corpus = "data"
datafile = os.path.join(corpus, "formatted_movie_lines_FR-fr.txt")
save_dir = os.path.join(corpus, "save")
voc, pairs = chatBotProcess.loadPrepareData("data", "movie_lines_FR-fr.txt", datafile, save_dir)

print("\nEntraînement des paires de questions/réponses:")
for pair in pairs:
    trainer.train(pair)

print(chatbot.get_response("Alors c'est tout ce que tu avais à dire."))
print(chatbot.get_response('Tu vas au truc de Bogey Lowenbrau samedi ?'))
print(chatbot.get_response("Combien de personnes viennent ici ?"))
print(chatbot.get_response('Tu connais le français ?'))

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
