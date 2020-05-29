import socket
import time
from PIL import ImageGrab
from io import BytesIO

address_sender = ('', 8888)  # 服务器地址


def divide_bytes(b: bytes) -> list:
    b_chunks = []
    chunk_size = 1024

    temp_ = b
    while True:
        length = len(temp_)
        if length < chunk_size:
            b_chunks.append(temp_)
            break
        else:
            b_chunks.append(temp_[:chunk_size])
            temp_ = temp_[chunk_size:]
    b_chunks.append(b'')
    return b_chunks


class Sender:

    def __init__(self):
        self.send_flag = True

    def send(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            # 不断发送数据
            while self.send_flag:
                # data = 'sender -> hello:' + str(time.time())
                # b_data = data.encode('utf8')
                b_data = self.get_one_pic()

                # 图片太大，切割发送
                data_chunks = divide_bytes(b_data)
                for b in data_chunks:
                    print('发')
                    s.sendto(b, address_sender)

                    print('收')
                    server_response = s.recvfrom(1024)
                    print(server_response)

                time.sleep(0.03)

    def send1(self):
        while self.send_flag:
            b_data = self.get_one_pic()
            # 图片太大，切割发送
            data_chunks = divide_bytes(b_data)
            for b in data_chunks:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.settimeout(0.5)
                        print('发')
                        s.sendto(b, address_sender)

                        print('收')
                        server_response = s.recvfrom(1024)
                        print(server_response)
                except:
                    print('error ')
                    pass

                time.sleep(0.03)

    def stop_send(self):
        self.send_flag = False

    def get_one_pic(self):
        buff = BytesIO()
        img = ImageGrab.grab()
        little_img = img.resize(size=(320, 240))
        img = little_img
        img.save(buff, format='jpeg')
        img_byte = buff.getvalue()
        buff.close()
        length = len(img_byte)
        return img_byte


if __name__ == '__main__':
    Sender().send1()
    # Sender().get_one_pic()
