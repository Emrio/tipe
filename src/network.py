from random import randint
import networkx as nx
import matplotlib.pyplot as plt

# base class for all networks
class NetworkGraph:
  def __init__ (self):
    self.graph = nx.Graph()
    self.total_packet_count = 0
    self.routing_iterator = iter([])

  def connect (self, node1, node2, weight=None):
    weight = weight if weight is not None else randint(1, 5)
    self.graph.add_edge(node1, node2, weight=weight)

  def show (self, get_edge_color=None, show_weight=False, file=None):
    if get_edge_color is None:
      get_edge_color = lambda _, __, ___: 'black'

    pos = nx.spring_layout(self.graph, iterations=100)

    color_map = [node._get_color() for node in self.graph]
    edge_color = [
      get_edge_color(node1, node2, self.weight(node1, node2))
      for node1, node2 in self.graph.edges()
    ]

    nx.draw(
        self.graph,
        pos,
        with_labels=True,
        node_color=color_map,
        edge_color=edge_color
    )

    # # bandwidth / weight / labelling stuff
    # edge_labels = nx.get_edge_attributes(self.graph, 'weight')
    # nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

    fig = plt.gcf()
    fig.set_size_inches(13, 8)

    if file:
      fig.savefig(file)

    plt.show()

  # test whether a node is linked to any other node
  def node_is_linked (self, node):
    return node in self.graph and len(self.graph.edges(node))

  # test wether two nodes are linked
  def nodes_are_linked (self, node1, node2):
    return self.graph.has_edge(node1, node2)

  # get the weight of a link given the two nodes
  def weight (self, node1, node2):
    if self.nodes_are_linked(node1, node2):
      return self.graph[node1][node2]['weight']
    return None

  # merge a network into this network
  def add (self, net):
    for node1, node2 in net.graph.edges():
      self.connect(node1, node2, weight=net.weight(node1, node2))

    # updating local network interfaces
    for node in net.graph.nodes():
      if node.interface is not None:
        node.interface.update_network(self)

  # execute one step of global packet routing
  def routing_step (self):
    node = next(self.routing_iterator, None)

    if node is None:
      nodes = filter(lambda n: len(n.packet_buffer) != 0, self.graph.nodes())
      nodes_list = list(nodes)
      if nodes_list == []:
        raise Exception('No route to host')
      self.routing_iterator = iter(nodes_list)
      return self.routing_step()

    node._update_buffer()

# python does not provide private properties and methods
# this class acts as a network abstraction for a node
class LocalNetworkInterface:
  def __init__ (self, node, network):
    self.node = node
    self.network = network

  def update_network (self, network):
    self.network = network

  def get_neighbors (self):
    if self.node not in self.network.graph:
      return []

    return self.network.graph.neighbors(self.node)

  def get_neighbors_and_weights (self):
    neighbors = self.get_neighbors()
    return [(node, self.network.weight(self.node, node)) for node in neighbors]

  def send_neighbor (self, node, packet):
    if node not in self.get_neighbors():
      raise Exception('Cannot send to this node : not my neighbor')

    # copying to avoid routers manipulating the same object (ttl, ...)
    # in some routing protocols like flooding
    new_packet = packet.copy()
    self.network.total_packet_count += 1

    node._on_receive_packet(new_packet, self.node)

class Packet:
  def __init__(self, data, src_addr, dest_addr, ttl=10, route=None):
    self.data = data
    self.ttl = ttl
    self.src_addr = src_addr
    self.dest_addr = dest_addr
    self.route = route if route is not None else []

  def is_dead (self):
    return self.ttl == 0

  def copy (self):
    route = self.route.copy()
    return Packet(self.data, self.src_addr, self.dest_addr, self.ttl, route)

  def add_node (self, node):
    self.route.append(node)
