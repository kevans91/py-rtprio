import unittest
import rtprio
from os import getpid, getuid
#import sysctl

class FuncTests(unittest.TestCase):
	def call_rtprio(self, **kwargs):
		try:
			return rtprio.rtprio(**kwargs)
		except Exception as exc:
			self.fail(exc)
	
	def test_get_own(self):
		mine = self.call_rtprio()

		self.assertEqual(mine[0], rtprio.rtprio_types.RTP_PRIO_NORMAL)

			# This /could/ fail, but it is unlikely
			# The system scheduler would have to bump
			# our priority in between these two lookups
		also_mine = self.call_rtprio(pid=getpid())
		self.assertEqual(mine, also_mine)

	def test_get_other(self):
			# Get priority of init -
		other = self.call_rtprio(pid=1)

	def set_mine(self):
		base_priority = 6
		priority = base_priority
		kern_ignores_prioval = [rtprio.rtprio_types.RTP_PRIO_NORMAL]

		for rtprio_type in rtprio.rtprio_types:
				# Try changing it to the type requested
			res = self.call_rtprio(type=rtprio_type, prio=priority)
			self.assertEqual(res, (rtprio_type, priority))

				# Verify that it's changed
			cur_priority = self.call_rtprio()

			if rtprio_type not in kern_ignores_prioval:
				self.assertEqual(res, cur_priority)
			else:
				self.assertEqual(res[0], cur_priority[0])

			priority += 1	

	@unittest.skipIf(getuid() != 0, 'Set tests must be ran as root')
	def test_privileged_set_mine(self):
		self.set_mine()


if __name__ == '__main__':
	unittest.main()
