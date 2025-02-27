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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llll11l111_opy_, bstack11ll111ll_opy_, bstack1l1111l1l1_opy_, bstack1lll1lll1l_opy_, \
    bstack1llll1lll11_opy_
from bstack_utils.measure import measure
def bstack11llll11_opy_(bstack1ll111l1lll_opy_):
    for driver in bstack1ll111l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11ll1l1_opy_, stage=STAGE.SINGLE)
def bstack1l1ll111l_opy_(driver, status, reason=bstack1ll1ll1_opy_ (u"ࠨ᜕ࠩ")):
    bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
    if bstack11lll1lll_opy_.bstack111l1lllll_opy_():
        return
    bstack11ll111ll1_opy_ = bstack1lll1l1l11_opy_(bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᜖"), bstack1ll1ll1_opy_ (u"ࠪࠫ᜗"), status, reason, bstack1ll1ll1_opy_ (u"ࠫࠬ᜘"), bstack1ll1ll1_opy_ (u"ࠬ࠭᜙"))
    driver.execute_script(bstack11ll111ll1_opy_)
@measure(event_name=EVENTS.bstack1l11ll1l1_opy_, stage=STAGE.SINGLE)
def bstack11llllll1l_opy_(page, status, reason=bstack1ll1ll1_opy_ (u"࠭ࠧ᜚")):
    try:
        if page is None:
            return
        bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
        if bstack11lll1lll_opy_.bstack111l1lllll_opy_():
            return
        bstack11ll111ll1_opy_ = bstack1lll1l1l11_opy_(bstack1ll1ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ᜛"), bstack1ll1ll1_opy_ (u"ࠨࠩ᜜"), status, reason, bstack1ll1ll1_opy_ (u"ࠩࠪ᜝"), bstack1ll1ll1_opy_ (u"ࠪࠫ᜞"))
        page.evaluate(bstack1ll1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᜟ"), bstack11ll111ll1_opy_)
    except Exception as e:
        print(bstack1ll1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᜠ"), e)
def bstack1lll1l1l11_opy_(type, name, status, reason, bstack1l1l111111_opy_, bstack1l1lll11_opy_):
    bstack1l1111ll11_opy_ = {
        bstack1ll1ll1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᜡ"): type,
        bstack1ll1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜢ"): {}
    }
    if type == bstack1ll1ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᜣ"):
        bstack1l1111ll11_opy_[bstack1ll1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᜤ")][bstack1ll1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᜥ")] = bstack1l1l111111_opy_
        bstack1l1111ll11_opy_[bstack1ll1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᜦ")][bstack1ll1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪᜧ")] = json.dumps(str(bstack1l1lll11_opy_))
    if type == bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᜨ"):
        bstack1l1111ll11_opy_[bstack1ll1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜩ")][bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᜪ")] = name
    if type == bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᜫ"):
        bstack1l1111ll11_opy_[bstack1ll1ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᜬ")][bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᜭ")] = status
        if status == bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᜮ") and str(reason) != bstack1ll1ll1_opy_ (u"ࠨࠢᜯ"):
            bstack1l1111ll11_opy_[bstack1ll1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜰ")][bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᜱ")] = json.dumps(str(reason))
    bstack111l111ll_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᜲ").format(json.dumps(bstack1l1111ll11_opy_))
    return bstack111l111ll_opy_
def bstack1l1l111lll_opy_(url, config, logger, bstack1llllll11_opy_=False):
    hostname = bstack11ll111ll_opy_(url)
    is_private = bstack1lll1lll1l_opy_(hostname)
    try:
        if is_private or bstack1llllll11_opy_:
            file_path = bstack1llll11l111_opy_(bstack1ll1ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᜳ"), bstack1ll1ll1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰ᜴ࠪ"), logger)
            if os.environ.get(bstack1ll1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ᜵")) and eval(
                    os.environ.get(bstack1ll1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ᜶"))):
                return
            if (bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᜷") in config and not config[bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᜸")]):
                os.environ[bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ᜹")] = str(True)
                bstack1ll111l1l11_opy_ = {bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ᜺"): hostname}
                bstack1llll1lll11_opy_(bstack1ll1ll1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᜻"), bstack1ll1ll1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ᜼"), bstack1ll111l1l11_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1lll111_opy_(caps, bstack1ll111l1ll1_opy_):
    if bstack1ll1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᜽") in caps:
        caps[bstack1ll1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᜾")][bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ᜿")] = True
        if bstack1ll111l1ll1_opy_:
            caps[bstack1ll1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᝀ")][bstack1ll1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᝁ")] = bstack1ll111l1ll1_opy_
    else:
        caps[bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᝂ")] = True
        if bstack1ll111l1ll1_opy_:
            caps[bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᝃ")] = bstack1ll111l1ll1_opy_
def bstack1ll11l1l111_opy_(bstack11l11111l1_opy_):
    bstack1ll111l1l1l_opy_ = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᝄ"), bstack1ll1ll1_opy_ (u"ࠧࠨᝅ"))
    if bstack1ll111l1l1l_opy_ == bstack1ll1ll1_opy_ (u"ࠨࠩᝆ") or bstack1ll111l1l1l_opy_ == bstack1ll1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᝇ"):
        threading.current_thread().testStatus = bstack11l11111l1_opy_
    else:
        if bstack11l11111l1_opy_ == bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᝈ"):
            threading.current_thread().testStatus = bstack11l11111l1_opy_