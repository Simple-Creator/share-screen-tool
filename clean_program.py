import redis
import time

# redis地址
pool_raw = redis.ConnectionPool(host='', password='')  # 填写redis信息
redis_conn = redis.Redis(connection_pool=pool_raw)


def clean_death_sender(clean_type: str):
    live_nodes = redis_conn.smembers('live_' + clean_type)
    for node in live_nodes:
        node_ip = node.decode('utf8')
        node_ip_key = clean_type + '_' + node_ip
        r = redis_conn.exists('status_{clean_type}_{node_ip_key}'.format(clean_type=clean_type, ip_key=node_ip_key))
        if not r:
            redis_conn.srem('live_' + clean_type, node)
            print('clean {clean_type}:'.format(clean_type=clean_type), node)

    time.sleep(2)


def main():
    print('clean start...')
    while True:
        clean_death_sender('s')
        clean_death_sender('client')
        time.sleep(10)


if __name__ == '__main__':
    main()
