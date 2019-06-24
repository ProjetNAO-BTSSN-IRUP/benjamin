# -*- coding: utf-8 -*-

import socket
import time
from datetime import datetime, timedelta
from naoqi import ALProxy
import MySQLdb


class Response:
    
    def __init__(self, ip_nao):
        self.tts = ALProxy("ALTextToSpeech", ip_nao, 9559)
        self.recognition = ALProxy("ALSpeechRecognition", ip_nao, 9559)
        self.memory = ALProxy("ALMemory", ip_nao, 9559)
        self.barcode = ALProxy("ALBarcodeReader", ip_nao, 9559)
        self.recognition.setLanguage("French")
        
        db = MySQLdb.connect(host="192.168.0.19",  # your host
                             user="Administrateur",  # username
                             passwd="N@o!SN17#BDD",  # password
                             db="nao", # name of the database
                             charset="utf8")
        
        # Create a Cursor object to execute queries.
        self.cur = db.cursor()
        # self.cur.execute("SELECT Reponse FROM audio WHERE idAudio = 0")
        
        
    def qr_code_recognition(self):
        """Code de Samantha Alton"""
        
        self.barcode.subscribe("test_barcode")
        
        is_recognized = False
        
        for i in range(20):
            data = self.memory.getData("BarcodeReader/BarcodeDetected")
            if data:
                is_recognized = True
                data = data[0][0].split(",")
                print type(data), data
                time.sleep(1)
                return is_recognized, data
            
            else:
                return is_recognized, data
    
    def get_response_in_database(self, data, id_response):
        # Select data from table using SQL query.
        print id_response
        self.cur.execute("SELECT * FROM audio WHERE idAudio = " + str(id_response))
        for row in self.cur.fetchall():
            self.id_audio = str(row[0])
            self.reponse = row[1].encode("utf-8")
        now = datetime.now().replace(microsecond=0)
        
        if id_response == 1:
    
            planning = self.cur.execute("SELECT * FROM planning WHERE idIntervenant =" + data[0] + " AND DateFin > '" + str(now) + "' ORDER BY DateDebut ASC LIMIT 1")
            print ">>>>", planning
            if planning == 1:
                for row in self.cur.fetchall():
                    print "row ", row
                    site = row[1]
                    salle = row[2]
                    heure = row[3].hour
                    minute = row[3].minute
                    promotion = row[5] + row[6]
                    if minute == 0:
                        temps = "{0} heures".format(heure)
                    else:
                        temps = "{0} heures {1}".format(heure, minute)
                    reponse = self.reponse.format(data[1], data[2], temps, salle, site, promotion)
                    print ">>>", reponse
            
                    self.tts.say(reponse)
    
            if planning == 0:
                self.tts.say("Bonjour {0} {1}. Je ne trouve aucun cours à venir ou ayant commencé vous concernant.".format(data[1], data[2]))
            
        if id_response == 2:
            self.cur.execute("SELECT FiliereApprenant, PromotionApprenant FROM apprenant WHERE idApprenant = " + data[0])
            for row in self.cur.fetchall():
                self.filiere = row[0]
                self.promotion = row[1]
            
            retard = self.cur.execute("SELECT DateCours, HeureArrivee, Matiere FROM retard WHERE idApprenant = " + data[0] + " ORDER BY idRetard DESC LIMIT 1")
            for row in self.cur.fetchall():
                app_cours = row[0]
                app_arrivee = row[1]
                cours = row[2].encode("utf-8")
                app_retard = app_arrivee - app_cours
    
                heure_cours = row[0].hour
                heure_arrivee = row[1].hour
                minute_cours = row[0].minute
                minute_arrivee = row[1].minute
                heure_retard = heure_arrivee - heure_cours
                minute_retard = minute_arrivee - minute_cours
                print cours
                
            self.cur.execute("SELECT DateFin FROM planning, retard WHERE retard.DateCours = planning.DateDebut AND retard.Matiere = planning.Matiere")
            
            for row in self.cur.fetchall():
                date_fin = row[0]
                print date_fin
            
            print "ret", retard
            if retard == 1:
                if date_fin > now:
                    if heure_retard == 0:
                        retard = "{0} minutes".format(str(minute_retard))
                    elif heure_retard > 0:
                        retard = "{0} heures et {1} minutes".format(str(heure_retard), str(minute_retard))
                    print "===", retard
                    
                    if app_retard > timedelta(minutes=0) and app_retard < timedelta(minutes=30):
                        self.cur.execute("SELECT * FROM audio WHERE idAudio = 3")
                        for row in self.cur.fetchall():
                            self.reponse = row[1].encode("utf-8")

                        planning = self.cur.execute(
                            "SELECT * FROM planning WHERE Filiere = '" + self.filiere + "' AND Promotion = '"
                            + self.promotion + "' AND DateFin > '" + str(now) + "' ORDER BY DateDebut ASC LIMIT 1")
                        
                        if planning == 1:
                            for line in self.cur.fetchall():
                                matiere = line[8].encode("utf-8")
                                id_intervenant = str(line[7])
                                salle = line[2].encode("utf-8")
                                site = line[1].encode("utf-8")
                                self.cur.execute("SELECT NomIntervenant, PrenomIntervenant FROM intervenant WHERE idIntervenant = " + id_intervenant)
                                for elt in self.cur.fetchall():
                                    nom = elt[0].encode("utf-8")
                                    prenom = elt[1].encode("utf-8")
                            
                            reponse = self.reponse.format(data[1], data[2], retard, matiere, prenom, nom, salle, site)
                            self.tts.say(reponse)
                            
                        elif planning == 0:
                            self.tts.say(
                                "Bonjour {0} {1}. Je ne trouve aucun cours à venir ou ayant commencé vous concernant.".format(
                                    data[1], data[2]))
                        
                    elif app_retard >= timedelta(minutes=30):
                        self.cur.execute("SELECT * FROM audio WHERE idAudio = 4")
                        for row in self.cur.fetchall():
                            self.reponse = row[1].encode("utf-8")
    
                        planning = self.cur.execute(
                            "SELECT * FROM planning WHERE Filiere = '" + self.filiere + "' AND Promotion = '"
                            + self.promotion + "' AND DateFin > '" + str(now) + "' ORDER BY DateDebut ASC LIMIT 1")
                        if planning == 1:
                            for line in self.cur.fetchall():
                                matiere = line[8].encode("utf-8")
                                id_intervenant = str(line[7])
                                salle = line[2].encode("utf-8")
                                site = line[1].encode("utf-8")
                                self.cur.execute(
                                    "SELECT NomIntervenant, PrenomIntervenant FROM intervenant WHERE idIntervenant = " + id_intervenant)
                                for elt in self.cur.fetchall():
                                    nom = elt[0].encode("utf-8")
                                    prenom = elt[1].encode("utf-8")
        
                            reponse = self.reponse.format(data[1], data[2], retard, matiere, prenom, nom, salle, site)
                            self.tts.say(reponse)
                            
                        elif planning == 0:
                            self.tts.say(
                                "Bonjour {0} {1}. Je ne trouve aucun cours à venir ou ayant commencé vous concernant.".format(
                                    data[1], data[2]))
                            
                elif date_fin < now:
                    retard = 0
                    
            if retard == 0:
                planning = self.cur.execute(
                    "SELECT * FROM planning WHERE Filiere = '" + self.filiere + "' AND Promotion = '" + self.promotion + "' AND DateFin > '" + str(now) + "' ORDER BY DateDebut DESC LIMIT 1")
                
                if planning == 1:
                    for row in self.cur.fetchall():
                        print "row ", row
                        site = row[1]
                        salle = row[2]
                        heure = row[3].hour
                        minute = row[3].minute
                        
                        if minute == 0:
                            temps = "{0} heures".format(heure)
                        else:
                            temps = "{0} heures {1}".format(heure, minute)
                            
                        self.cur.execute("SELECT NomIntervenant, PrenomIntervenant FROM intervenant WHERE idIntervenant = " + str(row[7]))
                        for line in self.cur.fetchall():
                            nom_professeur = line[0].encode("utf-8")
                            prenom_professeur = line[1].encode("utf-8")
                        matiere = row[8].encode("utf-8")
                        reponse = self.reponse.format(data[1], data[2], matiere, prenom_professeur, nom_professeur, temps, salle, site)
                        print ">>>", reponse
                        
                        self.tts.say(reponse)
                        
                if planning == 0:
                    self.tts.say(
                        "Bonjour {0} {1}. Je ne trouve aucun cours à venir ou ayant commencé vous concernant.".format(
                            data[1], data[2]))
                
        if id_response == 5:
            self.tts.say(self.reponse)
            
            words = ["technique", "filière", "inscription", "oui", "non", "annuler", "BTS", "BACHELOR", "S E E"]
            self.recognition.setVocabulary(words, False)
            
            self.memory.declareEvent("WordRecognized")
            
            self.recognition.subscribe("test_speech")
            print 'Speech recognition engine started'
            
            time.sleep(4)

            word = self.memory.getData("WordRecognized")
            self.recognition.unsubscribe("test_speech")
            
            if word:
                print ">>>>", word
                if word[0] == 'technique':
                    self.cur.execute("SELECT * FROM audio WHERE idAudio = 6")
                    for row in self.cur.fetchall():
                        print row
                        self.tts.say(row[1].encode("utf-8"))
                
                elif word[0] == 'filière':
                    self.tts.say('Bien sûr, quelle filière voulez-vous connaitre : BTS ? BACHELORE ? S E E ? Pour annuler, dîtes, annuler.')
                    
                    self.recognition.subscribe("test_speech")
                    print 'Speech recognition engine started'

                    time.sleep(4)

                    answer = self.memory.getData("WordRecognized")
                    self.recognition.unsubscribe("test_speech")
                    
                    if answer:
                        if answer[0] == "BTS":
                            self.cur.execute("SELECT * FROM audio WHERE idAudio = 7")
                            for row in self.cur.fetchall():
                                print row
                                self.tts.say(row[1].encode("utf-8"))
    
                        elif answer[0] == "BACHELOR":
                            self.cur.execute("SELECT * FROM audio WHERE idAudio = 8")
                            for row in self.cur.fetchall():
                                print row
                                self.tts.say(row[1].encode("utf-8"))
                                
                        elif answer[0] == "S E E":
                            self.cur.execute("SELECT * FROM audio WHERE idAudio = 9")
                            for row in self.cur.fetchall():
                                print row
                                self.tts.say(row[1].encode("utf-8"))

                        if word[0] == 'annuler':
                            self.tts.say("Pas de soucis, bonne journée !")

                    else:
                        self.cur.execute("SELECT * FROM audio WHERE idAudio = 11")
                        for row in self.cur.fetchall():
                            print row
                            self.tts.say(row[1].encode("utf-8"))
                        
                elif word[0] == 'inscription':
                    self.cur.execute("SELECT * FROM audio WHERE idAudio = 10")
                    for row in self.cur.fetchall():
                        print row
                        self.tts.say(row[1].encode("utf-8"))
                        
                if word[0] == 'annuler':
                    self.tts.say("Pas de soucis, bonne journée !")
                        
            else:
                self.cur.execute("SELECT * FROM audio WHERE idAudio = 11")
                for row in self.cur.fetchall():
                    print row
                    self.tts.say(row[1].encode("utf-8"))
            
    def response_from_facial_recognition(self, is_recognized, data):
        if is_recognized:
            if data[3] == "intervenant":
                self.get_response_in_database(data, 1)
    
            if data[3] == "apprenant":  # Si apprenant
                self.get_response_in_database(data, 2)
    
            if data[3] == "visiteur":
                self.get_response_in_database(data, 5)
            
        else:
            self.tts.say("Votre visage n'a pas été reconnu, veuillez montrer votre QR code.")
            self.response_from_qr_code_recognition()

    def response_from_qr_code_recognition(self):
        for i in range(3):
            # 3 tentatives de reconnaissance de QR code
            print "Tentative n°", i + 1
            is_recognized, data = self.qr_code_recognition()
            
            if is_recognized:
                if data[3] == "intervenant":
                    self.get_response_in_database(data, 1)
                
                if data[3] == "apprenant":  # Si apprenant
                    self.get_response_in_database(data, 2)
                    
                if data[3] == "visiteur":
                    self.get_response_in_database(data, 5)
                    
                break  # On sort de la boucle si un qr code est reconnu
                
            print is_recognized, ", non reconnu"
            
            time.sleep(2)
            
            # Si aucun qr code n'est reconnu au bout des 3 essais
            if i == 2 and is_recognized == False:
                print "Désolé, mais je n’arrive pas à reconnaître votre QR code. Veuillez vous renseigner auprès d’un de mes " \
                      "collègues humains. Bonne journée à vous."
                self.tts.say("Désolé, mais je n’arrive pas à reconnaître votre QR code. Veuillez vous renseigner auprès d’un "
                             "de mes collègues humains. Bonne journée à vous.")
    
