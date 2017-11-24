import cv2
import numpy as np
import sqldb as db
import time
from imutils import paths
import os
import uuid
import trainer
from PIL import Image

recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load("recognizer/trainingData.yml")
cascade = cv2.CascadeClassifier('./Classifiers/haarcascade_frontalface_default.xml')

def detectMultiScale(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=2, minSize=(8, 8),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects

def train_from_folder(path):
    for subdir, dirs, files in os.walk(path):
        # for file in files:
        trainer.getImagesWithId(subdir)

def image_detection(path):
    for imagePath in paths.list_images(path):
        img = cv2.imread(imagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        predict_image = np.array(gray, 'uint8')

        rects = detectMultiScale(predict_image, cascade)

        for x1, y1, x2, y2 in rects:
            result = cv2.face.MinDistancePredictCollector()
            recognizer.predict(predict_image[y1:y2, x1:x2], result, 0)
            id = result.getLabel()
            conf = result.getDist()
            profile = db.getProfile(id)
            name = profile[1]
            print(conf)
            if (conf < 100):
                directory = 'faceCrops/' + name

                # print(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                cv2.imwrite(directory + '/User_' + str(id) + '_' + str(count) + ".jpg", gray[y1:y2, x1:x2])
                train_from_folder(directory)

            else:
                id = db.getNewID()
                name = uuid.uuid4()

                directory = 'faceCrops/' + name
                # print(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                cv2.imwrite(directory + '/User_' + str(id) + '_' + str(count) + ".jpg", gray[y1:y2, x1:x2])
                train_from_folder(directory)


image_detection('/bodyCrops2')






