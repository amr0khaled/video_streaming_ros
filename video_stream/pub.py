
from typing import Any, Sequence
import rclpy as rc
from rclpy.node import Node
import std_msgs.msg as types
from json import JSONEncoder
import cv2


jsen = JSONEncoder()

json_data = [
  {
    "name": "John Doe",
    "age": 32,
    "salary": 75000,
    "jobTitle": "Software Engineer"
  },
  {
    "name": "Jane Smith",
    "age": 27,
    "salary": 60000,
    "jobTitle": "Data Analyst"
  },
  {
    "name": "Bob Brown",
    "age": 41,
    "salary": 90000,
    "jobTitle": "Product Manager"
  },
  {
    "name": "Alice Johnson",
    "age": 29,
    "salary": 65000,
    "jobTitle": "UX Designer"
  },
  {
    "name": "Mike Davis",
    "age": 35,
    "salary": 70000,
    "jobTitle": "DevOps Engineer"
  },
  {
    "name": "Emily Chen",
    "age": 28,
    "salary": 62000,
    "jobTitle": "Marketing Specialist"
  },
  {
    "name": "David Lee",
    "age": 40,
    "salary": 85000,
    "jobTitle": "Sales Manager"
  },
  {
    "name": "Sarah Taylor",
    "age": 25,
    "salary": 58000,
    "jobTitle": "Customer Support"
  },
  {
    "name": "Kevin White",
    "age": 38,
    "salary": 72000,
    "jobTitle": "IT Manager"
  },
  {
    "name": "Lisa Nguyen",
    "age": 30,
    "salary": 68000,
    "jobTitle": "Financial Analyst"
  }
]







class Pub(Node):
    mimetype ='multipart/x-mixed-replace; boundary=frame'
    def __init__(self):
        super().__init__('Pubber')
        self.counter = 0
        self.get_logger().info('Started')
        self.pub = self.create_publisher(types.String, 'YOU', 10)
        self.stream_pub = self.create_publisher(types.UInt8MultiArray, 'Stream', 1)
        self.index = 0

        # self.create_timer(0.001, self.send_stream)
        self.send_stream()
    def timer(self):
        self.counter += 1
        self.get_logger().info(f'{self.counter}')
        msg = types.String()
        msg.data = f'THIS IS NUMBER = {self.counter}'
        self.pub.publish(msg)
    def send_msg(self):
        msg = types.String()
        if self.index == len(json_data):
            self.index = self.index % len(json_data)
        msg.data = f'JSON msg: {self.to_json(json_data[self.index])}'
        self.get_logger().info("I Send: %s" % msg.data)
        self.index+=1
        self.pub.publish(msg)

    def to_json(self, data: dict[str, Any]):
        return jsen.encode(data)
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
        sucess, jpeg = cv2.imencode('.jpg', frame)
        if not sucess:
            break
        # Convert the JPEG to byte data
        jpeg_data: bytes = jpeg.tobytes()
        # Yield the frame as a part of the MJPEG stream
        yield list(jpeg_data)
        #yield (b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + jpeg_data + b'\r\n\r\n')


def main(args: list[str] | None=None):
    rc.init(args=args)
    node = Pub()
    rc.spin(node)
    node.destroy_node()
    rc.shutdown()


if __name__=='__main__':
    main()
