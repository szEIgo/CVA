import os
import cv2


def run(path, file):
        run.count = 0
        def makeFrames(videopath, videofile):
                videoname = videofile[:-4]
                folder = os.path.join(videopath, 'frames')
                if not os.path.exists(folder):
                    os.mkdir(folder)
                videofilepath = os.path.join(videopath, videofile)
                vidcap = cv2.VideoCapture(videofilepath)

                while True:
                        success,image = vidcap.read()
                        if not success:
                            break
                        cv2.imwrite(os.path.join(folder,videoname+"{:d}.jpg".format(run.count)), image)
                        run.count += 1
                        if(run.count % 100 == 0):
                            print('directory: ', folder)
                            print('Files: ', videoname+"{:d}.jpg".format(run.count))
                            print(run.count, "frames extracted")
                print("{} images are extracted in {}.".format(run.count,folder))



        makeFrames(path,file)
        
def allFiles(path):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                #print os.path.join(subdir, file)
                filepath = subdir + os.sep + file
                if filepath.endswith(".mkv") or filepath.endswith(".mp4"):
                    print(filepath)
                    run(subdir, file)



# allFiles('./videos/joni/')
# allFiles('./videos/joseph/')
# allFiles('./videos/alexg/')
# allFiles('./videos/')
