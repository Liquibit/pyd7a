import struct

from enum import Enum

from d7a.phy.channel_id import ChannelID
from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.phy.channel_header import ChannelHeader,ChannelCoding,ChannelClass,ChannelBand

class EngineeringModeMode(Enum):
  ENGINEERING_MODE_MODE_OFF = 0
  ENGINEERING_MODE_MODE_CONT_TX = 1
  ENGINEERING_MODE_MODE_TRANSIENT_TX = 2
  ENGINEERING_MODE_MODE_PER_RX = 3
  ENGINEERING_MODE_MODE_PER_TX = 4

  @staticmethod
  def from_string(s):
    if s == "OFF": return EngineeringModeMode.ENGINEERING_MODE_MODE_OFF
    if s == "CONT_TX": return EngineeringModeMode.ENGINEERING_MODE_MODE_CONT_TX
    if s == "TRANSIENT_TX": return EngineeringModeMode.ENGINEERING_MODE_MODE_TRANSIENT_TX
    if s == "PER_RX": return EngineeringModeMode.ENGINEERING_MODE_MODE_PER_RX
    if s == "PER_TX": return EngineeringModeMode.ENGINEERING_MODE_MODE_PER_TX

    raise NotImplementedError

  def __str__(self):
    if self.value == EngineeringModeMode.ENGINEERING_MODE_MODE_OFF: return "OFF"
    if self.value == EngineeringModeMode.ENGINEERING_MODE_MODE_CONT_TX: return "CONT_TX"
    if self.value == EngineeringModeMode.ENGINEERING_MODE_MODE_TRANSIENT_TX: return "TRANSIENT_TX"
    if self.value == EngineeringModeMode.ENGINEERING_MODE_MODE_PER_RX: return "PER_RX"
    if self.value == EngineeringModeMode.ENGINEERING_MODE_MODE_PER_TX: return "PER_TX"

class EngineeringModeFile(File, Validatable):

  SCHEMA = [{
    "mode": Types.ENUM(EngineeringModeMode),
    "flags": Types.INTEGER(min=0, max=255),
    "timeout": Types.INTEGER(min=0, max=255),
    "channel_id": Types.OBJECT(ChannelID),
    "eirp": Types.INTEGER(min=-128, max=127)
  }]

  def __init__(self, mode=EngineeringModeMode.ENGINEERING_MODE_MODE_OFF, flags=0, timeout=0,
               channel_id=ChannelID(channel_header=ChannelHeader(ChannelCoding.PN9,ChannelClass.LO_RATE,ChannelBand.BAND_868),
                                    channel_index=0),
               eirp=0):
    self.mode = mode
    self.flags = flags
    self.timeout = timeout
    self.channel_id = channel_id
    self.eirp = eirp
    File.__init__(self, SystemFileIds.ENGINEERING_MODE, 9)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    mode = EngineeringModeMode(int(s.read("uint:8")))
    flags = s.read("uint:8")
    timeout = s.read("uint:8")
    channel_id= ChannelID.parse(s)
    eirp = s.read("int:8")
    return EngineeringModeFile(mode=mode, flags=flags, timeout=timeout, channel_id=channel_id, eirp=eirp)

  def __iter__(self):
    yield int(self.mode.value)
    yield self.flags
    yield self.timeout
    for byte in self.channel_id:
      yield byte
    yield self.eirp
    yield 0
    yield 0

  def __str__(self):
    return "mode={}, flags={}, timeout={}, channel_id={{{}}}, eirp={}".format(self.mode, hex(self.flags),self.timeout, self.channel_id, self.eirp)