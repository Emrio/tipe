from random import random
from network import NetworkGraph

# WARN: The resulting graph is not garanteed to be connex
class ERNetwork(NetworkGraph):
  def __init__(self, nodes, p):
    super().__init__()
    for node1 in nodes:
      for node2 in nodes:
        if node1 is not node2 and random() < p:
          self.connect(node1, node2)
