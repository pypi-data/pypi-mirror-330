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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111l1l1l1l_opy_, bstack1llll11l1_opy_, get_host_info, bstack1lllllll1l1_opy_, \
 bstack1lll1l11_opy_, bstack1l1111l1l1_opy_, bstack11l111111l_opy_, bstack1llll11lll1_opy_, bstack1lll11ll1l_opy_
import bstack_utils.bstack111l1llll1_opy_ as bstack1ll11ll1_opy_
from bstack_utils.bstack11l1l1l1ll_opy_ import bstack11lllllll_opy_
from bstack_utils.percy import bstack1l1l1111_opy_
from bstack_utils.config import Config
bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l1111_opy_()
@bstack11l111111l_opy_(class_method=False)
def bstack1l1lll1l1ll_opy_(bs_config, bstack11llll1l_opy_):
  try:
    data = {
        bstack1ll1ll1_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᢄ"): bstack1ll1ll1_opy_ (u"ࠬࡰࡳࡰࡰࠪᢅ"),
        bstack1ll1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᢆ"): bs_config.get(bstack1ll1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᢇ"), bstack1ll1ll1_opy_ (u"ࠨࠩᢈ")),
        bstack1ll1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢉ"): bs_config.get(bstack1ll1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᢊ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢋ"): bs_config.get(bstack1ll1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢌ")),
        bstack1ll1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᢍ"): bs_config.get(bstack1ll1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᢎ"), bstack1ll1ll1_opy_ (u"ࠨࠩᢏ")),
        bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᢐ"): bstack1lll11ll1l_opy_(),
        bstack1ll1ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢑ"): bstack1lllllll1l1_opy_(bs_config),
        bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᢒ"): get_host_info(),
        bstack1ll1ll1_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᢓ"): bstack1llll11l1_opy_(),
        bstack1ll1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᢔ"): os.environ.get(bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᢕ")),
        bstack1ll1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᢖ"): os.environ.get(bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᢗ"), False),
        bstack1ll1ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᢘ"): bstack111l1l1l1l_opy_(),
        bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᢙ"): bstack1l1ll1l1lll_opy_(),
        bstack1ll1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩᢚ"): bstack1l1ll1ll111_opy_(bstack11llll1l_opy_),
        bstack1ll1ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᢛ"): bstack1llll1lll1_opy_(bs_config, bstack11llll1l_opy_.get(bstack1ll1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᢜ"), bstack1ll1ll1_opy_ (u"ࠨࠩᢝ"))),
        bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᢞ"): bstack1lll1l11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦᢟ").format(str(error)))
    return None
def bstack1l1ll1ll111_opy_(framework):
  return {
    bstack1ll1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᢠ"): framework.get(bstack1ll1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᢡ"), bstack1ll1ll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᢢ")),
    bstack1ll1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᢣ"): framework.get(bstack1ll1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᢤ")),
    bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢥ"): framework.get(bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᢦ")),
    bstack1ll1ll1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᢧ"): bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᢨ"),
    bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰᢩ࠭"): framework.get(bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᢪ"))
  }
def bstack1llll1lll1_opy_(bs_config, framework):
  bstack1l1l1l1l1_opy_ = False
  bstack1ll1llllll_opy_ = False
  bstack1l1ll1ll1l1_opy_ = False
  if bstack1ll1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᢫") in bs_config:
    bstack1l1ll1ll1l1_opy_ = True
  elif bstack1ll1ll1_opy_ (u"ࠩࡤࡴࡵ࠭᢬") in bs_config:
    bstack1l1l1l1l1_opy_ = True
  else:
    bstack1ll1llllll_opy_ = True
  bstack1111111l_opy_ = {
    bstack1ll1ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᢭"): bstack11lllllll_opy_.bstack1l1ll1lllll_opy_(bs_config, framework),
    bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᢮"): bstack1ll11ll1_opy_.bstack111l1l111l_opy_(bs_config),
    bstack1ll1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᢯"): bs_config.get(bstack1ll1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᢰ"), False),
    bstack1ll1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᢱ"): bstack1ll1llllll_opy_,
    bstack1ll1ll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᢲ"): bstack1l1l1l1l1_opy_,
    bstack1ll1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᢳ"): bstack1l1ll1ll1l1_opy_
  }
  return bstack1111111l_opy_
@bstack11l111111l_opy_(class_method=False)
def bstack1l1ll1l1lll_opy_():
  try:
    bstack1l1ll1lll11_opy_ = json.loads(os.getenv(bstack1ll1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᢴ"), bstack1ll1ll1_opy_ (u"ࠫࢀࢃࠧᢵ")))
    return {
        bstack1ll1ll1_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᢶ"): bstack1l1ll1lll11_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧᢷ").format(str(error)))
    return {}
def bstack1l1llllll11_opy_(array, bstack1l1ll1ll1ll_opy_, bstack1l1lll11111_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1ll1ll1ll_opy_]
    result[key] = o[bstack1l1lll11111_opy_]
  return result
def bstack1l1lll11lll_opy_(bstack111ll111l_opy_=bstack1ll1ll1_opy_ (u"ࠧࠨᢸ")):
  bstack1l1lll1111l_opy_ = bstack1ll11ll1_opy_.on()
  bstack1l1ll1lll1l_opy_ = bstack11lllllll_opy_.on()
  bstack1l1ll1ll11l_opy_ = percy.bstack1l1lll1ll_opy_()
  if bstack1l1ll1ll11l_opy_ and not bstack1l1ll1lll1l_opy_ and not bstack1l1lll1111l_opy_:
    return bstack111ll111l_opy_ not in [bstack1ll1ll1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᢹ"), bstack1ll1ll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᢺ")]
  elif bstack1l1lll1111l_opy_ and not bstack1l1ll1lll1l_opy_:
    return bstack111ll111l_opy_ not in [bstack1ll1ll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᢻ"), bstack1ll1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᢼ"), bstack1ll1ll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᢽ")]
  return bstack1l1lll1111l_opy_ or bstack1l1ll1lll1l_opy_ or bstack1l1ll1ll11l_opy_
@bstack11l111111l_opy_(class_method=False)
def bstack1l1lllll1ll_opy_(bstack111ll111l_opy_, test=None):
  bstack1l1ll1llll1_opy_ = bstack1ll11ll1_opy_.on()
  if not bstack1l1ll1llll1_opy_ or bstack111ll111l_opy_ not in [bstack1ll1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᢾ")] or test == None:
    return None
  return {
    bstack1ll1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᢿ"): bstack1l1ll1llll1_opy_ and bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᣀ"), None) == True and bstack1ll11ll1_opy_.bstack1ll11l11ll_opy_(test[bstack1ll1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᣁ")])
  }