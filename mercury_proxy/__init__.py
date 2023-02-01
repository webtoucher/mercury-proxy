# coding=utf8
import logging
import sys

from mercury_base import Meter
from mercury_base.utils import hex_str
from modbus_crc import add_crc, check_crc
from socket import socket
from simple_socket_server import FlaskSimpleSocketServer
from typing import Optional

server = FlaskSimpleSocketServer(None)

log_handler = logging.StreamHandler(sys.stderr)
log_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s\t%(message)s")
)
logger = logging.getLogger('mercury')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

meters = []
my_meter = Meter(37793503, '/dev/ttyACM0', logger=logger)
logger.info('Meter type: %s', my_meter.model)
meters.append(my_meter)


def find_by_package(package: bytes) -> Optional[Meter]:
    return next((meter for meter in meters if meter.test_package(package)), None)


@server.on_connect
def on_connect(sock: socket):
    logger.info('New connection from %s:%s', *sock.getpeername())


@server.on_disconnect
def on_disconnect(sock: socket):
    logger.info('Connection from %s:%s is closed', *sock.getpeername())


@server.on_message
def on_message(sock: socket, message: bytes):
    logger.info('[%s:%s] --> [proxy]\t%s', *sock.getpeername(), hex_str(message, ' '))
    if not check_crc(message):
        logger.warning('Package from %s:%s has wrong checksum', *sock.getpeername())
    meter = find_by_package(message)
    if meter:
        answer = meter.send_package(message)
        if answer:
            logger.info('[%s:%s] <-- [proxy]\t%s', *sock.getpeername(), hex_str(answer, ' '))
            server.send(sock, answer)


if __name__ == '__main__':

    server.run(port=5051)
