from random import choice
from network import NetworkGraph

class MeshNetwork(NetworkGraph):
  def __init__(self, nodes, deg_target):
    super().__init__()

    # TODO: Ensure the graph is connex
    for node1 in nodes:
      for _ in range(deg_target):
        node2 = choice(list(filter(lambda x: x is not node1, nodes)))
        self.connect(node1, node2)
