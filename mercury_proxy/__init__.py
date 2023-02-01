# coding=utf8
import logging
import sys

from mercury_base import Meter, MetersEventListener, check_crc, hex_str
from socket import socket
from simple_socket_server import SimpleSocketServer
from typing import Optional

if __name__ == '__main__':
    log_handler = logging.StreamHandler(sys.stderr)
    log_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s\t%(message)s")
    )
    logger = logging.getLogger('mercury')
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    server = SimpleSocketServer()
    meters_listener = MetersEventListener()
    meters = []


    def find_by_package(package: bytes) -> Optional[Meter]:
        return next((meter for meter in meters if meter.test_package(package)), None)


    @server.on_start
    def on_start(ip: str, port: int):
        logger.info('Proxy server is listening on %s:%s', ip, port)


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


    @meters_listener.on_connect
    def on_connect(meter: Meter):
        logger.info('Meter M%s with serial number %s is connected', meter.model, meter.serial_number)


    @meters_listener.on_request
    def on_request(meter: Meter, package: bytes):
        logger.debug('[proxy] --> [%s]\t%s', meter.serial_number or 'new meter', hex_str(package, ' '))


    @meters_listener.on_answer
    def on_answer(meter: Meter, package: bytes):
        logger.debug('[proxy] <-- [%s]\t%s', meter.serial_number or 'new meter', hex_str(package, ' '))


    my_meter = Meter(37793503, '/dev/ttyACM0', listener=meters_listener)
    if my_meter:
        meters.append(my_meter)

    server.run(port=5051)
