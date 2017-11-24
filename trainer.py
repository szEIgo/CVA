import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.createLBPHFaceRecognizer()


# recognizer = cv2.face.createFisherFaceRecognizer()
# recognizer = cv2.face.createEigenFaceRecognizer()


def getImagesWithId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        face_img = Image.open(imagePath).convert('L')
        face_npa = np.array(face_img, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('_')[1])
        faces.append(face_npa)
        print(ID)
        IDs.append(ID)
        cv2.imshow("training", face_npa)
        cv2.waitKey(10)
    return IDs, faces


# recognizer.load('recognizer/trainingData.yml')
def train(path):
    Ids, faces = getImagesWithId(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.save('recognizer/trainingData.yml')


train('unidentified/faces/blabla/')
