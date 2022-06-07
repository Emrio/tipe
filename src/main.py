from time import time
from random import choices
from network import LocalNetworkInterface, Packet
from routing_test import show_routing_graph, routing_test, init_bellman_ford, init_link_state
from nodes.base import Node
from nodes.tiers import TiersNode
from nodes.flooding import FloodingNode
from nodes.bellman_ford import BellmanFordNode
from nodes.link_state import LinkStateNode
from topo.ring import RingNetwork
from topo.star import StarNetwork
from topo.connected import ConnectedNetwork
from topo.mesh import MeshNetwork
from topo.er import ERNetwork
from topo.tiers import TiersNetwork, LocalAreaNetwork

# utility : create an image filename for network images
image_name = lambda: str(int(time())) + '.png'

def tiers ():
  net = TiersNetwork(T=3, NT=15, ET=8, ETT=5, S=8, NS=10, ES=5, L=20, NL=5)
  net.show(file=image_name())

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

def routing_flooding ():
  net, route, *_ = routing_test(FloodingNode, n=20, m=2)
  show_routing_graph(net, route)

def routing_bellman_ford ():
  net, route, *_ = routing_test(BellmanFordNode, init_bellman_ford, n=20, m=2)
  show_routing_graph(net, route)

def routing_link_state ():
  net, route, *_ = routing_test(LinkStateNode, init_link_state, n=20, m=2)
  show_routing_graph(net, route)

# er()
tiers()
# mesh()
# routing_flooding()
# routing_bellman_ford()
# routing_link_state()
