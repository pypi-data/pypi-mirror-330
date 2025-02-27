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
import bstack_utils.bstack111l1llll1_opy_ as bstack1ll11ll1_opy_
from bstack_utils.helper import bstack1l1111l1l1_opy_
logger = logging.getLogger(__name__)
def bstack1l1lll1l1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack11l11ll11_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬၽ"), [])
    bstack1l111l11l_opy_ = bstack1ll11ll1_opy_.bstack1ll11l11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l111l11l_opy_
    try:
      bstack11llll1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll1l1_opy_(bstack1ll1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧၾ")) else context.browser
      if bstack11llll1l1l_opy_ and bstack11llll1l1l_opy_.session_id and bstack1l111l11l_opy_ and bstack1l1111l1l1_opy_(
              threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨၿ"), None):
          threading.current_thread().isA11yTest = bstack1ll11ll1_opy_.bstack1l1l1l1l1l_opy_(bstack11llll1l1l_opy_, bstack1l111l11l_opy_)
    except Exception as e:
       logger.debug(bstack1ll1ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪႀ").format(str(e)))
def bstack1l11ll1l1l_opy_(bstack11llll1l1l_opy_):
    if bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨႁ"), None) and bstack1l1111l1l1_opy_(
      threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫႂ"), None) and not bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩႃ"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll11ll1_opy_.bstack1ll1111l1l_opy_(bstack11llll1l1l_opy_, name=bstack1ll1ll1_opy_ (u"ࠢࠣႄ"), path=bstack1ll1ll1_opy_ (u"ࠣࠤႅ"))