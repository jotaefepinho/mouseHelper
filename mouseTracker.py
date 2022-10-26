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

x, y, w, h = 600, 400, 100, 50 # simply hardcoded the values
track_window = (x, y, w, h)

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
        
        img2 = cv2.polylines(frame, [pts_g], True, (0, 255, 0), 2)
              
        
        if pts_g[0][0] > 0 and pts_g[0][0] < 600 and pts_g[0][1] > 0 and pts_g[0][1] < 400 and time == 0:
            pyautogui.moveTo(1920 * pts_g[0][0] / x, 1080 * pts_g[0][1] / y)

        
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