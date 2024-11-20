from tkinter import *
from tkinter import messagebox as msg
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import database as db

# CONFIG
path = "C:/Users/SOPORTE/simple/facial_recognition/" 
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"

color_white = "#f4f5f4"
color_black = "#101010"
color_black_btn = "#202020"
color_background = "#151515"
font_label = "Century Gothic"
size_screen = "500x300"

color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"

res_bd = {"id": 0, "affected": 0}  # database variable

# GENERAL
def getEnter(screen):
    ''' Set an enter inside the screen '''
    Label(screen, text="", bg=color_background).pack()

def printAndShow(screen, text, flag):
    ''' Prints and shows text '''
    if flag:
        print(color_success + text + color_normal)
        screen.destroy()
        msg.showinfo(message=text, title="¡Éxito!")
    else:
        print(color_error + text + color_normal)
        Label(screen, text=text, fg="red", bg=color_background, font=(font_label, 12)).pack()

def configure_screen(screen, text):
    ''' Configure global styles '''
    screen.title(text)
    screen.geometry(size_screen)
    screen.configure(bg=color_background)
    Label(screen, text=f"¡{text}!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

def credentials(screen, var, flag):
    ''' Configuration of user input '''
    Label(screen, text="Usuario:", fg=color_white, bg=color_background, font=(font_label, 12)).pack()
    entry = Entry(screen, textvariable=var, justify=CENTER, font=(font_label, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    getEnter(screen)
    if flag:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login_capture).pack()
    else:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register_capture).pack()
    return entry

def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1, len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

# REGISTER
def register_face_db(img):
    name_user = img.replace(".jpg","").replace(".png","")
    res_bd = db.registerUser (name_user, path + img)

    getEnter(screen1)
    if(res_bd["affected"]):
        printAndShow(screen1, "¡Éxito! Se ha registrado correctamente", 1)
    else:
        printAndShow(screen1, "¡Error! No se ha registrado correctamente", 0)

def capture_image(frame, window_title):
    ''' Capture image from webcam and return the filename '''
    img_filename = f"{window_title}.jpg"
    cv2.imshow(window_title, frame)
    if cv2.waitKey(1) == 27:  # Wait for 'Esc' to capture
        cv2.imwrite(img_filename, frame)
        return img_filename
    return None

def register_capture():
    ''' Handle the user face capture during registration '''
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        return
    
    user_reg_img = user1.get()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        img = capture_image(frame, "Registro Facial")
        if img:
            break
    
    cap.release()
    cv2.destroyAllWindows()

   