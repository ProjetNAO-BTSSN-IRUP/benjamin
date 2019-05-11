# Initialisation des librairies/modules
import sys
import time
import MySQLdb
import socket

from PIL import Image
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

# # # # # # # # #Definition du code


class HumanGreeterModule(ALModule):
    """
    Un module qui reagit lorsqu'un visage est detecte
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # IP non necessaire car le module ALBroker est utilise ici

        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FaceDetected",
            "HumanGreeter",
            "onFaceDetected")

    def onFaceDetected(self, *_args):
        """
        Cette event est appele a chaque fois qu'un visage est detecte
        """

        # Unsubcribe pour eviter les repetitions
        memory.unsubscribeToEvent("FaceDetected",
            "HumanGreeter")

        # Le processus qui sera appeler a chaque visage detecte
        self.tts.say("Ok")

        # Subscribe pour recommencer
        memory.subscribeToEvent("FaceDetected",
            "HumanGreeter",
            "onFaceDetected")


class PeoplePerception(object):

    def __init__(self, IP, PORT):
        self.proxy = None

        print " Processus de reconnaissance : Demarrage"
        self.RecoVisage(IP, PORT)

    def RecoVisage(self, IP, PORT):

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
                            nom_personne = faceExtraInfo[2]
                            print " Nom = %s" % (faceExtraInfo[2])
                        else:
                            print " Personne inconnu du systemes"

                except Exception, e:
                    print "Visage dectecte mais donnee invalide. ALValue ="
                    print face
                    print "Message d'erreur %s" % (str(e))
            else:
                print "Pas de visage detecte"


def main():
    """
    Main entry point
    """

    # Variables Globale
    global memory
    global HumanGreeter
    global faceInfo
    global faceShapeInfo
    global faceExtraInfo
    global nom_personne
    global timeStamp
    global PORT
    global IP_BTS
    global IP_Home

    IP_Home = "192.168.0.25"
    IP_BTS = "192.168.0.115"
    PORT = 9559

    parser = OptionParser()
    parser.add_option("--pip",
                      help=IP_Home,
                      dest="pip")
    parser.add_option("--pport",
                      help=PORT,
                      dest="pport",
                      type="int")
    parser.set_defaults(
        pip=IP_Home,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # listen to anyone
                        0,  # find a free port and use it
                        pip,  # parent broker IP
                        pport)  # parent broker port

    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable

    HumanGreeter = HumanGreeterModule("HumanGreeter")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()