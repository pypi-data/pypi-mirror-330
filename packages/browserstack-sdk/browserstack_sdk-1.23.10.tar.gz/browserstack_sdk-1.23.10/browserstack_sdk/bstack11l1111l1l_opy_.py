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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack111ll1l11l_opy_, bstack111ll11lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll1l11l_opy_ = bstack111ll1l11l_opy_
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l111l1l1_opy_(bstack111l1ll1ll_opy_):
        bstack111l1ll11l_opy_ = []
        if bstack111l1ll1ll_opy_:
            tokens = str(os.path.basename(bstack111l1ll1ll_opy_)).split(bstack1ll1ll1_opy_ (u"ࠤࡢࠦྭ"))
            camelcase_name = bstack1ll1ll1_opy_ (u"ࠥࠤࠧྮ").join(t.title() for t in tokens)
            suite_name, bstack111l1lll11_opy_ = os.path.splitext(camelcase_name)
            bstack111l1ll11l_opy_.append(suite_name)
        return bstack111l1ll11l_opy_
    @staticmethod
    def bstack111l1ll1l1_opy_(typename):
        if bstack1ll1ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢྯ") in typename:
            return bstack1ll1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨྰ")
        return bstack1ll1ll1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢྱ")