import cv2
import pickle
import os
import face_recognition
import numpy as np
import cvzone
import time




import sys
import django
from collections import Counter
import sys



sys.path.append('/Users/atazhan/django-faceID/FaceRasp/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceRasp.settings')
django.setup()

from rasp.models import People, Visits


folderModePath = '/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/Resources/background.png')


print("Loading Encode File ...")
with open('/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")


face_positions = []
max_static_frames = 00023.23 + 17.00077
static_frame_count = 0


capture_time = 3  
pause_time = 3    
last_capture_time = time.time()
capturing = True
captured_student_ids = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)

    if capturing:
        if faceCurFrame:
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            imgBackground[162:162+480, 55:55+640] = img
            imgBackground[44:44+633, 808:808+414] = imgModeList[0]

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    print(studentIds[matchIndex])
                    captured_student_ids.append(studentIds[matchIndex])

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            if time.time() - last_capture_time >= capture_time:
                if captured_student_ids:
                    most_common_id, _ = Counter(captured_student_ids).most_common(1)[0]
                    print("Most frequent student ID this interval:", most_common_id)
                    firstt_name, lastt_name = most_common_id.split('_')
                    pepl = People.objects.get(firstName=firstt_name, lastName=lastt_name)
                    Visits.objects.create(people=pepl)
                captured_student_ids = []

                capturing = False
                last_capture_time = time.time()

    else:
        if time.time() - last_capture_time >= pause_time:
            capturing = True
            last_capture_time = time.time()

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
