# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 01:10:59 2019

@author: Roland
"""

import csv
import random
import re
import os
import unicodedata
import codecs
from io import open
import itertools
import math


corpus = "data"

# Affiche les n premières lignes d'un fichier
def printFile(file, n=10):
    datafile = open(file, 'r', encoding='utf-8', errors = 'ignore')
    lines = datafile.readlines()
    for line in lines[:n]:
        print(line)
    datafile.close()

printFile(os.path.join(corpus, "movie_lines_FR-fr.txt"))

# Affiche les n premiers champs d'un dictionnaire
def printDict(d, n=10):
    res = dict(itertools.islice(d.items(), n))
    print(res)

# Affiche les n premiers éléments d'une liste
def printList(l, n=20):
    for line in l[:n]:
        print(line)

# Transforme chaque ligne en dictionnaire de champs
def loadLines(fileName, fields):
    lines = {}
    f = open(fileName, 'r', encoding='utf-8', errors = 'ignore')
    for line in f:
        values = line.split(" +++$+++ ")
        # Extraire les champs
        lineObj = {}
        for i, field in enumerate(fields):
            lineObj[field] = values[i]
            lines[ lineObj['lineID'] ] = lineObj

    f.close()
    return lines

# TEST de loadLines
champs_test_ll = ["lineID", "personnageID", "filmID", "personnage", "texte"]
lignes = loadLines(os.path.join(corpus, "movie_lines_FR-fr.txt"), champs_test_ll)
printDict(lignes)

# Transforme les champs de lignes issus de `loadLines` en conversations basées sur *movie_conversations.txt*
def loadConversations(fileName, lines, fields):
    conversations = []
    f = open(fileName, 'r', encoding='utf-8', errors = 'ignore')
    for line in f:
        values = line.split(" +++$+++ ")
        # Extraire les champs
        convObj = {}
        for i, field in enumerate(fields):
            convObj[field] = values[i]
        # Convertit un liste en chaîne (convObj["dialogueIDs"] == "['L598485', ...]")
        dialogue_id_pattern = re.compile('L[0-9]+')
        lineIds = dialogue_id_pattern.findall(convObj["dialogIDs"])
        # Rassembler les lignes
        convObj["lines"] = []
        for lineId in lineIds:
            if lineId in lines.keys():
                convObj["lines"].append(lines[lineId])
        conversations.append(convObj)

    f.close()
    return conversations

# TEST de loadConversations
champs_test_lc = ["personnage1ID", "personnage2ID", "filmID", "dialogIDs"]
conversations = loadConversations(os.path.join(corpus, "movie_conversations.txt"), lignes, champs_test_lc)
printList(conversations)


# Extrait les paires de phrases pour chaque conversation
def extractSentencePairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Boucler sur toutes les lignes de la conversation
        for i in range(len(conversation["lines"]) - 1):  # On ignore la dernière ligne (pas de réponse!)
            inputLine = conversation["lines"][i]["text"].strip()
            targetLine = conversation["lines"][i+1]["text"].strip()
            # On enlève les mauvais échantillons (si l'un de la liste est vide)
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs

# On définit un chemin vers un nouveau fichier
datafile = os.path.join(corpus, "formatted_movie_lines_FR-fr.txt")

delimiter = '\t'
# Enlever l'échappement sur le délimiteur (on veut un vrait \t pas \\t)
delimiter = str(codecs.decode(delimiter, "unicode_escape"))

# Initialiser lignes, conversations et champs
lines = {}
conversations = []
MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
MOVIE_CONVERSATIONS_FIELDS = ["character1ID", "character2ID", "movieID", "dialogIDs"]

# Charger les lignes et pré-traiter les conversations
print("\nDébut du pré-traitement...")
lines = loadLines(os.path.join(corpus, "movie_lines_FR-fr.txt"), MOVIE_LINES_FIELDS)
print("\nChargement des conversations...")
conversations = loadConversations(os.path.join(corpus, "movie_conversations.txt"),
                                  lines, MOVIE_CONVERSATIONS_FIELDS)

# Création d'un fichier de données au format csv contenant les paires questions/réponses
# séparées par un saut de ligne
print("\nEcriture du fichier formatté...")
outputfile = open(datafile, 'w', encoding='utf-8', errors = 'ignore')
writer = csv.writer(outputfile, delimiter=delimiter, lineterminator='\n')
for pair in extractSentencePairs(conversations):
    writer.writerow(pair)
outputfile.close()

# Afficher un échantillon des lignes
print("\nEchantillon des lignes:")
printFile(datafile)


# Default word tokens
PAD_token = 0  # Pour remplir les phrases courtes
SOS_token = 1  # Start-of-sentence token - Début de phrase
EOS_token = 2  # End-of-sentence token - Fin d'une phrase

class Vocable:
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3  # Compte SOS, EOS, PAD

    # Ajoute une phrase à notre dictionnaire
    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    # Ajoute un mot à notre dictionnaire
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    # Efface les mots qui n'apparaissent qu'en dessous d'un certain seuil
    def trim(self, min_count):
        if self.trimmed:
            return
        self.trimmed = True

        keep_words = []

        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        # Reinitialiser les dictionnaires
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3 # On compte les tokens par défaut

        for word in keep_words:
            self.addWord(word)

MAX_LENGTH = 10  # Longueur maximale

# Enlève les minuscules, les espaces et les chiffres et autres caractères bizarres
def normalizeString(s):
    s = re.sub(r"([!?])", r" \1", s)
    s = re.sub(r"([.])", r"\1 ", s)
    #s = re.sub(r"[^a-zA-Z.!?éèïê-ôëàâîçùüûœ']+", r" ", s)
    s = re.sub(r"[^a-zA-Z.!?éèïê-ôëàçù¨ûœÂÊÎÔÛÄËÏÖÜÀÆæÇÉÈŒœÙ']+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

# Lit les paires de questions réponses et retourne un objet Vocable
# On va travailler avec le fichier formatté
def readVocs(datafile, corpus_name):
    print("Lecture des lignes...")
    # Lit le fichier stocke chaque ligne dans un tableau
    # sans le '\n'
    lines = open(datafile, encoding='utf-8').\
        read().strip().split('\n')
    # Sépare chaque ligne en paires et les normalise
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    voc = Vocable(corpus_name)
    return voc, pairs

# Retourne vrai si les deux phrases dans un couple question/réponse
# ont une longuueur inférieure à MAX_LENGTH
def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH

# Filtre les paires en utilisant la condition
# de filterPair
def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

# Définir la fonction au-dessus, et retourner un objet Vocable ainsi qu'une suite de paires
def loadPrepareData(corpus, corpus_name, datafile, save_dir):
    print("Début de la phase d'entraînement ...")
    voc, pairs = readVocs(datafile, corpus_name)
    print("Lit {!s} paires de phrases".format(len(pairs)))
    pairs = filterPairs(pairs)
    print("Réduit en {!s} paires de phrases".format(len(pairs)))
    print("Comptage des mots...")
    for pair in pairs:
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
    print("Mots comptés:", voc.num_words)
    return voc, pairs


# Charger et assembler les objets vocable et les paires
save_dir = os.path.join(corpus, "save")
voc, pairs = loadPrepareData(corpus, "movie_lines_FR-fr.txt", datafile, save_dir)
# Afficher dix paires pour vérifier que tout marche nickel
print("\nPaires de questions/réponses:")
for pair in pairs[:10]:
    print(pair)

MIN_COUNT = 3    # Nombre d'occurences minimal accepté pour un moty

def trimRareWords(voc, pairs, MIN_COUNT):
    # Elimine les mots qui apparaissent moins de MIN_COUNT fois
    voc.trim(MIN_COUNT)
    # Enlève les paires qui contiennent des mots éliminés
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence = pair[1]
        keep_input = True
        keep_output = True
        # On vérifie la phrase d'entrée (question)
        for word in input_sentence.split(' '):
            if word not in voc.word2index:
                keep_input = False
                break
        # On vérifie la phrase de sortie (réponse)
        for word in output_sentence.split(' '):
            if word not in voc.word2index:
                keep_output = False
                break

        # Ne garde que les paires qui n'ont pas de mots éliminés
        if keep_input and keep_output:
            keep_pairs.append(pair)

    print("On avait {} paires et on en a gardé {}, soit un ratio de {:.4f}".format(len(pairs), len(keep_pairs), len(keep_pairs) / len(pairs)))
    return keep_pairs


# Retourne les paires dont les mots rares ont été filtrés
pairs = trimRareWords(voc, pairs, MIN_COUNT)
