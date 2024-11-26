import rclpy
from ackermann_msgs.msg import AckermannDriveStamped
from rclpy.node import Node
import sys, select, termios, tty

settings = termios.tcgetattr(sys.stdin)

class Autocar_Teleop(Node):
  def __init__(self):
    super().__init__("autocar_teleop_pub")
    self.speed = 0.0
    self.steering_angle = 0.0
    self.pub = self.create_publisher(AckermannDriveStamped, "/cmd_vel", 10)
    self.key_loop()

  def getKey(self):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
  
  def key_loop(self):
    while True:
      key = self.getKey()

      if key == '\x03' or key == '\x71':  # ctr-c or q
        break

      ackermann_cmd_msg = AckermannDriveStamped()

      if key == "i":
        self.speed += 1.0
      elif key == "k":
        self.speed -= 1.0
      elif key == "j":
        self.steering_angle += 10.0
      elif key == "l":
        self.steering_angle -= 10.0
      elif key == "p":
        self.steering_angle = 0.0
        self.speed = 0.0

      ackermann_cmd_msg.drive.speed = self.speed
      ackermann_cmd_msg.drive.steering_angle = self.steering_angle
      self.pub.publish(ackermann_cmd_msg)

      print(key)

    self.finalize()

  def finalize(self):
    self.settings = termios.tcgetattr(sys.stdin)
    ackermann_cmd_msg = AckermannDriveStamped()
    ackermann_cmd_msg.drive.speed = 0.0
    ackermann_cmd_msg.drive.steering_angle = 0.0
    self.pub.publish(ackermann_cmd_msg)
    sys.exit()

def main():
  rclpy.init()
  node = Autocar_Teleop()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.destroy_node()

if __name__ == "__main__":
  main()