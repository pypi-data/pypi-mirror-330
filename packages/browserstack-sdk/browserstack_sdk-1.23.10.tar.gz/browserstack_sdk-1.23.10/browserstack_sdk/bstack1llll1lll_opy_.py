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
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1l1l111_opy_ import bstack11l1l1l1l1_opy_, bstack11l1l111ll_opy_
from bstack_utils.bstack11l1l1l1ll_opy_ import bstack11lllllll_opy_
from bstack_utils.helper import bstack1l1111l1l1_opy_, bstack1lll11ll1l_opy_, Result
from bstack_utils.bstack11l1ll111l_opy_ import bstack1111l11l1_opy_
from bstack_utils.capture import bstack11l1ll11ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1llll1lll_opy_:
    def __init__(self):
        self.bstack11l1l11l1l_opy_ = bstack11l1ll11ll_opy_(self.bstack11l1ll1lll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1ll1lll_opy_(log):
        if not (log[bstack1ll1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๱")] and log[bstack1ll1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๲")].strip()):
            return
        active = bstack11lllllll_opy_.bstack11l1l11l11_opy_()
        log = {
            bstack1ll1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ๳"): log[bstack1ll1ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๴")],
            bstack1ll1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ๵"): bstack1lll11ll1l_opy_(),
            bstack1ll1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๶"): log[bstack1ll1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๷")],
        }
        if active:
            if active[bstack1ll1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭๸")] == bstack1ll1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ๹"):
                log[bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ๺")] = active[bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ๻")]
            elif active[bstack1ll1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ๼")] == bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ๽"):
                log[bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ๾")] = active[bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ๿")]
        bstack1111l11l1_opy_.bstack1l1l11ll1l_opy_([log])
    def start_test(self, attrs):
        bstack11l1ll1111_opy_ = uuid4().__str__()
        self.tests[bstack11l1ll1111_opy_] = {}
        self.bstack11l1l11l1l_opy_.start()
        driver = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ຀"), None)
        bstack11l1l1l111_opy_ = bstack11l1l111ll_opy_(
            name=attrs.scenario.name,
            uuid=bstack11l1ll1111_opy_,
            bstack11l1ll1l1l_opy_=bstack1lll11ll1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1ll1ll1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦກ"),
            framework=bstack1ll1ll1_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫຂ"),
            scope=[attrs.feature.name],
            bstack11l1l11lll_opy_=bstack1111l11l1_opy_.bstack11l1lll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11l1ll1111_opy_][bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ຃")] = bstack11l1l1l111_opy_
        threading.current_thread().current_test_uuid = bstack11l1ll1111_opy_
        bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧຄ"), bstack11l1l1l111_opy_)
    def end_test(self, attrs):
        bstack11l1l1111l_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ຅"): attrs.feature.name,
            bstack1ll1ll1_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨຆ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1l1l111_opy_ = self.tests[current_test_uuid][bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬງ")]
        meta = {
            bstack1ll1ll1_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦຈ"): bstack11l1l1111l_opy_,
            bstack1ll1ll1_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥຉ"): bstack11l1l1l111_opy_.meta.get(bstack1ll1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫຊ"), []),
            bstack1ll1ll1_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ຋"): {
                bstack1ll1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧຌ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1l1l111_opy_.bstack11l1ll1l11_opy_(meta)
        bstack11l1l1l111_opy_.bstack11l1l11111_opy_(bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ຍ"), []))
        bstack11l1ll1ll1_opy_, exception = self._11l1l1llll_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1l1ll11_opy_=[bstack11l1ll1ll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຎ")].stop(time=bstack1lll11ll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack11l1l1ll1l_opy_)
        bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬຏ"), self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຐ")])
    def bstack1l1111l1l_opy_(self, attrs):
        bstack11l1ll11l1_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠬ࡯ࡤࠨຑ"): uuid4().__str__(),
            bstack1ll1ll1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧຒ"): attrs.keyword,
            bstack1ll1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧຓ"): [],
            bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡼࡹ࠭ດ"): attrs.name,
            bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ຕ"): bstack1lll11ll1l_opy_(),
            bstack1ll1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪຖ"): bstack1ll1ll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬທ"),
            bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪຘ"): bstack1ll1ll1_opy_ (u"࠭ࠧນ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪບ")].add_step(bstack11l1ll11l1_opy_)
        threading.current_thread().current_step_uuid = bstack11l1ll11l1_opy_[bstack1ll1ll1_opy_ (u"ࠨ࡫ࡧࠫປ")]
    def bstack1ll11l1ll_opy_(self, attrs):
        current_test_id = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ຜ"), None)
        current_step_uuid = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧຝ"), None)
        bstack11l1ll1ll1_opy_, exception = self._11l1l1llll_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1l1ll11_opy_=[bstack11l1ll1ll1_opy_])
        self.tests[current_test_id][bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧພ")].bstack11l1l11ll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l1l1ll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1111l111_opy_(self, name, attrs):
        try:
            bstack11l1l1lll1_opy_ = uuid4().__str__()
            self.tests[bstack11l1l1lll1_opy_] = {}
            self.bstack11l1l11l1l_opy_.start()
            scopes = []
            driver = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫຟ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫຠ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1l1lll1_opy_)
            if name in [bstack1ll1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦມ"), bstack1ll1ll1_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦຢ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll1ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥຣ"), bstack1ll1ll1_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥ຤")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll1ll1_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬລ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1l1l1l1_opy_(
                name=name,
                uuid=bstack11l1l1lll1_opy_,
                bstack11l1ll1l1l_opy_=bstack1lll11ll1l_opy_(),
                file_path=file_path,
                framework=bstack1ll1ll1_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧ຦"),
                bstack11l1l11lll_opy_=bstack1111l11l1_opy_.bstack11l1lll1ll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll1ll1_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢວ"),
                hook_type=name
            )
            self.tests[bstack11l1l1lll1_opy_][bstack1ll1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥຨ")] = hook_data
            current_test_id = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧຩ"), None)
            if current_test_id:
                hook_data.bstack11l1lll111_opy_(current_test_id)
            if name == bstack1ll1ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨສ"):
                threading.current_thread().before_all_hook_uuid = bstack11l1l1lll1_opy_
            threading.current_thread().current_hook_uuid = bstack11l1l1lll1_opy_
            bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦຫ"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥຬ"), name, e)
    def bstack11111lll1_opy_(self, attrs):
        bstack11l1l1l11l_opy_ = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩອ"), None)
        hook_data = self.tests[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຮ")]
        status = bstack1ll1ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢຯ")
        exception = None
        bstack11l1ll1ll1_opy_ = None
        if hook_data.name == bstack1ll1ll1_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦະ"):
            self.bstack11l1l11l1l_opy_.reset()
            bstack11l1l111l1_opy_ = self.tests[bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩັ"), None)][bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭າ")].result.result
            if bstack11l1l111l1_opy_ == bstack1ll1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦຳ"):
                if attrs.hook_failures == 1:
                    status = bstack1ll1ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧິ")
                elif attrs.hook_failures == 2:
                    status = bstack1ll1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨີ")
            elif attrs.bstack11l1lll1l1_opy_:
                status = bstack1ll1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢຶ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬື") and attrs.hook_failures == 1:
                status = bstack1ll1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤຸ")
            elif hasattr(attrs, bstack1ll1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧູࠪ")) and attrs.error_message:
                status = bstack1ll1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧ຺ࠦ")
            bstack11l1ll1ll1_opy_, exception = self._11l1l1llll_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=status, exception=exception, bstack11l1l1ll11_opy_=[bstack11l1ll1ll1_opy_])
        hook_data.stop(time=bstack1lll11ll1l_opy_(), duration=0, result=bstack11l1l1ll1l_opy_)
        bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧົ"), self.tests[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຼ")])
        threading.current_thread().current_hook_uuid = None
    def _11l1l1llll_opy_(self, attrs):
        try:
            import traceback
            bstack11ll1lll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l1ll1ll1_opy_ = bstack11ll1lll1_opy_[-1] if bstack11ll1lll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦຽ"))
            bstack11l1ll1ll1_opy_ = None
            exception = None
        return bstack11l1ll1ll1_opy_, exception