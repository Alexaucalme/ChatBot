import pyttsx3
engine = pyttsx3.init()


engine.setProperty('rate', 120)    # Vitesse (peut dépasser 100)
engine.setProperty('volume', 3)
# Les identifiants de voix calculés par
# la fonction précédente.
# Elles dépendent du systèmevoices = engine.getProperty('voices')



engine.setProperty('voice', 'french')
engine.say("Je suis le botte d'alexandre et je parle !")

engine.runAndWait()
