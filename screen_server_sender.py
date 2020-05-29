import socketserver
import redis
import time
import threading
import multiprocessing

pool_raw = redis.ConnectionPool(host='', password='')  # 填写redis信息
redis_conn = redis.Redis(connection_pool=pool_raw)


class DataTransSender(socketserver.BaseRequestHandler):
    def setup(self):
        sender_ip = self.client_address[0]

        # 接受一个消息
        data_b, udp_sock = self.request

        # 数据操作：chunks写入redis
        sender_ip_key = 's_' + sender_ip
        # print(redis_conn.lrange(sender_ip_key, 0, 23))
        redis_conn.ltrim(sender_ip_key, 0, 20)
        redis_conn.lpush(sender_ip_key, data_b)
        redis_conn.expire(sender_ip_key, 2)

        # 向订阅者写数据
        self.publish_to_clients(data_b)

        print('sender->', len(data_b))

        # 返回本次结果
        udp_sock.sendto(b'ok', self.client_address)

        # 如果成功，将连接存入redis
        redis_conn.sadd('live_sender', sender_ip)

    def finish(self):
        sender_ip = self.client_address[0]
        # redis_conn.srem('sender_connections', ip)
        print(sender_ip, ' sender->finished')
        redis_conn.close()

    def publish_to_clients(self, data_b: bytes):
        sender_ip_children = 's_{ip}_children'.format(ip=self.client_address[0])
        sender_ip_children_set = redis_conn.smembers(sender_ip_children)
        for client_ip in sender_ip_children_set:
            client_ip = client_ip.decode('utf8')
            client_ip_key = 'c_' + client_ip
            redis_conn.lpush(client_ip_key, data_b)
            redis_conn.ltrim(client_ip_key, 0, 20)


def clean_death_sender():
    while True:
        ls = redis_conn.smembers('live_sender')
        for ip in ls:
            ip = ip.decode('utf8')
            ip_id = 'sender_' + ip
            r = redis_conn.get(ip_id)
            if not r:
                redis_conn.srem('live_sender', ip)
                print('clean program:', ip)


def clean_main():
    p1 = multiprocessing.Process(target=clean_death_sender)
    p1.daemon = False
    p1.start()
    print('clean program started')


def main_sender():
    address_server_sender = ('0.0.0.0', 7777)

    # 启动服务器
    socketserver.ThreadingUDPServer.allow_reuse_address = True
    server = socketserver.ThreadingUDPServer(address_server_sender, DataTransSender)
    print('start sender')
    server.serve_forever()


if __name__ == '__main__':
    main_sender()
