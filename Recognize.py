import datetime
import os
import time
import cv2
import pandas as pd


#-------------------------
def recognize_attendence(cam, recognizer, attendance):
    while True:
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cam.set(3, 640)  # set video width
        #cam.set(4, 480)  # set video height
        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        _,im = cam.read()
        if len(im) == 0:
            continue
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            min_conf = 30

            if conf < 100 and (100-conf) > min_conf:
                aa = df.loc[df['Id'] == Id]['Name'].values
                ab = df.loc[df['Id'] == Id]['MailID'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa+"-"+ab

            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            tt = str(tt)[2:-2]
            if(100-conf) > min_conf:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100-conf) > min_conf:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
            elif (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)



        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break