import cv2
import math
import time
import numpy as np
import  ModuleHandTracking as htm

# pycaw by AndreMiras https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

w, h = 500, 500

cam = cv2.VideoCapture(0)
cam.set(3, w)
cam.set(4, h)

tants = tagr = 0

detector = htm.Detector(mindetectco=0.8)

# pycaw settings
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

minv = volume.GetVolumeRange()[0]
maxv = volume.GetVolumeRange()[1]
#

while True:
    test, img = cam.read()

    img = detector.encmaos(img)

    lmlist = detector.posicao(img, draw=False)
    if len(lmlist) != 0:

        # Pegando a posição da ponta do indicador
        x1 = lmlist[4][1] 
        y1 = lmlist[4][2]

        # Pegando a posição da ponta do polegar
        x2 = lmlist[8][1]
        y2 = lmlist[8][2]

        # Pegando o ponto medio da linha entre a (x1, y1) e (x2, y2)
        mx = (x2 + x1) // 2
        my = (y2 + y1) // 2

        # Desenhando circulos nos pontos e uma linha entre (x1, y1) e (x2, y2)
        cv2.circle(img, (x1, y1), 8, (117, 113, 100), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (117, 113, 100), cv2.FILLED)
        cv2.circle(img, (mx, my), 8, (117, 113, 100), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (117, 113, 100), 2)

        # Calculo da distancia entre os pontos (x1, y1) e (x2, y2)
        dist = math.hypot(x2 - x1, y2 - y1)
        
        # Mudando a cor do ponto medio (mx, my) quando (x1, y1) e (x2, y2) ficam próximos 
        if dist < 15:
            cv2.circle(img, (mx, my), 8, (117, 0, 100), cv2.FILLED)

        # Usando numpy para converter o intervalo da distancia (5 - 150) para o intervalo do volume.GetVolumeRange() 
        vol = np.interp(dist, [5, 150], [minv, maxv])

        # Alterando o volume do computador com base no valor de vol
        volume.SetMasterVolumeLevel(vol, None)

    img = cv2.flip(img, 1)

    tagr = time.time()
    fps = int(1 / (tagr - tants))
    tants = tagr

    cv2.putText(img, str(fps), (580, 40), cv2.FONT_HERSHEY_PLAIN, 3, (117, 113, 100), 3)

    cv2.imshow("", img)
    cv2.waitKey(1)
