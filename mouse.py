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
high_yellow = np.array([36, 255, 255])

low_pink = np.array([160, 141, 161])
high_pink = np.array([179, 255, 255])

low_blue = np.array([103, 115, 146])
high_blue = np.array([117,255,255])

red = (0, 0, 255)
green = (0, 255, 0)
yellow = (0, 255, 255)
pink = (145, 80, 175)
blue = (255, 100, 0)


x, y, w, h = 600, 400, 100, 50 # simply hardcoded the values
track_window = (x, y, w, h)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
while True:
    ret, frame = cap.read()
    if ret == True:
        
        frame = cv2.flip(frame, 1)
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #mouse Tracking
        #choose mouse control colors on next line
        mask_mouse = cv2.inRange(hsv_frame, low_pink, high_pink)
        roi_hist_mouse = cv2.calcHist([hsv_frame],[0], mask_mouse,[180],[0,180])
        cv2.normalize(roi_hist_mouse, roi_hist_mouse, 0, 255, cv2.NORM_MINMAX)
        
        hsv_mouse = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst_mouse = cv2.calcBackProject([hsv_mouse],[0],roi_hist_mouse,[0,180],1)
        
        ret, track_window = cv2.CamShift(dst_mouse, track_window, term_crit)
        
        pts_m = cv2.boxPoints(ret)
        pts_m = np.int0(pts_m)
        
        
        #choose rectangle color on next line
        img2 = cv2.polylines(frame, [pts_m], True, pink, 2)
              
        
        if (1920 * pts_m[0][0] / x < 1920 and 1920 * pts_m[0][0] / x > 0) and (1080 * pts_m[0][1] / y < 1080 and 1080 * pts_m[0][1] / y > 0) and time == 0:
            pyautogui.moveTo(1920 * pts_m[0][0] / x, 1080 * pts_m[0][1] / y)

        coloredMask2 = cv2.bitwise_and(frame, frame, mask = mask_mouse)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #controls Tracking
        #choose scroll and click colors on next line
        mask_controls = cv2.inRange(hsv_frame, low_blue, high_blue)
        roi_hist_controls = cv2.calcHist([hsv_frame],[0], mask_controls,[180],[0,180])
        cv2.normalize(roi_hist_controls, roi_hist_controls, 0, 255, cv2.NORM_MINMAX)
        
        hsv_controls = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst_controls = cv2.calcBackProject([hsv_controls], [0],roi_hist_controls,[0,180],1)
        
        ret, track_window = cv2.CamShift(dst_controls, track_window, term_crit)
        
        pts_c = cv2.boxPoints(ret)
        pts_c = np.int0(pts_c)
        
        #choose rectangle color on next line
        img3 = cv2.polylines(frame, [pts_c], True, blue, 2)

        #scroll up and down        
        if pts_c[0][1] > 280:
            pyautogui.scroll(-30)
        elif pts_c[0][1] < 80 and pts_c[0][1] > 0:
            pyautogui.scroll(30)
 
        #click and right click
        if pts_c[1][1] > 300:
            #print(pts_c[1][1])
            pyautogui.click()
        elif pts_c[1][1] < 60 and pts_c[1][1] > 0:
            #print(pts_c[1][1])
            pyautogui.click(button = 'right')
            
        coloredMask = cv2.bitwise_and(frame, frame, mask = mask_controls)
           
        stacked = np.hstack((img3, coloredMask, coloredMask2))
        
        
        cv2.imshow("Tracking", cv2.resize(stacked, None, fx = 0.8, fy = 0.8))

        key = cv2.waitKey(30) & 0xff
        
        time = (time + 1) % 10
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
