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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll1lll1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll1ll1ll1_opy_, bstack11l1ll111_opy_, update, bstack1l11lllll1_opy_,
                                       bstack1ll111111_opy_, bstack111llllll_opy_, bstack1llll1l1ll_opy_, bstack1l1l1ll11_opy_,
                                       bstack1l111l1l1l_opy_, bstack1l1ll1lll1_opy_, bstack11ll1ll1l_opy_, bstack1l11lll111_opy_,
                                       bstack111ll11ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l111l_opy_)
from browserstack_sdk.bstack11llll1ll1_opy_ import bstack11ll11lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1ll1l1l_opy_
from bstack_utils.capture import bstack11l1ll11ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l11l1l1l1_opy_, bstack1111llll_opy_, bstack11ll1l1l_opy_, \
    bstack1l11l111_opy_
from bstack_utils.helper import bstack1l1111l1l1_opy_, bstack1llll11ll11_opy_, bstack11l11ll1ll_opy_, bstack11l11l1l_opy_, bstack1lll1lll1l1_opy_, bstack1lll11ll1l_opy_, \
    bstack1llll111l1l_opy_, \
    bstack1llll111111_opy_, bstack11ll11l111_opy_, bstack1ll1lll1l_opy_, bstack1lllllllll1_opy_, bstack1l111ll1l_opy_, Notset, \
    bstack1l1l1l1ll_opy_, bstack1llll1l1l1l_opy_, bstack1llll11l1l1_opy_, Result, bstack1llll111lll_opy_, bstack1lll1llll11_opy_, bstack11l111111l_opy_, \
    bstack111l1l11_opy_, bstack1l1l1lll1l_opy_, bstack11lll11111_opy_, bstack11111111ll_opy_
from bstack_utils.bstack1lll1l1ll11_opy_ import bstack1lll1l1l1l1_opy_
from bstack_utils.messages import bstack1l11l1l1_opy_, bstack1llllll1l_opy_, bstack1l1111ll_opy_, bstack1111ll1l1_opy_, bstack11l11111_opy_, \
    bstack1l1lll1l_opy_, bstack1l11ll111l_opy_, bstack1l1111ll1l_opy_, bstack1l1lllllll_opy_, bstack1ll1ll11_opy_, \
    bstack1l1llll1ll_opy_, bstack11l1l11l_opy_
from bstack_utils.proxy import bstack1ll1ll1111_opy_, bstack11l11llll_opy_
from bstack_utils.bstack1ll11l1l11_opy_ import bstack1ll11l1llll_opy_, bstack1ll11ll1l11_opy_, bstack1ll11l1l1ll_opy_, bstack1ll11l1l1l1_opy_, \
    bstack1ll11l1ll11_opy_, bstack1ll11l1lll1_opy_, bstack1ll11ll1111_opy_, bstack11ll1l11l1_opy_, bstack1ll11ll1l1l_opy_
from bstack_utils.bstack11ll111111_opy_ import bstack1ll111l1_opy_
from bstack_utils.bstack1111l1111_opy_ import bstack1lll1l1l11_opy_, bstack1l1l111lll_opy_, bstack1ll1lll111_opy_, \
    bstack1l1ll111l_opy_, bstack11llllll1l_opy_
from bstack_utils.bstack11l1l1l111_opy_ import bstack11l1l111ll_opy_
from bstack_utils.bstack11l1l1l1ll_opy_ import bstack11lllllll_opy_
import bstack_utils.bstack111l1llll1_opy_ as bstack1ll11ll1_opy_
from bstack_utils.bstack11l1ll111l_opy_ import bstack1111l11l1_opy_
from bstack_utils.bstack1ll1l1llll_opy_ import bstack1ll1l1llll_opy_
from browserstack_sdk.__init__ import bstack11lll111l1_opy_
bstack111l11lll_opy_ = None
bstack1l11ll11ll_opy_ = None
bstack11llllll_opy_ = None
bstack11lll1ll_opy_ = None
bstack1l1lllll11_opy_ = None
bstack1l11lll1l_opy_ = None
bstack1lll1l111l_opy_ = None
bstack1111lllll_opy_ = None
bstack1l11llll11_opy_ = None
bstack11l1llll1_opy_ = None
bstack1l11l11ll1_opy_ = None
bstack1l1l1l11l1_opy_ = None
bstack11ll1111l_opy_ = None
bstack1llll1l11_opy_ = bstack1ll1ll1_opy_ (u"ࠧࠨᣢ")
CONFIG = {}
bstack1l1ll1ll11_opy_ = False
bstack1l11111ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠨࠩᣣ")
bstack11l1l1lll_opy_ = bstack1ll1ll1_opy_ (u"ࠩࠪᣤ")
bstack1l1l1111l1_opy_ = False
bstack11ll11ll1l_opy_ = []
bstack1l1l11l1l_opy_ = bstack1l11l1l1l1_opy_
bstack1l1ll111lll_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᣥ")
bstack11lll1ll1l_opy_ = {}
bstack1lll11llll_opy_ = None
bstack1lllll11ll_opy_ = False
logger = bstack1l1ll1l1l_opy_.get_logger(__name__, bstack1l1l11l1l_opy_)
store = {
    bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᣦ"): []
}
bstack1l1ll11111l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l11l11ll_opy_ = {}
current_test_uuid = None
def bstack11111llll_opy_(page, bstack11ll11111l_opy_):
    try:
        page.evaluate(bstack1ll1ll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᣧ"),
                      bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᣨ") + json.dumps(
                          bstack11ll11111l_opy_) + bstack1ll1ll1_opy_ (u"ࠢࡾࡿࠥᣩ"))
    except Exception as e:
        print(bstack1ll1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᣪ"), e)
def bstack11lllll1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1ll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᣫ"), bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨᣬ") + json.dumps(
            message) + bstack1ll1ll1_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧᣭ") + json.dumps(level) + bstack1ll1ll1_opy_ (u"ࠬࢃࡽࠨᣮ"))
    except Exception as e:
        print(bstack1ll1ll1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤᣯ"), e)
def pytest_configure(config):
    bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
    config.args = bstack11lllllll_opy_.bstack1l1ll1l1l11_opy_(config.args)
    bstack11lll1lll_opy_.bstack1l11ll1l_opy_(bstack11lll11111_opy_(config.getoption(bstack1ll1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᣰ"))))
    try:
        bstack1l1ll1l1l_opy_.bstack1lll11l111l_opy_(config.inipath, config.rootpath)
    except:
        pass
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l1l1lllll1_opy_ = item.config.getoption(bstack1ll1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᣱ"))
    plugins = item.config.getoption(bstack1ll1ll1_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᣲ"))
    report = outcome.get_result()
    bstack1l1l1lll11l_opy_(item, call, report)
    if bstack1ll1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᣳ") not in plugins or bstack1l111ll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1ll1_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᣴ"), None)
    page = getattr(item, bstack1ll1ll1_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᣵ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1l1ll11llll_opy_(item, report, summary, bstack1l1l1lllll1_opy_)
    if (page is not None):
        bstack1l1ll11l11l_opy_(item, report, summary, bstack1l1l1lllll1_opy_)
def bstack1l1ll11llll_opy_(item, report, summary, bstack1l1l1lllll1_opy_):
    if report.when == bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ᣶") and report.skipped:
        bstack1ll11ll1l1l_opy_(report)
    if report.when in [bstack1ll1ll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ᣷"), bstack1ll1ll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ᣸")]:
        return
    if not bstack1lll1lll1l1_opy_():
        return
    try:
        if (str(bstack1l1l1lllll1_opy_).lower() != bstack1ll1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᣹")):
            item._driver.execute_script(
                bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ᣺") + json.dumps(
                    report.nodeid) + bstack1ll1ll1_opy_ (u"ࠫࢂࢃࠧ᣻"))
        os.environ[bstack1ll1ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ᣼")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨ᣽").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1ll1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ᣾")))
    bstack1l1l1lll_opy_ = bstack1ll1ll1_opy_ (u"ࠣࠤ᣿")
    bstack1ll11ll1l1l_opy_(report)
    if not passed:
        try:
            bstack1l1l1lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᤀ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1ll1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᤁ")))
        bstack1l1l1lll_opy_ = bstack1ll1ll1_opy_ (u"ࠦࠧᤂ")
        if not passed:
            try:
                bstack1l1l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1ll1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᤃ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᤄ")
                    + json.dumps(bstack1ll1ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᤅ"))
                    + bstack1ll1ll1_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᤆ")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᤇ")
                    + json.dumps(str(bstack1l1l1lll_opy_))
                    + bstack1ll1ll1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᤈ")
                )
        except Exception as e:
            summary.append(bstack1ll1ll1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᤉ").format(e))
def bstack1l1ll1l1111_opy_(test_name, error_message):
    try:
        bstack1l1ll111l11_opy_ = []
        bstack1l1ll1l1_opy_ = os.environ.get(bstack1ll1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᤊ"), bstack1ll1ll1_opy_ (u"࠭࠰ࠨᤋ"))
        bstack1l111l11ll_opy_ = {bstack1ll1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᤌ"): test_name, bstack1ll1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᤍ"): error_message, bstack1ll1ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᤎ"): bstack1l1ll1l1_opy_}
        bstack1l1ll11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll1_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᤏ"))
        if os.path.exists(bstack1l1ll11ll11_opy_):
            with open(bstack1l1ll11ll11_opy_) as f:
                bstack1l1ll111l11_opy_ = json.load(f)
        bstack1l1ll111l11_opy_.append(bstack1l111l11ll_opy_)
        with open(bstack1l1ll11ll11_opy_, bstack1ll1ll1_opy_ (u"ࠫࡼ࠭ᤐ")) as f:
            json.dump(bstack1l1ll111l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᤑ") + str(e))
def bstack1l1ll11l11l_opy_(item, report, summary, bstack1l1l1lllll1_opy_):
    if report.when in [bstack1ll1ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᤒ"), bstack1ll1ll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᤓ")]:
        return
    if (str(bstack1l1l1lllll1_opy_).lower() != bstack1ll1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᤔ")):
        bstack11111llll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1ll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᤕ")))
    bstack1l1l1lll_opy_ = bstack1ll1ll1_opy_ (u"ࠥࠦᤖ")
    bstack1ll11ll1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1ll1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᤗ").format(e)
                )
        try:
            if passed:
                bstack11llllll1l_opy_(getattr(item, bstack1ll1ll1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᤘ"), None), bstack1ll1ll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᤙ"))
            else:
                error_message = bstack1ll1ll1_opy_ (u"ࠧࠨᤚ")
                if bstack1l1l1lll_opy_:
                    bstack11lllll1l1_opy_(item._page, str(bstack1l1l1lll_opy_), bstack1ll1ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᤛ"))
                    bstack11llllll1l_opy_(getattr(item, bstack1ll1ll1_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᤜ"), None), bstack1ll1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᤝ"), str(bstack1l1l1lll_opy_))
                    error_message = str(bstack1l1l1lll_opy_)
                else:
                    bstack11llllll1l_opy_(getattr(item, bstack1ll1ll1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᤞ"), None), bstack1ll1ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᤟"))
                bstack1l1ll1l1111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᤠ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1ll1ll1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᤡ"), default=bstack1ll1ll1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᤢ"), help=bstack1ll1ll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᤣ"))
    parser.addoption(bstack1ll1ll1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᤤ"), default=bstack1ll1ll1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᤥ"), help=bstack1ll1ll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᤦ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1ll1_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᤧ"), action=bstack1ll1ll1_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᤨ"), default=bstack1ll1ll1_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᤩ"),
                         help=bstack1ll1ll1_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᤪ"))
def bstack11l1ll1lll_opy_(log):
    if not (log[bstack1ll1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᤫ")] and log[bstack1ll1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᤬")].strip()):
        return
    active = bstack11l1l11l11_opy_()
    log = {
        bstack1ll1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᤭"): log[bstack1ll1ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᤮")],
        bstack1ll1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᤯"): bstack11l11ll1ll_opy_().isoformat() + bstack1ll1ll1_opy_ (u"ࠨ࡜ࠪᤰ"),
        bstack1ll1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᤱ"): log[bstack1ll1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᤲ")],
    }
    if active:
        if active[bstack1ll1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᤳ")] == bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᤴ"):
            log[bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤵ")] = active[bstack1ll1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᤶ")]
        elif active[bstack1ll1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᤷ")] == bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺࠧᤸ"):
            log[bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ᤹ࠪ")] = active[bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᤺")]
    bstack1111l11l1_opy_.bstack1l1l11ll1l_opy_([log])
def bstack11l1l11l11_opy_():
    if len(store[bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥ᤻ࠩ")]) > 0 and store[bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ᤼")][-1]:
        return {
            bstack1ll1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ᤽"): bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭᤾"),
            bstack1ll1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᤿"): store[bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ᥀")][-1]
        }
    if store.get(bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ᥁"), None):
        return {
            bstack1ll1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ᥂"): bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ᥃"),
            bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᥄"): store[bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ᥅")]
        }
    return None
bstack11l1l11l1l_opy_ = bstack11l1ll11ll_opy_(bstack11l1ll1lll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1l1ll1111l1_opy_ = True
        bstack1l111l11l_opy_ = bstack1ll11ll1_opy_.bstack1ll11l11ll_opy_(bstack1llll111111_opy_(item.own_markers))
        item._a11y_test_case = bstack1l111l11l_opy_
        if bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᥆"), None):
            driver = getattr(item, bstack1ll1ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᥇"), None)
            item._a11y_started = bstack1ll11ll1_opy_.bstack1l1l1l1l1l_opy_(driver, bstack1l111l11l_opy_)
        if not bstack1111l11l1_opy_.on() or bstack1l1ll111lll_opy_ != bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᥈"):
            return
        global current_test_uuid, bstack11l1l11l1l_opy_
        bstack11l1l11l1l_opy_.start()
        bstack111llll111_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ᥉"): uuid4().__str__(),
            bstack1ll1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᥊"): bstack11l11ll1ll_opy_().isoformat() + bstack1ll1ll1_opy_ (u"࡛ࠧࠩ᥋")
        }
        current_test_uuid = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᥌")]
        store[bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᥍")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᥎")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l11l11ll_opy_[item.nodeid] = {**_11l11l11ll_opy_[item.nodeid], **bstack111llll111_opy_}
        bstack1l1l1lll1l1_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1ll1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᥏"))
    except Exception as err:
        print(bstack1ll1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᥐ"), str(err))
def pytest_runtest_setup(item):
    global bstack1l1ll11111l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1lllllllll1_opy_():
        atexit.register(bstack11llll11_opy_)
        if not bstack1l1ll11111l_opy_:
            try:
                bstack1l1ll111l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11111111ll_opy_():
                    bstack1l1ll111l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1ll111l1l_opy_:
                    signal.signal(s, bstack1l1l1ll1ll1_opy_)
                bstack1l1ll11111l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢᥑ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll11l1llll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᥒ")
    try:
        if not bstack1111l11l1_opy_.on():
            return
        bstack11l1l11l1l_opy_.start()
        uuid = uuid4().__str__()
        bstack111llll111_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᥓ"): uuid,
            bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᥔ"): bstack11l11ll1ll_opy_().isoformat() + bstack1ll1ll1_opy_ (u"ࠪ࡞ࠬᥕ"),
            bstack1ll1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᥖ"): bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᥗ"),
            bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᥘ"): bstack1ll1ll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᥙ"),
            bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᥚ"): bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᥛ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᥜ")] = item
        store[bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᥝ")] = [uuid]
        if not _11l11l11ll_opy_.get(item.nodeid, None):
            _11l11l11ll_opy_[item.nodeid] = {bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᥞ"): [], bstack1ll1ll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᥟ"): []}
        _11l11l11ll_opy_[item.nodeid][bstack1ll1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᥠ")].append(bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᥡ")])
        _11l11l11ll_opy_[item.nodeid + bstack1ll1ll1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᥢ")] = bstack111llll111_opy_
        bstack1l1l1ll1l11_opy_(item, bstack111llll111_opy_, bstack1ll1ll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᥣ"))
    except Exception as err:
        print(bstack1ll1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᥤ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11lll1ll1l_opy_
        bstack1l1ll1l1_opy_ = 0
        if bstack1l1l1111l1_opy_ is True:
            bstack1l1ll1l1_opy_ = int(os.environ.get(bstack1ll1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᥥ")))
        if bstack1l1l1111_opy_.bstack1l1lll1ll_opy_() == bstack1ll1ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦᥦ"):
            if bstack1l1l1111_opy_.bstack1l1l1ll1ll_opy_() == bstack1ll1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᥧ"):
                bstack1l1l1llllll_opy_ = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᥨ"), None)
                bstack1ll1ll1lll_opy_ = bstack1l1l1llllll_opy_ + bstack1ll1ll1_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᥩ")
                driver = getattr(item, bstack1ll1ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᥪ"), None)
                bstack11lllll11_opy_ = getattr(item, bstack1ll1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᥫ"), None)
                bstack11ll111l11_opy_ = getattr(item, bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᥬ"), None)
                PercySDK.screenshot(driver, bstack1ll1ll1lll_opy_, bstack11lllll11_opy_=bstack11lllll11_opy_, bstack11ll111l11_opy_=bstack11ll111l11_opy_, bstack1ll111111l_opy_=bstack1l1ll1l1_opy_)
        if getattr(item, bstack1ll1ll1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᥭ"), False):
            bstack11ll11lll_opy_.bstack1l11l1lll_opy_(getattr(item, bstack1ll1ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᥮"), None), bstack11lll1ll1l_opy_, logger, item)
        if not bstack1111l11l1_opy_.on():
            return
        bstack111llll111_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᥯"): uuid4().__str__(),
            bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᥰ"): bstack11l11ll1ll_opy_().isoformat() + bstack1ll1ll1_opy_ (u"ࠪ࡞ࠬᥱ"),
            bstack1ll1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᥲ"): bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᥳ"),
            bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᥴ"): bstack1ll1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ᥵"),
            bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ᥶"): bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ᥷")
        }
        _11l11l11ll_opy_[item.nodeid + bstack1ll1ll1_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭᥸")] = bstack111llll111_opy_
        bstack1l1l1ll1l11_opy_(item, bstack111llll111_opy_, bstack1ll1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᥹"))
    except Exception as err:
        print(bstack1ll1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ᥺"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1111l11l1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll11l1l1l1_opy_(fixturedef.argname):
        store[bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ᥻")] = request.node
    elif bstack1ll11l1ll11_opy_(fixturedef.argname):
        store[bstack1ll1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ᥼")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭᥽"): fixturedef.argname,
            bstack1ll1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᥾"): bstack1llll111l1l_opy_(outcome),
            bstack1ll1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ᥿"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᦀ")]
        if not _11l11l11ll_opy_.get(current_test_item.nodeid, None):
            _11l11l11ll_opy_[current_test_item.nodeid] = {bstack1ll1ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᦁ"): []}
        _11l11l11ll_opy_[current_test_item.nodeid][bstack1ll1ll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᦂ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᦃ"), str(err))
if bstack1l111ll1l_opy_() and bstack1111l11l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l11l11ll_opy_[request.node.nodeid][bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᦄ")].bstack1l1111l1l_opy_(id(step))
        except Exception as err:
            print(bstack1ll1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᦅ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l11l11ll_opy_[request.node.nodeid][bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᦆ")].bstack11l1l11ll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᦇ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11l1l1l111_opy_: bstack11l1l111ll_opy_ = _11l11l11ll_opy_[request.node.nodeid][bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᦈ")]
            bstack11l1l1l111_opy_.bstack11l1l11ll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᦉ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1ll111lll_opy_
        try:
            if not bstack1111l11l1_opy_.on() or bstack1l1ll111lll_opy_ != bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᦊ"):
                return
            global bstack11l1l11l1l_opy_
            bstack11l1l11l1l_opy_.start()
            driver = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᦋ"), None)
            if not _11l11l11ll_opy_.get(request.node.nodeid, None):
                _11l11l11ll_opy_[request.node.nodeid] = {}
            bstack11l1l1l111_opy_ = bstack11l1l111ll_opy_.bstack1ll111l1111_opy_(
                scenario, feature, request.node,
                name=bstack1ll11l1lll1_opy_(request.node, scenario),
                bstack11l1ll1l1l_opy_=bstack1lll11ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᦌ"),
                tags=bstack1ll11ll1111_opy_(feature, scenario),
                bstack11l1l11lll_opy_=bstack1111l11l1_opy_.bstack11l1lll1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _11l11l11ll_opy_[request.node.nodeid][bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᦍ")] = bstack11l1l1l111_opy_
            bstack1l1ll111111_opy_(bstack11l1l1l111_opy_.uuid)
            bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᦎ"), bstack11l1l1l111_opy_)
        except Exception as err:
            print(bstack1ll1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᦏ"), str(err))
def bstack1l1l1lll111_opy_(bstack11l1l1lll1_opy_):
    if bstack11l1l1lll1_opy_ in store[bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᦐ")]:
        store[bstack1ll1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᦑ")].remove(bstack11l1l1lll1_opy_)
def bstack1l1ll111111_opy_(bstack11l1ll1111_opy_):
    store[bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᦒ")] = bstack11l1ll1111_opy_
    threading.current_thread().current_test_uuid = bstack11l1ll1111_opy_
@bstack1111l11l1_opy_.bstack1l1lll111ll_opy_
def bstack1l1l1lll11l_opy_(item, call, report):
    logger.debug(bstack1ll1ll1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫᦓ"))
    global bstack1l1ll111lll_opy_
    bstack1llll11l1l_opy_ = bstack1lll11ll1l_opy_()
    if hasattr(report, bstack1ll1ll1_opy_ (u"ࠪࡷࡹࡵࡰࠨᦔ")):
        bstack1llll11l1l_opy_ = bstack1llll111lll_opy_(report.stop)
    elif hasattr(report, bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᦕ")):
        bstack1llll11l1l_opy_ = bstack1llll111lll_opy_(report.start)
    try:
        if getattr(report, bstack1ll1ll1_opy_ (u"ࠬࡽࡨࡦࡰࠪᦖ"), bstack1ll1ll1_opy_ (u"࠭ࠧᦗ")) == bstack1ll1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᦘ"):
            bstack11l1l11l1l_opy_.reset()
        if getattr(report, bstack1ll1ll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᦙ"), bstack1ll1ll1_opy_ (u"ࠩࠪᦚ")) == bstack1ll1ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᦛ"):
            logger.debug(bstack1ll1ll1_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭ᦜ").format(getattr(report, bstack1ll1ll1_opy_ (u"ࠬࡽࡨࡦࡰࠪᦝ"), bstack1ll1ll1_opy_ (u"࠭ࠧᦞ")).__str__(), bstack1l1ll111lll_opy_))
            if bstack1l1ll111lll_opy_ == bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᦟ"):
                _11l11l11ll_opy_[item.nodeid][bstack1ll1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᦠ")] = bstack1llll11l1l_opy_
                bstack1l1l1lll1l1_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1ll1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᦡ"), report, call)
                store[bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᦢ")] = None
            elif bstack1l1ll111lll_opy_ == bstack1ll1ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᦣ"):
                bstack11l1l1l111_opy_ = _11l11l11ll_opy_[item.nodeid][bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᦤ")]
                bstack11l1l1l111_opy_.set(hooks=_11l11l11ll_opy_[item.nodeid].get(bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᦥ"), []))
                exception, bstack11l1l1ll11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1l1ll11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭ᦦ"), bstack1ll1ll1_opy_ (u"ࠨࠩᦧ"))]
                bstack11l1l1l111_opy_.stop(time=bstack1llll11l1l_opy_, result=Result(result=getattr(report, bstack1ll1ll1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᦨ"), bstack1ll1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᦩ")), exception=exception, bstack11l1l1ll11_opy_=bstack11l1l1ll11_opy_))
                bstack1111l11l1_opy_.bstack11l1lll11l_opy_(bstack1ll1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᦪ"), _11l11l11ll_opy_[item.nodeid][bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᦫ")])
        elif getattr(report, bstack1ll1ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫ᦬"), bstack1ll1ll1_opy_ (u"ࠧࠨ᦭")) in [bstack1ll1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ᦮"), bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ᦯")]:
            logger.debug(bstack1ll1ll1_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬᦰ").format(getattr(report, bstack1ll1ll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᦱ"), bstack1ll1ll1_opy_ (u"ࠬ࠭ᦲ")).__str__(), bstack1l1ll111lll_opy_))
            bstack11l1l1l11l_opy_ = item.nodeid + bstack1ll1ll1_opy_ (u"࠭࠭ࠨᦳ") + getattr(report, bstack1ll1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᦴ"), bstack1ll1ll1_opy_ (u"ࠨࠩᦵ"))
            if getattr(report, bstack1ll1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᦶ"), False):
                hook_type = bstack1ll1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᦷ") if getattr(report, bstack1ll1ll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᦸ"), bstack1ll1ll1_opy_ (u"ࠬ࠭ᦹ")) == bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᦺ") else bstack1ll1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᦻ")
                _11l11l11ll_opy_[bstack11l1l1l11l_opy_] = {
                    bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦼ"): uuid4().__str__(),
                    bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᦽ"): bstack1llll11l1l_opy_,
                    bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᦾ"): hook_type
                }
            _11l11l11ll_opy_[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦿ")] = bstack1llll11l1l_opy_
            bstack1l1l1lll111_opy_(_11l11l11ll_opy_[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᧀ")])
            bstack1l1l1ll1l11_opy_(item, _11l11l11ll_opy_[bstack11l1l1l11l_opy_], bstack1ll1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᧁ"), report, call)
            if getattr(report, bstack1ll1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᧂ"), bstack1ll1ll1_opy_ (u"ࠨࠩᧃ")) == bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᧄ"):
                if getattr(report, bstack1ll1ll1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫᧅ"), bstack1ll1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᧆ")) == bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᧇ"):
                    bstack111llll111_opy_ = {
                        bstack1ll1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᧈ"): uuid4().__str__(),
                        bstack1ll1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᧉ"): bstack1lll11ll1l_opy_(),
                        bstack1ll1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᧊"): bstack1lll11ll1l_opy_()
                    }
                    _11l11l11ll_opy_[item.nodeid] = {**_11l11l11ll_opy_[item.nodeid], **bstack111llll111_opy_}
                    bstack1l1l1lll1l1_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1ll1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᧋"))
                    bstack1l1l1lll1l1_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1ll1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᧌"), report, call)
    except Exception as err:
        print(bstack1ll1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ᧍"), str(err))
def bstack1l1l1llll1l_opy_(test, bstack111llll111_opy_, result=None, call=None, bstack111ll111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1l1l111_opy_ = {
        bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ᧎"): bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᧏")],
        bstack1ll1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ᧐"): bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭᧑"),
        bstack1ll1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᧒"): test.name,
        bstack1ll1ll1_opy_ (u"ࠪࡦࡴࡪࡹࠨ᧓"): {
            bstack1ll1ll1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ᧔"): bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᧕"),
            bstack1ll1ll1_opy_ (u"࠭ࡣࡰࡦࡨࠫ᧖"): inspect.getsource(test.obj)
        },
        bstack1ll1ll1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᧗"): test.name,
        bstack1ll1ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ᧘"): test.name,
        bstack1ll1ll1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ᧙"): bstack11lllllll_opy_.bstack11l111l1l1_opy_(test),
        bstack1ll1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭᧚"): file_path,
        bstack1ll1ll1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭᧛"): file_path,
        bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᧜"): bstack1ll1ll1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ᧝"),
        bstack1ll1ll1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ᧞"): file_path,
        bstack1ll1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᧟"): bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᧠")],
        bstack1ll1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭᧡"): bstack1ll1ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ᧢"),
        bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ᧣"): {
            bstack1ll1ll1_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ᧤"): test.nodeid
        },
        bstack1ll1ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬ᧥"): bstack1llll111111_opy_(test.own_markers)
    }
    if bstack111ll111l_opy_ in [bstack1ll1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ᧦"), bstack1ll1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᧧")]:
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠪࡱࡪࡺࡡࠨ᧨")] = {
            bstack1ll1ll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭᧩"): bstack111llll111_opy_.get(bstack1ll1ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ᧪"), [])
        }
    if bstack111ll111l_opy_ == bstack1ll1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ᧫"):
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᧬")] = bstack1ll1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᧭")
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᧮")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᧯")]
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᧰")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᧱")]
    if result:
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᧲")] = result.outcome
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ᧳")] = result.duration * 1000
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᧴")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᧵")]
        if result.failed:
            bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ᧶")] = bstack1111l11l1_opy_.bstack111l1ll1l1_opy_(call.excinfo.typename)
            bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᧷")] = bstack1111l11l1_opy_.bstack1l1lll1l11l_opy_(call.excinfo, result)
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᧸")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᧹")]
    if outcome:
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᧺")] = bstack1llll111l1l_opy_(outcome)
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᧻")] = 0
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᧼")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᧽")]
        if bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᧾")] == bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᧿"):
            bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᨀ")] = bstack1ll1ll1_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᨁ")  # bstack1l1ll11l111_opy_
            bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᨂ")] = [{bstack1ll1ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᨃ"): [bstack1ll1ll1_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᨄ")]}]
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᨅ")] = bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᨆ")]
    return bstack11l1l1l111_opy_
def bstack1l1ll11lll1_opy_(test, bstack11l11lllll_opy_, bstack111ll111l_opy_, result, call, outcome, bstack1l1ll11l1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᨇ")]
    hook_name = bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᨈ")]
    hook_data = {
        bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᨉ"): bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᨊ")],
        bstack1ll1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᨋ"): bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᨌ"),
        bstack1ll1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᨍ"): bstack1ll1ll1_opy_ (u"࠭ࡻࡾࠩᨎ").format(bstack1ll11ll1l11_opy_(hook_name)),
        bstack1ll1ll1_opy_ (u"ࠧࡣࡱࡧࡽࠬᨏ"): {
            bstack1ll1ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᨐ"): bstack1ll1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᨑ"),
            bstack1ll1ll1_opy_ (u"ࠪࡧࡴࡪࡥࠨᨒ"): None
        },
        bstack1ll1ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᨓ"): test.name,
        bstack1ll1ll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᨔ"): bstack11lllllll_opy_.bstack11l111l1l1_opy_(test, hook_name),
        bstack1ll1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᨕ"): file_path,
        bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᨖ"): file_path,
        bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᨗ"): bstack1ll1ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩᨘࠪ"),
        bstack1ll1ll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᨙ"): file_path,
        bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᨚ"): bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᨛ")],
        bstack1ll1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᨜"): bstack1ll1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ᨝") if bstack1l1ll111lll_opy_ == bstack1ll1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ᨞") else bstack1ll1ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ᨟"),
        bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᨠ"): hook_type
    }
    bstack1ll1111lll1_opy_ = bstack111lll111l_opy_(_11l11l11ll_opy_.get(test.nodeid, None))
    if bstack1ll1111lll1_opy_:
        hook_data[bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᨡ")] = bstack1ll1111lll1_opy_
    if result:
        hook_data[bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᨢ")] = result.outcome
        hook_data[bstack1ll1ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᨣ")] = result.duration * 1000
        hook_data[bstack1ll1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᨤ")] = bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᨥ")]
        if result.failed:
            hook_data[bstack1ll1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᨦ")] = bstack1111l11l1_opy_.bstack111l1ll1l1_opy_(call.excinfo.typename)
            hook_data[bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᨧ")] = bstack1111l11l1_opy_.bstack1l1lll1l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᨨ")] = bstack1llll111l1l_opy_(outcome)
        hook_data[bstack1ll1ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᨩ")] = 100
        hook_data[bstack1ll1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᨪ")] = bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᨫ")]
        if hook_data[bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᨬ")] == bstack1ll1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᨭ"):
            hook_data[bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᨮ")] = bstack1ll1ll1_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᨯ")  # bstack1l1ll11l111_opy_
            hook_data[bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᨰ")] = [{bstack1ll1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᨱ"): [bstack1ll1ll1_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᨲ")]}]
    if bstack1l1ll11l1ll_opy_:
        hook_data[bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᨳ")] = bstack1l1ll11l1ll_opy_.result
        hook_data[bstack1ll1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᨴ")] = bstack1llll1l1l1l_opy_(bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᨵ")], bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᨶ")])
        hook_data[bstack1ll1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᨷ")] = bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᨸ")]
        if hook_data[bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᨹ")] == bstack1ll1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᨺ"):
            hook_data[bstack1ll1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᨻ")] = bstack1111l11l1_opy_.bstack111l1ll1l1_opy_(bstack1l1ll11l1ll_opy_.exception_type)
            hook_data[bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᨼ")] = [{bstack1ll1ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᨽ"): bstack1llll11l1l1_opy_(bstack1l1ll11l1ll_opy_.exception)}]
    return hook_data
def bstack1l1l1lll1l1_opy_(test, bstack111llll111_opy_, bstack111ll111l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1ll1ll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩᨾ").format(bstack111ll111l_opy_))
    bstack11l1l1l111_opy_ = bstack1l1l1llll1l_opy_(test, bstack111llll111_opy_, result, call, bstack111ll111l_opy_, outcome)
    driver = getattr(test, bstack1ll1ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᨿ"), None)
    if bstack111ll111l_opy_ == bstack1ll1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᩀ") and driver:
        bstack11l1l1l111_opy_[bstack1ll1ll1_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᩁ")] = bstack1111l11l1_opy_.bstack11l1lll1ll_opy_(driver)
    if bstack111ll111l_opy_ == bstack1ll1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᩂ"):
        bstack111ll111l_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᩃ")
    bstack11l11l111l_opy_ = {
        bstack1ll1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᩄ"): bstack111ll111l_opy_,
        bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᩅ"): bstack11l1l1l111_opy_
    }
    bstack1111l11l1_opy_.bstack1l1lllll1l_opy_(bstack11l11l111l_opy_)
    if bstack111ll111l_opy_ == bstack1ll1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᩆ"):
        threading.current_thread().bstackTestMeta = {bstack1ll1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᩇ"): bstack1ll1ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᩈ")}
    elif bstack111ll111l_opy_ == bstack1ll1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᩉ"):
        threading.current_thread().bstackTestMeta = {bstack1ll1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᩊ"): getattr(result, bstack1ll1ll1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᩋ"), bstack1ll1ll1_opy_ (u"ࠬ࠭ᩌ"))}
def bstack1l1l1ll1l11_opy_(test, bstack111llll111_opy_, bstack111ll111l_opy_, result=None, call=None, outcome=None, bstack1l1ll11l1ll_opy_=None):
    logger.debug(bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭ᩍ").format(bstack111ll111l_opy_))
    hook_data = bstack1l1ll11lll1_opy_(test, bstack111llll111_opy_, bstack111ll111l_opy_, result, call, outcome, bstack1l1ll11l1ll_opy_)
    bstack11l11l111l_opy_ = {
        bstack1ll1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᩎ"): bstack111ll111l_opy_,
        bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᩏ"): hook_data
    }
    bstack1111l11l1_opy_.bstack1l1lllll1l_opy_(bstack11l11l111l_opy_)
def bstack111lll111l_opy_(bstack111llll111_opy_):
    if not bstack111llll111_opy_:
        return None
    if bstack111llll111_opy_.get(bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᩐ"), None):
        return getattr(bstack111llll111_opy_[bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᩑ")], bstack1ll1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᩒ"), None)
    return bstack111llll111_opy_.get(bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᩓ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1111l11l1_opy_.on():
            return
        places = [bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᩔ"), bstack1ll1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᩕ"), bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᩖ")]
        bstack11l11l1lll_opy_ = []
        for bstack1l1ll11l1l1_opy_ in places:
            records = caplog.get_records(bstack1l1ll11l1l1_opy_)
            bstack1l1l1ll1lll_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᩗ") if bstack1l1ll11l1l1_opy_ == bstack1ll1ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᩘ") else bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᩙ")
            bstack1l1ll1111ll_opy_ = request.node.nodeid + (bstack1ll1ll1_opy_ (u"ࠬ࠭ᩚ") if bstack1l1ll11l1l1_opy_ == bstack1ll1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᩛ") else bstack1ll1ll1_opy_ (u"ࠧ࠮ࠩᩜ") + bstack1l1ll11l1l1_opy_)
            bstack11l1ll1111_opy_ = bstack111lll111l_opy_(_11l11l11ll_opy_.get(bstack1l1ll1111ll_opy_, None))
            if not bstack11l1ll1111_opy_:
                continue
            for record in records:
                if bstack1lll1llll11_opy_(record.message):
                    continue
                bstack11l11l1lll_opy_.append({
                    bstack1ll1ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᩝ"): bstack1llll11ll11_opy_(record.created).isoformat() + bstack1ll1ll1_opy_ (u"ࠩ࡝ࠫᩞ"),
                    bstack1ll1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᩟"): record.levelname,
                    bstack1ll1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩ᩠ࠬ"): record.message,
                    bstack1l1l1ll1lll_opy_: bstack11l1ll1111_opy_
                })
        if len(bstack11l11l1lll_opy_) > 0:
            bstack1111l11l1_opy_.bstack1l1l11ll1l_opy_(bstack11l11l1lll_opy_)
    except Exception as err:
        print(bstack1ll1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᩡ"), str(err))
def bstack11llll1ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1lllll11ll_opy_
    bstack11ll11l1ll_opy_ = bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᩢ"), None) and bstack1l1111l1l1_opy_(
            threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᩣ"), None)
    bstack11lll11l11_opy_ = getattr(driver, bstack1ll1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᩤ"), None) != None and getattr(driver, bstack1ll1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᩥ"), None) == True
    if sequence == bstack1ll1ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᩦ") and driver != None:
      if not bstack1lllll11ll_opy_ and bstack1lll1lll1l1_opy_() and bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᩧ") in CONFIG and CONFIG[bstack1ll1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᩨ")] == True and bstack1ll1l1llll_opy_.bstack1ll11l1l1_opy_(driver_command) and (bstack11lll11l11_opy_ or bstack11ll11l1ll_opy_) and not bstack1l111l111l_opy_(args):
        try:
          bstack1lllll11ll_opy_ = True
          logger.debug(bstack1ll1ll1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨᩩ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬᩪ").format(str(err)))
        bstack1lllll11ll_opy_ = False
    if sequence == bstack1ll1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᩫ"):
        if driver_command == bstack1ll1ll1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᩬ"):
            bstack1111l11l1_opy_.bstack1lll1l1l1_opy_({
                bstack1ll1ll1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᩭ"): response[bstack1ll1ll1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᩮ")],
                bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᩯ"): store[bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᩰ")]
            })
def bstack11llll11_opy_():
    global bstack11ll11ll1l_opy_
    bstack1l1ll1l1l_opy_.bstack11l11l1ll_opy_()
    logging.shutdown()
    bstack1111l11l1_opy_.bstack11l111l111_opy_()
    for driver in bstack11ll11ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l1ll1ll1_opy_(*args):
    global bstack11ll11ll1l_opy_
    bstack1111l11l1_opy_.bstack11l111l111_opy_()
    for driver in bstack11ll11ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll1ll1l_opy_, stage=STAGE.SINGLE, bstack11l111ll1_opy_=bstack1lll11llll_opy_)
def bstack11l1l11ll_opy_(self, *args, **kwargs):
    bstack1111l1lll_opy_ = bstack111l11lll_opy_(self, *args, **kwargs)
    bstack1ll111ll1_opy_ = getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨᩱ"), None)
    if bstack1ll111ll1_opy_ and bstack1ll111ll1_opy_.get(bstack1ll1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᩲ"), bstack1ll1ll1_opy_ (u"ࠩࠪᩳ")) == bstack1ll1ll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᩴ"):
        bstack1111l11l1_opy_.bstack1l111llll1_opy_(self)
    return bstack1111l1lll_opy_
@measure(event_name=EVENTS.bstack1ll1l1ll1_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack11l111ll1_opy_=bstack1lll11llll_opy_)
def bstack1l111111l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
    if bstack11lll1lll_opy_.get_property(bstack1ll1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ᩵")):
        return
    bstack11lll1lll_opy_.bstack1lll1ll1_opy_(bstack1ll1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ᩶"), True)
    global bstack1llll1l11_opy_
    global bstack1l1l1lll11_opy_
    bstack1llll1l11_opy_ = framework_name
    logger.info(bstack11l1l11l_opy_.format(bstack1llll1l11_opy_.split(bstack1ll1ll1_opy_ (u"࠭࠭ࠨ᩷"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1lll1lll1l1_opy_():
            Service.start = bstack1llll1l1ll_opy_
            Service.stop = bstack1l1l1ll11_opy_
            webdriver.Remote.__init__ = bstack11ll11ll1_opy_
            webdriver.Remote.get = bstack1l1l11111_opy_
            if not isinstance(os.getenv(bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ᩸")), str):
                return
            WebDriver.close = bstack1l111l1l1l_opy_
            WebDriver.quit = bstack11ll1ll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1lll1lll1l1_opy_() and bstack1111l11l1_opy_.on():
            webdriver.Remote.__init__ = bstack11l1l11ll_opy_
        bstack1l1l1lll11_opy_ = True
    except Exception as e:
        pass
    bstack11l1l1l1l_opy_()
    if os.environ.get(bstack1ll1ll1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭᩹")):
        bstack1l1l1lll11_opy_ = eval(os.environ.get(bstack1ll1ll1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ᩺")))
    if not bstack1l1l1lll11_opy_:
        bstack11ll1ll1l_opy_(bstack1ll1ll1_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ᩻"), bstack1l1llll1ll_opy_)
    if bstack1l1lll1lll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1l1l11_opy_ = bstack1ll1l111l1_opy_
        except Exception as e:
            logger.error(bstack1l1lll1l_opy_.format(str(e)))
    if bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᩼") in str(framework_name).lower():
        if not bstack1lll1lll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll111111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111llllll_opy_
            Config.getoption = bstack1ll1lll11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll1l11l1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll1llll_opy_, stage=STAGE.SINGLE, bstack11l111ll1_opy_=bstack1lll11llll_opy_)
def bstack11ll1ll1_opy_(self):
    global bstack1llll1l11_opy_
    global bstack1l111l1l11_opy_
    global bstack1l11ll11ll_opy_
    try:
        if bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᩽") in bstack1llll1l11_opy_ and self.session_id != None and bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ᩾"), bstack1ll1ll1_opy_ (u"ࠧࠨ᩿")) != bstack1ll1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᪀"):
            bstack11lll1111l_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᪁") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᪂")
            bstack1l1l1lll1l_opy_(logger, True)
            if self != None:
                bstack1l1ll111l_opy_(self, bstack11lll1111l_opy_, bstack1ll1ll1_opy_ (u"ࠫ࠱ࠦࠧ᪃").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᪄"), None)
        if item is not None and bstack1l1111l1l1_opy_(threading.current_thread(), bstack1ll1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᪅"), None):
            bstack11ll11lll_opy_.bstack1l11l1lll_opy_(self, bstack11lll1ll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1ll1_opy_ (u"ࠧࠨ᪆")
    except Exception as e:
        logger.debug(bstack1ll1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ᪇") + str(e))
    bstack1l11ll11ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11ll11llll_opy_, stage=STAGE.SINGLE, bstack11l111ll1_opy_=bstack1lll11llll_opy_)
def bstack11ll11ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l111l1l11_opy_
    global bstack1lll11llll_opy_
    global bstack1l1l1111l1_opy_
    global bstack1llll1l11_opy_
    global bstack111l11lll_opy_
    global bstack11ll11ll1l_opy_
    global bstack1l11111ll1_opy_
    global bstack11l1l1lll_opy_
    global bstack11lll1ll1l_opy_
    CONFIG[bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᪈")] = str(bstack1llll1l11_opy_) + str(__version__)
    command_executor = bstack1ll1lll1l_opy_(bstack1l11111ll1_opy_, CONFIG)
    logger.debug(bstack1111ll1l1_opy_.format(command_executor))
    proxy = bstack111ll11ll_opy_(CONFIG, proxy)
    bstack1l1ll1l1_opy_ = 0
    try:
        if bstack1l1l1111l1_opy_ is True:
            bstack1l1ll1l1_opy_ = int(os.environ.get(bstack1ll1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᪉")))
    except:
        bstack1l1ll1l1_opy_ = 0
    bstack1l11lll1_opy_ = bstack1ll1ll1ll1_opy_(CONFIG, bstack1l1ll1l1_opy_)
    logger.debug(bstack1l1111ll1l_opy_.format(str(bstack1l11lll1_opy_)))
    bstack11lll1ll1l_opy_ = CONFIG.get(bstack1ll1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᪊"))[bstack1l1ll1l1_opy_]
    if bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ᪋") in CONFIG and CONFIG[bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ᪌")]:
        bstack1ll1lll111_opy_(bstack1l11lll1_opy_, bstack11l1l1lll_opy_)
    if bstack1ll11ll1_opy_.bstack11llll11l1_opy_(CONFIG, bstack1l1ll1l1_opy_) and bstack1ll11ll1_opy_.bstack1l11111ll_opy_(bstack1l11lll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack1ll11ll1_opy_.set_capabilities(bstack1l11lll1_opy_, CONFIG)
    if desired_capabilities:
        bstack111l1ll1_opy_ = bstack11l1ll111_opy_(desired_capabilities)
        bstack111l1ll1_opy_[bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ᪍")] = bstack1l1l1l1ll_opy_(CONFIG)
        bstack1ll1111l11_opy_ = bstack1ll1ll1ll1_opy_(bstack111l1ll1_opy_)
        if bstack1ll1111l11_opy_:
            bstack1l11lll1_opy_ = update(bstack1ll1111l11_opy_, bstack1l11lll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll1lll1_opy_(options, bstack1l11lll1_opy_)
    if not options:
        options = bstack1l11lllll1_opy_(bstack1l11lll1_opy_)
    if proxy and bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᪎")):
        options.proxy(proxy)
    if options and bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᪏")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll11l111_opy_() < version.parse(bstack1ll1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᪐")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11lll1_opy_)
    logger.info(bstack1l1111ll_opy_)
    bstack1ll1lll1_opy_.end(EVENTS.bstack1ll1l1ll1_opy_.value, EVENTS.bstack1ll1l1ll1_opy_.value + bstack1ll1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᪑"),
                               EVENTS.bstack1ll1l1ll1_opy_.value + bstack1ll1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᪒"), True, None)
    if bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭᪓")):
        bstack111l11lll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭᪔")):
        bstack111l11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ᪕")):
        bstack111l11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack111l11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1111lll1_opy_ = bstack1ll1ll1_opy_ (u"ࠩࠪ᪖")
        if bstack11ll11l111_opy_() >= version.parse(bstack1ll1ll1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ᪗")):
            bstack1111lll1_opy_ = self.caps.get(bstack1ll1ll1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ᪘"))
        else:
            bstack1111lll1_opy_ = self.capabilities.get(bstack1ll1ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᪙"))
        if bstack1111lll1_opy_:
            bstack111l1l11_opy_(bstack1111lll1_opy_)
            if bstack11ll11l111_opy_() <= version.parse(bstack1ll1ll1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭᪚")):
                self.command_executor._url = bstack1ll1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᪛") + bstack1l11111ll1_opy_ + bstack1ll1ll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ᪜")
            else:
                self.command_executor._url = bstack1ll1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᪝") + bstack1111lll1_opy_ + bstack1ll1ll1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ᪞")
            logger.debug(bstack1llllll1l_opy_.format(bstack1111lll1_opy_))
        else:
            logger.debug(bstack1l11l1l1_opy_.format(bstack1ll1ll1_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ᪟")))
    except Exception as e:
        logger.debug(bstack1l11l1l1_opy_.format(e))
    bstack1l111l1l11_opy_ = self.session_id
    if bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᪠") in bstack1llll1l11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᪡"), None)
        if item:
            bstack1l1l1llll11_opy_ = getattr(item, bstack1ll1ll1_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ᪢"), False)
            if not getattr(item, bstack1ll1ll1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᪣"), None) and bstack1l1l1llll11_opy_:
                setattr(store[bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᪤")], bstack1ll1ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᪥"), self)
        bstack1ll111ll1_opy_ = getattr(threading.current_thread(), bstack1ll1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ᪦"), None)
        if bstack1ll111ll1_opy_ and bstack1ll111ll1_opy_.get(bstack1ll1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᪧ"), bstack1ll1ll1_opy_ (u"࠭ࠧ᪨")) == bstack1ll1ll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ᪩"):
            bstack1111l11l1_opy_.bstack1l111llll1_opy_(self)
    bstack11ll11ll1l_opy_.append(self)
    if bstack1ll1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᪪") in CONFIG and bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᪫") in CONFIG[bstack1ll1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᪬")][bstack1l1ll1l1_opy_]:
        bstack1lll11llll_opy_ = CONFIG[bstack1ll1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᪭")][bstack1l1ll1l1_opy_][bstack1ll1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᪮")]
    logger.debug(bstack1ll1ll11_opy_.format(bstack1l111l1l11_opy_))
@measure(event_name=EVENTS.bstack11ll1llll_opy_, stage=STAGE.SINGLE, bstack11l111ll1_opy_=bstack1lll11llll_opy_)
def bstack1l1l11111_opy_(self, url):
    global bstack1l11llll11_opy_
    global CONFIG
    try:
        bstack1l1l111lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1lllllll_opy_.format(str(err)))
    try:
        bstack1l11llll11_opy_(self, url)
    except Exception as e:
        try:
            bstack11lllllll1_opy_ = str(e)
            if any(err_msg in bstack11lllllll1_opy_ for err_msg in bstack11ll1l1l_opy_):
                bstack1l1l111lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1lllllll_opy_.format(str(err)))
        raise e
def bstack1l1111l11l_opy_(item, when):
    global bstack1l1l1l11l1_opy_
    try:
        bstack1l1l1l11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l11l1_opy_(item, call, rep):
    global bstack11ll1111l_opy_
    global bstack11ll11ll1l_opy_
    name = bstack1ll1ll1_opy_ (u"࠭ࠧ᪯")
    try:
        if rep.when == bstack1ll1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ᪰"):
            bstack1l111l1l11_opy_ = threading.current_thread().bstackSessionId
            bstack1l1l1lllll1_opy_ = item.config.getoption(bstack1ll1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᪱"))
            try:
                if (str(bstack1l1l1lllll1_opy_).lower() != bstack1ll1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᪲")):
                    name = str(rep.nodeid)
                    bstack11ll111ll1_opy_ = bstack1lll1l1l11_opy_(bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᪳"), name, bstack1ll1ll1_opy_ (u"ࠫࠬ᪴"), bstack1ll1ll1_opy_ (u"᪵ࠬ࠭"), bstack1ll1ll1_opy_ (u"᪶࠭ࠧ"), bstack1ll1ll1_opy_ (u"ࠧࠨ᪷"))
                    os.environ[bstack1ll1ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈ᪸ࠫ")] = name
                    for driver in bstack11ll11ll1l_opy_:
                        if bstack1l111l1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll111ll1_opy_)
            except Exception as e:
                logger.debug(bstack1ll1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾ᪹ࠩ").format(str(e)))
            try:
                bstack11ll1l11l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧ᪺ࠫ"):
                    status = bstack1ll1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᪻") if rep.outcome.lower() == bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᪼") else bstack1ll1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ᪽࠭")
                    reason = bstack1ll1ll1_opy_ (u"ࠧࠨ᪾")
                    if status == bstack1ll1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᪿ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵᫀࠧ") if status == bstack1ll1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᫁") else bstack1ll1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᫂")
                    data = name + bstack1ll1ll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩ᫃ࠧࠧ") if status == bstack1ll1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ᫄࠭") else name + bstack1ll1ll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ᫅") + reason
                    bstack11111ll1l_opy_ = bstack1lll1l1l11_opy_(bstack1ll1ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᫆"), bstack1ll1ll1_opy_ (u"ࠩࠪ᫇"), bstack1ll1ll1_opy_ (u"ࠪࠫ᫈"), bstack1ll1ll1_opy_ (u"ࠫࠬ᫉"), level, data)
                    for driver in bstack11ll11ll1l_opy_:
                        if bstack1l111l1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack11111ll1l_opy_)
            except Exception as e:
                logger.debug(bstack1ll1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾ᫊ࠩ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ᫋").format(str(e)))
    bstack11ll1111l_opy_(item, call, rep)
notset = Notset()
def bstack1ll1lll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l11ll1_opy_
    if str(name).lower() == bstack1ll1ll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᫌ"):
        return bstack1ll1ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᫍ")
    else:
        return bstack1l11l11ll1_opy_(self, name, default, skip)
def bstack1ll1l111l1_opy_(self):
    global CONFIG
    global bstack1lll1l111l_opy_
    try:
        proxy = bstack1ll1ll1111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1ll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᫎ")):
                proxies = bstack11l11llll_opy_(proxy, bstack1ll1lll1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack111ll11l1_opy_ = proxies.popitem()
                    if bstack1ll1ll1_opy_ (u"ࠥ࠾࠴࠵ࠢ᫏") in bstack111ll11l1_opy_:
                        return bstack111ll11l1_opy_
                    else:
                        return bstack1ll1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ᫐") + bstack111ll11l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ᫑").format(str(e)))
    return bstack1lll1l111l_opy_(self)
def bstack1l1lll1lll_opy_():
    return (bstack1ll1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᫒") in CONFIG or bstack1ll1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᫓") in CONFIG) and bstack11l11l1l_opy_() and bstack11ll11l111_opy_() >= version.parse(
        bstack1111llll_opy_)
def bstack11ll1ll1l1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lll11llll_opy_
    global bstack1l1l1111l1_opy_
    global bstack1llll1l11_opy_
    CONFIG[bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᫔")] = str(bstack1llll1l11_opy_) + str(__version__)
    bstack1l1ll1l1_opy_ = 0
    try:
        if bstack1l1l1111l1_opy_ is True:
            bstack1l1ll1l1_opy_ = int(os.environ.get(bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᫕")))
    except:
        bstack1l1ll1l1_opy_ = 0
    CONFIG[bstack1ll1ll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᫖")] = True
    bstack1l11lll1_opy_ = bstack1ll1ll1ll1_opy_(CONFIG, bstack1l1ll1l1_opy_)
    logger.debug(bstack1l1111ll1l_opy_.format(str(bstack1l11lll1_opy_)))
    if CONFIG.get(bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᫗")):
        bstack1ll1lll111_opy_(bstack1l11lll1_opy_, bstack11l1l1lll_opy_)
    if bstack1ll1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᫘") in CONFIG and bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᫙") in CONFIG[bstack1ll1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᫚")][bstack1l1ll1l1_opy_]:
        bstack1lll11llll_opy_ = CONFIG[bstack1ll1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᫛")][bstack1l1ll1l1_opy_][bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᫜")]
    import urllib
    import json
    if bstack1ll1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᫝") in CONFIG and str(CONFIG[bstack1ll1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᫞")]).lower() != bstack1ll1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ᫟"):
        bstack1l1111ll1_opy_ = bstack11lll111l1_opy_()
        bstack11ll1l1l1_opy_ = bstack1l1111ll1_opy_ + urllib.parse.quote(json.dumps(bstack1l11lll1_opy_))
    else:
        bstack11ll1l1l1_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ᫠") + urllib.parse.quote(json.dumps(bstack1l11lll1_opy_))
    browser = self.connect(bstack11ll1l1l1_opy_)
    return browser
def bstack11l1l1l1l_opy_():
    global bstack1l1l1lll11_opy_
    global bstack1llll1l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1111111l1_opy_
        if not bstack1lll1lll1l1_opy_():
            global bstack1l1l1l1111_opy_
            if not bstack1l1l1l1111_opy_:
                from bstack_utils.helper import bstack111ll11l_opy_, bstack11111l1l1_opy_
                bstack1l1l1l1111_opy_ = bstack111ll11l_opy_()
                bstack11111l1l1_opy_(bstack1llll1l11_opy_)
            BrowserType.connect = bstack1111111l1_opy_
            return
        BrowserType.launch = bstack11ll1ll1l1_opy_
        bstack1l1l1lll11_opy_ = True
    except Exception as e:
        pass
def bstack1l1ll111ll1_opy_():
    global CONFIG
    global bstack1l1ll1ll11_opy_
    global bstack1l11111ll1_opy_
    global bstack11l1l1lll_opy_
    global bstack1l1l1111l1_opy_
    global bstack1l1l11l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭᫡")))
    bstack1l1ll1ll11_opy_ = eval(os.environ.get(bstack1ll1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᫢")))
    bstack1l11111ll1_opy_ = os.environ.get(bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ᫣"))
    bstack1l11lll111_opy_(CONFIG, bstack1l1ll1ll11_opy_)
    bstack1l1l11l1l_opy_ = bstack1l1ll1l1l_opy_.bstack11111l111_opy_(CONFIG, bstack1l1l11l1l_opy_)
    global bstack111l11lll_opy_
    global bstack1l11ll11ll_opy_
    global bstack11llllll_opy_
    global bstack11lll1ll_opy_
    global bstack1l1lllll11_opy_
    global bstack1l11lll1l_opy_
    global bstack1111lllll_opy_
    global bstack1l11llll11_opy_
    global bstack1lll1l111l_opy_
    global bstack1l11l11ll1_opy_
    global bstack1l1l1l11l1_opy_
    global bstack11ll1111l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111l11lll_opy_ = webdriver.Remote.__init__
        bstack1l11ll11ll_opy_ = WebDriver.quit
        bstack1111lllll_opy_ = WebDriver.close
        bstack1l11llll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᫤") in CONFIG or bstack1ll1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᫥") in CONFIG) and bstack11l11l1l_opy_():
        if bstack11ll11l111_opy_() < version.parse(bstack1111llll_opy_):
            logger.error(bstack1l11ll111l_opy_.format(bstack11ll11l111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1lll1l111l_opy_ = RemoteConnection._1l1l1l11_opy_
            except Exception as e:
                logger.error(bstack1l1lll1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l11l11ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l1l11l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l11111_opy_)
    try:
        from pytest_bdd import reporting
        bstack11ll1111l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1ll1ll1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭᫦"))
    bstack11l1l1lll_opy_ = CONFIG.get(bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᫧"), {}).get(bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᫨"))
    bstack1l1l1111l1_opy_ = True
    bstack1l111111l1_opy_(bstack1l11l111_opy_)
if (bstack1lllllllll1_opy_()):
    bstack1l1ll111ll1_opy_()
@bstack11l111111l_opy_(class_method=False)
def bstack1l1l1ll11l1_opy_(hook_name, event, bstack1l1l1lll1ll_opy_=None):
    if hook_name not in [bstack1ll1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ᫩"), bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᫪"), bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᫫"), bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᫬"), bstack1ll1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ᫭"), bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ᫮"), bstack1ll1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᫯"), bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ᫰")]:
        return
    node = store[bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᫱")]
    if hook_name in [bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᫲"), bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᫳")]:
        node = store[bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ᫴")]
    elif hook_name in [bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ᫵"), bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ᫶")]:
        node = store[bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭᫷")]
    if event == bstack1ll1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ᫸"):
        hook_type = bstack1ll11l1l1ll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l11lllll_opy_ = {
            bstack1ll1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᫹"): uuid,
            bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᫺"): bstack1lll11ll1l_opy_(),
            bstack1ll1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ᫻"): bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᫼"),
            bstack1ll1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ᫽"): hook_type,
            bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ᫾"): hook_name
        }
        store[bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭᫿")].append(uuid)
        bstack1l1l1ll1l1l_opy_ = node.nodeid
        if hook_type == bstack1ll1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᬀ"):
            if not _11l11l11ll_opy_.get(bstack1l1l1ll1l1l_opy_, None):
                _11l11l11ll_opy_[bstack1l1l1ll1l1l_opy_] = {bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᬁ"): []}
            _11l11l11ll_opy_[bstack1l1l1ll1l1l_opy_][bstack1ll1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᬂ")].append(bstack11l11lllll_opy_[bstack1ll1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᬃ")])
        _11l11l11ll_opy_[bstack1l1l1ll1l1l_opy_ + bstack1ll1ll1_opy_ (u"ࠧ࠮ࠩᬄ") + hook_name] = bstack11l11lllll_opy_
        bstack1l1l1ll1l11_opy_(node, bstack11l11lllll_opy_, bstack1ll1ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᬅ"))
    elif event == bstack1ll1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᬆ"):
        bstack11l1l1l11l_opy_ = node.nodeid + bstack1ll1ll1_opy_ (u"ࠪ࠱ࠬᬇ") + hook_name
        _11l11l11ll_opy_[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᬈ")] = bstack1lll11ll1l_opy_()
        bstack1l1l1lll111_opy_(_11l11l11ll_opy_[bstack11l1l1l11l_opy_][bstack1ll1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᬉ")])
        bstack1l1l1ll1l11_opy_(node, _11l11l11ll_opy_[bstack11l1l1l11l_opy_], bstack1ll1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᬊ"), bstack1l1ll11l1ll_opy_=bstack1l1l1lll1ll_opy_)
def bstack1l1ll11ll1l_opy_():
    global bstack1l1ll111lll_opy_
    if bstack1l111ll1l_opy_():
        bstack1l1ll111lll_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᬋ")
    else:
        bstack1l1ll111lll_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᬌ")
@bstack1111l11l1_opy_.bstack1l1lll111ll_opy_
def bstack1l1l1ll11ll_opy_():
    bstack1l1ll11ll1l_opy_()
    if bstack11l11l1l_opy_():
        bstack11lll1lll_opy_ = Config.bstack111llll1_opy_()
        bstack1ll1ll1_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬᬍ")
        if bstack11lll1lll_opy_.get_property(bstack1ll1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧᬎ")):
            if CONFIG.get(bstack1ll1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᬏ")) is not None and int(CONFIG[bstack1ll1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᬐ")]) > 1:
                bstack1ll111l1_opy_(bstack11llll1ll_opy_)
            return
        bstack1ll111l1_opy_(bstack11llll1ll_opy_)
    try:
        bstack1lll1l1l1l1_opy_(bstack1l1l1ll11l1_opy_)
    except Exception as e:
        logger.debug(bstack1ll1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᬑ").format(e))
bstack1l1l1ll11ll_opy_()