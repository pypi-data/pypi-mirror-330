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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1ll1l1l_opy_ import get_logger
from bstack_utils.bstack1ll1lll1_opy_ import bstack111l111ll1_opy_
bstack1ll1lll1_opy_ = bstack111l111ll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l111ll1_opy_: Optional[str] = None):
    bstack1ll1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᗦ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack111l11l11l_opy_: str = bstack1ll1lll1_opy_.bstack1111llll11_opy_(label)
            start_mark: str = label + bstack1ll1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᗧ")
            end_mark: str = label + bstack1ll1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᗨ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll11l11_opy_.value:
                    bstack1ll1lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll1lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l111ll1_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = bstack111l11l11l_opy_ + bstack1ll1ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᗩ")
                    end_mark: str = bstack111l11l11l_opy_ + bstack1ll1ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᗪ")
                    bstack1ll1lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll1lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l111ll1_opy_)
            except Exception as e:
                bstack1ll1lll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l111ll1_opy_)
            return result
        return wrapper
    return decorator