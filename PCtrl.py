import cv2
import time
import numpy as np
import ModuleHandTracking as htm

# pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#

#para o controle do mouse
import pyautogui

w, h = 640, 480

cam = cv2.VideoCapture(0)
cam.set(3, w)
cam.set(4, h)

tants = tagr = 0

volporc = 0

barvol = 0

detector = htm.Detector(mindetectco=0.8, maxh=1)

# pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#

while True:

    test, img = cam.read()

    img = cv2.flip(img, 1)

    img, dire = detector.encmaos(img)

    lmlist, allxy = detector.posicao(img, draw=True)

    if len(lmlist) != 0:

        ddpc = detector.ddspcima()
        
        
        if ddpc == [0, 1, 1, 0, 0] or ddpc == [1, 1, 1, 0, 0]:
            pos = detector.posicao(img)
            print(pos[0][8])
            screenWidth, screenHeight = pyautogui.size()

            # if not pyautogui.onScreen(screenWidth, screenHeight):
            #     ajusx = np.interp(pos[0][8][1], [125, 500], [1, screenWidth - 1])
            #     ajusy = np.interp(pos[0][8][2], [255, 420], [1, screenHeight - 1])
                
            #     tremilick2 = 5
            #     ajusx = tremilick2 * round(ajusx / tremilick2)
            #     ajusy = tremilick2 * round(ajusy / tremilick2)
            #     if ajusx > 0 and ajusy > 0:
            #         pyautogui.moveTo(ajusx, ajusy)


        # Se todos os dedos estiverem para cima
        if ddpc == [1, 1, 1, 1, 1]:
            dist, img, ult = detector.distdd(4, 8, img, draw=True)

            # Convertendo os intervalos
            barvol = np.interp(dist, [0, 160], [400, 150])
            volporc = np.interp(dist, [0, 160], [0, 100])

            # Deixando mais suave
            tremilick = 10
            volporc = tremilick * round(volporc / tremilick)

            volume.SetMasterVolumeLevelScalar(volporc / 100, None)

            # Muda o lado da barra de volume dependendo da mão que aparecer 
            if dire == 'Right':
                cv2.rectangle(img, (50, 150), (85, 400), (117, 0, 100), 3)
                cv2.rectangle(img, (50, int(barvol)), (85, 400), (117, 0, 100), cv2.FILLED)
                cv2.putText(img, f'{volporc} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (117, 0, 100), 2)
            else:
                cv2.rectangle(img, (590, 150), (555, 400), (117, 0, 100), 3)
                cv2.rectangle(img, (590, int(barvol)), (555, 400), (117, 0, 100), cv2.FILLED)
                cv2.putText(img, f'{volporc} %', (500, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (117, 0, 100), 2)

    tagr = time.time()
    fps = int(1 / (tagr - tants))
    tants = tagr

    cv2.putText(img, str(fps), (580, 40), cv2.FONT_HERSHEY_PLAIN, 3, (117, 113, 100), 3)

    cv2.imshow("", img)
    cv2.waitKey(1)
