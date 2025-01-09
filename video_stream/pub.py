from typing import Any
import rclpy as rc
from rclpy.node import Node
import std_msgs.msg as types
import cv2

class Pub(Node):
  def __init__(self):
    super().__init__('Video_Streaming_Publisher')
    self.get_logger().info('Started')
    self.stream_pub = self.create_publisher(types.UInt8MultiArray, 'Stream', 1)

    # Start Streaming
    self.send_stream()

  def send_stream(self):
    msg = types.UInt8MultiArray()
    for i in generate():
      msg.data = i
      self.get_logger().info('SEnd a frame of stream')
      self.stream_pub.publish(msg)


def generate():
  camera = cv2.VideoCapture(0)  # Change to 1, 2, etc., if multiple cameras are available
  while True:
    # Read a frame from the camera
    sucess, frame = camera.read()
    if not sucess:
        break
    # Encode the frame as JPEG
    sucess, image = cv2.imencode('.jpg', frame)
    if not sucess:
        break
    # Convert the JPEG to byte data
    image_data: bytes = image.tobytes()
    # Yield the frame as a part of the MJPEG stream
    yield list(image_data)


def main(args: list[str] | None=None):
    rc.init(args=args)
    node = Pub()
    rc.spin(node)
    node.destroy_node()
    rc.shutdown()


if __name__=='__main__':
    main()
