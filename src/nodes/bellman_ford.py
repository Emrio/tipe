from nodes.base import Node

class BellmanFordNode(Node):
  def __init__ (self, addr):
    super().__init__(addr)
    self.weights = {}
    self.routing_table = {}

  # retrieve weights of edges and updates internal routing table with this
  # new information
  def update_weights (self):
    self.weights = dict(self.interface.get_neighbors_and_weights())

    for node, weight in self.weights.items():
      self.routing_table[node.addr] = (node, weight)

  # sends routing table to adjacent nodes
  def notify_neighbors (self):
    data = {
      node_addr: weight for node_addr, (_, weight) in self.routing_table.items()
    }

    for neighbor in self.interface.get_neighbors():
      neighbor._notify(data, self)

  # internal method, called by adjacent nodes which send their routing table
  # our routing table will be updated accordingly when better routes are
  # discovered
  def _notify (self, data, sender):
    edge_weight = self.weights[sender]
    table = self.routing_table

    for node_addr, weight in data.items():
      w = edge_weight + weight

      # address unregistered or better route
      if node_addr not in table or table[node_addr][1] > w:
        table[node_addr] = (sender, w)

  def _route_packet (self, packet, sender):
    dst = packet.dest_addr

    if dst not in self.routing_table:
      print(self, ':: No route to host')
      return

    direction, _ = self.routing_table[dst]
    self.interface.send_neighbor(direction, packet)
