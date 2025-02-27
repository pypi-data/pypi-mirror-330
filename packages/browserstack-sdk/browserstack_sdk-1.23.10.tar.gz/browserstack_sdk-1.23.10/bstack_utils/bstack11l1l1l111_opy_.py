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
from uuid import uuid4
from bstack_utils.helper import bstack1lll11ll1l_opy_, bstack1llll1l1l1l_opy_
from bstack_utils.bstack1ll11l1l11_opy_ import bstack1ll11l1l11l_opy_
class bstack11l11ll11l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l1ll1l1l_opy_=None, framework=None, tags=[], scope=[], bstack1ll1111111l_opy_=None, bstack1ll11111lll_opy_=True, bstack1ll11111l11_opy_=None, bstack111ll111l_opy_=None, result=None, duration=None, bstack111lll11ll_opy_=None, meta={}):
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11111lll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l1ll1l1l_opy_ = bstack11l1ll1l1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1111111l_opy_ = bstack1ll1111111l_opy_
        self.bstack1ll11111l11_opy_ = bstack1ll11111l11_opy_
        self.bstack111ll111l_opy_ = bstack111ll111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111lll1l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1ll1l11_opy_(self, meta):
        self.meta = meta
    def bstack11l1l11111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll111111l1_opy_(self):
        bstack1ll1111l111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᝉ"): bstack1ll1111l111_opy_,
            bstack1ll1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᝊ"): bstack1ll1111l111_opy_,
            bstack1ll1ll1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᝋ"): bstack1ll1111l111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1ll1_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᝌ") + key)
            setattr(self, key, val)
    def bstack1ll111l11ll_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᝍ"): self.name,
            bstack1ll1ll1_opy_ (u"ࠩࡥࡳࡩࡿࠧᝎ"): {
                bstack1ll1ll1_opy_ (u"ࠪࡰࡦࡴࡧࠨᝏ"): bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᝐ"),
                bstack1ll1ll1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᝑ"): self.code
            },
            bstack1ll1ll1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᝒ"): self.scope,
            bstack1ll1ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬᝓ"): self.tags,
            bstack1ll1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ᝔"): self.framework,
            bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᝕"): self.bstack11l1ll1l1l_opy_
        }
    def bstack1ll111111ll_opy_(self):
        return {
         bstack1ll1ll1_opy_ (u"ࠪࡱࡪࡺࡡࠨ᝖"): self.meta
        }
    def bstack1ll1111ll11_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ᝗"): {
                bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ᝘"): self.bstack1ll1111111l_opy_
            }
        }
    def bstack1ll11111ll1_opy_(self, bstack1ll111l11l1_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1ll1_opy_ (u"࠭ࡩࡥࠩ᝙")] == bstack1ll111l11l1_opy_, self.meta[bstack1ll1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᝚")]), None)
        step.update(details)
    def bstack1l1111l1l_opy_(self, bstack1ll111l11l1_opy_):
        step = next(filter(lambda st: st[bstack1ll1ll1_opy_ (u"ࠨ࡫ࡧࠫ᝛")] == bstack1ll111l11l1_opy_, self.meta[bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᝜")]), None)
        step.update({
            bstack1ll1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᝝"): bstack1lll11ll1l_opy_()
        })
    def bstack11l1l11ll1_opy_(self, bstack1ll111l11l1_opy_, result, duration=None):
        bstack1ll11111l11_opy_ = bstack1lll11ll1l_opy_()
        if bstack1ll111l11l1_opy_ is not None and self.meta.get(bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᝞")):
            step = next(filter(lambda st: st[bstack1ll1ll1_opy_ (u"ࠬ࡯ࡤࠨ᝟")] == bstack1ll111l11l1_opy_, self.meta[bstack1ll1ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᝠ")]), None)
            step.update({
                bstack1ll1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᝡ"): bstack1ll11111l11_opy_,
                bstack1ll1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᝢ"): duration if duration else bstack1llll1l1l1l_opy_(step[bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᝣ")], bstack1ll11111l11_opy_),
                bstack1ll1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᝤ"): result.result,
                bstack1ll1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᝥ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll111l111l_opy_):
        if self.meta.get(bstack1ll1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᝦ")):
            self.meta[bstack1ll1ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᝧ")].append(bstack1ll111l111l_opy_)
        else:
            self.meta[bstack1ll1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᝨ")] = [ bstack1ll111l111l_opy_ ]
    def bstack1ll1111l1l1_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᝩ"): self.bstack111lll1l1l_opy_(),
            **self.bstack1ll111l11ll_opy_(),
            **self.bstack1ll111111l1_opy_(),
            **self.bstack1ll111111ll_opy_()
        }
    def bstack1ll1111l1ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᝪ"): self.bstack1ll11111l11_opy_,
            bstack1ll1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᝫ"): self.duration,
            bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᝬ"): self.result.result
        }
        if data[bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᝭")] == bstack1ll1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᝮ"):
            data[bstack1ll1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᝯ")] = self.result.bstack111l1ll1l1_opy_()
            data[bstack1ll1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᝰ")] = [{bstack1ll1ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ᝱"): self.result.bstack1llll1ll1l1_opy_()}]
        return data
    def bstack1ll1111llll_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝲ"): self.bstack111lll1l1l_opy_(),
            **self.bstack1ll111l11ll_opy_(),
            **self.bstack1ll111111l1_opy_(),
            **self.bstack1ll1111l1ll_opy_(),
            **self.bstack1ll111111ll_opy_()
        }
    def bstack111ll1llll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1ll1_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬᝳ") in event:
            return self.bstack1ll1111l1l1_opy_()
        elif bstack1ll1ll1_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᝴") in event:
            return self.bstack1ll1111llll_opy_()
    def bstack11l111ll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll11111l11_opy_ = time if time else bstack1lll11ll1l_opy_()
        self.duration = duration if duration else bstack1llll1l1l1l_opy_(self.bstack11l1ll1l1l_opy_, self.bstack1ll11111l11_opy_)
        if result:
            self.result = result
class bstack11l1l111ll_opy_(bstack11l11ll11l_opy_):
    def __init__(self, hooks=[], bstack11l1l11lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1l11lll_opy_ = bstack11l1l11lll_opy_
        super().__init__(*args, **kwargs, bstack111ll111l_opy_=bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ᝵"))
    @classmethod
    def bstack1ll111l1111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1ll1_opy_ (u"ࠧࡪࡦࠪ᝶"): id(step),
                bstack1ll1ll1_opy_ (u"ࠨࡶࡨࡼࡹ࠭᝷"): step.name,
                bstack1ll1ll1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ᝸"): step.keyword,
            })
        return bstack11l1l111ll_opy_(
            **kwargs,
            meta={
                bstack1ll1ll1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫ᝹"): {
                    bstack1ll1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᝺"): feature.name,
                    bstack1ll1ll1_opy_ (u"ࠬࡶࡡࡵࡪࠪ᝻"): feature.filename,
                    bstack1ll1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᝼"): feature.description
                },
                bstack1ll1ll1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ᝽"): {
                    bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭᝾"): scenario.name
                },
                bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᝿"): steps,
                bstack1ll1ll1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬក"): bstack1ll11l1l11l_opy_(test)
            }
        )
    def bstack1ll11111l1l_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪខ"): self.hooks
        }
    def bstack1ll1111ll1l_opy_(self):
        if self.bstack11l1l11lll_opy_:
            return {
                bstack1ll1ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫគ"): self.bstack11l1l11lll_opy_
            }
        return {}
    def bstack1ll1111llll_opy_(self):
        return {
            **super().bstack1ll1111llll_opy_(),
            **self.bstack1ll11111l1l_opy_()
        }
    def bstack1ll1111l1l1_opy_(self):
        return {
            **super().bstack1ll1111l1l1_opy_(),
            **self.bstack1ll1111ll1l_opy_()
        }
    def bstack11l111ll1l_opy_(self):
        return bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨឃ")
class bstack11l1l1l1l1_opy_(bstack11l11ll11l_opy_):
    def __init__(self, hook_type, *args,bstack11l1l11lll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1111lll1_opy_ = None
        self.bstack11l1l11lll_opy_ = bstack11l1l11lll_opy_
        super().__init__(*args, **kwargs, bstack111ll111l_opy_=bstack1ll1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬង"))
    def bstack111lll1ll1_opy_(self):
        return self.hook_type
    def bstack1ll1111l11l_opy_(self):
        return {
            bstack1ll1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫច"): self.hook_type
        }
    def bstack1ll1111llll_opy_(self):
        return {
            **super().bstack1ll1111llll_opy_(),
            **self.bstack1ll1111l11l_opy_()
        }
    def bstack1ll1111l1l1_opy_(self):
        return {
            **super().bstack1ll1111l1l1_opy_(),
            bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧឆ"): self.bstack1ll1111lll1_opy_,
            **self.bstack1ll1111l11l_opy_()
        }
    def bstack11l111ll1l_opy_(self):
        return bstack1ll1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬជ")
    def bstack11l1lll111_opy_(self, bstack1ll1111lll1_opy_):
        self.bstack1ll1111lll1_opy_ = bstack1ll1111lll1_opy_