import socketserver
import time

import redis

pool_raw = redis.ConnectionPool(host='', password='')  # 填写redis信息
redis_conn = redis.Redis(connection_pool=pool_raw)


class DataTransReceiver(socketserver.BaseRequestHandler):
    def setup(self):
        # 注册客户端:
        client_ip = self.client_address[0]
        client_ip_key = 'c_' + client_ip
        client_ip_status = 'status_c_' + client_ip
        redis_conn.sadd('live_client', client_ip)
        redis_conn.expire('live_client', 2)

        # 用于清理内存
        redis_conn.set(client_ip_status, 'live')
        redis_conn.expire(client_ip_status, 1)

        # 接受一个消息
        data_b, udp_sock = self.request
        req_ip = data_b.decode('utf8')

        # 将c_ip挂在对应的sender_ip=req_ip下面:
        req_ip_key = 's_{req_ip}_children'.format(req_ip=req_ip)
        redis_conn.sadd(req_ip_key, client_ip)
        redis_conn.expire(req_ip_key, 2)

        try:
            one_msg = redis_conn.rpop(client_ip_key)
        except Exception as err:
            print('error:', err)
        else:
            if one_msg is None:
                print('no data: ', time.time())
                one_msg = b'None'
            udp_sock.sendto(one_msg, self.client_address)

        # redis_conn.rpop(req_ip_key, client_ip)  todo 需要清理离线客户端

    def finish(self):
        ip = self.client_address[0]
        print(ip, ' has removed')
        redis_conn.close()

    def register_a_client(self):
        redis_conn.sadd('live_receiver', self.client_address[0])


def main_receiver():
    address_server_receiver = ('0.0.0.0', 8888)
    socketserver.ThreadingUDPServer.allow_reuse_address = True
    server = socketserver.ThreadingUDPServer(address_server_receiver, DataTransReceiver)
    print('start receiver')
    server.serve_forever()


if __name__ == '__main__':
    main_receiver()
