import cv2
import numpy as np
import pyautogui

time = 0
cap = cv2.VideoCapture(0)

ret, frame = cap.read()

low_red = np.array([0, 140, 172])
high_red = np.array([9, 255, 255])

low_green = np.array([44, 168, 45])
high_green = np.array([140,255,158])

low_yellow = np.array([16, 139, 16])
high_yellow = np.array([36, 209, 255])

low_pink = np.array([160, 141, 161])
high_pink = np.array([179, 255, 255])

red = (0, 0, 255)
green = (0, 255, 0)
yellow = (0, 255, 255)
pink = (145, 80, 175)
blue = (255, 100, 0)

#widthcv, heightcv  = cap.get(3), cap.get(4)
widthcv = 1280
heightcv = 720
width, height = pyautogui.size()

x, y, w, h = widthcv, heightcv, 100, 50 # simply hardcoded the values
track_window = (x, y, w, h)


width = 2560
height = 1600

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
while True:
    ret, frame = cap.read()
    if ret == True:
        
        frame = cv2.flip(frame, 1)
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #green Tracking
        mask_green = cv2.inRange(hsv_frame, low_green, high_green)
        roi_hist_green = cv2.calcHist([hsv_frame],[0], mask_green,[180],[0,180])
        cv2.normalize(roi_hist_green, roi_hist_green, 0, 255, cv2.NORM_MINMAX)
        
        hsv_green = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst_green = cv2.calcBackProject([hsv_green],[0],roi_hist_green,[0,180],1)
        
        ret, track_window = cv2.CamShift(dst_green, track_window, term_crit)
        
        pts_g = cv2.boxPoints(ret)
        pts_g = np.int0(pts_g)
        
        print(pts_g)
        img2 = cv2.polylines(frame, [pts_g], True, green, 2)
        #img3 = cv2.circle(frame, [pts_g], True, green, 2)
        
        if pts_g[0][0] > 0 and pts_g[0][0] < widthcv and pts_g[0][1] > 0 and pts_g[0][1] < heightcv and time == 0:
            #pyautogui.moveTo(width * pts_g[0][0] / x, height * pts_g[0][1] / y)
            print(width * pts_g[0][0] / x, height * pts_g[0][1] / y)
            #print(pts_g[0][0], pts_g[0][1])

        
        mask2 = cv2.inRange(hsv_frame, low_green, high_green)
        
        coloredMask2 = cv2.bitwise_and(frame, frame, mask = mask_green)
           
        stacked = np.hstack((img2, coloredMask2))
        cv2.imshow("Tracking", cv2.resize(stacked, None, fx = 0.8, fy = 0.8))

        key = cv2.waitKey(30) & 0xff
        
        time = (time + 1) % 10
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()