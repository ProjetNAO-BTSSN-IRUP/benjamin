import sys
import time

from PIL import Image
from naoqi import ALProxy


class PeoplePerception(object):

    def __init__(self, IP, PORT):
        self.proxy = None

        print " Processus de reconnaissance : Demarrage"
        self.NewPpl(IP, PORT)

    def NewPpl(self, IP, PORT):

        faceproxy = ALProxy("ALFaceDetection", IP, PORT)
        faceproxy.subscribe("Test_Face", 500, 0.0)

        memory = ALProxy("ALMemory", IP, PORT)
        memValue = "FaceDetected"


        for i in range(0, 20):
            time.sleep(0.5)
            face = memory.getData(memValue)

            print ""
            print "*****"
            print ""

            # Verification lorsque que la donnee renvoyer est correcte
            if face and isinstance(face, list) and len(face) >= 2:

                # Visage detecte
                # Pour chaque visage, les valeurs de ce derniers sont recuperer

                # Premier champ = Valeur de temps
                timeStamp = face[0]

                # Deuxieme champ = Face Info.
                faceInfoArray = face[1]

                try:
                    # Pour recuperer chaque valeur de chaque visage rencontre
                    for j in range(len(faceInfoArray) - 1):
                        faceInfo = faceInfoArray[j]


                        # Premier champ = info de forme
                        faceShapeInfo = faceInfo[0]

                        # Second champ = info bonus
                        faceExtraInfo = faceInfo[1]

                        print faceInfo
                        print "  Dist %.3f - Angle %.3f" % (faceShapeInfo[1], faceShapeInfo[2])  # Valeur de distane et d'angle de vue entre le robot et le visage
                        print "  Largeur %.3f - Hauteur %.3f" % (faceShapeInfo[3], faceShapeInfo[4]) # Valeur de largeur et de hauteur du visage dectecte

                        if faceExtraInfo[2] != "":
                            print " Nom = %s" % (faceExtraInfo[2])
                        else:
                            print " Personne inconnu du systemes"

                except Exception, e:
                    print "Visage dectecte mais donnee invalide. ALValue ="
                    print face
                    print "Message d'erreur %s" % (str(e))
            else:
                print "Pas de visage detecte"


# PeoplePerception("192.168.0.115", 9559)
PeoplePerception("192.168.1.43", 9559)