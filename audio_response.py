# -*- coding: utf-8 -*

import socket
from naoqi import ALProxy
import MySQLdb


class Response():
    
    def __init__(self):
        ip_nao = socket.gethostbyname("NAO")
        print ">>>{0}".format(ip_nao)
        self.tts = ALProxy("ALTextToSpeech", ip_nao, 9559)
        
        db = MySQLdb.connect(host="SRV-NAO",  # your host
                             user="benjamin",  # username
                             passwd="benjamin",  # password
                             db="benjamin")  # name of the database
        
        # Create a Cursor object to execute queries.
        self.cur = db.cursor()
        # Select data from table using SQL query.
        self.cur.execute("SELECT Reponse FROM audio")
        self.prenom = "Frederic"
        self.nom = "Chopin"
        self.retard = 40
    
    def get_response_in_database(self):
        n = 0
        for row in self.cur.fetchall():
            if n == 0:  # Dire que la premiere ligne
                # print type(row[0]), row[0]
                response = row[0]
                response = response.format(self.prenom, self.nom, self.retard)
                self.tts.say(response)
                # n += 1
    
    def response_from_facial_recognition(self):
        is_recognized = True
        
        if is_recognized:
            print "Face reconnue"
            self.get_response_in_database()
            
        else:
            print "Aucune reconnaissance"

    def response_from_qr_code_recognition(self):
        is_recognized = False
    
        if is_recognized:
            
            self.get_response_in_database()
    
        else:
            print "Aucune reconnaissance"
            

Response().response_from_facial_recognition()


# Question/Réponse
# tts.say("Tu vas bien ?")
# x = raw_input()
# if x == "oui":
#     tts.say("C'est bien.")
# if x == "non":
#     tts.say("Cool.")


