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
class bstack1ll111l1_opy_:
    def __init__(self, handler):
        self._1ll111ll1ll_opy_ = None
        self.handler = handler
        self._1ll111ll111_opy_ = self.bstack1ll111ll11l_opy_()
        self.patch()
    def patch(self):
        self._1ll111ll1ll_opy_ = self._1ll111ll111_opy_.execute
        self._1ll111ll111_opy_.execute = self.bstack1ll111ll1l1_opy_()
    def bstack1ll111ll1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᜓ"), driver_command, None, this, args)
            response = self._1ll111ll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1ll1_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ᜔"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll111ll111_opy_.execute = self._1ll111ll1ll_opy_
    @staticmethod
    def bstack1ll111ll11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver