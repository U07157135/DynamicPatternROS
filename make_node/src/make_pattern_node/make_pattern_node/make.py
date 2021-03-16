from pattern_interfaces.srv import PassData
from pattern_interfaces.srv import PassImage
from make_pattern_node.DynamicPatternTOP import DynamicPatternTOP
import rclpy
from rclpy.node import Node
import base64
import ast

class PassPatternNode(Node):

    def __init__(self):
        super().__init__('PassClient')
        self.cli = self.create_client(PassImage, 'pass_image')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = PassImage.Request()

    def send_image(self):
        with open("circle.png", "rb") as image2string: 
            image_data=base64.b64encode(image2string.read())
            self.req.data = image_data.decode()
        self.future = self.cli.call_async(self.req)

class MakePatternNode(Node):

    def __init__(self):
        super().__init__('MakeService')
        self.srv = self.create_service(PassData, 'pass_data', self.draw)

    def draw(self,request,response):
        dp = DynamicPatternTOP()
        data = ast.literal_eval(request.data)
        dp.set_pattern_dict(data)
        dp.set_resolution(request.width,request.height)
        dp.save_image("")
        pass_pattern_node = PassPatternNode()
        pass_pattern_node.send_image()
        while rclpy.ok():
            rclpy.spin_once(pass_pattern_node)
            if pass_pattern_node.future.done():
                try:
                    respon = pass_pattern_node.future.result()
                except Exception as e:
                    pass_pattern_node.get_logger().info(
                    'Service call failed %r' % (e,))
                else:
                    pass_pattern_node.get_logger().info('response:%s' %(
                    respon.show_pattern_response))
                break
        pass_pattern_node.destroy_node()
        response.make_pattern_response = str(data)
        return response
    


def main(args=None):
    rclpy.init(args=args)
    make_pattern_service = MakePatternNode()
    rclpy.spin(make_pattern_service)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
