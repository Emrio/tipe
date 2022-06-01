import networkx as nx

def _get_shortest_paths (net):
  graph = net.graph
  paths = dict(nx.all_pairs_bellman_ford_path(graph, weight='weight'))
  return paths

def _map_nodes2 (net, f):
  paths = _get_shortest_paths(net)
  nodes = net.graph.nodes()
  return [f(paths[node1][node2]) for node2 in nodes() for node1 in nodes()]

def sum_along_path (net, path):
  return sum([net.graph.weight(x, y) for x, y in zip(path[:-2], path[1:])])

def avg_hop_distance (net):
  distances = _map_nodes2(net, len)
  return sum(distances) / len(distances)

def avg_weighted_distance (net):
  weighted_distances = _map_nodes2(net, lambda path: sum_along_path(net, path))

  return sum(weighted_distances) / len(weighted_distances)

def hop_diameter (net):
  return nx.diameter(net.graph)

def weighted_diameter (net):
  weighted_distances = _map_nodes2(net, lambda path: sum_along_path(net, path))

  return max(weighted_distances)
