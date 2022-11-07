import cv2
import numpy as np
import pyautogui
import datetime
def chooseColor(choice):

    low_red = np.array([0, 140, 172])
    high_red = np.array([9, 255, 255])

    low_green = np.array([60, 60, 143])
    high_green = np.array([80, 255, 255])

    low_yellow = np.array([16, 139, 16])
    high_yellow = np.array([36, 255, 255])

    low_pink = np.array([160, 141, 161])
    high_pink = np.array([179, 255, 255])

    low_blue = np.array([103, 115, 146])
    high_blue = np.array([117, 255, 255])

    red = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (0, 255, 255)
    pink = (145, 80, 175)
    blue = (255, 100, 0)

    if choice == 'red':
        return red, low_red, high_red
    if choice == 'green':
        return green, low_green, high_green
    if choice == 'blue':
        return blue, low_blue, high_blue
    if choice == 'pink':
        return pink, low_pink, high_pink
    if choice == 'yellow':
        return yellow, low_yellow, high_yellow
    else:
        return 0

#inicialização da captura da webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

#definição da cor branca para o texto-guia
white = (255, 255, 255)

#Escolha da cor para o acompanhamento do ponteiro do mouse
print("Choose a color for mouse tracking:\n" + "red\n" + "green\n" + "blue\n" + "pink\n" + "yellow\n")
choice = input()
color_m, low_color_m, high_color_m = chooseColor(choice)

#Escolha da cor para os controles do mouse
print("Choose a color for controls:\n" + "red\n" + "green\n" + "blue\n" + "pink\n" + "yellow\n")
choice = input()
color_c, low_color_c, high_color_c = chooseColor(choice)

#marcação do tempo para o acompanhamento do ponteiro: 
#taxa de atualização de meio segundo
next_time = datetime.datetime.now()
delta = datetime.timedelta(seconds = 0.5)

x, y, w, h = 640, 360, 100, 50
track_window1 = (x, y, w, h)
track_window2 = (x, y, w, h)

#dimensões do monitor para o controle do ponteiro do mouse
width = 1920
height = 1080

cap_width = np.size(frame, 1)
cap_height = np.size(frame, 0)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
m_flag = 0
while True:
    ret, frame = cap.read()
    period = datetime.datetime.now()
    if ret == True:
        
        frame = cv2.flip(frame, 1)
                
        #mouse Tracking
        hsv_mouse = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask_mouse = cv2.inRange(hsv_mouse, low_color_m, high_color_m)
        roi_hist_mouse = cv2.calcHist([hsv_mouse],[0], mask_mouse,[180],[0,180])
        cv2.normalize(roi_hist_mouse, roi_hist_mouse, 0, 255, cv2.NORM_MINMAX)
        
          
        #control Tracking
        hsv_controls = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        mask_controls = cv2.inRange(hsv_controls, low_color_c, high_color_c)
        roi_hist_controls = cv2.calcHist([hsv_controls],[0], mask_controls,[180],[0,180])
        cv2.normalize(roi_hist_controls, roi_hist_controls, 0, 255, cv2.NORM_MINMAX)
         
        dst_mouse = cv2.calcBackProject([hsv_mouse],[0],roi_hist_mouse,[0,180],1)
        
        ret_m, track_window1 = cv2.CamShift(dst_mouse, track_window1, term_crit)
        
        pts_m = cv2.boxPoints(ret_m)
        pts_m = np.int0(pts_m)
        center_m = (int((pts_m[0][0] + pts_m[1][0] + pts_m[2][0] + pts_m[3][0])/4), int((pts_m[0][1] + pts_m[1][1] + pts_m[2][1] + pts_m[3][1])/4))
        
        img2 = cv2.polylines(frame, [pts_m], True, color_m, 2)
        cv2.circle(img2, center_m, 1, color_m, 15)
        
        
        if (width * center_m[0] / x < width and center_m[0] / x > 0) and (height * center_m[1] / y < height and height * center_m[1] / y > 0) and period >= next_time:
            pyautogui.moveTo(width * center_m[0] / x, height * center_m[1] / y)
            next_time += delta

        coloredMask2 = cv2.bitwise_and(frame, frame, mask = mask_mouse)

        dst_controls = cv2.calcBackProject([hsv_controls], [0],roi_hist_controls,[0,180],1)
        
        ret_c, track_window2 = cv2.CamShift(dst_controls, track_window2, term_crit)
        
        pts_c = cv2.boxPoints(ret_c)
        pts_c = np.int0(pts_c)
        center_c = (int((pts_c[0][0] + pts_c[1][0] + pts_c[2][0] + pts_c[3][0])/4), int((pts_c[0][1] + pts_c[1][1] + pts_c[2][1] + pts_c[3][1])/4))
        
        img3 = cv2.polylines(frame, [pts_c], True, color_c, 2)
        cv2.circle(img3, center_c, 1, color_c, 15)

        #scroll up and down        
        if center_c[1] > (cap_height - cap_height * 0.3) and center_c[0] < cap_width - cap_width * 0.2 and center_c[0] > cap_width * 0.2:
            #print("scroll down")
            pyautogui.scroll(-30)
        elif center_c[1] < (cap_height * 0.3) and center_c[0] < cap_width - cap_width * 0.2 and center_c[0] > cap_width * 0.2:
            #print("scroll up")
            pyautogui.scroll(30)

        #click and right click
        if center_c[0] > (cap_width - cap_width * 0.2) and m_flag == 0:
            #print("click")
            pyautogui.click()
            m_flag = 1
        elif center_c[0] < cap_width * 0.2 and center_c[0] > 0 and m_flag == 0:
            #print("right click")
            pyautogui.click(button = 'right')
            m_flag = 1
        elif m_flag == 1 and center_c[0] > (cap_width * 0.2) and center_c[0] < (cap_width - cap_width * 0.2):
            m_flag = 0

        coloredMask = cv2.bitwise_and(frame, frame, mask = mask_controls)

        img3 = cv2.line(img3, (int(cap_width * 0.2), int(cap_height * 0.3)), (int(cap_width - cap_width * 0.2), int(cap_height * 0.3)), color_c, 2)
        img3 = cv2.line(img3, (int(cap_width * 0.2), int(cap_height - cap_height * 0.3)), (int(cap_width - cap_width * 0.2), int(cap_height - cap_height * 0.3)), color_c, 2)

        img3 = cv2.line(img3, (int(cap_width * 0.2), 0), (int(cap_width * 0.2), cap_height), color_c, 2)
        img3 = cv2.line(img3, (int(cap_width - cap_width * 0.2), 0), (int(cap_width - cap_width * 0.2), height), color_c, 2)
    
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        fontScale = 1
        thickness = 3

        img3 = cv2.putText(img3, 'Scroll Up', (int(cap_width * 0.3), int(cap_height * 0.15)), font, fontScale, white, thickness, cv2.LINE_AA)
        img3 = cv2.putText(img3, 'Scroll Down', (int(cap_width * 0.3), int(cap_height * 0.85)), font, fontScale, white, thickness, cv2.LINE_AA)
        img3 = cv2.putText(img3, 'Click', (int(cap_width * 0.80), int(cap_height * 0.5)), font, fontScale, white, thickness, cv2.LINE_AA)
        img3 = cv2.putText(img3, 'RClick', (int(cap_width * 0.05), int(cap_height * 0.5)), font, fontScale, white, thickness, cv2.LINE_AA)
         
        stacked = np.hstack((img3, coloredMask, coloredMask2))
        cv2.imshow("Tracking", cv2.resize(stacked, None, fx = 0.6, fy = 0.6))

        #cv2.imshow("mouseHelper", cv2.resize(img3, None, fx = 0.8, fy = 0.8))
        key = cv2.waitKey(30) & 0xff
    
    else:
        break
    if key == 27:
        break
    
    
cap.release()
cv2.destroyAllWindows()
