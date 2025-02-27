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
import builtins
import logging
class bstack11l1ll11ll_opy_:
    def __init__(self, handler):
        self._1111l1l11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l1ll11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧႆ"), bstack1ll1ll1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩႇ"), bstack1ll1ll1_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬႈ"), bstack1ll1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫႉ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l1ll1l_opy_
        self._1111l1l1ll_opy_()
    def _1111l1ll1l_opy_(self, *args, **kwargs):
        self._1111l1l11l_opy_(*args, **kwargs)
        message = bstack1ll1ll1_opy_ (u"࠭ࠠࠨႊ").join(map(str, args)) + bstack1ll1ll1_opy_ (u"ࠧ࡝ࡰࠪႋ")
        self._log_message(bstack1ll1ll1_opy_ (u"ࠨࡋࡑࡊࡔ࠭ႌ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨႍ"): level, bstack1ll1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႎ"): msg})
    def _1111l1l1ll_opy_(self):
        for level, bstack1111l1lll1_opy_ in self._1111l1ll11_opy_.items():
            setattr(logging, level, self._1111l1l1l1_opy_(level, bstack1111l1lll1_opy_))
    def _1111l1l1l1_opy_(self, level, bstack1111l1lll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l1lll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111l1l11l_opy_
        for level, bstack1111l1lll1_opy_ in self._1111l1ll11_opy_.items():
            setattr(logging, level, bstack1111l1lll1_opy_)