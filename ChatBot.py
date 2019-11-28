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

Dialogues = open("Sources/movie_lines_traduit.txt", "r", encoding = "utf-8", errors="ignore")
TxtDialogue = Dialogues.read()

Conversations = open("Sources/movie_conversations.txt", "r", encoding = "utf-8", errors="ignore")
TxtConversations = Conversations.read()
