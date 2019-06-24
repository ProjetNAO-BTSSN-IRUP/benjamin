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
    
    cours = datetime.now().replace(microsecond=0) - timedelta(minutes=10)
    now = datetime.now().replace(microsecond=0)
    fin = now + timedelta(hours=3)
    
    cur.execute("INSERT INTO planning (Site, Salle, DateDebut, DateFin, Filiere, Promotion, idIntervenant, Matiere) VALUES ('Fraissinette', 'E T13', '" + str(cours) + "', '" + str(fin) + "', 'SN', '17', '1', 'Réseau')")
    cur.execute("INSERT INTO retard (DateCours, HeureArrivee, Matiere, idApprenant) VALUES ('" + str(cours) + "', '" + str(now) + "', 'Réseau', '1')")
    db.commit()
    
insert()