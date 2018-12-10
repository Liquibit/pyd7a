import struct

from d7a.support.schema import Validatable, Types


class LoRaWANInterfaceConfigurationABP(Validatable):

  SCHEMA = [{
    # # TODO first byte is extensible with other fields, for example ADR or SFx
    # "request_ack": Types.BOOLEAN(),
    # "application_port": Types.BYTE(),
    # "netw_session_key": Types.BYTES(),
    # "app_session_key": Types.BYTES(),
    # "dev_addr": Types.BYTES(),
    # "netw_id": Types.BYTES(),
  }]

  def __init__(self, request_ack, app_port, netw_session_key, app_session_key, dev_addr, netw_id):
    self.request_ack = request_ack
    self.app_port = app_port
    self.netw_session_key = netw_session_key
    self.app_session_key = app_session_key
    self.dev_addr = dev_addr
    self.netw_id = netw_id
    super(LoRaWANInterfaceConfigurationABP, self).__init__()

  def __iter__(self):
    byte = 0
    if self.request_ack:
      byte |= 1 << 1

    yield byte
    yield self.app_port
    for byte in self.netw_session_key:
      yield byte

    for byte in self.app_session_key:
      yield byte

    for byte in bytearray(struct.pack(">I", self.dev_addr)):
      yield byte

    for byte in bytearray(struct.pack(">I", self.netw_id)):
      yield byte

  def __str__(self):
    return str(self.as_dict())

  @staticmethod
  def parse(s):
    _rfu = s.read("bits:6")
    request_ack = s.read("bool")
    _rfu = s.read("bits:1")
    app_port = s.read("uint:8")

    netw_session_key = s.read("bytes:16")
    app_session_key = s.read("bytes:16")
    dev_addr = s.read("uint:32")
    netw_id = s.read("uint:32")

    return LoRaWANInterfaceConfigurationABP(
      request_ack=request_ack,
      app_port=app_port,
      netw_session_key=netw_session_key,
      app_session_key=app_session_key,
      dev_addr=dev_addr,
      netw_id=netw_id,
    )


