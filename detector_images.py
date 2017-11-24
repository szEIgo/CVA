import cv2
import numpy as np
import sqldb as db
import time
from imutils import paths
import os
import uuid
from PIL import Image
import trainer as train
import shutil


######################################## List of who's on work##################################
# for key, value in personDict.items():
#     personDict.update({key: time.time() - value})
#     print('time from dict: ',value)
#     if (personDict[key] > 5 and personDict[key] < 10):
#         if key in onWorkList:
#             onWorkList.remove(key)
#     if (key not in onWorkList and personDict[key] < 5):
#         onWorkList.append(key)
#     for value in onWorkList:
#         cv2.putText(vis, str(value), (25, int(40 * (onWorkList.index(value) + 1) * 0.5) + 130),
#                     cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
# cv2.putText(vis, str('Here:' + str(len(onWorkList))), (10, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
#             (255, 255, 255), 2)
######################################## List of who's on work##################################

# source = recognition(0)
# source = recognition("rtsp://allunite-1:Skippy123@192.168.128.38:554/videoMain")

def most_common(lst):
    return max(set(lst), key=lst.count)


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=2, minSize=(8, 8),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def draw_text(img, rects, text, location, font, fontScale, fontColor, lineType):
    for x1, y1, x2, y2 in rects:
        cv2.putText(img, str(text), location, font, fontScale, fontColor, lineType)


def recognize_images(path):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("recognizer/trainingData.yml")
    cascade = cv2.CascadeClassifier('./Classifiers/haarcascade_frontalface_alt.xml')
    count = 0

    for imagePath in paths.list_images(path):
        ### Read image & make compatible for LBPH
        img = cv2.imread(imagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        ### Extract image to matrix
        predict_image = np.array(gray, 'uint8')
        vis = img.copy()

        rects = detect(predict_image, cascade)

        for x1, y1, x2, y2 in rects:
            count += 1
            result = cv2.face.MinDistancePredictCollector()
            recognizer.predict(predict_image[y1:y2, x1:x2], result, 0)
            id = result.getLabel()
            conf = result.getDist()
            profile = db.getProfile(id)
            print(conf, '  --------  ', profile[0])
            if (conf < 120):
                if (profile != None):
                    directory = 'unorganized/'
                    # print(directory)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        cv2.imwrite(
                            directory + profile[0] + '_' + str(id) + '_' + str(count) + ".jpg",
                            gray[y1:y2, x1:x2])
                        train.train(directory)

            else:
                name = str(uuid.uuid4())
                id = db.getNewID()
                db.insertOrUpdate(id, name)
                directory = 'unorganized/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                cv2.imwrite(directory + '/' + name + '_' + str(id) + '_' + str(count) + ".jpg", gray[y1:y2, x1:x2])
                print('training all images')
                train.train(directory)


def recognize_folder(path):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("recognizer/trainingData.yml")
    cascade = cv2.CascadeClassifier('./Classifiers/haarcascade_frontalface_alt2.xml')
    count = 0
    rcount = 0
    rprofiles = []
    rfiles = list()
    for imagePath in paths.list_images(path):
        ### Read image & make compatible for LBPH
        img = cv2.imread(imagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        ### Extract image to matrix
        predict_image = np.array(gray, 'uint8')

        rects = detect(predict_image, cascade)

        for x1, y1, x2, y2 in rects:
            count += 1
            result = cv2.face.MinDistancePredictCollector()
            recognizer.predict(predict_image[y1:y2, x1:x2], result, 0)
            id = result.getLabel()
            conf = result.getDist()
            profile = db.getProfile(id)
            print(profile)
            rprofiles.append(profile[0])
            directory = 'unorganized/'
            print(conf)
            if (conf < 80):
                # if (profile != None):
                #     if not os.path.exists(directory+profile[0]):
                #         os.makedirs(directory+profile[0])
                #     directory += profile[0]
                #     cv2.imwrite(
                #         directory + '/' + profile[0] + '_' + str(id) + '_' + str(count) + ".jpg",
                #         gray[y1:y2, x1:x2])
                rcount += 1
                rfiles.append(str(imagePath.split('/')[4]))

    print(rfiles)
    print(rprofiles)
    threshold = int(rcount / count * 100)
    print(str(int(rcount / count * 100)) + ' %')
    # if known
    print(path)
    if threshold > 50:
        name = most_common(rprofiles)

        for subdir, dirs, files in os.walk(path):
            for file in files:
                if file in rfiles:
                    if not os.path.exists("./organized/" + name):
                        os.makedirs("./organized/" + name)
                    print(subdir+'/'+file)
                    # shutil.move(subdir+'/'+file, "/organized/" + name + '/' + file)

    # if unkown
    if threshold < 50:
        name = uuid.uuid4()
        print(name)

        # print(count/rcount)

        # name = str(uuid.uuid4())[1:4]
        # id = db.getNewID()
        # db.insertOrUpdate(id, name)
        # directory = 'unorganized/'
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        # cv2.imwrite(directory + '/' + name + '_' + str(id) + '_' + str(count) + ".jpg", gray[y1:y2, x1:x2])
        # print('training all images')
        # train.train(directory)


recognize_folder('./unidentified/faces/blabla')
