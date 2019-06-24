# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime, timedelta

def insert():
    db = MySQLdb.connect(host="192.168.0.19",  # your host
                         user="Administrateur",  # username
                         passwd="N@o!SN17#BDD",  # password
                         db="nao",  # name of the database
                         charset="utf8")
    
    cur = db.cursor()
    
    now = datetime.now().replace(microsecond=0) + timedelta(minutes=10)
    print "now", now
    fin = now + timedelta(hours=3, minutes=30)
    print "fin", fin
    
    cur.execute("INSERT INTO planning (Site, Salle, DateDebut, DateFin, Filiere, Promotion, idIntervenant, Matiere) VALUES ('Fraissinette', 'E T13', '" + str(now) + "', '" + str(fin) + "' , 'SN', '17', '1', 'Réseau')")
    db.commit()
    
insert()