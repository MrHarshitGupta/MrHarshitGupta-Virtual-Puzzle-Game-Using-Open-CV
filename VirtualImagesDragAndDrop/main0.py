import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.6)


class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2


# img1 = cv2.imread("JPG Image/1.jpg")
# img1 = cv2.imread("PNG Image/1.png", cv2.IMREAD_UNCHANGED)
# ox, oy = 200, 200

path = "PNG Image"
mylist = os.listdir(path)
print(mylist)

listImg = []
for x, pathImg in enumerate(mylist):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [10 + x * 150, 10], imgType))

print(len(listImg))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']

        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

                 # This is to Draw
                # ox, oy = img.posOrigin
                # h, w = img.size
                # cv2.img(img, (ox - w // 2, oy - h // 2),
                #                   (ox + w // 2, oy + h // 2), imgObject, cv2.FILLED)
                # cvzone.cornerImg(img, (ox - w // 2, oy - h // 2, w, h), img=0)

    try:

        for imgObject in listImg:

            # Draw for JPG Images
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
