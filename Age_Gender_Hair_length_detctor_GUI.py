# Importing Necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Loading the Model
from keras._tf_keras.keras.models import load_model
hair_length_model = load_model('Hair_length_Detection.keras')
age_gender_model = load_model('AgeGrp_Gender_Detection.keras')

# Initializing the GUI
gui = Tk()
gui.geometry('600x500')
gui.title('Gender Detector based on Hair Length')
gui.configure(background='#c0dfea')

heading = Label(gui,text='Gender Detector based on Hair Length',padx=20,pady=10,font=('arial',20,'bold'))
heading.configure(background='#c0dfea',foreground='#315495')
heading.pack()

image_label = tk.Label(gui)
gender_label = tk.Label(gui)
age_grp_label = tk.Label(gui)
hair_length_label = tk.Label(gui)

# Defining the detect function which detects the age and gender of the person in image using the model.
def detect(file_path):
    global age_grp_f,hair_length_f,age,hair_length
    image = Image.open(file_path)
    image = image.resize((64,64))
    image = np.array(image)
    print(image.shape)
    image = np.array([image/255])

    hair_pred = hair_length_model.predict(image)
    ag_pred = age_gender_model.predict(image)

    hair_length_f = ['Short Hair','Long Hair']
    gender_f = ['Male','Female']
    age_grp_f = ['Other','20-30']

    hair_length = int(np.round(hair_pred[0]))
    age = int(np.round(ag_pred[1][0]))
    gender = int(np.round(ag_pred[0][0]))

    if age == 1:
        gender = hair_length
    
    print("Predicted Hair Length is "+hair_length_f[hair_length])
    print("Predicted Age Grp is "+age_grp_f[age])
    print("Predicted Gender is "+gender_f[gender])

    gender_label.configure(text=gender_f[gender],padx=20,pady=10,font=('arial',20,'bold'))
    gender_label.configure(background='#c0dfea',foreground='#315495')
    gender_label.place(relx=0.79,rely=0.45,anchor='center')

    detect_button.place_forget()
    image_label.place(relx=0.35,rely=0.45,anchor='center')
    show_pred_age_hair_button()

# Defining the show button to show the predicted age_grp and hair length
def show_pred_age_hair_button():
    global show_button
    show_button = tk.Button(gui,text='Show Age & Hair Length',command=show_pred_age_hair)
    show_button.configure(padx=20,pady=10,background='#315495',foreground='white',font=('arial',10,'bold'))
    show_button.configure(activebackground='white',activeforeground='#315495')
    show_button.place(relx=0.75,rely=0.9,anchor='center')

# Defining the function of the show button 
def show_pred_age_hair():
    age_grp_label.configure(text=age_grp_f[age],padx=20,pady=10,font=('arial',20,'bold'))
    age_grp_label.configure(background='#c0dfea',foreground='#315495')
    age_grp_label.place(relx=0.79,rely=0.30,anchor='center')

    hair_length_label.configure(text=hair_length_f[hair_length],padx=20,pady=10,font=('arial',20,'bold'))
    hair_length_label.configure(background='#c0dfea',foreground='#315495')
    hair_length_label.place(relx=0.79,rely=0.60,anchor='center')

    show_button.configure(text='Unshow Age & Hair Length',command=unshow_pred_age_hair)
    show_button.place(relx=0.75,rely=0.9,anchor='center')

# Defining the unshow function to unshow the predicted age_grp and hair length
def unshow_pred_age_hair():
    age_grp_label.place_forget()
    hair_length_label.place_forget()
    show_button.configure(text='Show Age & Hair Length',command=show_pred_age_hair)

# Defining the detect button function
def show_detect_button(file_path):
    global detect_button
    detect_button = tk.Button(gui,text='Detect',command=lambda: detect(file_path))
    detect_button.configure(padx=20,pady=10,background='#315495',foreground='white',font=('arial',10,'bold'))
    detect_button.configure(activebackground='white',activeforeground='#315495')
    detect_button.place(relx=0.75,rely=0.9,anchor='center')
    
# Defining the Upload-Image Function
def upload_image():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        uploaded = Image.open(file_path)
        uploaded.thumbnail(((gui.winfo_width()/2.25),(gui.winfo_height()/2.25)))

        im = ImageTk.PhotoImage(uploaded)
        image_label.image = im
        image_label.configure(image=im)
        image_label.place(relx=0.5,rely=0.45,anchor='center')

        try:
            gender_label.place_forget()
            age_grp_label.place_forget()
            hair_length_label.place_forget()
            show_button.place_forget()
        except:
            pass

        upload_button.configure(text='Upload Again')
        upload_button.place(relx=0.25,rely=0.9,anchor='center')
        show_detect_button(file_path)
    except:
        pass

# Making upload button
upload_button = tk.Button(gui,text='Upload an Image',padx=20,pady=10,command=upload_image)
upload_button.configure(background='#315495',foreground='white',font=('arial',10,'bold'))
upload_button.configure(activebackground='white',activeforeground='#315495')
upload_button.place(relx=0.5,rely=0.5,anchor='center')

gui.mainloop()