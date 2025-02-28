from slidge.util.test import SlidgeTest

import messlidger


class TestMesslidger(SlidgeTest):
    def test_base(self):
        self.recv("<presence />")
        reply = self.next_sent()
        assert reply["type"] == "error"
