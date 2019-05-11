# -*- coding: utf-8 -*

import socket
import time
from naoqi import ALProxy
import MySQLdb


def nao_ip():
    ip_nao = socket.gethostbyname("NAO")
    return ip_nao


def qr_code_recognition():
    # ip_nao = nao_ip()
    ip_nao = "192.168.0.25"
    barcode = ALProxy("ALBarcodeReader", ip_nao, 9559)
    barcode.subscribe("test_barcode")
    
    memory = ALProxy("ALMemory", ip_nao, 9559)
    
    for i in range(20):
        data = memory.getData("BarcodeReader/BarcodeDetected")
        if data:
            is_recognized = True
            data = data[0][0].split(",")
            print type(data), data
            time.sleep(1)
            return is_recognized, data
        

qr_code_recognition()

class Response:
    
    def __init__(self):
        ip_nao = nao_ip()
        print ">>>{0}".format(ip_nao)
        self.tts = ALProxy("ALTextToSpeech", ip_nao, 9559)
        
        db = MySQLdb.connect(host="SRV-NAO",  # your host
                             user="benjamin",  # username
                             passwd="benjamin",  # password
                             db="benjamin",
                             charset="utf8")  # name of the database
        
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
        is_recognized = True
    
        if is_recognized:
            
            self.get_response_in_database()
    
        else:
            print "Aucune reconnaissance"
            

# Response().response_from_qr_code_recognition()
