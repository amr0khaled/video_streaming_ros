from typing import Any
import rclpy as rc
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import cv_bridge as c

class Pub(Node):
  def __init__(self):
    super().__init__('Video_Streaming_Publisher')
    self.get_logger().info('Started')
    self.stream_pub = self.create_publisher(Image, 'Stream', 1)

    # Start Streaming
    self.send_stream()

  def send_stream(self):
    for i in generate():
      self.get_logger().info('SEnd a frame of stream %s' % i.header.stamp.sec)
      self.stream_pub.publish(i)


def generate():
  camera = cv2.VideoCapture(0)  # Change to 1, 2, etc., if multiple cameras are available
  bridge = c.CvBridge()
  while True:
    # Read a frame from the camera
    sucess, frame = camera.read()
    if not sucess:
        break
    ros_image = bridge.cv2_to_imgmsg(frame, 'rgb8');
    # Encode the frame as JPEG
    sucess, image = cv2.imencode('.jpg', frame)
    if not sucess:
        break
    # Convert the JPEG to byte data
    # Yield the frame as a part of the MJPEG stream
    yield ros_image

def main(args: list[str] | None=None):
    rc.init(args=args)
    node = Pub()
    rc.spin(node)
    node.destroy_node()
    rc.shutdown()


if __name__=='__main__':
    main()
