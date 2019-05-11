# -*- coding: utf-8 -*

import socket
from naoqi import ALProxy
import MySQLdb


class Conn:
    def __init__(self, pNom, pLargeur, pHauteur, pExtraInfo = ""):

        localhost = "127.0.0.1"
        SRV_NAO = "192.168.0.19"
        db = MySQLdb.connect(host=localhost,  # your host
                             user="olivier",  # username
                             passwd="olivier",  # password
                             db="olivier")  # name of the database

        # Create a Cursor object to execute queries.
        self.cur = db.cursor()

        # Select data from table using SQL query.
        if (pNom != "") and (pLargeur != "") and (pHauteur != ""):
            if pExtraInfo == "":
                self.cur.execute("SELECT `InfoPersonne`, `idFaciale`, `Largeur_Visage`, `Hauteur_Visage`,"
                                 "`Extra_Info`, `idApprenant`, `idProfesseur` "
                                 "FROM `faciale` WHERE `InfoPersonne` = '" + pNom + "' AND `Largeur_Visage` = '" + pLargeur + "' AND `Hauteur_Visage` = '" + pHauteur + "' ")
            else:
                self.cur.execute("SELECT `InfoPersonne`, `idFaciale`, `Largeur_Visage`, `Hauteur_Visage`,"
                                 "`Extra_Info`, `idApprenant`, `idProfesseur` "
                                 "FROM `faciale` WHERE `InfoPersonne` = '" + pNom + "' AND `Largeur_Visage` = '" + pLargeur + "' AND `Hauteur_Visage` = '" + pHauteur + "' AND `Extra_Info` = '" + pExtraInfo + "' ")

    def InsertInfo(self, pNom, pLargeur, pHauteur, pExtraInfo = ""):
        self.cur.execute("INSERT INTO faciale(`InfoPersonne`,`Largeur_Visage`, `Hauteur_Visage`, `Extra_Info` ,`idApprenant` ,`idProfesseur`) "
                         "VALUES (pNom, pLargeur, pHauteur, pExtraInfo, idApprenant, idProfesseur)")

    def RecupVal(self):
        i = 0
        rc = self.cur.rowcount
        for row in self.cur.fetchall():

            while i < rc:

                print "***************"
                print rc
                print ""
                print row[i]
                print ""
                print "***************"
                i += 1


print "/*/*/*/*/*/*/*/*/*/"
print ("TABLE FACIALE")
Conn().get_all()
print "/*/*/*/*/*/*/*/*/*/"