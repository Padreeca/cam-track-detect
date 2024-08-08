import cv2
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from datetime import datetime
from PIL import Image, ImageTk
from tkinterdnd2 import *


def main_screen_config():
    global main_screen
    main_screen = Tk()
    main_screen.title("Cam Detector")
    main_screen.config(background="#e9e9e9")
    main_screen.geometry("1000x600")
    centralize_window(main_screen)
    # bandeira=0 ################ HOME

def main_screen_components():
    btn_photo = Button(main_screen, text="Tirar foto", command=btn_tirarFoto)
    btn_photo.place(relx=0.25, rely=0.5, anchor=CENTER)

    btn_folder = Button(main_screen, text="Selecionar Pasta", command=btn_select_folder)
    btn_folder.place(relx=0.75, rely=0.40, anchor=CENTER)

    btn_start_detracking_home = Button(main_screen, text="Iniciar Detecção", command=start_detection)
    btn_start_detracking_home.place(relx=0.75, rely=0.60, anchor=CENTER)

    vertical_line = Label(main_screen, width=1, bg="black")
    vertical_line.place(relx=0.5, rely=0, height=600)

def photo_screen_open():
    global photo_screen, cam, lbl_video, online

    online = True
    photo_screen = Toplevel(main_screen)
    photo_screen.title("Cam Detector")
    photo_screen.config(background="#000000")
    # centralize_window(photo_screen)
    photo_screen.geometry("1200x745")
    

    # centralize_window(photo_screen)
    photo_screen.focus_force()

    # Inicializa a captura da câmera
    cam = cv2.VideoCapture(0)

    # Label para exibir o vídeo da câmera
    lbl_video = Label(photo_screen)
    lbl_video.place(x=10, y=10)

    back_home_btn = Button(photo_screen, text="Voltar", command=back_home)
    back_home_btn.place(relx=0.90, rely=0.10, anchor=CENTER)

    btn_print = Button(photo_screen, text="📷",font=("Helvetica", 70), command=print_on_folder)
    btn_print.place(relx=0.90, rely=0.5, anchor=CENTER)

    open_folder = Button(photo_screen, text="Verificar Pasta", command=see_folder)
    open_folder.place(relx=0.90, rely=0.700, anchor=CENTER)

    change_folder_btn = Button(photo_screen, text="Alterar Pasta", command=btn_select_folder)
    change_folder_btn.place(relx=0.90, rely=0.770, anchor=CENTER)

    btn_start_detracking_photo = Button(photo_screen, text="Iniciar Detecção", command=start_detection) #####
    btn_start_detracking_photo.place(relx=0.90, rely=0.90, anchor=CENTER)
    #verificar ao iniciar detecção
    # if len(array_imagens)==0:
    #         messagebox.showerror("Erro", "Pasta sem imagem ")

    carregando_window.destroy()

    def atualizar_frame():
        global frame
        if online:
            ret, frame = cam.read()
            if ret:
                # Redimensiona o frame para um tamanho específico (por exemplo, 640x360)
                frame = cv2.resize(frame, (960,720))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                lbl_video.imgtk = img
                lbl_video.configure(image=img)

            # Atualiza o frame após 10 milissegundos
            lbl_video.after(2, atualizar_frame)

    def click_X():
        global online
        online = False
        back_home()
        cam.release()
        photo_screen.destroy()

    # Define o protocolo para fechar a janela
    photo_screen.protocol("WM_DELETE_WINDOW", click_X)
    atualizar_frame()

def centralize_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)

    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

def create_img_folder():
    global inside_folder_path, nome_imagem, system_pictures_path

    inside_folder_path = os.path.join(complete_folder_path, inside_folder_name)

    if not os.path.exists(complete_folder_path):
        os.mkdir(complete_folder_path)
    if not os.path.exists(inside_folder_path):
        os.mkdir(inside_folder_path)
    return inside_folder_path

def btn_tirarFoto():
    global array_imagens, n_img

    auto_close_carregando()
    main_screen.after(500,photo_screen_open) #espera 0,5sec pra abrir
    main_screen.after(500,create_img_folder) #espera 0,5sec pra abrir
    array_imagens= []
    n_img=1

    main_screen.withdraw()

def btn_select_folder():
    global array_imagens,inside_folder_path, tamanho_array

    selected = filedialog.askdirectory(initialdir=system_pictures_path)

    if selected=='':
        pass
    else:
        array_imagens = []
        inside_folder_path=selected
        for arquivo in os.listdir(inside_folder_path):
            if arquivo.lower().endswith(('.png','.jpg','.jpeg')):
                array_imagens.append(os.path.join(inside_folder_path, arquivo))
                tamanho_array = len(array_imagens)
    
def start_detection():
        global inside_folder_path
        if inside_folder_path==None or inside_folder_path=='':
            messagebox.showerror("Erro","Selecione uma Pasta")
            print(inside_folder_path)
            print(array_imagens)

        elif len(array_imagens)==0:
            messagebox.showerror("Erro","Pasta Sem Imagem")
            print(inside_folder_path)
            print(array_imagens)
        else:
            background_screen_open()
            # print("INICIAR DETECÇÃO")
            print(inside_folder_path)
            print(array_imagens)

def auto_close_carregando():
    global carregando_window, array_imagens
    carregando_window = Toplevel(main_screen)
    carregando_window.title("Câmera")
    carregando_window.config(background="#ffffff")
    carregando_window.geometry("250x100")
    centralize_window(carregando_window)
    carregando_window.focus_force()

    lbl_carregando = Label(carregando_window,text="Carregando...", bg="white")
    lbl_carregando.place(relx=0.5, rely=0.5, anchor=CENTER)

    carregando_window.after(2000,carregando_window.destroy)

    array_imagens= []

def print_on_folder():
    global n_img, nome_imagem, inside_folder_path, array_imagens

    print(array_imagens)

    n_img=len(array_imagens)+1

    nome_imagem= f"Objeto_{n_img}.jpg"
    caminho_nome = os.path.join(inside_folder_path, nome_imagem)
    array_imagens.insert(n_img,caminho_nome)

    cv2.imwrite(caminho_nome, frame)
    n_img=n_img+1

def see_folder():
    global inside_folder_path
    os.startfile(inside_folder_path)

def back_home():
    main_screen.deiconify()
    photo_screen.destroy()

def background_screen_open():
    background_screen = Toplevel(photo_screen)
    background_screen.title("Cam Detector")
    background_screen.config(background="#e9e9e9")
    background_screen.geometry("1200x745")
    centralize_window(background_screen)
    background_screen.focus_force()



    lbl_background = Label(background_screen,text="Background")
    lbl_background.place(x=0.5, y=0.1)


system_pictures_path = os.path.join(os.path.expanduser("~"), 'Pictures')
complete_folder_path= os.path.join(system_pictures_path,"Cam Detector")
horario_atual = datetime.now().strftime("%d-%m-%Y %Hh%Mm")
inside_folder_name = f"Cam Detector {horario_atual}"
inside_folder_path=None
array_imagens= []
main_screen_config()
main_screen_components()
main_screen.mainloop()


#for no array para selecionar o roi de cada imagem
#for brute force