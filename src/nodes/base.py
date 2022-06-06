from network import LocalNetworkInterface

# base class for all nodes
class Node:
  def __init__ (self, addr):
    self.addr = addr
    self.interface = None

  def __repr__ (self):
    return 'Node #' + str(self.addr)

  def __str__ (self):
    return str(self.addr)

  def __hash__ (self):
    return self.addr

  # used by NetworkGraph to give a color to the node
  def _get_color (self):
    return 'gray'
