import cv2
import numpy as np
import imutils
import mysql.connector
from imutils import paths
import time
import os
from scipy import ndimage


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith('.mp4') or f.endswith(".mkv"):
                print('{}{}'.format(subindent, f))


def list_dirs(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        print(subindent)


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def crop_images(path, show):
    cascade = cv2.CascadeClassifier(begin.classifier)
    directory = 'unidentified/faces/'

    # for imagePath in paths.list_images(path):

    for subdir, dirs, files in os.walk(path):
        for imagePath in files:
            filepath = subdir + os.sep + imagePath
            if(filepath not in begin.seen):
                if filepath.endswith(".jpg") or filepath.endswith(".jpg"):
                    dirName = filepath.split('/')[2]

                    print('read: ', begin.readCount, 'saved: ', begin.count)
                    begin.readCount += 1
                    img = cv2.imread(filepath)
                    orig = img.copy()
                    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
                    gray = cv2.equalizeHist(gray)
                    rects = detect(gray, cascade)
                    begin.seen.append(filepath)

                    for x1, y1, x2, y2 in rects:
                        begin.count += 1
                        if not os.path.exists(directory + dirName):
                            os.makedirs(directory + dirName)
                        cv2.imwrite(directory + dirName + '/' + str(begin.count) + ".jpg", gray[y1:y2, x1:x2])
                        print('SAVED: ' + directory + str(begin.count) + ".jpg")
                        if (show):
                            draw_rects(img, rects, (255, 133, 133))
                    if show:
                        cv2.imshow("Face", img)
                        cv2.moveWindow('before', 0, 0)
                        cv2.waitKey(10)


def crop_videos(video, show):
    cascade = cv2.CascadeClassifier(begin.classifier)
    cam = 0
    orig = 0
    toned_image = 0
    cam = cv2.VideoCapture(video)
    fileName = str(video.split('/')[-1])[:-4]
    directory = 'unidentified/faces/'
    while (True):
        ret, image = cam.read()
        cv2.waitKey(5)
        if image is None:
            cam.release()
            break
        toned_image = image.copy()
        gray = cv2.cvtColor(toned_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        begin.readCount += 1
        print('read: ', begin.readCount, 'saved: ', begin.count)

        orig = image.copy()
        # image = imutils.resize(image, width=(int(image.shape[1] / 4)))
        rects = detect(gray, cascade)

        for x1, y1, x2, y2 in rects:
            begin.count += 1
            print(directory)
            if not os.path.exists(directory + fileName):
                os.makedirs(directory + fileName)
            cv2.imwrite(directory + fileName + '/' + str(begin.count) + ".jpg",
                        orig[y1:y2, x1:x2])
            print(directory + fileName + '/' + str(begin.count))
            if (show):
                draw_rects(image, rects, (255, 133, 133))
        if show:
            cv2.imshow("Face", image)
            cv2.moveWindow('before', 0, 0)
            cv2.waitKey(1)
        cv2.waitKey(1)
    while False:
        cam.release()


def produce(path, show, choice):
    if choice == 3 or choice == 4:
        if choice == 3:
            crop_videos(path, show)
        elif choice == 4:
            crop_videos(path, show)

    elif choice == 1 or choice == 2:
        for subdir, dirs, files in os.walk(path):
            for file in files:
                filepath = subdir + os.sep + file
                if choice == 1:
                    if filepath.endswith(".mkv") or filepath.endswith(".mp4"):
                        crop_videos(filepath, show)
                else:
                    if filepath.endswith('jpg') or filepath.endswith('png'):
                        crop_images(subdir, show)
                        # os.remove(filepath)


def begin():
    begin.count = 0
    begin.readCount = 0
    begin.seen = []
    begin.classifier = './Classifiers/haarcascade_frontalface_alt2.xml'
    os.system('cls' if os.name == 'nt' else 'clear')

    showWork = input('Crop bodies from source '
                     'do you want to see pictures '
                     'while its working? \n\n'
                     'Y/N or YES/NO\n'
                     '_____________________________\n').lower()

    if showWork != 'y' and showWork != 'n' and showWork != 'no' and showWork != 'yes':
        os.system('cls' if os.name == 'nt' else 'clear')
        begin()
    else:
        if (showWork == 'y' or showWork == 'yes'):
            showWork = True
        else:
            showWork = False

        os.system('cls' if os.name == 'nt' else 'clear')
        choice = int(input('Input a number 1-4:\n'
                           '1. Crop all videos in subdirectories\n'
                           '2. Crop all images in subdirectories\n'
                           '3. Crop images in a specific directory\n'
                           '4. Crop video\n'))

        if choice > 4 or choice < 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            begin()

        if choice == 1:
            produce('./videos', showWork, choice)
        elif choice == 2:
            produce('./unidentified/bodies', showWork, choice)
        else:

            if choice == 3:
                dir = input('list all relevant directories?\n'
                            '______________________________\n'
                            'Y/N or YES/NO\n').lower()
                if dir != 'y' and dir != 'n' and dir != 'no' and dir != 'yes':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    begin()
                else:
                    if (dir == 'y' or dir == 'yes'):
                        list_dirs('./')
                    else:
                        dir = False
                    dir = str(input('write path!\n '
                                    'example: unidentified/bodies/}\n'))

                crop_images(dir, showWork)
            if choice == 4:
                dir = input('list all relevant directories?\n'
                            '______________________________\n'
                            'Y/N or YES/NO\n').lower()
                if dir != 'y' and dir != 'n' and dir != 'no' and dir != 'yes':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    begin()
                else:
                    if (dir == 'y' or dir == 'yes'):
                        list_files('./videos')
                    else:
                        dir = False
                    dir = str(
                        input(
                            'write path example: \n./videos/movie.mp4\nor \nrtsp://username:password@IP:PORT/SRC\n'))
                    crop_videos(dir, showWork)
    print('read: ', begin.readCount, 'saved: ', begin.count)


# crop_videos('./videos/MDalarm_20170907_133339.mkv', True)
begin()
cv2.destroyAllWindows()


