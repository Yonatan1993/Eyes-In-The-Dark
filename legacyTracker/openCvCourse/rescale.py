import cv2 as cv

# img = cv.imread('Photos/cat_large.jpg')
# cv.imshow('Cat', img)
#
#
# def rescaleFrame(frame, scale=0.75):
#     width = int(frame.shape[1] * scale)
#     height = int(frame.shape[0] * scale)
#     dimensions = (width, height)
#     return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
#
#
# resized_image = rescaleFrame(img, scale=.4)
# cv.imshow('Image', resized_image)
# capture = cv.VideoCapture('Videos/dog.mp4')
# while True:
#     isTrue, frame = capture.read()
#     frame_resized = rescaleFrame(frame, scale=.2)
#
#     cv.imshow('Video', frame)
#     cv.imshow('Video Resized', frame_resized)
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break
#
# capture.release()
# cv.destroyWindows()


#####Rescale Live Video
def changeRes(width,height):
    # Only for Live Video
    cap.set(3, width)
    cap.set(4, height)


cap = cv.VideoCapture(0)
#changeRes(1920, 1080)
while True:
    success, frame = cap.read()
    #grayFrame = cv.imread(frame, cv.IMREAD_GRAYSCALE)
    grayImage = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #(thresh, blackAndWhiteFrame) = cv.threshold(grayFrame, 127, 255, cv.THRESH_BINARY)
    cv.imshow("Frame", grayImage)
    if cv.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
cv.waitKey(0)
