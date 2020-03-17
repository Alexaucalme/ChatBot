#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 18:32:14 2019

@author: alexaucalme
"""

FichierTraduit = open("Sources/movie_lines_traduit.txt", "w", encoding = "utf-8", errors="ignore")
FichierATraduire = open("Sources/movie_lines.txt", "r", encoding = "utf-8", errors="ignore")
FichierTraductions = open("Sources/dialogues_fr-cut.txt", "r", encoding = "utf-8", errors="ignore")

TableauLignesAModifier =  []
for ligne in FichierATraduire:
    TableauLignesAModifier.append(ligne.split(" +++$+++ "))

TableauLignesTraduites =  []
for ligne in FichierTraductions:
    TableauLignesTraduites.append(ligne)

for i in range(15000):
    Ligne = TableauLignesAModifier[i][0] + " +++$+++ " + TableauLignesAModifier[i][1] + " +++$+++ "+ TableauLignesAModifier[i][2] + " +++$+++ " + TableauLignesAModifier[i][3] + " +++$+++ " + TableauLignesTraduites[i] + "\n"
    FichierTraduit.write(Ligne)

FichierTraduit.close()
FichierATraduire.close()
FichierTraductions.close()