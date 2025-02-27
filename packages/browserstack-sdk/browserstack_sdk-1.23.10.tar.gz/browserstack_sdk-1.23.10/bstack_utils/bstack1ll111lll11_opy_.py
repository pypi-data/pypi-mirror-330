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
import threading
import logging
logger = logging.getLogger(__name__)
bstack1ll111lll1l_opy_ = 1000
bstack1ll11l1111l_opy_ = 2
class bstack1ll11l11l11_opy_:
    def __init__(self, handler, bstack1ll11l11ll1_opy_=bstack1ll111lll1l_opy_, bstack1ll11l11l1l_opy_=bstack1ll11l1111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll11l11ll1_opy_ = bstack1ll11l11ll1_opy_
        self.bstack1ll11l11l1l_opy_ = bstack1ll11l11l1l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll11l11lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll11l11111_opy_()
    def bstack1ll11l11111_opy_(self):
        self.bstack1ll11l11lll_opy_ = threading.Event()
        def bstack1ll111lllll_opy_():
            self.bstack1ll11l11lll_opy_.wait(self.bstack1ll11l11l1l_opy_)
            if not self.bstack1ll11l11lll_opy_.is_set():
                self.bstack1ll11l111l1_opy_()
        self.timer = threading.Thread(target=bstack1ll111lllll_opy_, daemon=True)
        self.timer.start()
    def bstack1ll111llll1_opy_(self):
        try:
            if self.bstack1ll11l11lll_opy_ and not self.bstack1ll11l11lll_opy_.is_set():
                self.bstack1ll11l11lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll1ll1_opy_ (u"ࠨ࡝ࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࡷࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࠬᜎ") + (str(e) or bstack1ll1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡨࡵ࡮ࡷࡧࡵࡸࡪࡪࠠࡵࡱࠣࡷࡹࡸࡩ࡯ࡩࠥᜏ")))
        finally:
            self.timer = None
    def bstack1ll11l111ll_opy_(self):
        if self.timer:
            self.bstack1ll111llll1_opy_()
        self.bstack1ll11l11111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll11l11ll1_opy_:
                threading.Thread(target=self.bstack1ll11l111l1_opy_).start()
    def bstack1ll11l111l1_opy_(self, source = bstack1ll1ll1_opy_ (u"ࠪࠫᜐ")):
        with self.lock:
            if not self.queue:
                self.bstack1ll11l111ll_opy_()
                return
            data = self.queue[:self.bstack1ll11l11ll1_opy_]
            del self.queue[:self.bstack1ll11l11ll1_opy_]
        self.handler(data)
        if source != bstack1ll1ll1_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᜑ"):
            self.bstack1ll11l111ll_opy_()
    def shutdown(self):
        self.bstack1ll111llll1_opy_()
        while self.queue:
            self.bstack1ll11l111l1_opy_(source=bstack1ll1ll1_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᜒ"))