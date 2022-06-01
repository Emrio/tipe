from network import LocalNetworkInterface

# base class for all nodes
class Node:
  def __init__ (self, addr):
    self.addr = addr
    self.interface = None
    self.packet_buffer = []
    self.packets_received = []

  def __repr__ (self):
    return 'Node #' + str(self.addr)

  def __str__ (self):
    return str(self.addr)

  def __hash__ (self):
    return self.addr

  # can be called by the network or the node factory to change the interface
  # used especially during network merge operations
  def set_interface (self, interface):
    self.interface = interface

  def _route_packet (self, packet, sender):
    # INFO: routing logic goes here
    # INFO: override this method to implement a routing strategy
    raise Exception('No routing algorithm')

  # this method is called by the network to indicate the router that it can
  # process its packet buffer
  # at that point, all buffer times are decremented and suitable packets
  # are routed
  def _update_buffer (self):
    def filter_buffer (b):
      packet, sender, buffer_time = b
      if buffer_time > 0:
        return True
      self._route_packet(packet, sender)
      return False

    self.packet_buffer = list(filter(filter_buffer, self.packet_buffer))

    for b in self.packet_buffer:
      b[2] -= 1

  # internal method called when receiving a packet
  # this method is called before the _route_packet method
  # it implements TTL and reception of packets intended to this node
  def _on_receive_packet (self, packet, sender):
    packet.add_node(self)

    if packet.dest_addr == self.addr:
      self.packets_received.append(packet)
      print(self, ':: received packet:', packet.data, packet.route)
      return

    packet.ttl -= 1

    if packet.is_dead():
      return

    if sender is None:
      buffer_time = 0
    else:
      buffer_time = self.interface.network.graph.weight(sender, self)

    self.packet_buffer.append([packet, sender, buffer_time])

  # public method to send a packet through the network beginning at this router
  def send_packet (self, packet):
    self._on_receive_packet(packet, sender=None)

  # used by NetworkGraph to give a color to the node
  def _get_color (self):
    return 'gray'
