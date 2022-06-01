from time import time
from random import choices
import numpy as np
from metrics import *
from network import LocalNetworkInterface, Packet
from nodes.base import Node
from nodes.tiers import TiersNode
from nodes.flooding import FloodingNode
from nodes.bellman_ford import BellmanFordNode
from topo.ring import RingNetwork
from topo.star import StarNetwork
from topo.connected import ConnectedNetwork
from topo.mesh import MeshNetwork
from topo.er import ERNetwork
from topo.tiers import TiersNetwork, LocalAreaNetwork

# utility : create an image filename for network images
image_name = lambda: str(int(time())) + '.png'

def tiers ():
  net = TiersNetwork(T=3, NT=15, ET=8, ETT=4, S=8, NS=10, ES=5, L=20, NL=5)
  net.show(file=image_name())

  print(avg_hop_distance(net.graph))
  print(avg_weighted_distance(net.graph))
  print(hop_diameter(net.graph))
  print(weighted_diameter(net.graph))

def star ():
  n = 5
  nodes = [Node(i + 2) for i in range(n)]
  net = StarNetwork(Node(1), nodes)
  net.show(file='star.png')

def ring ():
  n = 10
  nodes = [Node(i + 1) for i in range(n)]
  net = RingNetwork(nodes)
  net.show(file='ring.png')

def connected ():
  n = 10
  nodes = [Node(i + 1) for i in range(n)]
  net = ConnectedNetwork(nodes)
  net.show(file='connected.png')

def mesh ():
  n = 10
  m = 3
  nodes = [Node(i + 1) for i in range(n)]
  net = MeshNetwork(nodes, m)
  net.show(file='mesh.png')

def er ():
  n = 20
  m = 80
  p = m / n / (n - 1) # m / (n 2)
  nodes = [Node(i + 1) for i in range(n)]
  net = ERNetwork(nodes, p)
  net.show(file='er.png')

def lan ():
  net = LocalAreaNetwork(8)
  net.show(file='lan.png')

def get_routable_net (Node):
  n = 20
  m = 30
  p = m / n / (n - 1) # m / (n 2)
  nodes = [Node(i + 1) for i in range(n)]
  # net = MeshNetwork(nodes, m)
  net = ERNetwork(nodes, p)

  for node in nodes:
    interface = LocalNetworkInterface(node, net)
    node.set_interface(interface)

  return net, nodes

def routing_flooding ():
  net, nodes = get_routable_net(FloodingNode)
  src, dst = choices(nodes, k=2)

  src.send_packet(Packet('hello world', src.addr, dst.addr))

  while len(dst.packets_received) == 0:
    net.routing_step()

  route = dst.packets_received[0].route
  edges = set((node1, node2) for node1, node2 in zip(route[:-1], route[1:]))
  def get_edge_color (node1, node2, weight):
    if (node1, node2) in edges or (node2, node1) in edges:
      return 'red'
    return 'black'

  net.show(file=image_name(), get_edge_color=get_edge_color)

def routing_bellman_ford ():
  net, nodes = get_routable_net(BellmanFordNode)

  for node in nodes:
    node.update_weights()

  for _ in range(50):
    for node in nodes:
      node.notify_neighbors()

  src, dst = choices(nodes, k=2)

  src.send_packet(Packet('hello world', src.addr, dst.addr))

  while len(dst.packets_received) == 0:
    net.routing_step()

  route = dst.packets_received[0].route
  edges = set((node1, node2) for node1, node2 in zip(route[:-1], route[1:]))
  def get_edge_color (node1, node2, weight):
    if (node1, node2) in edges or (node2, node1) in edges:
      return 'red'
    return 'black'

  net.show(file=image_name(), get_edge_color=get_edge_color)

# routing_bellman_ford()
# mesh()
# tiers()
# gene_net()
# er()
