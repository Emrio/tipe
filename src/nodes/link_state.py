import networkx as nx
from nodes.routable import RoutableNode

class LinkStateNode(RoutableNode):
  def __init__ (self, addr):
    super().__init__(addr)

    self.graph = nx.Graph()
    self.neighbors = {}

  def update_graph_with_neighbors (self):
    for neighbor, weight in self.interface.get_neighbors_and_weights():
      self.graph.add_edge(self.addr, neighbor.addr, weight=weight)
      self.neighbors[neighbor.addr] = neighbor

  # sends routing table to adjacent nodes
  def notify_neighbors (self):
    for neighbor in self.interface.get_neighbors():
      neighbor._notify(self.graph)

  # internal method, called by adjacent nodes which send their graph
  # our graph table will be updated accordingly with new topology information
  def _notify (self, graph):
    for node1, node2, weight in graph.edges.data('weight', default=1):
      self.graph.add_edge(node1, node2, weight=weight)

  def _route_packet (self, packet, sender):
    try:
      dst = packet.dest_addr
      route = nx.dijkstra_path(self.graph, self.addr, dst, weight='weight')
      next_addr = route[1]
      next_node = self.neighbors[next_addr]
      self.interface.send_neighbor(next_node, packet)
    except nx.NetworkXNoPath as e:
      print(self, ':: No route to host')
