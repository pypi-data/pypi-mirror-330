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
class bstack1111ll11ll_opy_(object):
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll1_opy_ (u"ࠧࡿࠩၨ")), bstack1ll1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨၩ"))
  bstack1111ll11l1_opy_ = os.path.join(bstack111l1111l_opy_, bstack1ll1ll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩၪ"))
  bstack1111l1llll_opy_ = None
  perform_scan = None
  bstack1l11l1ll_opy_ = None
  bstack1l11llllll_opy_ = None
  bstack111l1l1111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1ll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬၫ")):
      cls.instance = super(bstack1111ll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack1111ll1111_opy_()
    return cls.instance
  def bstack1111ll1111_opy_(self):
    try:
      with open(self.bstack1111ll11l1_opy_, bstack1ll1ll1_opy_ (u"ࠫࡷ࠭ၬ")) as bstack1ll1llll11_opy_:
        bstack1111ll111l_opy_ = bstack1ll1llll11_opy_.read()
        data = json.loads(bstack1111ll111l_opy_)
        if bstack1ll1ll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧၭ") in data:
          self.bstack111l111lll_opy_(data[bstack1ll1ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨၮ")])
        if bstack1ll1ll1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨၯ") in data:
          self.bstack1111ll1ll1_opy_(data[bstack1ll1ll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩၰ")])
    except:
      pass
  def bstack1111ll1ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1ll1ll1_opy_ (u"ࠩࡶࡧࡦࡴࠧၱ")]
      self.bstack1l11l1ll_opy_ = scripts[bstack1ll1ll1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧၲ")]
      self.bstack1l11llllll_opy_ = scripts[bstack1ll1ll1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨၳ")]
      self.bstack111l1l1111_opy_ = scripts[bstack1ll1ll1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪၴ")]
  def bstack111l111lll_opy_(self, bstack1111l1llll_opy_):
    if bstack1111l1llll_opy_ != None and len(bstack1111l1llll_opy_) != 0:
      self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
  def store(self):
    try:
      with open(self.bstack1111ll11l1_opy_, bstack1ll1ll1_opy_ (u"࠭ࡷࠨၵ")) as file:
        json.dump({
          bstack1ll1ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤၶ"): self.bstack1111l1llll_opy_,
          bstack1ll1ll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤၷ"): {
            bstack1ll1ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢၸ"): self.perform_scan,
            bstack1ll1ll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢၹ"): self.bstack1l11l1ll_opy_,
            bstack1ll1ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣၺ"): self.bstack1l11llllll_opy_,
            bstack1ll1ll1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥၻ"): self.bstack111l1l1111_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll11l1l1_opy_(self, bstack1111ll1l11_opy_):
    try:
      return any(command.get(bstack1ll1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫၼ")) == bstack1111ll1l11_opy_ for command in self.bstack1111l1llll_opy_)
    except:
      return False
bstack1ll1l1llll_opy_ = bstack1111ll11ll_opy_()