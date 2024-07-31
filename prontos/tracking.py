import cv2

# Captura da imagem estática e seleção da ROI
fita_img = cv2.imread("fita.png")
fita_quadrado = cv2.selectROI("select_roi", fita_img, fromCenter=False, showCrosshair=False)
cv2.destroyWindow("select_roi")     # Fecha a janela de seleção de ROI

# Criação e configuração do tracker
fita_tracker = cv2.legacy.TrackerMOSSE_create()
ok = fita_tracker.init(fita_img, fita_quadrado)

# Inicialização da captura de vídeo ao vivo
cam = cv2.VideoCapture(0)

while cam.isOpened():
    funcionou, frame = cam.read()
    if not funcionou:
        break
    
    ok, fita_quadrado = fita_tracker.update(frame)
    
    if ok:
        pt1 = (int(fita_quadrado[0]), int(fita_quadrado[1]))
        pt2 = (int(fita_quadrado[0] + fita_quadrado[2]), int(fita_quadrado[1] + fita_quadrado[3]))
        cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2, 1)
    else:
        print("Quadrado não encontrado")
    
    cv2.imshow("Cam", frame)
    
    if cv2.waitKey(1) == 27:  # Tecla 'ESC' para sair
        break

cam.release()
cv2.destroyAllWindows()