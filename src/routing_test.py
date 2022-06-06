from time import time
from timeit import timeit
from random import choices
from math import sqrt
import networkx as nx
from network import LocalNetworkInterface, Packet
from nodes.flooding import FloodingNode
from nodes.bellman_ford import BellmanFordNode
from nodes.link_state import LinkStateNode
from topo.mesh import MeshNetwork
from topo.er import ERNetwork

def _get_routable_net (Node, n, p=None, m=None):
  nodes = [Node(i + 1) for i in range(n)]

  if m is not None:
    net = MeshNetwork(nodes, m)
  elif p is not None:
    net = ERNetwork(nodes, p)
  else:
    raise Exception('Expected p or m to be provided')

  for node in nodes:
    interface = LocalNetworkInterface(node, net)
    node.set_interface(interface)

  return net, nodes

def show_routing_graph (net, route, filename=None):
  edges = set((node1, node2) for node1, node2 in zip(route[:-1], route[1:]))

  def get_edge_color (node1, node2, weight):
    if (node1, node2) in edges or (node2, node1) in edges:
      return 'red'
    return 'black'

  net.show(file=filename, get_edge_color=get_edge_color)

def routing_test (NodeClass, init_func=None, n=20, p=None, m=None):
  t0 = time()

  net, nodes = _get_routable_net(NodeClass, n=n, p=p, m=m)
  t1 = time()

  if init_func:
    init_func(net, nodes)
  t2 = time()

  src, dst = choices(nodes, k=2)

  src.send_packet(Packet('hello world', src.addr, dst.addr))

  while len(dst.packets_received) == 0:
    net.routing_step()
  t3 = time()

  route = dst.packets_received[0].route

  return net, route, t0, t1, t2, t3

def routing_flooding (n=20):
  return routing_test(FloodingNode, n=n, m=2)

def init_bellman_ford (net, nodes):
  for node in nodes:
    node.update_weights()

  d = nx.diameter(net.graph)

  for _ in range(d + 2):
    for node in nodes:
      node.notify_neighbors()

def routing_bellman_ford (n=20):
  return routing_test(BellmanFordNode, init_bellman_ford, n=n, m=2)

def init_link_state (net, nodes):
  for node in nodes:
    node.update_graph_with_neighbors()

  d = nx.diameter(net.graph)

  for _ in range(d + 2):
    for node in nodes:
      node.notify_neighbors()

def routing_link_state (n=20):
  return routing_test(LinkStateNode, init_link_state, n=n, m=2)

def avgstd (data):
  n = len(data)
  s = sum(data)
  m = s / n
  e = sqrt(sum((x - m) ** 2 for x in data) / (n * (n - 1)))
  return m, e

def performace_test (func, n=20, k=50):
  network_size = n
  route_lengths, routers_hits, init_times, routing_times = [], [], [], []

  for i in range(k):
    net, route, t0, t1, t2, t3 = func(n)
    route_lengths.append(len(route))
    routers_hits.append(net.total_packet_count)
    init_times.append(1000 * (t2 - t0))
    routing_times.append(1000 * (t3 - t2))

  return (
    network_size,
    avgstd(route_lengths),
    avgstd(routers_hits),
    avgstd(init_times),
    avgstd(routing_times)
  )

def perf_on_size (n, k=50):
  return [
    performace_test(routing_flooding, n=n, k=k),
    performace_test(routing_bellman_ford, n=n, k=k),
    performace_test(routing_link_state, n=n, k=k)
  ]

if __name__ == '__main__':
  # print(perf_on_size(50, k=50))
  # print(perf_on_size(100, k=50))
  # print(perf_on_size(500, k=50))
  print('Done')
