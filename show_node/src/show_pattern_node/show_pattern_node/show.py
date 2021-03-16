
from pattern_interfaces.srv import PassImage
from show_pattern_node.pattern import Arrow
from rclpy.node import Node
import rclpy
import base64
import threading

class ShowPatternThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        Arrow()


class ShowPatternNode(Node):

    def __init__(self):
        super().__init__('ShowClient')
        self.thread1 = ShowPatternThread()
        self.thread1.daemon = True
        self.thread1.start()
        self.srv = self.create_service(PassImage, 'pass_image', self.save_image)

    def save_image(self,request,response):
        pattern_string = request.data
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(pattern_string.encode()))
        response.show_pattern_response = str("Show Done")
        return response
    
def main(args=None):
    rclpy.init(args=args)
    show_pattern_service = ShowPatternNode()
    rclpy.spin(show_pattern_service)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
