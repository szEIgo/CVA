import cv2
import numpy as np
import sqlite3
import mysql.connector
import time
import os

def recognition(video):

    recognition.count = 0
    recognition.fps = 0
    nowTime = time.time()
    personDict = {}
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("recognizer/trainingData.yml")
    cascade = cv2.CascadeClassifier('./Classifiers/haarcascade_frontalface_default.xml')
    # nested = cv2.CascadeClassifier('./Classifiers/haarcascade_eye.xml')
    # nested = cv2.CascadeClassifier('./Classifiers/pedestrians.xml')
    cam = cv2.VideoCapture(video)
    onWorkList = []
    # cam.set(5, 5)
    # path = 'dataSet'

    def getProfile(id):
        conn = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='root',
                                       password='allunite')
        cmd = "SELECT * FROM People WHERE ID=" + str(id)
        cursor = conn.cursor()
        cursor.execute(cmd)
        profile = None
        for row in cursor:
            profile = row
        conn.close()
        return profile

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

    while (True):
        recognition.count = recognition.count + 1
        # recognition.fps = recognition.fps + cam.get(cv2.CAP_PROP_FPS)
        # print(recognition.fps)
        timeElapsed = int(time.time()-nowTime)
        # textInfo1 = 'frames read: ', int(recognition.count), 'time elapsed: ', int(timeElapsed)
        # textInfo2 = 'AVG FPS: ', int(recognition.count / timeElapsed)
        # if(timeElapsed % 10 == 0):
            # print('frames read: ', recognition.count, 'time elapsed: ', timeElapsed)
            # print('FPS: ', recognition.count/timeElapsed)
        # percentOfInput = (recognition.fps-recognition.count)/(recognition.fps)
        # print(100-percentOfInput)
        # cam.set(1, recognition.fps)
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        predict_image = np.array(gray, 'uint8')

        rects = detect(predict_image, cascade)
        #############
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        #############
        # cv2.putText(vis, str(textInfo1), (10, 300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7,
        #             (0, 255, 0), 2)
        # cv2.putText(vis, str(textInfo2), (10, 320),
        #             cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 255, 0), 2)



        ######################################## List of who's on work ##################################
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





        for x1, y1, x2, y2 in rects:
            # subrects = detect(roi.copy(), nested)
            # draw_rects(vis_roi, subrects, (255, 0, 0))
            result = cv2.face.MinDistancePredictCollector()
            recognizer.predict(predict_image[y1:y2, x1:x2], result, 0)
            id = result.getLabel()
            conf = result.getDist()
            profile = getProfile(id)
            print('profile: ', profile, 'conf: ', conf)
            if (conf < 70):
                if (profile != None):
                    # distConf = conf-40
                    conf = int((200-conf)/2)
                    personDict.update({profile[1]: time.time()})
                    directory = 'faceCrops/' + profile[1]
                    print(directory)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    cv2.imwrite(directory + '/' + profile[1] + str(recognition.count) + ".jpg", predict_image[y1:y2, x1:x2])
                    draw_text(vis, rects, profile[0], (x1, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2),
                    draw_text(vis, rects, profile[1], (x1, y1 + 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255),2),
                    draw_text(vis, rects, str(conf) + '%', (x1, y1-25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2),
            else:
                draw_text(vis, rects, "unknown", (x1, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        cv2.imshow("Face", vis)
        conf = 0
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    print(time.time() - nowTime)

#
# ### Ip Camera (android)
# recognition(0)
# recognition('rtsp://192.168.128.87:8080/h264_pcm.sdp')
#
# ### IT-departmentb
# recognition('rtsp://admin:allunite12@192.168.128.10:554/videoMain')
# ### HALL
recognition('rtsp://allunite-1:Skippy123@192.168.128.38:554/videoMain')
#
# ### Video source
# recognition('./videos/alexg/3.mkv')
