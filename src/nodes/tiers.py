from nodes.base import Node

class TiersNode(Node):
  def __init__(self, addr, type):
    super().__init__(addr)
    self.type = type

  def _get_color (self):
    if self.type == 'wan':
      return 'pink'
    if self.type == 'man':
      return 'green'
    if self.type == 'lan-center':
      return 'teal'
    return 'cyan'
