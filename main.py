import datetime
import os
import time
import cv2
import pandas as pd
import Recognize
import Train_Image
import webcam
import threading
import Capture_Image
import automail

recognizer = cv2.face_LBPHFaceRecognizer.create() # cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
col_names = ['Id', 'Name', 'Date', 'Time']
attendance = pd.DataFrame(columns=col_names)

def mask(cam):
    webcam.detect_face_mask(cam, recognizer)

def recognize(cam):
    Recognize.recognize_attendence(cam, recognizer, attendance)

def main():
    #Train_Image.TrainImages()
    #while True:
    choice = int(input('\n \n \n1 For Starting MSDP \n2 for Registering New Face \n3 For Sending Defaulters List To ADMIN \n\nEnter Choice: '))
    if choice == 1:
        recognizer.read("./Trainner/Trainner.yml")
        cam = cv2.VideoCapture(0)
        t1 = threading.Thread(target=mask, args=(cam,))
        t2 = threading.Thread(target=recognize, args=(cam,))
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        cam.release()
        cv2.destroyAllWindows()
        
    if choice == 2:
        Capture_Image.takeImages()
    if choice == 3:
        automail.send_email()

if __name__ == "__main__":
    main()