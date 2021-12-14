import datetime
import os
import time
import cv2
import pandas as pd
import Recognize
import webcam_copy_2 as webcam
import threading
import Capture_Image
import automail

recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
recognizer.read("./Trainner/Trainner.yml")
col_names = ['Id', 'Name', 'Date', 'Time']
attendance = pd.DataFrame(columns=col_names)

def mask(cam):
    webcam.detect_face_mask(cam, recognizer)

def recognize(cam):
    Recognize.recognize_attendence(cam, recognizer, attendance)

def main():
    while True:
        choice = int(input('\n \n \n1 For Starting MSDP \n2 for Registering New Face \n3 For Sending Defaulters List To ADMIN \n\nEnter Choice: '))
        if choice == 1:
            cam = cv2.VideoCapture(0)
            t1 = threading.Thread(target=mask, args=(cam,))
            t2 = threading.Thread(target=recognize, args=(cam,))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            attendance.to_csv(fileName, index=False)
            print("Attendance Successful")
            cam.release()
            cv2.destroyAllWindows()
            break
        if choice == 2:
            Capture_Image.takeImages()
        if choice == 3:
            automail.send_email()

if __name__ == "__main__":
    main()