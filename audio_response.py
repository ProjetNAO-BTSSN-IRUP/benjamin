# -*- coding: utf-8 -*

import socket
import time
from naoqi import ALProxy
import MySQLdb


class Response:
    
    def __init__(self):
        self.ip_nao = socket.gethostbyname("NAO")
        print ">>>{0}".format(self.ip_nao)
        self.tts = ALProxy("ALTextToSpeech", self.ip_nao, 9559)
        
        db = MySQLdb.connect(host="127.0.0.1",  # your host
                             user="root",  # username
                             passwd="",  # password
                             db="benjamin",
                             charset="utf8")  # name of the database
        
        # Create a Cursor object to execute queries.
        self.cur = db.cursor()
        # Select data from table using SQL query.
        self.cur.execute("SELECT Reponse FROM audio")

    def qr_code_recognition(self):
        barcode = ALProxy("ALBarcodeReader", self.ip_nao, 9559)
        barcode.subscribe("test_barcode")
    
        memory = ALProxy("ALMemory", self.ip_nao, 9559)
        
        is_recognized = False
        
        for i in range(20):
            data = memory.getData("BarcodeReader/BarcodeDetected")
            if data:
                is_recognized = True
                data = data[0][0].split(",")
                print type(data), data
                time.sleep(1)
                return is_recognized, data
            
            else:
                return is_recognized, data
    
    def get_response_in_database(self):
        n = 0
        for row in self.cur.fetchall():
            if n == 0:  # Dire que la premiere ligne
                response = row[0].encode("utf-8")
                print type(response), response
                # response = response.format(self.prenom, self.nom, self.retard)
                self.tts.say(response)
                # n += 1
    
    def response_from_facial_recognition(self):
        is_recognized = False
        
        if is_recognized:
            print "Face reconnue"
            self.get_response_in_database()
            
        else:
            print "Aucune reconnaissance"

    def response_from_qr_code_recognition(self):
        for i in range(3):
            # 3 tentatives de reconnaissance de QR code
            print i
            is_recognized, data = self.qr_code_recognition()
            if is_recognized:
                self.get_response_in_database()
                break  # On sort de la boucle si un qr code est reconnu
                
            print is_recognized
                
            time.sleep(2)
            
            # Si aucun qr code n'est reconnu au bout des 3 essais 
            if i == 2 and is_recognized == False:
                self.tts.say("Pas de QR code reconnu.")
    
        
    
            

Response().response_from_qr_code_recognition()
