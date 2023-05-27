import cv2 as cv

##### Read Photos
# img = cv.imread('Photos\cat_large.jpg')
# cv.imshow('Cat',img)
# cv.waitKey(0)
##########

####Read Videos
capture = cv.VideoCapture('Videos/dog.mp4')
while True:
    isTrue, frame = capture.read()
    grayImage = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('Video', grayImage)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyWindows()
cv.waitKey(0)
