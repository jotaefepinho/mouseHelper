import cv2
import numpy as np
import pyautogui

time = 0
cap = cv2.VideoCapture(0)

ret, frame = cap.read()

low_red = np.array([0, 140, 172])
high_red = np.array([9, 255, 255])

low_green = np.array([40, 175, 45])
high_green = np.array([121,255,255])

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

        #pink Tracking
        mask_red = cv2.inRange(hsv_frame, low_pink, high_pink)
        roi_hist_red = cv2.calcHist([hsv_frame],[0], mask_red,[180],[0,180])
        cv2.normalize(roi_hist_red, roi_hist_red, 0, 255, cv2.NORM_MINMAX)
        
        hsv_red = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst_red = cv2.calcBackProject([hsv_red], [0],roi_hist_red,[0,180],1)
        
        ret, track_window = cv2.CamShift(dst_red, track_window, term_crit)
        
        pts_r = cv2.boxPoints(ret)
        pts_r = np.int0(pts_r)
        
        img3 = cv2.polylines(frame, [pts_r], True, (145, 80, 175), 2)
        
        if pts_r[0][1] > 300:
            #print("baixo")
            pyautogui.scroll(-30)
        elif pts_r[0][1] < 100 and pts_r[0][1] > 0:
            #print("alto")
            pyautogui.scroll(30)
        #else:
            #print("medio")
            
        coloredMask = cv2.bitwise_and(frame, frame, mask = mask_red)
           
        stacked = np.hstack((img3, coloredMask))
        cv2.imshow("Tracking", cv2.resize(stacked, None, fx = 0.8, fy = 0.8))


        key = cv2.waitKey(30) & 0xff
        
        time = (time + 1) % 10
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()