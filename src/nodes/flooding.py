from nodes.base import Node

class FloodingNode(Node):
  def __init__ (self, addr):
    super().__init__(addr)

  def _route_packet (self, packet, sender):
    neighbors = self.interface.get_neighbors()
    recipients = filter(lambda n: n is not sender, neighbors)

    for recipient in recipients:
      self.interface.send_neighbor(recipient, packet)
