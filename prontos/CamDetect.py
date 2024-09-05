import cv2 #opencv
import numpy as np #array suports
import os

cam = cv2.VideoCapture(0)

online=True

foto_um=None
foto_dois=None
foto_tres=None
i=0                     # 0 -> printar tudo / 1 -> printar uma / 2 -> printar nenhuma
obj1=0                  # 0 -> selecionar roi / 1 -> roi já selecionado
obj2=0                  #           ""                  ""

foto_x=None

#verifica se apertou o X
def is_closed(cam):
    return cv2.getWindowProperty(cam, cv2.WND_PROP_VISIBLE) < 1


if cam.isOpened():
    while online == True:
        while i<2:
        # while foto_um and foto_dois and foto_tres != None:
            funcionou, frame = cam.read()
            cv2.imshow("Cam",frame)
            print(i)
            #clicar uma tecla
            key = cv2.waitKey(1) & 0xFF

            #printa foto 1
            if key == 49:                    #1
                cv2.imwrite("foto1.jpg", frame)
                i=i+1

            #printa foto 2                   #2
            if key == 50:
                cv2.imwrite("foto2.jpg", frame)
                i=i+1
            #printa foto 3                   #3
            # if key == 51:
            #    cv2.imwrite("foto3.jpeg", frame)
                # foto_tres="foto3.jpeg"

            #fecha
            if key == 27 or is_closed("Cam"):
                online=False
                break
            if i==2:
                break
        
        funcionou, frame = cam.read()
        cv2.imshow("Cam",frame)


        #clicar uma tecla
        key = cv2.waitKey(1) & 0xFF

        #fecha
        if key == 27 or is_closed("Cam"):
            online=False
            break


        #ler e transformar as imagens em cinza
        img_reference1 = cv2.imread("chave.png", cv2.IMREAD_GRAYSCALE)      #IMAGEM 1
        img_reference2 = cv2.imread("fita.png", cv2.IMREAD_GRAYSCALE)      #IMAGEM 2
        # img_reference3 = cv2.imread("foto3.jpeg", cv2.IMREAD_GRAYSCALE)   #IMAGEM 3


        #transforma o frame em foto
        # cv2.imwrite("fotoX.jpeg", frame)                   # aqui


        img_X = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)              #IMAGEM COMPARADA


        #cria orientação. keypoints e descritores para cada imagem
        orb = cv2.ORB.create()
        keypoint1, descritor1 = orb.detectAndCompute(img_reference1, None)
        keypoint2, descritor2 = orb.detectAndCompute(img_reference2, None)
        # keypoint3, descritor3 = orb.detectAndCompute(img_reference3, None)


        keypointX, descritorX = orb.detectAndCompute(img_X, None)

        #configura a comparação e compara imagem1 com imagemx, imagem2 com imagemx
        forca_bruta = cv2.BFMatcher(cv2.NORM_L2SQR, crossCheck=True)

        igual_1 = forca_bruta.match(descritorX, descritor1)
        igual_2 = forca_bruta.match(descritorX, descritor2)
        # igual_3 = forca_bruta.match(descritorX, descritor3)


        #retorna quantidade de relações, quanto maior melhor
        # print(len(igual_1))
        # print (len(igual_2))
        # print (len(igual_3))


        if len(igual_1)>len(igual_2) and len(igual_1)>100:
            print("chave")

            if obj1==0:     #trocar obj por clicar tecla (r). se clicar, apaga o roi anterior e cria outro
                roi1 = cv2.selectROI("select_roi_1", frame, fromCenter=False, showCrosshair=False)
                cv2.destroyWindow("select_roi_1")
                obj1=1
            else:
                continue
            tracker_1 = cv2.legacy.TrackerMOSSE_create()
            ok1 = tracker_1.init(frame, roi1)
            ok1, roi1 = tracker_1.update(frame)
            if ok1:
                pt1 = (int(roi1[0]), int(roi1[1]))
                pt2 = (int(roi1[0] + roi1[2]), int(roi1[1] + roi1[3]))
                cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2, 1)



        if len(igual_2)>len(igual_1) and len(igual_2)>100:
            print("fita")
            if obj2==0:     #trocar obj por clicar tecla (r). se clicar, apaga o roi anterior e cria outro
                roi2 = cv2.selectROI("select_roi_2", frame, fromCenter=False, showCrosshair=False)
                cv2.destroyWindow("select_roi_2")
                obj2=1
            else:
                continue
            tracker_2 = cv2.legacy.TrackerMOSSE_create()
            ok2 = tracker_2.init(frame, roi2)
            ok2, roi2 = tracker_2.update(frame)
            if ok2:
                pt3 = (int(roi2[0]), int(roi2[1]))
                pt4 = (int(roi2[0] + roi2[2]), int(roi2[1] + roi2[3]))
                cv2.rectangle(frame, pt3, pt4, (255, 0, 0), 2, 1)
        else:
            continue

cam.release()
cv2.destroyAllWindows()