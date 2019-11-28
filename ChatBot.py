#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 18:32:14 2019

@author: alexaucalme
"""

import numpy as np
import tensorflow as tf
import re
import time

#################################
### PARTIE 1 : PRE-TRAITEMENT ###
#################################

FichierDialogues = open('Sources/dialogues_fr.txt', 'r', encoding = 'utf-8', errors = 'ignore').read().split('\n')
FichierConversations = open('Sources/movie_conversations.txt', 'r', encoding = 'utf-8', errors = 'ignore').read().split('\n')

# Créer un dictionnaire pour associer chaque phrase à son ID

DictionnairePhrases = {}                                                        # On créé notre dictionnaire
for Ligne in FichierDialogues:                                                  # On parcours les dialogues
    LigneTemporaire = Ligne.split(' +++$+++ ')                                  # On sépare chaque ligne en tableau
    if len(LigneTemporaire) == 5:                                               # Si la longueur de la ligne est conforme
        DictionnairePhrases[LigneTemporaire[0]] = LigneTemporaire[-1]           # On ajoute au dictionnaire la phrase avec le numéro du phrase en indice

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
        if Conversation[IndicePhrase] in DictionnairePhrases.keys():            # Si l'indice a bien une case dans le dictionnaire
            Questions.append(DictionnairePhrases[Conversation[IndicePhrase]])   # On ajoute le premier indice comme questions
            Reponses.append(DictionnairePhrases[Conversation[IndicePhrase + 1]])# et le suivant comme réponse, ainsi une question peux être une réponse

# Nettoyage des questions et des réponses en enlevent [] () {} _ + =

def NettoyageTexte(Texte):                                                      # On défini NettoyageTexte qui prends un texte en paramètre
    Texte = Texte.lower()                                                       # On mets le texte en minuscule
    Caracteres = r"[]()\"\'{}_+=#@;<>:/.,%$¥$*£&?!0123456789"                   # On créé un tableau contenant les caractères à enlever
    for Caractere in Caracteres:                                                # On parcours ce tableau
        Texte = Texte.replace(Caractere, '')                                    # On enleve chaque caractère
    return Texte                                                                # On retourne le texte

print(NettoyageTexte("Bonjour.;2489HZIJFB@#°"))

"""
QuestionsNettoye = []
ReponsesNettoye = []

for Question in Questions:
    QuestionsNettoye.append(NettoyageTexte(Question))

for Reponse in Reponses:
    ReponsesNettoye.append(NettoyageTexte(Reponse))

# Créé un dictionnaire qui associer à chaque mot le nombre de fois où il apparait

DictionnaireMots = {}

for Question in QuestionsNettoye:
    for Mot in Question.split():
        if Mot not in DictionnaireMots:
            DictionnaireMots[Mot] = 1
        else:
            DictionnaireMots[Mot] += 1

for Reponse in ReponsesNettoye:
    for Mot in Reponse.split():
        if Mot not in DictionnaireMots:
            DictionnaireMots[Mot] = 1
        else:
            DictionnaireMots[Mot] += 1
"""
