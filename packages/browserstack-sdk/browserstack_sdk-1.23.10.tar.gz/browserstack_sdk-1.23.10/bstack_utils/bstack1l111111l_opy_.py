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
from browserstack_sdk.bstack11llll1ll1_opy_ import bstack11ll11lll_opy_
from browserstack_sdk.bstack11l1111l1l_opy_ import RobotHandler
def bstack1ll1l11ll1_opy_(framework):
    if framework.lower() == bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᎛"):
        return bstack11ll11lll_opy_.version()
    elif framework.lower() == bstack1ll1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ᎜"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ᎝"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1ll1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫ᎞")
def bstack1lllll11l1_opy_():
    import bstack1111111lll_opy_
    framework_name=[]
    bstack111111l111_opy_=[]
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭᎟"))
        bstack111111l111_opy_.append(bstack1111111lll_opy_.bstack111111l11l_opy_(bstack1ll1ll1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᎠ")).version)
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1ll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᎡ"))
        bstack111111l111_opy_.append(bstack1111111lll_opy_.bstack111111l11l_opy_(bstack1ll1ll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᎢ")).version)
    except:
        pass
    return {
        bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꭳ"): bstack1ll1ll1_opy_ (u"ࠩࡢࠫᎤ").join(framework_name),
        bstack1ll1ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᎥ"): bstack1ll1ll1_opy_ (u"ࠫࡤ࠭Ꭶ").join(bstack111111l111_opy_)
    }