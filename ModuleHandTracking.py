import cv2
import mediapipe as mp
import time


class Detector:
    def __init__(self, md=False, maxh=2, mdlcom=1, mindetectco=0.5, mintrackco=0.5):
        self.resul = None
        self.md = md
        self.maxh = maxh
        self.mdlcom = mdlcom  # TALVEZ INUTIL
        self.mindetectco = 0.5
        self.mintrackco = 0.5

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.md, self.maxh, self.mdlcom, self.mindetectco, self.mintrackco)

    def encmaos(self, img, draw=True):
        imgcolors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.resul = self.hands.process(imgcolors)

        if self.resul.multi_hand_landmarks:
            for hlms in self.resul.multi_hand_landmarks:
                if draw:  # Só vai fazer o desenho se draw for True
                    self.mp_draw.draw_landmarks(img, hlms, self.mp_hands.HAND_CONNECTIONS)

        return img

    def posicao(self, img, numh=0, draw=True):

        lmlist = []

        if self.resul.multi_hand_landmarks:
            mao = self.resul.multi_hand_landmarks[numh]

            for num, lm in enumerate(mao.landmark):
                height, width, c = img.shape

                cx = int(lm.x * width)
                cy = int(lm.y * height)

                lmlist.append([num, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 8, (117, 113, 100), cv2.FILLED)

        return lmlist


def main():
    cam = cv2.VideoCapture(0)  # Escolhendo a webcam 0 do PC

    tants = tagr = 0  # Variáveis para o calculo do FPS

    # Armazenando a class Detector em uma variável
    detector = Detector()
    while True:
        # Verificador e a leitura da imagem da webcam
        test, img = cam.read()

        # Chamando o método encmaos da class Detector
        detector.encmaos(img)

        # Chamando o método posicao da class Detector
        lmlist = detector.posicao(img)

        if len(lmlist) != 0:
            print(lmlist[4])

        img = cv2.flip(img, 1)  # Espelhando a imagem da webcam

        # Parte do FPS
        tagr = time.time()
        fps = int(1 / (tagr - tants))
        tants = tagr

        # Mostrando o FPS
        cv2.putText(img, str(fps), (580, 40), cv2.FONT_HERSHEY_PLAIN, 3, (117, 113, 100), 3)

        # Mostrando a webcam com as linhas da mão com um delay de 1 ms
        cv2.imshow("", img)  # Nome da janela que abre → ""
        cv2.waitKey(1)  # Só aceita valores inteiros maiores que 0


if __name__ == "__main__":
    main()
