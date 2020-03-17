#
#
# Le dossier chatterbot-corpus-master issu du github de chatterbot_corpus
# doit être mis dans le dossier data du projet.
#
# Le mode verbeux affiche les Questions suivies des réponses, True pour verbeux, False pour non-verbeux
#
# CheminFichier correspond au chemin à partir du dossier contenant les langues
# Exemple pour le fichier trivia.yml du corpus francais : "french/trivia.yml"
# Exemple pour le fichier conversations.yml du corpus telugu : "telugu/conversations.yml"
#
# La fonction retourne le tableau contenant les conversations selon la nomenclature suivante :
# [[Question 1, Reponse 1, Reponse 2], [Question 2, Reponse 1, Reponse 2, Reponse 3], etc...]
#
#
def ymlProcess(CheminFichier, Verbeux=False):
    # On lis le fichier
    Chemin = "data/chatterbot-corpus-master/chatterbot_corpus/data/" + CheminFichier
    Fichier = open(Chemin,'r')
    Tableau = Fichier.readlines()
    Fichier.close()
    # Création d'un tableau poubelle pour récupérer les questions
    TableauPoubelle = []
    # Création du tableau final
    TableauConversations = []
    # On retire les trois premières lignes et les sauts de lignes
    Tableau = Tableau[3:]
    # On boucle dans le tableau pour récupérer les conversations
    for i in range(len(Tableau)):
        # Si on tombe sur une question
        if Tableau[i][:4] == '- - ':
            # On l'affiche si on est verbeux
            if Verbeux: print('Question : ' + Tableau[i][4:-1])
            # On ajoute la question au tableau final
            TableauConversations.append([Tableau[i][4:-1]])
            # On stock l'indice de la question dans le tableau final
            IndiceQuestion = len(TableauConversations) - 1
            # On boucle de la phrase suivant la question jusqu'a la fin du tableau
            for u in range(i + 1, len(Tableau)):
                # Si on retombe sur une question
                if Tableau[u][:4] == '- - ':
                    # Alors on ajoute l'indice de cette question dans le tableau poubelle
                    TableauPoubelle.append(u)
            # Si le tableau n'est pas vide alors on sauvegarde l'indice de la
            # première occurence d'une question après la précédente.
            if TableauPoubelle != []: IndiceProchaineQuestion = TableauPoubelle[0]
            # Sinon c'est qu'aucune question n'a été trouvé, donc on considère
            # que la dernière question est la fin du tableau
            else: IndiceProchaineQuestion = len(Tableau)
            # On vide le tableau pour la prochaine question
            TableauPoubelle = []
            # On boucle de l'indice suivant la premère question jusqu'à l'indice
            # de la prochaine question : on boucle entre les deux questions
            for j in range(i + 1, IndiceProchaineQuestion):
                # Si on tombe sur une réponse
                if Tableau[j][:4] == '  - ':
                    # Si on est verbeux, on l'affiche
                    if Verbeux: print('--------- Réponse : ' + Tableau[j][4:-1])
                    # On l'ajoute à la liste contenant la question,
                    # et les potentielles autres réponses
                    TableauConversations[IndiceQuestion].append(Tableau[j][4:-1])
    return TableauConversations

# Fonction formattant le tableau de ymlProcess en pairs de Questions/Réponses
# exploitables pour entrainer le ChatBot, elle prends en paramètre le tableau.
def FormattagePairs(TableauConversations):
    Pairs = []
    for i in range(len(TableauConversations)):
        for u in range(1, len(TableauConversations[i])):
            Pairs.append([TableauConversations[i][0],TableauConversations[i][u]])
    return Pairs

# Tests :
pairs = FormattagePairs(ymlProcess('french/conversations.yml'))
print(pairs)
