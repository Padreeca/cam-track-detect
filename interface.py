import cv2
import os

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from datetime import datetime
from PIL import Image, ImageTk
from tkinterdnd2 import *


def main_screen_config():
    global main_screen, bandeira
    main_screen = Tk()
    main_screen.title("Cam Detector")
    main_screen.config(background="#e9e9e9")
    main_screen.geometry("1000x600")
    centralize_window(main_screen)
    bandeira=0 ################ HOME

def main_screen_components():
    btn_photo = Button(main_screen, text="Tirar foto", command=btn_tirarFoto)
    btn_photo.place(relx=0.25, rely=0.5, anchor=CENTER)

    btn_folder = Button(main_screen, text="Selecionar Pasta", command=btn_select_folder)
    btn_folder.place(relx=0.75, rely=0.40, anchor=CENTER)

    btn_start_detracking_home = Button(main_screen, text="Iniciar Detecção", command=start_detection)
    btn_start_detracking_home.place(relx=0.75, rely=0.60, anchor=CENTER)

    vertical_line = Label(main_screen, width=1, bg="black")
    vertical_line.place(relx=0.5, rely=0, height=600)

    folder_input = Entry(main_screen, width=50)
    folder_input.place(relx=0.75, rely=0.2)

    # Define o campo como somente leitura
    folder_input.config(state="readonly")

    # Exemplo: Define um caminho da pasta
    set_folder_path("/caminho/para/a/pasta")



def photo_screen_open():
    global photo_screen, cam, lbl_video, online, bandeira, array_imagens

    array_imagens= []

    bandeira=1
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

    def click_X_photo_screen():
        global online
        online = False
        back_home()
        cam.release()
        photo_screen.destroy()

    # Define o protocolo para fechar a janela
    photo_screen.protocol("WM_DELETE_WINDOW", click_X_photo_screen)
    atualizar_frame()

    print(array_imagens)

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
        # try:
        if inside_folder_path==None or inside_folder_path=='':
            messagebox.showerror("Erro","Selecione uma Pasta")
            print(inside_folder_path)
            print(array_imagens)

        elif len(array_imagens)==0:
            messagebox.showerror("Erro","Pasta Sem Imagem")
            print(inside_folder_path)
            print(array_imagens)
        else:
            background_screen_choice()
            print("INICIAR DETECÇÃO")
            # print(inside_folder_path)
            # print(array_imagens)
        # except:
        #     messagebox.showerror("Erro","Selecione uma Pasta")

def auto_close_carregando():
    global carregando_window
    carregando_window = Toplevel(main_screen)
    carregando_window.title("Câmera")
    carregando_window.config(background="#ffffff")
    carregando_window.geometry("250x100")
    centralize_window(carregando_window)
    carregando_window.focus_force()

    lbl_carregando = Label(carregando_window,text="Carregando...", bg="white")
    lbl_carregando.place(relx=0.5, rely=0.5, anchor=CENTER)

    carregando_window.after(2000,carregando_window.destroy)


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
    global bandeira
    main_screen.deiconify()
    bandeira = 0

    try:
        photo_screen.destroy()
        cam.release()

    except:
        background_screen.destroy()

def background_screen_choice():
    global background_screen

    try:
        photo_screen.destroy()
        cam.release()
    except:
        main_screen.withdraw()
    

    bold_font = font.Font(family="Helvetica", size=18, weight="bold")
    background_screen = Toplevel()
    background_screen.title("Background")
    background_screen.config(background="#e9e9e9")
    background_screen.geometry("800x480")
    centralize_window(background_screen)
    # background_screen.focus_force()
    

    background_screen.protocol("WM_DELETE_WINDOW", click_X_bg_choice)




    lbl_background = Label(background_screen,text="Defina o Background", bg="#e9e9e9", fg='black', font=bold_font)
    lbl_background.place(relx=0.35, rely=0.05)

    lbl_explicacao_bg = Label(background_screen, bg="#e9e9e9", fg="black", text="O Background é uma imagem da exata posição de trabalho da câmera, porém sem os objetos(a serem identificados).")
    lbl_explicacao_bg.place(relx=0.1, rely=0.13)

    lbl_voltar = Button(background_screen, text="Voltar", command=back_home)
    lbl_voltar.place(relx=0.02, rely=0.03)

    btn_photo = Button(background_screen, text="Tirar Foto", command=loading_background)
    btn_photo.place(relx=0.2, rely=0.6)

    btn_select_photo = Button(background_screen, text="Escolher na Pasta", command=select_bg)
    btn_select_photo.place(relx=0.7, rely=0.6)

def loading_background():
    auto_close_carregando()
    background_screen.after(500,background_screen_pic)

def background_screen_pic():
    global cam_bg, lbl_bg_video, online_bg  # Certifique-se de que lbl_bg_video é global

    bg_pic = Toplevel(background_screen)  # Cria uma nova janela para o background
    bg_pic.title("Cam Detector")
    bg_pic.config(background="#000000")
    bg_pic.geometry("1200x745")
    bg_pic.focus_force()

    cam_bg = cv2.VideoCapture(0)  # Inicializa a câmera para o background
    online_bg = True

    lbl_bg_video = Label(bg_pic)  # Label para exibir o vídeo
    lbl_bg_video.place(x=10, y=10)

    # Chama a função para atualizar o vídeo
    atualizar_frame_bg(bg_pic)

    def click_X_bg_pic():  # Função para parar a captura de vídeo ao fechar a janela
        global online_bg
        online_bg = False
        cam_bg.release()
        bg_pic.destroy()

    # Define o protocolo para fechar a janela e parar a câmera
    bg_pic.protocol("WM_DELETE_WINDOW", click_X_bg_pic)


def click_X_bg_choice():
    background_screen.destroy()
    if bandeira==0:
        main_screen.deiconify()
    else:
        btn_tirarFoto()
       
def select_bg():
    global bg_file
    file=filedialog.askopenfile(initialdir=inside_folder_path, title="Background", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg" )])
    
    try:
        file=file.name  #transforma em string um nome esquisito do objeto
        if file =='':
            pass
        if file.startswith(inside_folder_path):
            bg_file= file
            print('background escolhido')
        
        else:
            messagebox.showerror("Erro", "Você escolheu imagem de outra pasta.")
            select_bg()
    except:
        pass

def atualizar_frame_bg(bg_pic):
    global quadro, cam_bg, lbl_bg_video, online_bg

    if online_bg:
        ret, quadro = cam_bg.read()  # Captura um frame da câmera
        if ret:
            quadro = cv2.resize(quadro, (960, 720))  # Redimensiona o frame
            quadro_rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)  # Converte para RGB
            img = ImageTk.PhotoImage(image=Image.fromarray(quadro_rgb))  # Converte para ImageTk
            lbl_bg_video.imgtk = img  # Atualiza a imagem no Label
            lbl_bg_video.configure(image=img)

        lbl_bg_video.after(2, lambda: atualizar_frame_bg(bg_pic))  # Atualiza o frame a cada 2ms

def set_folder_path(path):
    folder_input.config(state=NORMAL)  # Permite alterar o campo temporariamente
    folder_input.delete(0, END)  # Limpa o conteúdo atual
    folder_input.insert(0, path)  # Insere o novo caminho
    folder_input.config(state="readonly")  # Define o campo como somente leitura novamente

folder_input = None
bandeira = None
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