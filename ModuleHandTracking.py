import cv2
import mediapipe as mp
import time
import math


class Detector:
    def __init__(self, md=False, maxh=2, mdlcom=1, mindetectco=0.5, mintrackco=0.5):
        # Variáveis
        self.dire = None
        self.lmlist = None
        self.resul = None
        self.ptnum = [4, 8, 12, 16, 20]

        self.md = md
        self.maxh = maxh
        self.mdlcom = mdlcom
        self.mindetectco = mindetectco
        self.mintrackco = mintrackco

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.md, self.maxh, self.mdlcom, self.mindetectco, self.mintrackco)

    # Método para encontrar a mão
    def encmaos(self, img, draw=True):
        imgcolors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.resul = self.hands.process(imgcolors)

        if self.resul.multi_hand_landmarks:
            self.dire = self.resul.multi_handedness[0].classification[0].label
            for hlms in self.resul.multi_hand_landmarks:
                if draw:  # Só vai fazer o desenho se draw for True
                    self.mp_draw.draw_landmarks(img, hlms, self.mp_hands.HAND_CONNECTIONS)
        return img, self.dire

    # Método que retorna as posições de cada parte da mão e os pontos máximo mínimo
    def posicao(self, img, numh=0, draw=True):
        allx = list()
        ally = list()
        allxy = list()
        self.lmlist = list()

        if self.resul.multi_hand_landmarks:
            mao = self.resul.multi_hand_landmarks[numh]

            for num, lm in enumerate(mao.landmark):
                height, width, c = img.shape

                cx = int(lm.x * width)
                cy = int(lm.y * height)

                allx.append(cx)
                ally.append(cy)

                self.lmlist.append([num, cx, cy])

            xmx = max(allx)
            xmn = min(allx)

            ymx = max(ally)
            ymn = min(ally)

            allxy = [xmn, ymn, xmx, ymx]

            if draw:
                cv2.rectangle(img, (allxy[0] - 25, allxy[1] - 25), (allxy[2] + 25, allxy[3] + 25), (0, 255, 0), 2)

        return self.lmlist, allxy

    def distdd(self, a, b, img=None, draw=True):
        x1 = self.lmlist[a][1]
        y1 = self.lmlist[a][2]

        x2 = self.lmlist[b][1]
        y2 = self.lmlist[b][2]

        mx = (x2 + x1) // 2
        my = (y2 + y1) // 2

        dist = math.hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.circle(img, (x1, y1), 8, (117, 113, 100), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (117, 113, 100), cv2.FILLED)
            cv2.circle(img, (mx, my), 8, (117, 113, 100), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (117, 113, 100), 2)
            if dist < 25:
                cv2.circle(img, (mx, my), 8, (117, 0, 100), cv2.FILLED)

        return dist, img, [x1, y1, x2, y2, mx, my]

    def ddspcima(self):
        ddpc = list()

        # Polegar
        distupp, lp, mcp = self.distdd(4, 0, draw=False)
        if distupp > 110:
            ddpc.append(1)
        else:
            ddpc.append(0)

        # Resto dos dedos
        for i in range(1, 5):
            distup, l, m = self.distdd(self.ptnum[i], 0, draw=False)
            if distup > 120:
                ddpc.append(1)
            else:
                ddpc.append(0)

        return ddpc


def main():
    # Tamanho da janela da webcam
    w, h = 400, 400

    cam = cv2.VideoCapture(0)  # Escolhendo a webcam 0 do PC
    cam.set(3, w)
    cam.set(4, h)

    tants = tagr = 0  # Variáveis para o calculo do FPS

    # Armazenando a class Detector em uma variável
    detector = Detector()
    while True:
        # Verificador e a leitura da imagem da webcam
        test, img = cam.read()

        # Chamando o método encmaos da class Detector
        img = detector.encmaos(img)

        # Chamando o método posicao da class Detector
        lmlist = detector.posicao(img)

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
