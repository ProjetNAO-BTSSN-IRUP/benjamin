
import sys
import time

from PIL import Image
from naoqi import ALProxy


class PeoplePerception(object):

    def __init__(self, IP, PORT):
        self.peopleproxy = ALProxy("ALFaceDetection", IP, PORT)

        print "FaceDetection"
        print "***********************************"
        self.SetPpl(IP, PORT)
        print "***********************************"

    def SetPpl(self, IP, PORT):

        self.peopleproxy.subscribe("FaceDetection", 500, 00)

        self.peopleproxy.setRecognitionEnabled = True
        self.peopleproxy.setTrackingEnabled = True

        # print self.peopleproxy.forgetPerson("Olivier")
        print self.peopleproxy.learnFace("Olivier")
        print self.peopleproxy.getLearnedFacesList()

        self.peopleproxy.unsubscribe

    def getData(self, IP, PORT):

        self.memproxy = ALProxy("ALFaceDetection", IP, PORT)


# PeoplePerception("192.168.0.115", 9559)
PeoplePerception("192.168.1.43", 9559)