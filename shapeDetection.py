import cv2 as cv
import numpy as np

#Griding method
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

#contours method

def getContours(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,
    cv.CHAIN_APPROX_NONE) #rete_ex is for fining the outer part of shape

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500: #we will detect shape avobe 500 area , in this we can we won't detect nosied area
            cv.drawContours(imgContour,cnt,-1,(255,0,255),1)
            param = cv.arcLength(cnt,True)
            # print(param) #check the values  
            aprox = cv.approxPolyDP(cnt,0.02*param,True) #its a array .inside this array we have all the individual corner values 
            # print(len(aprox)) #check the values 
            objCor = len(aprox) #is variable contains the len of aprox array. if array have 3 elements variable will contain 3 int 
            x, y, w, h = cv.boundingRect(aprox) #it will help to create a box aroud the shape for detect the shape it has 4 values  
            cv.rectangle(imgContour,(x,y),(x+w,y+h),(255,0,255),1) #it will create a box around the shapes 
            # setting up condition for detecting shapes
            if objCor   == 3   : objType  = "triangle"
            elif objCor == 4 :
                aspratio =w/float(h)
                if aspratio > 0.95 and aspratio < 1.05: objType = "Square"
                else: objType = "Rectangle"
            elif objCor == 5 : objType = "Pentagon"
            elif objCor == 6 : objType = "Hexagon"
            elif objCor == 7 : objType = "Heptagon"
            elif objCor == 8 : objType = "Octagon"
            elif objCor > 10 : objType = "Circle"
            else: objType = "none"

            cv.putText(imgContour,objType,(x+(w//2)-10,y+(h//2)-10),cv.FONT_HERSHEY_SIMPLEX,0.3,(255,0,255)) #it will put text near the center of the shape 

    


path = r"demo.jpg"

img = cv.imread(path)
imgContour = img.copy() 
imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY) #step 1 make it rgb to gray 
imgBlur = cv.GaussianBlur(imgGray,(7,7),0.5) #step 2 make litte blur 
imgCanny = cv.Canny(imgBlur,50,50) #step 3 make canny image .black and white to reduce nosie of the image change the threshhold values exmple:(50,50)
imageBlank = np.zeros_like(img) #blank image it is used in the stackImages method to complet up 3x3 array 
    
getContours(imgCanny) #called getconturs method 

grid = stackImages(0.9,([[img,imgGray,imgBlur],[imgCanny,imgContour,imageBlank]])) #if you use differten image check first atribute(scale) of the method

cv.imshow("m",grid)

cv.waitKey(0)
