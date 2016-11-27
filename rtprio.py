from ctypes import CDLL, get_errno, c_ushort, Structure, pointer
from ctypes.util import find_library

from enum import Enum
from os import strerror
from sys import platform

plat = platform.lower()

if plat[:7] != 'freebsd' and plat[:12] != 'dragonflybsd':
	raise NotImplementedError("rtprio(2) is not implemented for '{}'".format(platform))

class rtprio_func(Enum):
	RTP_LOOKUP = 0
	RTP_SET = 1

class rtprio_prio(Enum):
	RTP_PRIO_MIN = 0
	RTP_PRIO_MAX = 31

class rtprio_types(Enum):
	RTP_PRIO_REALTIME = 2
	RTP_PRIO_NORMAL = 3
	RTP_PRIO_IDLE = 4

class rtprio_info(Structure):
	_fields_ = [("type", c_ushort), ("prio", c_ushort)]

libc = CDLL(find_library('c'), use_errno=True)

def rtprio(type = rtprio_types.RTP_PRIO_REALTIME, prio = None, pid = 0):
	func = rtprio_func.RTP_LOOKUP

	if prio is None:
		prio = 0
	else:
		func = rtprio_func.RTP_SET
		if isinstance(prio, rtprio_prio):
			prio = prio.value
	
	info = rtprio_info(type.value, prio)
	ret = libc.rtprio(func.value, pid, pointer(info))

	if ret != 0:
		raise OSError(get_errno(), strerror(get_errno()))

	return (rtprio_types(info.type), info.prio)
