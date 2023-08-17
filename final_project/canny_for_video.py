import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage import filters

# Step 1 : GaussianFilter
def gaussian_kernel(kernalSize, sigma):
    if kernalSize % 2 == 0:
        kernalSize = kernalSize + 1
    max_point = kernalSize // 2  # both directions (x,y) maximum cell start point
    min_point = -max_point  # both directions (x,y) minimum cell start point!!

    K = np.zeros((kernalSize, kernalSize))  # kernel matrix
    for x in range(min_point, max_point + 1):
        for y in range(min_point, max_point + 1):
            value = (1 / (2 * np.pi * (sigma ** 2)) * np.exp((-(x ** 2 + y ** 2)) / (2 * (sigma ** 2))))
            K[x - min_point, y - min_point] = value

    return K

def f_NMS(Gm, Gd):
    num_rows, num_cols = Gm.shape[0], Gm.shape[1]
    Gd_bins = 45 * (np.round(Gd / 45))

    G_NMS = np.zeros(Gm.shape)
    neighbor_a, neighbor_b = 0., 0.
    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            angle = Gd_bins[r, c]
            if np.any(angle == 180.) or np.any(angle == -180.) or np.any(angle == 0.):
                neighbor_a, neighbor_b = Gm[r + 1, c], Gm[r - 1, c]
            elif np.any(angle == 90.) or np.any(angle == -90.):
                neighbor_a, neighbor_b = Gm[r, c - 1], Gm[r, c + 1]
            elif np.any(angle == 45.) or np.any(angle == -135.):
                neighbor_a, neighbor_b = Gm[r + 1, c + 1], Gm[r - 1, c - 1]
            elif np.any(angle == -45.) or np.any(angle == 135.):
                neighbor_a, neighbor_b = Gm[r - 1, c + 1], Gm[r + 1, c - 1]
            else:
                print("error")
                return

            if np.any(Gm[r, c] > neighbor_a) and np.any(Gm[r, c] > neighbor_b):
                G_NMS[r, c] = Gm[r, c]

    return G_NMS


def doCannyFilter(img):
    kernel = gaussian_kernel(11, 1)
    img_gaussian = cv.filter2D(img, -1, kernel)
    img_gaussian = np.float64(img_gaussian)

    mask_x = np.zeros((2, 1))
    mask_x[0] = -1
    mask_x[1] = 1

    I_x = cv.filter2D(img_gaussian, -1, mask_x)
    mask_y = mask_x.T
    I_y = cv.filter2D(img_gaussian, -1, mask_y)

    Gm = (I_x ** 2 + I_y ** 2) ** 0.5
    Gd = np.rad2deg(np.arctan2(I_y, I_x))
    G_NMS = f_NMS(Gm, Gd)

    E = filters.apply_hysteresis_threshold(G_NMS, G_NMS.max() / 8, G_NMS.max() / 5)
    E = cv.convertScaleAbs(E*255)
    return E

    # E = E * 1
    # new_E = np.array(map(lambda n: n * 255, E))
    # return cv.convertScaleAbs(new_E)
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 680)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    success, frame = cap.read()
    grayImage = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameAfterCanny = doCannyFilter(grayImage)
    cv.imshow("Frame", frameAfterCanny)
    if cv.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
cv.waitKey(0)



