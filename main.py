import cv2
import numpy as np
import imutils
import sys


cap = cv2.VideoCapture(0)

def pre_coded_parts():
    #a func which stores points (x1,y1) and (x2,y2)...(hardcoded...and determined earlier)
    #dummy values
    x1, x2, y1, y2 = 1, 2, 3, 4
    return x1, x2, y1, y2

while True:
    ret, frame = cap.read()
    roi = frame[:, 350: 550]
    cv2.imshow("Original after horizontal scaling", roi)
    if ret is False:
        sys.exit()
    else:
        #all bots have same colour, my plan is to hard code mqtt to gib instructions
        #to a bot for a definite amount of time and then switch to the next bot
        #and use an exit sequence to trigger exit after the above procedure happens 4 times

        #hsv space of bot colour
        upper = ()
        lower = ()

        mask = cv2.inRange(roi, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("Aftr masking", mask)

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
            print()
        else:
            print("No contours found")
            continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Keyboard interrupt")
            break


cap.release()
cv2.destroyAllWindows()
