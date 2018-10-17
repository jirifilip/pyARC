import unittest

from pyarc.qcba.data_structures import Interval


class TestInterval(unittest.TestCase):

    def test_overlaps_with(self):
        i1 = Interval(3, 5, True, True)
        i2 = Interval(4, 4.5, True, True)

        i3 = Interval(4, 6, True, True)
        i4 = Interval(3, 4, True, True)

        i5 = Interval(6, 7, True, True)

        assert i2.overlaps_with(i1)
        assert i1.overlaps_with(i2)

        assert i1.overlaps_with(i3)
        assert i3.overlaps_with(i1)

        assert i1.overlaps_with(i4)
        assert i4.overlaps_with(i1)

        assert not i1.overlaps_with(i5)
        assert not i5.overlaps_with(i1)
