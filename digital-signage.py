import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
import re

screen = Tk()
screen.title("Digital Signage")
screen.config(background="#e9e9e9")
# screen.iconbitmap("logo.ico")

images_folder = None
list_files = None
minutes = None
telinha_aberta = True

def select_folder():
    global images_folder
    global list_files
    images_folder = filedialog.askdirectory()

    list_files = os.listdir(images_folder)
    verify_end_all()
    
def verify_end_all():
    global image_file
    global images_folder
    global list_files

    image_file = None
    for img_file in list_files:
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg','.avif','.webp')):
            image_file = os.path.join(images_folder,img_file)

    if not image_file:
            none_image=Tk()
            none_image.withdraw()
            messagebox.showerror("Erro", "Arquivo sem imagem ")
            none_image.destroy()
            images_folder=None

def in_validate(P):
    if P.isdigit() or P == "":
        return True
    else:
        return False
    
def start_loop():

    if images_folder == None or images_folder=='':
        falta_erro = Tk()
        falta_erro.withdraw()
        messagebox.showerror("Erro", "Selecione uma Pasta")
        falta_erro.destroy()
    else:
        try:

            global list_files
            aberto=True

            minutes = int(time_entry.get())

            screen.destroy()

            while aberto == True:
            
                list_files = os.listdir(images_folder)
        
                for img_file in list_files:
                    try:
                        if img_file.lower().endswith(('.png', '.jpg', '.jpeg','.avif','.webp')):
                            image_file = os.path.join(images_folder, img_file)

                            image_file = re.sub(r'[\\/]', r'\\\\', image_file)

                            mostrar = cv2.imdecode(np.fromfile(r'' + image_file, np.uint8), cv2.IMREAD_UNCHANGED)

                            cv2.namedWindow('Fullscreen', cv2.WINDOW_NORMAL)
                            cv2.setWindowProperty('Fullscreen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                            cv2.imshow('Fullscreen', mostrar)

                            key = cv2.waitKey(minutes * 1000) & 0xFF

                            if key == 27: #ESC
                                aberto = False
                                break
                    except Exception as e:
                        continue

        except ValueError as e:
            falta_erro = Tk()
            falta_erro.withdraw()
            messagebox.showerror("Erro", "Insira um Tempo")
            falta_erro.destroy()


validation = screen.register(in_validate)

folder_btn = Button(screen, text="Selecionar Pasta de Imagens", command=select_folder, padx=20, bg="#ffffff", bd=3)
folder_btn.grid(column=0, row=0, pady=(30,0), padx=50)

quest_lbl = Label(screen, text="Tempo entre as telas:",bg="#e9e9e9",font=('Arial', 12))
quest_lbl.grid(column=0, row=2, padx=100, pady=(20,0))

in_minutes_lbl = Label(screen, font=('Arial', 10), text="(em segundos)",bg="#e9e9e9")
in_minutes_lbl.grid(column=0, row=3)

time_entry = Entry(screen,font=('Arial', 12), validate="key", validatecommand=(validation, "%P"),width=8,justify='center', bg="#ffffff", bd=2)
time_entry.grid(column=0, row=4, pady=(10,10))

confirm_btn = Button(screen, text="OK", command=start_loop, padx=20, width=10, bg="#ffffff", bd=4)
confirm_btn.grid(column=0, row=5, pady=(0,15))

screen.mainloop()