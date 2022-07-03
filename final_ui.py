# Project Name: Face Recognition for Attendance
# Project Duration: 1st June, 2022 to 30th June, 2022
# Project Group: G5


# UI Libraries
from tkinter import *
from PIL import Image, ImageTk

# Processing Libraries
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Global Variables
window_height = 500
window_width = 600

'''
Function: capture_data
Trigger: "Register" Button Click.
Purpose:    1. Checks whether all entry fields are filled or not.
            2. Captures the current frame and stores in the "data_image" folder.
'''
def capture_data():
    # Checking if all input fields are entered.
    if f_name_entry.get() and l_name_entry.get and reg_id_entry.get():

        # Indicating the user.
        reg_msg.configure(text="Successfully registered your face.", fg='green')

        print(os.path.curdir)

        # Getting the entry fields data
        cap_id = reg_id_entry.get()
        cap_fname = f_name_entry.get()
        cap_lname = l_name_entry.get()

        print(f'{cap_id},{cap_fname},{cap_lname}')

        # Capturing screenshot
        file_name = f'{cap_id}_{cap_fname}_{cap_lname}'
        file_name = file_name.upper() + '.png'
        print(f'data_images/{file_name}')

        cap_image = Image.fromarray(cv2image)
        cap_image.save(f'data_images/{file_name}')

    else:
        # Throwing an error msg.
        reg_msg.configure(text="All inputs fields are required", fg='red')


'''
Function: mark_attendance
Trigger: "Mark Attendance" Button Click
Purpose:    1. Generate encodings of dataset.
            2. Capture frames of webcam and find encodings
                2.1. Compare the encodings of captured frame and dataset images.
                2.2. If matched, Draw the rectangle around the face along with the details.
                2.3. Call the attendance function to store the details in .csv file.
'''
def mark_attendance():
    # attendance.py File
    path = 'data_images'    # Dataset Folder Path
    csv_path = 'csv_data'   # Csv Data Folder Path
    images = []
    personNames = []
    myList = os.listdir(path)
    TOLERANCE = 0.6

    print(f'Dataset Images are {myList}')
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])

    def faceEncodings(dataset):
        encodeList = []
        for image in dataset:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Check if face is present or not
            encode = face_recognition.face_encodings(image)

            if len(encode) > 0:
                encode = encode[0]
                encodeList.append(encode)
            else:
                pass
        return encodeList

    def attendance(id_n, first_n, last_n):
        time_now = datetime.now()
        tStr = time_now.strftime('%H:%M:%S')
        dStr = time_now.strftime('%d/%m/%Y')

        file = dStr.replace('/', '-')
        filename = f'{csv_path}/{file}.csv'

        with open(filename, 'a+') as f:

            # Checking all lines of csv
            myDataList = f.readlines()

            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if id_n not in nameList:
                f.writelines(f'\n  {id_n},{first_n}, {last_n}, {tStr},{dStr}')

        print(f'Attendance marked for {first_n} {last_n}.')

    print("Encoding Dataset....\n Wait for some time as we process the dataset.")
    encodeListKnown = faceEncodings(images)
    print('Encoding Successfully Completed.')

    #  0: Internal Webcam
    #  1: External Webcam
    webcam = cv2.VideoCapture(0)

    while True:
        ret, frame = webcam.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces, model='hog')
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, TOLERANCE)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                # Splitting the name into id,first,last name
                detail_name = name.split("_")
                id_no = detail_name[0]
                first_Name = detail_name[1]
                last_Name = detail_name[2]

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                attendance(id_no, first_Name, last_Name)

            else:
                name = "Unknown_Person"
                id_no = '00'
                first_Name = 'Unknown'
                last_Name = 'Unknown'
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                attendance(id_no, first_Name, last_Name)

        cv2.imshow('Mark Attendance Window', frame)
        if cv2.waitKey(1) == 13:
            break

    webcam.release()
    cv2.destroyAllWindows()


# Welcome Message
print("--------Welcome to Face Recognition for Attendance--------")


# Tkinter UI
cap = cv2.VideoCapture(0)

root = Tk()
root.geometry(f"{window_width}x{window_height}")
root.title("Code Wind G5")

# Header
main_header_frame = LabelFrame(root, bg='orange', height=60, width=600, border=0)
main_header_frame.place(x=0, y=0)

main_header = Label(main_header_frame, text="Attendance System", font=('Consolas', 16, "bold"), bg='orange')
main_header.place(anchor="center", x=300, y=30)

# Left Frame (Invisible)
left_frame = LabelFrame(root, bg='white', height=440, width=300, border=0)
left_frame.place(x=0, y=60)

left_label = Label(left_frame, bg='white', text="Register Here", font=('Consolas', 14, 'bold'))
left_label.place(anchor='center', x=150, y=20)

left_reg_webcam = Label(left_frame, bg='orange', height=180, width=200)
left_reg_webcam.place(x=40, y=50)

# Left Bottom Frame (Invisible)
left_bottom_frame = LabelFrame(left_frame, bg='white', height=200, width=300, border=0)
left_bottom_frame.place(x=0, y=280)

f_name = Label(left_bottom_frame, text="First Name *", font=('Poppins', 10), bg='white')
f_name.place(x=20, y=0)

f_name_entry = Entry(left_bottom_frame, border=0, bg='#dcdcdc')
f_name_entry.place(x=110, y=0, height=20)

l_name = Label(left_bottom_frame, text="Last Name *", font=('Poppins', 10), bg='white')
l_name.place(x=20, y=30)

l_name_entry = Entry(left_bottom_frame, border=0, bg='#dcdcdc')
l_name_entry.place(x=110, y=30, height=20)

reg_id = Label(left_bottom_frame, text="Id Number *", font=('Poppins', 10), bg='white')
reg_id.place(x=20, y=60)

reg_id_entry = Entry(left_bottom_frame, border=0, bg='#dcdcdc')
reg_id_entry.place(x=110, y=60, height=20)

reg_button = Button(left_bottom_frame, bg='orange', text="Register", border=1, width=10, pady=6, padx=8, command=capture_data)
reg_button.place(anchor='center', x=150, y=110)

reg_msg = Label(left_bottom_frame, bg='white', text="<Field Message and Success Indication>", font=('Poppins', 8))
reg_msg.place(anchor='center', x=150, y=145)

# Right Frame (Invisible)

right_frame = LabelFrame(root, bg="white", width=300, height=440)
right_frame.place(x=300, y=60)

right_label = Label(right_frame, text="Attendance Mark", bg="white", font=('Consolas', 14, 'bold'))
right_label.place(anchor='center', x=150, y=20)

# Instructions
mark_instr = Label(right_frame, text='Instructions', font=("Consolas", 12), bg='white')
mark_instr.place(anchor='center', x=150, y=50)

# Instructions here
instr_1 = Label(right_frame, text="1. Make sure to register first before marking \n the attendance.",
                font=('Poppins', 10), bg="white")
instr_1.place(x=20, y=80)

instr_2 = Label(right_frame, text="2. After clicking mark attendance wait for a \n while before if processes.\n",
                font=('Poppins', 10), bg="white")
instr_2.place(x=20, y=120)

instr_3 = Label(right_frame, text="3. Register with your correct credentials.",
                font=('Poppins', 10), bg="white")
instr_3.place(x=20, y=160)

mark_button = Button(right_frame, bg='orange', text="Mark Attendance", border=1, width=15, pady=6, padx=8,
                     command=mark_attendance)
mark_button.place(anchor='center', x=150, y=315)

mark_msg_1 = Label(right_frame, bg='white', text='<Encoding Message Here>', fg='green')
mark_msg_1.place(anchor='center', x=150, y=350)


while True:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

    # Get the latest frame and convert into Image
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)

    # Updating Webcams
    left_reg_webcam.configure(image=imgtk)
    root.update()
