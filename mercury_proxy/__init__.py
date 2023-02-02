# coding=utf8
import logging
import sys

from mercury_base import Meter, Meters, MetersEventListener, check_crc, hex_str
from mercury_proxy.api import Api
from socket import socket
from simple_socket_server import SimpleSocketServer


with_api = True


if __name__ == '__main__':
    meters_listener = MetersEventListener()
    meters = Meters(meters_listener)

    socket_server = SimpleSocketServer()

    if with_api:
        api = Api(meters)
        logger = api.logger
    else:
        api = None
        logger = logging.getLogger(__name__)

    log_handler = logging.StreamHandler(sys.stderr)
    log_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s\t%(message)s")
    )
    logger.handlers = [log_handler]

    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)


    @socket_server.on_start
    def on_start(ip: str, port: int):
        logger.info('Proxy server is listening on %s:%s', ip, port)


    @socket_server.on_connect
    def on_connect(sock: socket):
        logger.debug('New connection from %s:%s', *sock.getpeername())


    @socket_server.on_disconnect
    def on_disconnect(sock: socket):
        logger.debug('Connection from %s:%s is closed', *sock.getpeername())


    @socket_server.on_message
    def on_message(sock: socket, message: bytes):
        if bytearray(message)[:1].isalpha():
            logger.warning('It looks like the socket request is HTTP')
            raise ConnectionResetError()
        logger.debug('[%s:%s] --> [proxy]\t%s', *sock.getpeername(), hex_str(message, ' '))
        if not check_crc(message):
            logger.warning('Package from %s:%s has wrong checksum', *sock.getpeername())
            return
        meter = meters.find_by_package(message)
        if meter:
            answer = meter.send_package(message)
            if answer:
                logger.debug('[%s:%s] <-- [proxy]\t%s', *sock.getpeername(), hex_str(answer, ' '))
                socket_server.send(sock, answer)


    @meters_listener.on_connect
    def on_connect(meter: Meter):
        logger.info('Meter M%s with serial number %s is connected', meter.model, meter.serial_number)


    @meters_listener.on_request
    def on_request(meter: Meter, package: bytes):
        logger.debug('[proxy] --> [%s]\t%s', meter.serial_number or 'new meter', hex_str(package, ' '))


    @meters_listener.on_answer
    def on_answer(meter: Meter, package: bytes):
        logger.debug('[proxy] <-- [%s]\t%s', meter.serial_number or 'new meter', hex_str(package, ' '))


    meters.connect_meter(37793503, '/dev/ttyACM0')

    if api:
        api.run(port=5052)
    socket_server.run(port=5051)
