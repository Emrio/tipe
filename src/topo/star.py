from network import NetworkGraph

class StarNetwork(NetworkGraph):
  def __init__(self, center_node, orbiting_nodes):
    super().__init__()
    self.center_node = center_node
    self.orbiting_nodes = orbiting_nodes

    for node in orbiting_nodes:
      self.connect(node, center_node)
