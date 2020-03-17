#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Créé le Jeudi 7 Novembre 2019

@author: Alexandre Monroche
"""

import numpy as np                                                              # On importe les bibliotèques nécessaires
import tensorflow as tf
import re
import time

#################################
### PARTIE 1 : PRE-TRAITEMENT ###
#################################
                                                                                # On lit les fichiers contenant les phrases des films et les conversations
FichierDialogues = open('Sources/dialogues_fr.txt', 'r', encoding = 'utf-8', errors = 'ignore').read().split('\n')
FichierConversations = open('Sources/movie_conversations.txt', 'r', encoding = 'utf-8', errors = 'ignore').read().split('\n')

# Créer un dictionnaire pour associer chaque phrase à son ID

DictionnairePhrasesVersID = {}                                                  # On créé notre dictionnaire
for Ligne in FichierDialogues:                                                  # On parcours les dialogues
    LigneTemporaire = Ligne.split(' +++$+++ ')                                  # On sépare chaque ligne en tableau
    if len(LigneTemporaire) == 5:                                               # Si la longueur de la ligne est conforme
        DictionnairePhrasesVersID[LigneTemporaire[0]] = LigneTemporaire[-1]     # On ajoute au dictionnaire la phrase avec le numéro du phrase en indice

# Créer une liste contenant toutes les conversations

Conversations = []                                                              # On créé le tableau contenant les conversations
for Ligne in FichierConversations:                                              # On parcours les conversations
    ConversationTemporaire = Ligne.split(' +++$+++ ')                           # On découpe la ligne en tableau
    ConversationTemporaire = ConversationTemporaire[-1]                         # On prends que les indices
    ConversationTemporaire = ConversationTemporaire.replace("'", '')            # On  remplace les caractères non utiles par rien
    ConversationTemporaire = ConversationTemporaire.replace(' ', '')
    ConversationTemporaire = ConversationTemporaire.replace('[', '')
    ConversationTemporaire = ConversationTemporaire.replace(']', '')
    ConversationTemporaire = ConversationTemporaire.split(',')                  # On récupère le tableau dont les éléments sont séparés par une virgule
    Conversations.append(ConversationTemporaire)                                # On ajoute le tableau de cette conversation au tableau contenant toutes les conversations

# Créer un tableau pour les questions et un tableau pour les réponses

Questions = []                                                                  # On créé le tableau contenant les questions
Reponses = []                                                                   # On créé le tableau contenant les réponses
for Conversation in Conversations:                                              # On parcours le tableau contenant les conversations
    for IndicePhrase in range(len(Conversation) - 1):                           # On parcours le tableau contenant les indices des phrases pour chaques conversations
        if Conversation[IndicePhrase] in DictionnairePhrasesVersID.keys():      # Si l'indice a bien une case dans le dictionnaire
            Questions.append(DictionnairePhrasesVersID[Conversation[IndicePhrase]])     # On ajoute le premier indice comme questions
            Reponses.append(DictionnairePhrasesVersID[Conversation[IndicePhrase + 1]])  # et le suivant comme réponse, ainsi une question peux être une réponse

# Nettoyage des questions et des réponses en enlevent [] () {} _ + =

def NettoyageTexte(Texte):                                                      # On défini NettoyageTexte qui prends un texte en paramètre
    Texte = Texte.lower()                                                       # On mets le texte en minuscule
    Caracteres = r"[]()\"\'{}_+=#@;<>:/.,%$¥$*£&?!0123456789-"                   # On créé un tableau contenant les caractères à enlever
    for Caractere in Caracteres:                                                # On parcours ce tableau
        Texte = Texte.replace(Caractere, '')                                    # On enleve chaque caractère
    return Texte                                                                # On retourne le texte

QuestionsNettoye = []                                                           # On créé un nouveau tableau pour les questions nettoyées
ReponsesNettoye = []                                                            # On créé un nouveau tableau pour les réponses nettoyées

for Question in Questions:                                                      # On parcourt le tableau des questions
    QuestionsNettoye.append(NettoyageTexte(Question))                           # On passe chaque question dans la fonction NettoyageTexte pour la nettoyer

for Reponse in Reponses:                                                        # Idem pour les réponses
    ReponsesNettoye.append(NettoyageTexte(Reponse))

# Créé un dictionnaire qui associe à chaque mot le nombre de fois où il apparait

DictionnaireMotsVersOccurence = {}                                              # On créé le dictionnaire

for Question in QuestionsNettoye:                                               # On parcours le tableau des questions nettoyées
    for Mot in Question.split():                                                # On parcours chaque mot de la question "spliter"
        if Mot not in DictionnaireMotsVersOccurence:                            # Si le mot n'est pas dans le Dictionnaire
            DictionnaireMotsVersOccurence[Mot] = 1                              # On le place dans le dictionnaire avec une itération
        else:                                                                   # Sinon
            DictionnaireMotsVersOccurence[Mot] += 1                             # On ajoute une itération au mot trouvé

for Reponse in ReponsesNettoye:                                                 # Idem pour les réponses
    for Mot in Reponse.split():
        if Mot not in DictionnaireMotsVersOccurence:
            DictionnaireMotsVersOccurence[Mot] = 1
        else:
            DictionnaireMotsVersOccurence[Mot] += 1

# Créé les dictionnaires qui associent chaque mot d'une question (et d'une réponse) à un identifiant unique et leurs inverses

NombreOccurenceMinimal = 20                                                     # On fixe le nombre d'occurence minimal d'un mot à 20
DictionnairesMotsQuestionsVersIdentifiant = {}                                  # On créé le dictionnaire qui associe chaque mots des questions à un identifiant unique
DictionnairesIdentifiantVersMotsQuestions = {}                                  # On créé le dictionnaire inverse qui associe chaque identifiant à un mot

i = 0                                                                           # On initialise un compteur à 0
for Question in QuestionsNettoye:                                               # Pour chaque question du tableau des questions nettoyées
    for Mot in Question.split():                                                # Pour chaque mots de la question
        if DictionnaireMotsVersOccurence[Mot] >= NombreOccurenceMinimal:        # Si ce mot est apparue au moins 20 fois dans toutes les phrases
            if Mot not in DictionnairesMotsQuestionsVersIdentifiant:            # Si le mot n'est pas dans le dictionnaire, on l'ajoute, sinon on fait rien
                DictionnairesMotsQuestionsVersIdentifiant[Mot] = i              # On le place dans les tableaux
                DictionnairesIdentifiantVersMotsQuestions[i] = Mot
                i += 1                                                          # On incrémente i de 1

DictionnairesMotsReponsesVersIdentifiant = {}                                   # Idem pour
DictionnairesIdentifiantVersMotsReponses = {}

i = 0
for Reponse in ReponsesNettoye:
    for Mot in Reponse.split():
        if DictionnaireMotsVersOccurence[Mot] >= NombreOccurenceMinimal:
            if Mot not in DictionnairesMotsReponsesVersIdentifiant:
                DictionnairesMotsReponsesVersIdentifiant[Mot] = i
                DictionnairesIdentifiantVersMotsReponses[i] = Mot
                i += 1

# Enrichissement des dictionnaires avec les tokens

Tokens = ['<EOS>', '<SOS>', '<PAD>', '<OUT>']                                   # Tableau contenant les tokens à rajouter
for Token in Tokens:                                                            # Pour chaque tokens
    DictionnairesMotsQuestionsVersIdentifiant[Token] = i                        # On l'ajoute à chaque tableau suivant leur nomenclature
    DictionnairesIdentifiantVersMotsQuestions[i] = Token                        # En utilisant i étant à cette ligne l'indice du dernier mot
    DictionnairesMotsReponsesVersIdentifiant[Token] = i
    DictionnairesIdentifiantVersMotsReponses[i] = Token
    i += 1                                                                      # On incrémente i de 1

# Fonction pour ajouter un token à la fin des phrases d'un tableau

def AjoutTokenFinPhrases(TableauPhrases, Token):                                # Définition de la fonction avec le tableau des phrases et le token à ajouter en paramètre
    Token = ' ' + Token                                                         # On ajoute un espace avant le token
    for i in range(len(TableauPhrases)):                                        # On parcours le tableau des phrases
        TableauPhrases[i] += Token                                              # Pour chaque phrase on ajoute le Token à la fin
    return TableauPhrases                                                       # On retourne le tableau modifier

# Ajout du token <EOS> à la fin de chaque réponses

QuestionsNettoye = AjoutTokenFinPhrases(QuestionsNettoye, Tokens[0])            # Appel de la fonction avec le Token <EOS> et les questions nettoyes en paramètres
