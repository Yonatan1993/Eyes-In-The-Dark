import cv2,imutils

tracker = cv2.legacy.TrackerCSRT_create()



########################################################


video = cv2.VideoCapture(0)
# TRACKER INITIALIZATION
_,frame = video.read()
frame = imutils.resize(frame,width=720)
BB = cv2.selectROI(frame,False)
tracker.init(frame, BB)


#def drawBox(img,bbox):
    #x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    #cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    #cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:
    _,frame = video.read()
    frame = imutils.resize(frame,width=720)
    tracker_success,BB = tracker.update(frame)
    if tracker_success:
        top_left = (int(BB[0]),int(BB[1]))
        bottom_right = (int(BB[0]+BB[2]))