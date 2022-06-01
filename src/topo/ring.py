from network import NetworkGraph

class RingNetwork(NetworkGraph):
  def __init__(self, nodes):
    super().__init__()
    for node1, node2 in zip(nodes, nodes[1:] + [nodes[0]]):
      self.connect(node1, node2)
