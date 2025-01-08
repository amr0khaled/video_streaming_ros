from typing import Any, Generator
import rclpy as rc
from rclpy.node import Node
import std_msgs.msg as types
from json import JSONDecoder, JSONDecodeError
from flask import *
import threading as threads
server = Flask('Host Stream')

jsde = JSONDecoder()
def stream():
    out = [b'\00']
    while True:
        out = yield
        # print(type(out))
        yield out
class Sub(Node):
    def __init__(self, callback):
        super().__init__('SubSS') 
        self.sub = self.create_subscription(types.String, 'YOU', self.listen, 10)
        self.stream_sub = self.create_subscription(types.UInt8MultiArray, 'Stream', self.stream_listen, 1)
        self.send_callback = callback
    def listen(self, s):
        a = s
    def stream_listen(self, msg: types.UInt8MultiArray):
        raw = bytes(msg.data)
        self.get_logger().info('I get a stream frame')
        data = (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + raw + b'\r\n\r\n')
        self.send_callback(data)
                
    def from_json(self, data: types.String):
        try:
            return jsde.decode(data.data)
        except JSONDecodeError:
            self.get_logger().error("JSON DECODING ERROR: '%s'" % data.data)

queue: list[bytes] = []

def send_queue(data: bytes):
    queue.append(data)

def gen():
    while True:
        if queue:
            message = queue.pop(0)
            yield message
def main(args: list[str] | None = None):
    rc.init(args=args)
    sub = Sub(send_queue)

    @server.route('/')
    def video_feed():
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @server.route('/test')
    def testing():
        return 'IT WORKS'
    def start_node():
        rc.spin(sub)
        global server
    try:
        thread = threads.Thread(target=start_node, daemon=True)
        thread.start()
        server.run(debug=True, host='127.0.0.1', port=5000)
    finally:
        sub.destroy_node()
        rc.shutdown()

if __name__=='__main__':
    main()





