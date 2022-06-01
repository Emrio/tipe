from network import NetworkGraph

class ConnectedNetwork(NetworkGraph):
  def __init__(self, nodes):
    super().__init__()
    for node1 in nodes:
      for node2 in nodes:
        if node1 is not node2:
          self.connect(node1, node2)
