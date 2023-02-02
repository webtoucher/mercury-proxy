# coding=utf8
from flask import Flask, abort, jsonify, make_response, request
from flask.app import BadRequest
from mercury_base import Meters
from threading import Thread
from waitress import serve


class Api(object):
    def __init__(self, meters: Meters):
        self.__app = Flask(__name__)
        self.__meters = meters

        @self.__app.errorhandler(404)
        def not_found(_error):
            return make_response(jsonify({'error': 'Not found'}), 404)

        @self.__app.errorhandler(BadRequest)
        def internal_error(error):
            return make_response(jsonify({'error': 'Bad request'}), error.code)

        @self.__app.errorhandler(Exception)
        def internal_error(error):
            self.__app.logger.exception(error)
            return make_response(jsonify({'error': f'{error}'}), error.code)

        @self.__app.get('/v1.0/list')
        def get_list():
            data = {}
            for meter in self.__meters.meters:
                data.update({meter.serial_number: meter.model})
            return jsonify(data)

        @self.__app.get('/v1.0/meter/<int:serial_number>/<name>')
        def get_meter_value(serial_number: int, name: str):
            self.__app.logger.debug('Request GET /v1.0/meter/%s/%s', serial_number, name)
            meter = self.__meters.find_by_serial_number(serial_number)
            if not meter:
                self.__app.logger.error('Meter %s is not found', serial_number)
                abort(404)
            command = 'get_' + name
            if not meter.has_command(command):
                self.__app.logger.error('Command %s is not found', command)
                abort(404)
            data = meter.command(command)
            return jsonify(data)

        @self.__app.post('/v1.0/meter/<int:serial_number>/<name>')
        def set_meter_value(serial_number: int, name: str):
            if not request.json or type(request.json) != dict:
                abort(400)
            self.__app.logger.debug('Request POST /v1.0/meter/%s/%s', serial_number, name)
            meter = self.__meters.find_by_serial_number(serial_number)
            if not meter:
                self.__app.logger.error('Meter %s is not found', serial_number)
                abort(404)
            command = 'set_' + name
            if not meter.has_command(command):
                self.__app.logger.error('Command %s is not found', command)
                abort(404)
            data = meter.command(command, request.json)
            return jsonify(data)

    def run(self, host='0.0.0.0', port=5052):
        kwargs = {
            'host': host,
            'port': port,
            '_quiet': True,
        }
        thread = Thread(target=serve, args=(self.__app,), kwargs=kwargs)
        thread.start()
        self.__app.logger.info('Api server is listening on %s:%s', host, port)

    @property
    def logger(self):
        return self.__app.logger
