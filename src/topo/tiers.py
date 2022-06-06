from random import choice, shuffle, randint
from numpy.random import normal
from network import NetworkGraph
from nodes.tiers import TiersNode
from topo.mesh import MeshNetwork
from topo.star import StarNetwork

# fast list.remove
def pop2 (lst, i):
  lst[i], lst[-1] = lst[-1], lst[i]
  return lst.pop()

# control address attribution
class TiersNodeFactory:
  def __init__ (self, network, addr_start=0):
    self.addr_count = addr_start
    self.network = network

  def make_node (self, type):
    self.addr_count += 1
    return TiersNode(self.addr_count, type)

class TiersNetwork(NetworkGraph):
  def __init__(self, T=1, NT=1, ET=2, ETT=1, S=1, NS=1, ES=2, L=1, NL=1):
    super().__init__()
    self.T = T # nbr of transit domains
    self.NT = NT # avg nbr of nodes per transit domain
    self.ET = ET # nbr of edges within transit domains
    self.ETT = ETT # nbr of edges between transit domains
    self.S = S # nbr of stub domains
    self.NS = NS # avg nbr of nodes per stub domains
    self.ES = ES # nbr of edges within stub domains
    self.L = L # nbr of LANs
    self.NL = NL # avg nbr of nodes per LAN

    self.factory = TiersNodeFactory(self)

    self._generate()

  # strategy: generate individual WANs, MANs, and LANs
  # afterwards, connect and merge networks in order to
  # obtain a single connex network
  def _generate (self):
    make_node = self.factory.make_node

    T = self.T
    print('T =', T)

    NT, ET = self.NT, self.ET
    self.wans = []
    for _ in range(T):
      self.wans.append(WideAreaNetwork(NT, ET, make_node))

    S = self.S
    print('S =', S)
    NS, ES = self.NS, self.ES
    self.mans = []
    for _ in range(S):
      self.mans.append(MetropolitanAreaNetwork(NS, ES, make_node))

    L = self.L
    print('L =', L)

    NL = self.NL
    self.lans = []
    for _ in range(L):
      self.lans.append(LocalAreaNetwork(NL, make_node))

    for lan in self.lans:
      lan_node = lan.center

      man = choice(self.mans)
      man_node = choice(man.nodes)

      man.add(lan)
      man.connect(lan_node, man_node)

    for man in self.mans:
      man_node = choice(man.nodes)

      wan = choice(self.wans)
      wan_node = choice(wan.nodes)

      wan.add(man)
      wan.connect(man_node, wan_node)

    # making a connex component
    subnets = self.wans.copy()
    while len(subnets) > 1:
      i1 = randint(0, len(subnets) - 1)
      wan1 = pop2(subnets, i1)

      i2 = randint(0, len(subnets) - 1)
      wan2 = pop2(subnets, i2)

      node1 = choice(wan1.nodes)
      node2 = choice(wan2.nodes)

      wan1.add(wan2)
      wan1.connect(node1, node2)

      subnets.append(wan1)

    self.add(subnets[0])

    # satisfying ETT
    wans = self.wans.copy()
    remaining = self.ETT - len(wans)
    for _ in range(remaining):
      wan1 = choice(wans)
      wan2 = choice(wans)

      if wan1 is wan2:
        continue

      node1 = choice(wan1.nodes)
      node2 = choice(wan2.nodes)

      self.connect(node1, node2)

# WAN and MAN base
class MeshPartNetwork(MeshNetwork):
  def __init__ (self, type, n, m, make_node):
    self.nodes = [make_node(type=type) for _ in range(n)]
    self.type = type
    super().__init__(self.nodes, m)

# WAN
class WideAreaNetwork(MeshPartNetwork):
  def __init__(self, n, m, make_node):
    super().__init__('wan', n, m, make_node)

# MAN
class MetropolitanAreaNetwork(MeshPartNetwork):
  def __init__(self, n, m, make_node):
    super().__init__('man', n, m, make_node)

# LAN
class LocalAreaNetwork(StarNetwork):
  def __init__(self, node_count, make_node):
    self.center = make_node(type='lan-center')
    nodes = [make_node(type='lan') for _ in range(node_count - 1)]
    super().__init__(self.center, nodes)
