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
import threading
from bstack_utils.helper import bstack11lll11111_opy_
from bstack_utils.constants import bstack11111l1lll_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1ll1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lllllll_opy_:
    bstack1ll111lll11_opy_ = None
    @classmethod
    def bstack1l111l1l_opy_(cls):
        if cls.on():
            logger.info(
                bstack1ll1ll1_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ᣂ").format(os.environ[bstack1ll1ll1_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᣃ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᣄ"), None) is None or os.environ[bstack1ll1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᣅ")] == bstack1ll1ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᣆ"):
            return False
        return True
    @classmethod
    def bstack1l1ll1lllll_opy_(cls, bs_config, framework=bstack1ll1ll1_opy_ (u"ࠣࠤᣇ")):
        bstack1111l11ll1_opy_ = False
        for fw in bstack11111l1lll_opy_:
            if fw in framework:
                bstack1111l11ll1_opy_ = True
        return bstack11lll11111_opy_(bs_config.get(bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᣈ"), bstack1111l11ll1_opy_))
    @classmethod
    def bstack1l1ll1l1l1l_opy_(cls, framework):
        return framework in bstack11111l1lll_opy_
    @classmethod
    def bstack1l1lll1l1l1_opy_(cls, bs_config, framework):
        return cls.bstack1l1ll1lllll_opy_(bs_config, framework) is True and cls.bstack1l1ll1l1l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᣉ"), None)
    @staticmethod
    def bstack11l1l11l11_opy_():
        if getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᣊ"), None):
            return {
                bstack1ll1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᣋ"): bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫᣌ"),
                bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᣍ"): getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᣎ"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᣏ"), None):
            return {
                bstack1ll1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᣐ"): bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᣑ"),
                bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᣒ"): getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᣓ"), None)
            }
        return None
    @staticmethod
    def bstack1l1ll1l1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lllllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l111l1l1_opy_(test, hook_name=None):
        bstack1l1ll1l111l_opy_ = test.parent
        if hook_name in [bstack1ll1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᣔ"), bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᣕ"), bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᣖ"), bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᣗ")]:
            bstack1l1ll1l111l_opy_ = test
        scope = []
        while bstack1l1ll1l111l_opy_ is not None:
            scope.append(bstack1l1ll1l111l_opy_.name)
            bstack1l1ll1l111l_opy_ = bstack1l1ll1l111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1ll1l11l1_opy_(hook_type):
        if hook_type == bstack1ll1ll1_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤᣘ"):
            return bstack1ll1ll1_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤᣙ")
        elif hook_type == bstack1ll1ll1_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥᣚ"):
            return bstack1ll1ll1_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢᣛ")
    @staticmethod
    def bstack1l1ll1l1l11_opy_(bstack1ll1l11111_opy_):
        try:
            if not bstack11lllllll_opy_.on():
                return bstack1ll1l11111_opy_
            if os.environ.get(bstack1ll1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨᣜ"), None) == bstack1ll1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᣝ"):
                tests = os.environ.get(bstack1ll1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢᣞ"), None)
                if tests is None or tests == bstack1ll1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᣟ"):
                    return bstack1ll1l11111_opy_
                bstack1ll1l11111_opy_ = tests.split(bstack1ll1ll1_opy_ (u"ࠬ࠲ࠧᣠ"))
                return bstack1ll1l11111_opy_
        except Exception as exc:
            logger.debug(bstack1l1ll1l11ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࡻࡴࡶࡵࠬࡪࡾࡣࠪࡿࠥᣡ"))
        return bstack1ll1l11111_opy_