import unittest
import rtprio

class ImplTests(unittest.TestCase):
	def test_libc(self):
		self.assertIsNotNone(rtprio.libc)	

	def test_exists(self):
		self.assertTrue(rtprio.rtprio_exists())

if __name__ == '__main__':
	unittest.main()
