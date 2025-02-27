# coding: UTF-8
import sys
bstack11l1lll_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack1ll1ll1_opy_ (bstack11lll11_opy_):
    global bstack1111l_opy_
    bstack11lll_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1llll1_opy_ = bstack11lll11_opy_ [:-1]
    bstack111l111_opy_ = bstack11lll_opy_ % len (bstack1llll1_opy_)
    bstack1llll1l_opy_ = bstack1llll1_opy_ [:bstack111l111_opy_] + bstack1llll1_opy_ [bstack111l111_opy_:]
    if bstack11l1lll_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1ll1111_opy_ + bstack11lll_opy_) % bstack1ll1lll_opy_) for bstack1ll1111_opy_, char in enumerate (bstack1llll1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1ll1111_opy_ + bstack11lll_opy_) % bstack1ll1lll_opy_) for bstack1ll1111_opy_, char in enumerate (bstack1llll1l_opy_)])
    return eval (bstack11ll111_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l11l1l111_opy_:
    def __init__(self):
        self._1ll1l111lll_opy_ = deque()
        self._1ll1l1l1111_opy_ = {}
        self._1ll1l111l1l_opy_ = False
    def bstack1ll1l11ll1l_opy_(self, test_name, bstack1ll1l1111ll_opy_):
        bstack1ll1l11l1ll_opy_ = self._1ll1l1l1111_opy_.get(test_name, {})
        return bstack1ll1l11l1ll_opy_.get(bstack1ll1l1111ll_opy_, 0)
    def bstack1ll1l11lll1_opy_(self, test_name, bstack1ll1l1111ll_opy_):
        bstack1ll1l111ll1_opy_ = self.bstack1ll1l11ll1l_opy_(test_name, bstack1ll1l1111ll_opy_)
        self.bstack1ll1l11l11l_opy_(test_name, bstack1ll1l1111ll_opy_)
        return bstack1ll1l111ll1_opy_
    def bstack1ll1l11l11l_opy_(self, test_name, bstack1ll1l1111ll_opy_):
        if test_name not in self._1ll1l1l1111_opy_:
            self._1ll1l1l1111_opy_[test_name] = {}
        bstack1ll1l11l1ll_opy_ = self._1ll1l1l1111_opy_[test_name]
        bstack1ll1l111ll1_opy_ = bstack1ll1l11l1ll_opy_.get(bstack1ll1l1111ll_opy_, 0)
        bstack1ll1l11l1ll_opy_[bstack1ll1l1111ll_opy_] = bstack1ll1l111ll1_opy_ + 1
    def bstack1l1ll1l1l1_opy_(self, bstack1ll1l11ll11_opy_, bstack1ll1l111l11_opy_):
        bstack1ll1l11llll_opy_ = self.bstack1ll1l11lll1_opy_(bstack1ll1l11ll11_opy_, bstack1ll1l111l11_opy_)
        event_name = bstack111111ll11_opy_[bstack1ll1l111l11_opy_]
        bstack1ll1l11l111_opy_ = bstack1ll1ll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᚥ").format(bstack1ll1l11ll11_opy_, event_name, bstack1ll1l11llll_opy_)
        self._1ll1l111lll_opy_.append(bstack1ll1l11l111_opy_)
    def bstack11lllll1_opy_(self):
        return len(self._1ll1l111lll_opy_) == 0
    def bstack1l1l1ll111_opy_(self):
        bstack1ll1l11l1l1_opy_ = self._1ll1l111lll_opy_.popleft()
        return bstack1ll1l11l1l1_opy_
    def capturing(self):
        return self._1ll1l111l1l_opy_
    def bstack1ll1111ll1_opy_(self):
        self._1ll1l111l1l_opy_ = True
    def bstack1l11l11l_opy_(self):
        self._1ll1l111l1l_opy_ = False