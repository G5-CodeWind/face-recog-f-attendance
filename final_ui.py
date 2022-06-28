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
cap = cv2.VideoCapture(0)

# Registration: Capturing the Image, Input Values and Storing the image.
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
        file_name = file_name.upper() + '.jpg'
        print(f'data_images/{file_name}')

        cap_image = Image.fromarray(cv2image)
        cap_image.save(f'data_images/{file_name}')

    else:
        # Throwing an error msg.
        reg_msg.configure(text="All inputs fields are required", fg='red')

# Tkinter UI
root = Tk()
root.geometry(f"{window_width}x{window_height}")
root.title("Code Wind G5")

# Header
main_header_frame = LabelFrame(root, bg='orange', height=60, width=600, border=0)
main_header_frame.place(x=0, y=0)

main_header = Label(main_header_frame, text="Attendance System", font=('Poppins', 16), bg='orange')
main_header.place(anchor="center", x=300, y=30)

# Left Frame (Invisible)
left_frame = LabelFrame(root, bg='white', height=440, width=300, border=0)
left_frame.place(x=0, y=60)

left_label = Label(left_frame, bg='white', text="Register Here", font=('Poppins', 12, 'bold'))
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

reg_msg = Label(left_bottom_frame, bg='white', text="", font=('Poppins', 8))
reg_msg.place(anchor='center', x=150, y=145)

# Right Frame (Invisible)

right_frame = LabelFrame(root, bg="white", width=300, height=440)
right_frame.place(x=300, y=60)

right_label = Label(right_frame, text="Attendance Mark", bg="white", font=('Poppins', 12, 'bold'))
right_label.place(anchor='center', x=150, y=20)

right_reg_webcam = Label(right_frame, bg='orange', height=180, width=200, border=2)
right_reg_webcam.place(x=40, y=50)

mark_button = Button(right_frame, bg='orange', text="Mark", border=1, width=10, pady=6, padx=8)
mark_button.place(anchor='center', x=150, y=315)


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
    right_reg_webcam.configure(image=imgtk)
    root.update()
