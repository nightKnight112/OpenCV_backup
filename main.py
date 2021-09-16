import cv2
import numpy as np
import imutils
import sys

def callback():
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("HSV_Trackbars")

# range of Hue= 0-179, range of Saturation and Value = 0-255
cv2.createTrackbar("L_H", "HSV_Trackbars", 0, 179, callback)
cv2.createTrackbar("L_S", "HSV_Trackbars", 0, 255, callback)
cv2.createTrackbar("L_V", "HSV_Trackbars", 0, 255, callback)
cv2.createTrackbar("U_H", "HSV_Trackbars", 179, 179, callback)
cv2.createTrackbar("U_S", "HSV_Trackbars", 255, 255, callback)
cv2.createTrackbar("U_V", "HSV_Trackbars", 255, 255, callback)

#have used hsv to find lower upper value, will be hard coded once the code runs
def hsv_space_detector():
    lower_hue = cv2.getTrackbarPos("L_H", "HSV_Trackbars")
    lower_saturation = cv2.getTrackbarPos("L_S", "HSV_Trackbars")
    lower_value = cv2.getTrackbarPos("L_V", "HSV_Trackbars")
    upper_hue = cv2.getTrackbarPos("U_H", "HSV_Trackbars")
    upper_saturation = cv2.getTrackbarPos("U_S", "HSV_Trackbars")
    upper_value = cv2.getTrackbarPos("U_V", "HSV_Trackbars")

    return np.array([lower_hue, lower_saturation, lower_value]), np.array([upper_hue, upper_saturation, upper_value])

def pre_coded_parts():
    #a func which stores points (x1,y1) and (x2,y2)...(hardcoded...and determined earlier)
    #dummy values
    x1, x2, y1, y2 = 1, 2, 3, 4
    return x1, x2, y1, y2

while True:
    ret, frame = cap.read()
    #roi = frame[:, 350: 550]  #to be used later
    cv2.imshow("Original after horizontal scaling", frame)
    cnv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if ret is False:
        sys.exit()
    else:
        #all bots have same colour, my plan is to hard code mqtt to gib instructions
        #to a bot for a definite amount of time and then switch to the next bot
        #and use an exit sequence to trigger exit after the above procedure happens 4 times

        #hsv space of bot colour
        lower, upper = hsv_space_detector()

        cv2.imshow("hsv", cnv_frame)
        mask = cv2.inRange(cnv_frame, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        frame = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('image_final', frame)
        
        #problems arising with contour detection, to be solved
        '''
        #will use mask.copy() at final stage as img gets modified in findcontours func
        contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("Aftr contour detection", mask)
        cnts = imutils.grab_contours(contours)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]  #stores first 10 largest contour points
        largest = cnts[0]
        print(largest)

        center = None

        #done till finding out of the largest contour(i.e. the bot's realtime position)
        if len(cnts) > 0:
            for points in cnts:
                print(points)
        else:
            print("No contours found")
            continue
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Keyboard interrupt")
            break


cap.release()
cv2.destroyAllWindows()
