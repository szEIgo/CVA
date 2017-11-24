from threading import Thread
print('run ds_faces')
import ds_faces
print('run video2frames')

import video2frames
print('run detector')
# import trainer
import detector
print('run detector_images')
import detector_images
print('run ds_bodies')
import ds_bodies





def start():
    # t = Thread(target=video2frames.allFiles('./videos'), args=())
    # t.daemon = True
    # t.start()
    t2 = Thread(target=detector.recognition(0), args=())
    t2.daemon = True
    t2.start()
    return t1, t2

start()