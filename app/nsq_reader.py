import nsq
import os
from dill import loads

tcp_address = os.getenv('NSQTCP_ADDRESS')
topic = os.getenv('NSQ_TOPIC')
channel = os.getenv('NSQ_CHANNEL')

print('Reader started by address {}'.format(tcp_address))

def handler(message):
    data = loads(message.body)
    print('address = {}'.format(data['address']))
    print('word_count = {}'.format(data['word_count']))
    print('create_time = {}'.format(data['create_time']))
    print('status_code = {}'.format(data['status_code']))
    print('status = {}'.format(data['status']))
    return True

r = nsq.Reader(message_handler=handler,
        nsqd_tcp_addresses=tcp_address,
        topic=topic,
        channel=channel,
        lookupd_poll_interval=15)

if __name__ == '__main__':
    nsq.run()
