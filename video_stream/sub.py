from collections.abc import Generator
from typing import Any, Never
import rclpy as rc
from rclpy.node import Node
import std_msgs.msg as types
from sensor_msgs.msg import Image
from flask import Flask, Response
import threading as threads
import cv_bridge
import cv2

bridge = cv_bridge.CvBridge()

class Sub(Node):
  def __init__(self, callback):
    super().__init__('Video_Streaming_Subscriber') 
    self.get_logger().info('Started')
    self.stream_sub = self.create_subscription(Image, 'Stream', self.stream_listen, 1)
    self.send_callback = callback

  def stream_listen(self, msg: Image):
    try:
      image_cv = bridge.imgmsg_to_cv2(msg)
      success, image = cv2.imencode('.jpg', image_cv);
      self.get_logger().info('I get a stream frame in %s' % msg.header.stamp.sec)
      data = (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')
      self.send_callback(data)
    except cv_bridge.CvBridgeError or cv2.Error:
      print("error")
      pass

queue: list[bytes] = []

def send_queue(data: bytes):
  queue.append(data)

def gen():
  while True:
    if queue:
      message = queue.pop()
      yield message

def start_server(app: Flask, stream_generator: Generator[bytes, Any, Never]):
  @app.route('/')
  def video_feed():
    return Response(stream_generator, mimetype='multipart/x-mixed-replace; boundary=frame')
  # just for testing if it works
  @app.route('/test')
  def testing():
    return 'IT WORKS'

def main(args: list[str] | None = None):
  server = Flask('Host Stream')
  rc.init(args=args)
  sub = Sub(send_queue)

  def start_node():
    rc.spin(sub)
  try:
    # Start subscriber on another thread
    thread = threads.Thread(target=start_node, daemon=True)
    thread.start()
    # Start flask server
    start_server(server, gen())
    server.run(debug=True, host='127.0.0.1', port=5000)
  finally:
    sub.destroy_node()
    rc.shutdown()

if __name__=='__main__':
    main()
