#!/usr/bin/env python3

import serial
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

RAW_SIZE = 22
PORT_NAME = '/dev/ttyS0'
LISTEN_PORT = 8035

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        try:
            raw_data = b''
            device_CI6000.flushInput()
            while len(raw_data) < RAW_SIZE:
                raw_data = device_CI6000.readline()

            stable = raw_data.startswith(b'ST')
            weight = float(raw_data[9:17].decode('ascii').replace(' ',''))
            units = raw_data[18:20].decode('ascii').lstrip()
            weight_dict = {"stable":stable, "weight":weight, "units":units}

        except Exception:
            weight_dict = {"stable":False, "weight":9999.99, "units":"t"}
            print(f'Oops! - {Exception}')

        self.wfile.write(json.dumps(weight_dict).encode('utf-8'))
        return


if __name__ == '__main__':
    try:
        device_CI6000 = serial.Serial(PORT_NAME)
        server = HTTPServer(('', LISTEN_PORT), MyHandler)
        print('Server started')
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, abort !')
        device_CI6000.close()
        server.socket.close()
    except Exception as e:
        print(f'Oops ! {e}')
    finally:
        print('Closed')
        device_CI6000.close()
        server.socket.close()
