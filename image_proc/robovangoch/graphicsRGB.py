import numpy as np
import cv2
import serial

def readImage(filename,height,width):
    image =  cv2.imread(filename)
    resizedImg = np.ones((height, width, 3), np.uint8)
    resizedImg = cv2.resize(image,(height,width))

    return resizedImg

def findMinDistance(pixelVal,colors):
    minIdx = 0
    minVal = 1e10
    for i in xrange(0,len(colors)):
        dist = np.linalg.norm(colors[i] - pixelVal)
        if dist < minVal:
            minVal = dist
            minIdx = i
    return minIdx

def splitImageIntoBins(img,colors) :
    height, width, depth = img.shape
    binaryImages = []

    for i in xrange(0,len(colors)):

        binaryImages.append(np.ones((height,width,1), np.uint8))
        binaryImages[i][:,:] = 255

    for i in xrange(0,height):
        for j in xrange(0,width):
            closestIdx = findMinDistance(img[i,j],colors)
            binaryImages[closestIdx][i,j] = 0

    return binaryImages

if __name__ == "__main__":
    filename = "super_mario_bros.png"
    # color order (B,G,R)
    # colro order
    colorNames = ["orange","green","red","yellow","blue","pink","purple","white"]
    colors = [(23,92,189),(6,78,35),(28,31,122),(2,147,173),(76,40,34),(105,73,174),(56,37,40),(255,255,255)]
    height, width = (287,200)


    img = readImage(filename,height,width)


    binaries = splitImageIntoBins(img,colors)
    for i in xrange(0,len(binaries)):
        cv2.imshow(colorNames[i],binaries[i])
        cv2.waitKey(0)

    cv2.destroyAllWindows()
