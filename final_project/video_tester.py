import numpy as np
import torch
import cv2

#

#cap = cv2.VideoCapture('C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5/data/video/live_no_obsqq.mp4')
cap = cv2.VideoCapture(0)
current_focal_length = cap.get(cv2.CAP_PROP_FOCUS)
print(f"Current focal length: {current_focal_length}")

path = 'C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5/yolov5s.pt'
# count=0

model = torch.hub.load('C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5', 'custom', path, source='local')
b = model.names[2] = 'car'

size = 416
count = 0
counter = 0
color = (0, 0, 255)
cy1 = 250
offset = 12

while True:
    ret, img = cap.read()

    count += 1
    if count % 4 != 0:
        continue
    img = cv2.resize(img, (600, 500))
    # cv2.line(img,(79,cy1+offset),(599,cy1+offset),(0,0,255),2)
    # cv2.line(img,(79,cy1),(599,cy1),(0,0,255),2)
    # cv2.line(img,(79,cy1-offset),(599,cy1-offset),(0,0,255),2)

    results = model(img, size)
    a = results.pandas().xyxy[0]
    for index, row, in results.pandas().xyxy[0].iterrows():
        print(f"In count ={count}")
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        d = (row['class'])
        if d == 36:
            continue
        if (d == 2):
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 55), 2)
            recx1, recty1 = ((x1 + x2) / 2, (y1 + y2) / 2)
            rect_center = int(recx1), int(recty1)
            cx = rect_center[0]
            cy = rect_center[1]
            cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
            cv2.putText(img, str(b), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (225, 255, 255), 2)
            #cv2.putText(img, '('+str(x1)+','+str(y1)+')',(x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
            if cy < (cy1 + offset) and cy > (cy1 - offset):
                counter += 1
                # cv2.line(img, (79, cy1), (590, cy1), (0, 255, 0), 2)

        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 55), 2)
            recx1, recty1 = ((x1 + x2) / 2, (y1 + y2) / 2)
            rect_center = int(recx1), int(recty1)
            cx = rect_center[0]
            cy = rect_center[1]
            cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
            cv2.putText(img, row['name'], (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (225, 255, 255), 2)
            #cv2.putText(img, '('+str(x1)+','+str(y1)+')',(x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
            if cy < (cy1 + offset) and cy > (cy1 - offset):
                counter += 1
                # cv2.line(img, (79, cy1), (590, cy1), (0, 255, 0), 2)

        print(row)

    cv2.imshow("IMG", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
