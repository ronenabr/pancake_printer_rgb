import numpy as np
import cv2
import serial
import armtrig
import time
import math

def readImage(filename, width, height):
    image = cv2.imread(filename)
    resizedImg = cv2.resize(image, (width, height))

    resizedHSV = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2HSV)
    cv2.imshow("resized", resizedImg)
    cv2.waitKey(0)

    return resizedHSV


def findMinDistance(pixelVal, colors):
    minIdx = 0
    minVal = 1e10
    print 'here'
    for i in xrange(0, len(colors)):
        dist = np.linalg.norm(colors[i][0] - pixelVal[0])
        if dist < minVal:
            minVal = dist
            minIdx = i
    return minIdx


def splitImageIntoBins(img, colors):
    print 'splittin'
    height, width, depth = img.shape
    binaryImages = []

    for i in xrange(0, len(colors)):
        binaryImages.append(np.ones((height, width, 1), np.uint8))
        binaryImages[i][:, :] = 255

    for i in xrange(0, height):
        for j in xrange(0, width):
            closestIdx = findMinDistance(img[i, j], colors)
            binaryImages[closestIdx][i,j] = 0

    return binaryImages


if __name__ == "__main__":
    filename = "death.jpg"
    # color order (B,G,R)
    # color order
    #height, width = (190,277)
    height, width = (50,73)

    colorNames = ["pink", "orange", "green", "red",  "yellow", "blue",  "purple", "white"]
    colors = [[171, 158, 165], [10, 234, 186], [48, 242, 73], [1, 196, 122], [25, 255, 168], [115, 132, 71],  [124, 92, 56], [0, 0, 255]]
    BGRcolors = [[9,67,186],[9,80,37],[30,33,124],[1,146,172], [74,45,38],[98,68,169],[54,35,38],[255,255,255]]
    newColors = []
    #colors = [(21, 92, 73), (96, 95, 29), (1, 77, 48), (50, 100, 66), (230, 52, 28), (342, 62, 65), (231, 52, 25),(0, 0, 100)]
    #for i in xrange(0,len(colors)):
    #    newColors.append((colors[i][0]*180/360 ,colors[i][1]*255/100 ,colors[i][2]*255/100 ))
    print newColors
    ser = serial.Serial('/dev/cu.usbmodem1411',9600)
    theta0 = 50
    maxDistBeforeLift = 3

    img = readImage(filename, width, height)
    binaries = splitImageIntoBins(img, colors)

    for i in xrange(0, len(binaries)):
        cv2.imshow(colorNames[i],binaries[i])
        cv2.waitKey(0)
    currentImage = np.ones((height, width, 3), np.uint8)
    currentImage[:, :, :] = 255

    for i in xrange(0, len(binaries)):
        raw_input("Press any key to close to next color %s" % colorNames[i])
        ser.write(b'close\n')
        print ser.readline()


        lastx,lasty = 0,0
        for ix in xrange(0,width):
            for iy in xrange(0,height):
                if binaries[i][iy,ix] == 0:
                    dist = (ix - lastx)**2+(iy - lasty)**2

                    currentImage[iy,ix,0] = BGRcolors[i][0]
                    currentImage[iy,ix,1] = BGRcolors[i][1]
                    currentImage[iy,ix,2] = BGRcolors[i][2]

                    theta,phi = armtrig.transform((ix-width/2,height-iy))
                    if(not math.isnan(theta) and not math.isnan(phi)):
                        if dist > maxDistBeforeLift:
                            print "up"
                            ser.write(b'up\n')
                            ser.readline()

                        ser.write(b'T:%f P:%f\n' % (theta-theta0, phi))
                        ser.readline()
                        print 'T:%f P:%f' % (theta-theta0, phi)

                        if dist > maxDistBeforeLift:
                            print "down"

                            ser.write(b'down\n')
                            ser.readline()

                        lastx = ix
                        lasty = iy
                    cv2.imshow("current state",currentImage)
                    cv2.waitKey(1)
                    cv2.destroyAllWindows()


        ser.write(b'open\n')
        print ser.readline()
        ser.write(b'')

        raw_input("Press any key to move to next color")

    cv2.destroyAllWindows()



