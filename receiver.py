import socket
import time
import cv2
from PIL import Image
from io import BytesIO
import numpy as np

address_receiver = ('', 8888)  # 服务器地址


class Receiver:
    def __init__(self, ip: str):
        self.ip_choose = ip
        self.receive_flag = True
        self.client_name = 'remote desktop ' + str(time.time())[-3:]

    def receive(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            ip_option = self.ip_choose

            # chunk对齐到开始
            self.img_sync(s)

            while True:
                # 接收一个图片字节流
                img_bytes = self.receive_a_img(s)

                # 显示
                self.show_img(img_bytes)
                time.sleep(0.06)

    def img_sync(self, sock: socket.socket):
        while True:
            sock.sendto(self.ip_choose.encode('utf8'), address_receiver)
            data_b, conn = sock.recvfrom(1024)
            if data_b == b'None':
                continue

            print("sync->", data_b)
            if not data_b:
                break

    def receive_a_img(self, sock: socket.socket) -> BytesIO:
        buffer = BytesIO()
        while True:
            sock.sendto(self.ip_choose.encode('utf8'), address_receiver)
            data_b, conn = sock.recvfrom(1024)

            if data_b == b'None':
                continue

            if not data_b:
                break
            else:
                buffer.write(data_b)

        b_data = buffer.getvalue()
        buffer.close()
        print('receiver one img over->', time.time())
        return b_data

    def show_img(self, img_bytes: bytes):
        try:
            img = Image.open(BytesIO(img_bytes))
            img_mat = np.array(img)
            bgr_img = cv2.cvtColor(img_mat, cv2.COLOR_RGB2BGR)
        except:
            pass
        else:
            cv2.imshow(self.client_name, bgr_img)
            cv2.waitKey(1)


if __name__ == '__main__':
    ip = input('请输入接入ip:')  # 目前是 sender ip
    Receiver(ip).receive()
