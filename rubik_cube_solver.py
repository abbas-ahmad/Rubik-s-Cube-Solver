import cv2
import numpy as np
from imutils import contours
from webcolors import rgb_to_name
from  kociema_module import *

color = []
cubecolor = (0,0,0)
cubelineSize = 2

def getcolor(r,g,b): # compare rgb values and return color
    # print("Detected RGB: ", r,g,b)
    if (r > 70 and r <= 140 ) and (g >= 70 and g <= 140) and (b > 70 and b < 140):
        return 'o'
    elif 70 <= r <= 260 and (g >= 55 and g <= 140) and (b >= 100 and b <= 255):
        return 'r'
    elif (r >= 180 and r <= 260 ) and (g >= 180 and g <= 260) and (b >= 180 and b <= 260):
        return 'w'
    elif (r >= 70 and r <= 140 ) and (g > 120 and g <= 210) and (b > 65  and b <= 130):
        return 'g'
    elif (r >= 75 and r <= 260 ) and (g > 130 and g <= 255) and (b > 90 and b <= 255):
        return 'y'
    elif (r > 70 and r <= 120 ) and (g >= 70 and g <= 130) and (b > 70 and b < 130):
        return 'o'
    elif (r >= 30 and r <= 210 ) and (g >= 60 and g < 130) and (b >= 50 and b < 170):
        return 'b'
    else:
        print("Color Out of range:", r,g,b)
        return None
        
def drawCube(img, cubesize, cubeshape, start_point): # start_poing (100, 60)
    cubecell = int(cubesize / cubeshape)
    # draw horizontal lines first
    for i in range(cubeshape + 1):
        start_line = (start_point[0], start_point[1] + i * cubecell)
        end_line = (start_point[0] + cubesize, start_point[1] + i * cubecell)
        cv2.line(img, start_line, end_line, cubecolor, 2)
    
    for i in range(cubeshape + 1):
        start_line = (start_point[0] + i * cubecell, start_point[1])
        end_line = (start_point[0] + i * cubecell, start_point[1] + cubesize)
        cv2.line(img, start_line, end_line, cubecolor, cubelineSize)
    return img

def flattenList(data):
    results = []
    for rec in data:
        if isinstance(rec, list):
            results.extend(rec)
            results = flattenList(results)
        else:
            results.append(rec)
    return results

def showlable(img,index): 
    if index == 1: 
        cv2.putText(cubeImg, "Show face which contain yellow cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    elif index == 2: 
        cv2.putText(cubeImg, "Show face which contain blue cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    elif index == 3: 
        cv2.putText(cubeImg, "Show face which contain red cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    elif index == 4: 
        cv2.putText(cubeImg, "Show face which contain green cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    elif index == 5: 
        cv2.putText(cubeImg, "Show face which contain black cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    elif index == 6: 
        cv2.putText(cubeImg, "Show face which contain white cubies at center", (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
    else:
        pass


url = "http://192.168.0.100:8080"
# cap = cv2.VideoCapture(url+"/video")
cap = cv2.VideoCapture(0)
index = 1
while True:
    cubeImg = np.zeros((480,640))
    
    res, cubeImg = cap.read()
    
    cv2.waitKey(10)
    drawCube(cubeImg,180,3,(100,60))
    cv2.imshow("cube",cubeImg)
    showlable(cubeImg, index)
    
    if cv2.waitKey(1) == ord('c'): # extracting color from cube after click 'c' on keyboard
        index = index + 1
    
        print("start processing")
        
        showlable(cubeImg, index)
        img = cubeImg.copy()
        # print(img)
        # print(img.shape)
        
        img1 = img[80:100,120:140]      #[h,w]
        # print(img1.shape)
        # print(img1)
        img2 = img[80:100,180:200]
        # print(img2)
        img3 = img[80:100,240:260]
        # print(img3)
        img4 = img[140:160,120:140]
        # print(img4)
        img5 = img[140:160,180:200]
        # print(img5)
        img6 = img[140:160,240:260]
        # print(img6)
        img7 = img[200:220,120:140]
        # print(img7)
        img8 = img[200:220,180:200]
        # print(img8)
        img9 = img[200:220,240:260]
        # print(img9)
        pixel = [img1, img2, img3, img4, img5, img6, img7, img8, img9] 

        concat = np.concatenate((img1, img2, img3, img4, img5, img6, img7, img8, img9), axis=1)
        cv2.imshow("cells", concat)
        result = []
        flag = False
        for i in pixel: # white balancing of image
            r, g, b = cv2.split(i)
            r_avg = cv2.mean(r)[0]
            g_avg = cv2.mean(g)[0]
            b_avg = cv2.mean(b)[0]
            # print(int(r_avg),int(g_avg),int(b_avg))
            res = getcolor(int(r_avg),int(g_avg),int(b_avg))
            
            if res is None:
                index = index - 1
                print("Please show this face again.")
                flag = True
                break
            else:
                result.append(res)
        if flag:
            continue
        else:
            color.append(result)

        cv2.putText(cubeImg, result[0] + " " + result[1] + " " + result[2], (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.putText(cubeImg, result[3] + " " + result[4] + " " + result[5], (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.putText(cubeImg, result[6] + " " + result[7] + " " + result[8], (int(17), 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
        cv2.imshow("cube",cubeImg)
        print(color)

    if cv2.waitKey(10) == ord('s'): # start kociema module  
        color = flattenList(color)
        print(color)
        cube = ''.join(color) 
        print("Current STATE:", cube)  
        cap.release()
        kociema(cube)
    if cv2.waitKey(10) == ord('q'):
        break