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
import re
from enum import Enum
bstack1ll1l1l111_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ႔"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ႕"),
  bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ႖"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ႗"),
  bstack1ll1ll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ႘"): bstack1ll1ll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ႙"),
  bstack1ll1ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨႚ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩႛ"),
  bstack1ll1ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨႜ"): bstack1ll1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬႝ"),
  bstack1ll1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ႞"): bstack1ll1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ႟"),
  bstack1ll1ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬႠ"): bstack1ll1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ⴁ"),
  bstack1ll1ll1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨႢ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨႣ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩႤ"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬႥ"),
  bstack1ll1ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫႦ"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫႧ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬႨ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬႩ"),
  bstack1ll1ll1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩႪ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩႫ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫႬ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫႭ"),
  bstack1ll1ll1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧႮ"): bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧႯ"),
  bstack1ll1ll1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧႰ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧႱ"),
  bstack1ll1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭Ⴒ"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭Ⴓ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨႴ"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႵ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧႶ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧႷ"),
  bstack1ll1ll1_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨႸ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨႹ"),
  bstack1ll1ll1_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬႺ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬႻ"),
  bstack1ll1ll1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩႼ"): bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩႽ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫႾ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫႿ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪჀ"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪჁ"),
  bstack1ll1ll1_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧჂ"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧჃ"),
  bstack1ll1ll1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩჄ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩჅ"),
  bstack1ll1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭჆"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭Ⴧ"),
  bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ჈"): bstack1ll1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭჉"),
  bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ჊"): bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭჋"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ჌"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪჍ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ჎"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ჏"),
  bstack1ll1ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧა"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧბ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧგ"): bstack1ll1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪდ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬე"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬვ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬზ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬთ"),
  bstack1ll1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩი"): bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩკ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫლ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫმ"),
  bstack1ll1ll1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧნ"): bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧო"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪპ"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪჟ"),
  bstack1ll1ll1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭რ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ს"),
  bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ტ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭უ"),
  bstack1ll1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧფ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧქ")
}
bstack11111ll111_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠧࡰࡵࠪღ"),
  bstack1ll1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫყ"),
  bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫშ"),
  bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨჩ"),
  bstack1ll1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨც"),
  bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩძ"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭წ"),
]
bstack1111l1l1l_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩჭ"): [bstack1ll1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩხ"), bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫჯ")],
  bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ჰ"): bstack1ll1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧჱ"),
  bstack1ll1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨჲ"): bstack1ll1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩჳ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬჴ"): bstack1ll1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ჵ"),
  bstack1ll1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫჶ"): bstack1ll1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬჷ"),
  bstack1ll1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫჸ"): bstack1ll1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ჹ"),
  bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪჺ"): bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ჻"),
  bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬჼ"): bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ჽ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡵࡶࠧჾ"): [bstack1ll1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖ࡟ࡊࡆࠪჿ"), bstack1ll1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࠨᄀ")],
  bstack1ll1ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᄁ"): bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡐࡔࡍࡌࡆࡘࡈࡐࠬᄂ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᄃ"): bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᄄ"),
  bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᄅ"): bstack1ll1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠨᄆ"),
  bstack1ll1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᄇ"): bstack1ll1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡕࡓࡄࡒࡗࡈࡇࡌࡆࠩᄈ")
}
bstack1111l111l_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᄉ"): [bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᄊ"), bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᄋ")],
  bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᄌ"): [bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧᄍ"), bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᄎ")],
  bstack1ll1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᄏ"): bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᄐ"),
  bstack1ll1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᄑ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᄒ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᄓ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᄔ"),
  bstack1ll1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᄕ"): [bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩᄖ"), bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᄗ")],
  bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᄘ"): bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᄙ"),
  bstack1ll1ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᄚ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᄛ"),
  bstack1ll1ll1_opy_ (u"ࠬࡧࡰࡱࠩᄜ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩᄝ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᄞ"): bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᄟ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄠ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄡ")
}
bstack11l1l111_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᄢ"): bstack1ll1ll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄣ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᄤ"): [bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄥ"), bstack1ll1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᄦ")],
  bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᄧ"): bstack1ll1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᄨ"),
  bstack1ll1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᄩ"): bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᄪ"),
  bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᄫ"): [bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᄬ"), bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᄭ")],
  bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᄮ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᄯ"),
  bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᄰ"): bstack1ll1ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᄱ"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᄲ"): [bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᄳ"), bstack1ll1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄴ")],
  bstack1ll1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᄵ"): [bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᄶ"), bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᄷ")]
}
bstack1111lll11_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᄸ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᄹ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᄺ"),
  bstack1ll1ll1_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨᄻ"),
  bstack1ll1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᄼ"),
  bstack1ll1ll1_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᄽ"),
  bstack1ll1ll1_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᄾ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᄿ"),
  bstack1ll1ll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᅀ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᅁ"),
  bstack1ll1ll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᅂ"),
  bstack1ll1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᅃ"),
]
bstack1llll1l1_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᅄ"),
  bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᅅ"),
  bstack1ll1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᅆ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᅇ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅈ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᅉ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᅊ"),
  bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᅋ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᅌ"),
  bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᅍ"),
  bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᅎ"),
  bstack1ll1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᅏ"),
  bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫᅐ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᅑ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᅒ"),
  bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᅓ"),
  bstack1ll1ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫᅔ"),
  bstack1ll1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬᅕ"),
  bstack1ll1ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭ᅖ"),
  bstack1ll1ll1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧᅗ"),
  bstack1ll1ll1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨᅘ"),
  bstack1ll1ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩᅙ"),
  bstack1ll1ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪᅚ"),
  bstack1ll1ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫᅛ"),
  bstack1ll1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬᅜ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᅝ"),
  bstack1ll1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᅞ"),
  bstack1ll1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᅟ"),
  bstack1ll1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᅠ"),
  bstack1ll1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᅡ"),
  bstack1ll1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅢ")
]
bstack11111l11ll_opy_ = [
  bstack1ll1ll1_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᅣ"),
  bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᅤ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᅥ"),
  bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᅦ"),
  bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡑࡴ࡬ࡳࡷ࡯ࡴࡺࠩᅧ"),
  bstack1ll1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᅨ"),
  bstack1ll1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡦ࡭ࠧᅩ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᅪ"),
  bstack1ll1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᅫ"),
  bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᅬ"),
  bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᅭ"),
  bstack1ll1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᅮ"),
  bstack1ll1ll1_opy_ (u"ࠫࡴࡹࠧᅯ"),
  bstack1ll1ll1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᅰ"),
  bstack1ll1ll1_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬᅱ"),
  bstack1ll1ll1_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᅲ"),
  bstack1ll1ll1_opy_ (u"ࠨࡴࡨ࡫࡮ࡵ࡮ࠨᅳ"),
  bstack1ll1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᅴ"),
  bstack1ll1ll1_opy_ (u"ࠪࡱࡦࡩࡨࡪࡰࡨࠫᅵ"),
  bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨᅶ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅷ"),
  bstack1ll1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᅸ"),
  bstack1ll1ll1_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ᅹ"),
  bstack1ll1ll1_opy_ (u"ࠨࡰࡲࡔࡦ࡭ࡥࡍࡱࡤࡨ࡙࡯࡭ࡦࡱࡸࡸࠬᅺ"),
  bstack1ll1ll1_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᅻ"),
  bstack1ll1ll1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᅼ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᅽ"),
  bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᅾ"),
  bstack1ll1ll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᅿ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡯ࡱࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠫᆀ"),
  bstack1ll1ll1_opy_ (u"ࠨࡥ࡫ࡩࡨࡱࡕࡓࡎࠪᆁ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᆂ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡆࡳࡴࡱࡩࡦࡵࠪᆃ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡧࡰࡵࡷࡵࡩࡈࡸࡡࡴࡪࠪᆄ"),
  bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᆅ"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᆆ"),
  bstack1ll1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࡚ࡪࡸࡳࡪࡱࡱࠫᆇ"),
  bstack1ll1ll1_opy_ (u"ࠨࡰࡲࡆࡱࡧ࡮࡬ࡒࡲࡰࡱ࡯࡮ࡨࠩᆈ"),
  bstack1ll1ll1_opy_ (u"ࠩࡰࡥࡸࡱࡓࡦࡰࡧࡏࡪࡿࡳࠨᆉ"),
  bstack1ll1ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡏࡳ࡬ࡹࠧᆊ"),
  bstack1ll1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡍࡩ࠭ᆋ"),
  bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡥ࡫ࡦࡥࡹ࡫ࡤࡅࡧࡹ࡭ࡨ࡫ࠧᆌ"),
  bstack1ll1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡖࡡࡳࡣࡰࡷࠬᆍ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡪࡲࡲࡪࡔࡵ࡮ࡤࡨࡶࠬᆎ"),
  bstack1ll1ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᆏ"),
  bstack1ll1ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡏࡱࡶ࡬ࡳࡳࡹࠧᆐ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨᆑ"),
  bstack1ll1ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᆒ"),
  bstack1ll1ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩᆓ"),
  bstack1ll1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡈࡩࡰ࡯ࡨࡸࡷ࡯ࡣࠨᆔ"),
  bstack1ll1ll1_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࡜࠲ࠨᆕ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡯࡬ࡨࡘ࡫ࡳࡴ࡫ࡲࡲࡎࡴࡳࡵࡣ࡯ࡰࡆࡶࡰࡴࠩᆖ"),
  bstack1ll1ll1_opy_ (u"ࠩࡨࡷࡵࡸࡥࡴࡵࡲࡗࡪࡸࡶࡦࡴࠪᆗ"),
  bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᆘ"),
  bstack1ll1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡉࡤࡱࠩᆙ"),
  bstack1ll1ll1_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᆚ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡺࡰࡦࡘ࡮ࡳࡥࡘ࡫ࡷ࡬ࡓ࡚ࡐࠨᆛ"),
  bstack1ll1ll1_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᆜ"),
  bstack1ll1ll1_opy_ (u"ࠨࡩࡳࡷࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᆝ"),
  bstack1ll1ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᆞ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᆟ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࡆ࡬ࡦࡴࡧࡦࡌࡤࡶࠬᆠ"),
  bstack1ll1ll1_opy_ (u"ࠬࡾ࡭ࡴࡌࡤࡶࠬᆡ"),
  bstack1ll1ll1_opy_ (u"࠭ࡸ࡮ࡺࡍࡥࡷ࠭ᆢ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᆣ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᆤ"),
  bstack1ll1ll1_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᆥ"),
  bstack1ll1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ᆦ"),
  bstack1ll1ll1_opy_ (u"ࠫࡦࡶࡰࡗࡧࡵࡷ࡮ࡵ࡮ࠨᆧ"),
  bstack1ll1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᆨ"),
  bstack1ll1ll1_opy_ (u"࠭ࡲࡦࡵ࡬࡫ࡳࡇࡰࡱࠩᆩ"),
  bstack1ll1ll1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࡶࠫᆪ"),
  bstack1ll1ll1_opy_ (u"ࠨࡥࡤࡲࡦࡸࡹࠨᆫ"),
  bstack1ll1ll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᆬ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᆭ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡮࡫ࠧᆮ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᆯ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᆰ"),
  bstack1ll1ll1_opy_ (u"ࠧࡲࡷࡨࡹࡪ࠭ᆱ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪᆲ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡴࡵ࡙ࡴࡰࡴࡨࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠪᆳ"),
  bstack1ll1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡆࡥࡲ࡫ࡲࡢࡋࡰࡥ࡬࡫ࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩᆴ"),
  bstack1ll1ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡇࡻࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧᆵ"),
  bstack1ll1ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡌࡲࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᆶ"),
  bstack1ll1ll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᆷ"),
  bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡶࡩࡷࡼࡥࡅࡧࡹ࡭ࡨ࡫ࠧᆸ"),
  bstack1ll1ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᆹ"),
  bstack1ll1ll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫᆺ"),
  bstack1ll1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡥࡸࡹࡣࡰࡦࡨࠫᆻ"),
  bstack1ll1ll1_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡍࡴࡹࡄࡦࡸ࡬ࡧࡪ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᆼ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬᆽ"),
  bstack1ll1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡰࡱ࡮ࡨࡔࡦࡿࠧᆾ"),
  bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᆿ"),
  bstack1ll1ll1_opy_ (u"ࠨࡹࡧ࡭ࡴ࡙ࡥࡳࡸ࡬ࡧࡪ࠭ᇀ"),
  bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᇁ"),
  bstack1ll1ll1_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷࡇࡷࡵࡳࡴࡕ࡬ࡸࡪ࡚ࡲࡢࡥ࡮࡭ࡳ࡭ࠧᇂ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡭࡯ࡧࡩࡅࡲࡲࡹࡸࡡࡴࡶࠪᇃ"),
  bstack1ll1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡕࡸࡥࡧࡧࡵࡩࡳࡩࡥࡴࠩᇄ"),
  bstack1ll1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩᇅ"),
  bstack1ll1ll1_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᇆ"),
  bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡱࡴࡼࡥࡊࡑࡖࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࡍࡱࡦࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᇇ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫᇈ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᇉ"),
  bstack1ll1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᇊ"),
  bstack1ll1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᇋ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᇌ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᇍ"),
  bstack1ll1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᇎ"),
  bstack1ll1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᇏ"),
  bstack1ll1ll1_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ᇐ")
]
bstack1l1111111_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠫࡻ࠭ᇑ"): bstack1ll1ll1_opy_ (u"ࠬࡼࠧᇒ"),
  bstack1ll1ll1_opy_ (u"࠭ࡦࠨᇓ"): bstack1ll1ll1_opy_ (u"ࠧࡧࠩᇔ"),
  bstack1ll1ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᇕ"): bstack1ll1ll1_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᇖ"),
  bstack1ll1ll1_opy_ (u"ࠪࡳࡳࡲࡹࡢࡷࡷࡳࡲࡧࡴࡦࠩᇗ"): bstack1ll1ll1_opy_ (u"ࠫࡴࡴ࡬ࡺࡃࡸࡸࡴࡳࡡࡵࡧࠪᇘ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᇙ"): bstack1ll1ll1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪᇚ"),
  bstack1ll1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪᇛ"): bstack1ll1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᇜ"),
  bstack1ll1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬᇝ"): bstack1ll1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᇞ"),
  bstack1ll1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᇟ"): bstack1ll1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᇠ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᇡ"): bstack1ll1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᇢ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᇣ"): bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᇤ"),
  bstack1ll1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᇥ"): bstack1ll1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬᇦ"),
  bstack1ll1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᇧ"): bstack1ll1ll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᇨ"),
  bstack1ll1ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᇩ"): bstack1ll1ll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᇪ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᇫ"): bstack1ll1ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᇬ"),
  bstack1ll1ll1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᇭ"): bstack1ll1ll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᇮ"),
  bstack1ll1ll1_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᇯ"): bstack1ll1ll1_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᇰ"),
  bstack1ll1ll1_opy_ (u"ࠨࡲࡤࡧ࡫࡯࡬ࡦࠩᇱ"): bstack1ll1ll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᇲ"),
  bstack1ll1ll1_opy_ (u"ࠪࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᇳ"): bstack1ll1ll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᇴ"),
  bstack1ll1ll1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᇵ"): bstack1ll1ll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᇶ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᇷ"): bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᇸ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᇹ"): bstack1ll1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᇺ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ᇻ"): bstack1ll1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡰࡦࡣࡷࡩࡷ࠭ᇼ")
}
bstack11111l11l1_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨ࡫ࡷ࡬ࡺࡨ࠮ࡤࡱࡰ࠳ࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯࠯ࡳࡧ࡯ࡩࡦࡹࡥࡴ࠱࡯ࡥࡹ࡫ࡳࡵ࠱ࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᇽ")
bstack11111l1l11_opy_ = bstack1ll1ll1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠯ࡩࡧࡤࡰࡹ࡮ࡣࡩࡧࡦ࡯ࠧᇾ")
bstack11ll1ll1ll_opy_ = bstack1ll1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡨࡨࡸ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡶࡩࡳࡪ࡟ࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦᇿ")
bstack1l1l11l111_opy_ = bstack1ll1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡻࡩ࠵ࡨࡶࡤࠪሀ")
bstack1l11ll11_opy_ = bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧ࠭ሁ")
bstack1ll111llll_opy_ = bstack1ll1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨሂ")
bstack11111llll1_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠬࡩࡲࡪࡶ࡬ࡧࡦࡲࠧሃ"): 50,
  bstack1ll1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬሄ"): 40,
  bstack1ll1ll1_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨህ"): 30,
  bstack1ll1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ሆ"): 20,
  bstack1ll1ll1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨሇ"): 10
}
bstack1l11l1l1l1_opy_ = bstack11111llll1_opy_[bstack1ll1ll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨለ")]
bstack1ll1111lll_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪሉ")
bstack1lll1lll1_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪሊ")
bstack1lllllll11_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬላ")
bstack1l11l111_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ሌ")
bstack11l11111_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡲࡩࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡲࡤࡧࡰࡧࡧࡦࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭ል")
bstack11111l111l_opy_ = [bstack1ll1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪሎ"), bstack1ll1ll1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪሏ")]
bstack11111ll1ll_opy_ = [bstack1ll1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧሐ"), bstack1ll1ll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧሑ")]
bstack11111ll11_opy_ = re.compile(bstack1ll1ll1_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬሒ"))
bstack1ll111ll11_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨሓ"),
  bstack1ll1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪሔ"),
  bstack1ll1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ሕ"),
  bstack1ll1ll1_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧሖ"),
  bstack1ll1ll1_opy_ (u"ࠫࡦࡶࡰࠨሗ"),
  bstack1ll1ll1_opy_ (u"ࠬࡻࡤࡪࡦࠪመ"),
  bstack1ll1ll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨሙ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧሚ"),
  bstack1ll1ll1_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ማ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧሜ"),
  bstack1ll1ll1_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫም"), bstack1ll1ll1_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧሞ"),
  bstack1ll1ll1_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨሟ"),
  bstack1ll1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬሠ"),
  bstack1ll1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫሡ"),
  bstack1ll1ll1_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫሢ"),
  bstack1ll1ll1_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪሣ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨሤ"), bstack1ll1ll1_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨሥ"), bstack1ll1ll1_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧሦ"), bstack1ll1ll1_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧሧ"), bstack1ll1ll1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩረ"),
  bstack1ll1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ሩ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ሪ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬራ"), bstack1ll1ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨሬ"),
  bstack1ll1ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪር"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧሮ"),
  bstack1ll1ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭ሯ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩሰ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧሱ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡻࡪࠧሲ"), bstack1ll1ll1_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧሳ"), bstack1ll1ll1_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧሴ"), bstack1ll1ll1_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧስ"),
  bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬሶ"), bstack1ll1ll1_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧሷ"), bstack1ll1ll1_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬሸ"),
  bstack1ll1ll1_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬሹ"), bstack1ll1ll1_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩሺ"),
  bstack1ll1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧሻ"), bstack1ll1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩሼ"), bstack1ll1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬሽ"), bstack1ll1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪሾ"), bstack1ll1ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ሿ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ቀ"), bstack1ll1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨቁ"),
  bstack1ll1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧቂ"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫቃ"),
  bstack1ll1ll1_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭ቄ"), bstack1ll1ll1_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩቅ"), bstack1ll1ll1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧቆ"), bstack1ll1ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ቇ"),
  bstack1ll1ll1_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩቈ"),
  bstack1ll1ll1_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ቉"), bstack1ll1ll1_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ቊ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧቋ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪቌ"),
  bstack1ll1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫቍ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ቎"),
  bstack1ll1ll1_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ቏"),
  bstack1ll1ll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫቐ"),
  bstack1ll1ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧቑ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭ቒ"),
  bstack1ll1ll1_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬቓ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭ቔ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫቕ"),
  bstack1ll1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪቖ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ቗"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭ቘ"),
  bstack1ll1ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ቙"),
  bstack1ll1ll1_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬቚ"),
  bstack1ll1ll1_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩቛ"),
  bstack1ll1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧቜ"), bstack1ll1ll1_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨቝ"), bstack1ll1ll1_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ቞"),
  bstack1ll1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ቟"),
  bstack1ll1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫበ"),
  bstack1ll1ll1_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪቡ"),
  bstack1ll1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫቢ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧባ"),
  bstack1ll1ll1_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨቤ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨብ"), bstack1ll1ll1_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬቦ"), bstack1ll1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪቧ"),
  bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨቨ"),
  bstack1ll1ll1_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪቩ"),
  bstack1ll1ll1_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬቪ"),
  bstack1ll1ll1_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫቫ"),
  bstack1ll1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨቬ"), bstack1ll1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬቭ"),
  bstack1ll1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪቮ"), bstack1ll1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬቯ"),
  bstack1ll1ll1_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩተ"),
  bstack1ll1ll1_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩቱ"),
  bstack1ll1ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧቲ"), bstack1ll1ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩታ"), bstack1ll1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪቴ"), bstack1ll1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧት"),
  bstack1ll1ll1_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨቶ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪቷ"),
  bstack1ll1ll1_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ቸ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫቹ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩቺ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨቻ"),
  bstack1ll1ll1_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨቼ"), bstack1ll1ll1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩች"),
  bstack1ll1ll1_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬቾ"),
  bstack1ll1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪቿ"),
  bstack1ll1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬኀ"),
  bstack1ll1ll1_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬኁ"),
  bstack1ll1ll1_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨኂ"),
  bstack1ll1ll1_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪኃ"),
  bstack1ll1ll1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩኄ"),
  bstack1ll1ll1_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪኅ"),
  bstack1ll1ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪኆ"),
  bstack1ll1ll1_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩኇ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪኈ"),
  bstack1ll1ll1_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ኉"),
  bstack1ll1ll1_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭ኊ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪኋ"),
  bstack1ll1ll1_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫኌ"),
  bstack1ll1ll1_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭ኍ"),
  bstack1ll1ll1_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬ኎"),
  bstack1ll1ll1_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭኏"),
  bstack1ll1ll1_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪነ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭ኑ"),
  bstack1ll1ll1_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫኒ"),
  bstack1ll1ll1_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬና"), bstack1ll1ll1_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪኔ"),
  bstack1ll1ll1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨን"), bstack1ll1ll1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭ኖ"),
  bstack1ll1ll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫኗ"),
  bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪኘ"),
  bstack1ll1ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪኙ"),
  bstack1ll1ll1_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭ኚ"), bstack1ll1ll1_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭ኛ"),
  bstack1ll1ll1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧኜ"),
  bstack1ll1ll1_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪኝ"),
  bstack1ll1ll1_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭ኞ"),
  bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨኟ"),
  bstack1ll1ll1_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪአ"),
  bstack1ll1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬኡ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨኢ"),
  bstack1ll1ll1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪኣ"),
  bstack1ll1ll1_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧኤ"),
  bstack1ll1ll1_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬእ"), bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫኦ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨኧ"),
  bstack1ll1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬከ")
]
bstack1l11l11l1l_opy_ = bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩኩ")
bstack1l11lll11l_opy_ = [bstack1ll1ll1_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩኪ"), bstack1ll1ll1_opy_ (u"ࠬ࠴ࡡࡢࡤࠪካ"), bstack1ll1ll1_opy_ (u"࠭࠮ࡪࡲࡤࠫኬ")]
bstack1lllll1l1l_opy_ = [bstack1ll1ll1_opy_ (u"ࠧࡪࡦࠪክ"), bstack1ll1ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭ኮ"), bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬኯ"), bstack1ll1ll1_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩኰ")]
bstack1ll1ll11l1_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ኱"): bstack1ll1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኲ"),
  bstack1ll1ll1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧኳ"): bstack1ll1ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬኴ"),
  bstack1ll1ll1_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ኵ"): bstack1ll1ll1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ኶"),
  bstack1ll1ll1_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭኷"): bstack1ll1ll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኸ"),
  bstack1ll1ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬኹ"): bstack1ll1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧኺ")
}
bstack1ll11111l_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬኻ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ኼ"),
  bstack1ll1ll1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኽ"),
  bstack1ll1ll1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩኾ"),
  bstack1ll1ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ኿"),
]
bstack1l1lll111_opy_ = bstack1llll1l1_opy_ + bstack11111l11ll_opy_ + bstack1ll111ll11_opy_
bstack11l1111ll_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪዀ"),
  bstack1ll1ll1_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧ዁"),
  bstack1ll1ll1_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ዂ"),
  bstack1ll1ll1_opy_ (u"ࠨࡠ࠴࠴࠳࠭ዃ"),
  bstack1ll1ll1_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨዄ"),
  bstack1ll1ll1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩዅ"),
  bstack1ll1ll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪ዆"),
  bstack1ll1ll1_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ዇")
]
bstack1111l1111l_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧወ")
bstack1ll1ll1l1l_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭ዉ")
bstack11ll1lll_opy_ = [ bstack1ll1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪዊ") ]
bstack1lll111l11_opy_ = [ bstack1ll1ll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨዋ") ]
bstack1lllllllll_opy_ = [bstack1ll1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧዌ")]
bstack1l111ll1_opy_ = [ bstack1ll1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫው") ]
bstack1ll1l1lll1_opy_ = bstack1ll1ll1_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧዎ")
bstack1lll1llll_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩዏ")
bstack111l1lll1_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫዐ")
bstack1111llll_opy_ = bstack1ll1ll1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧዑ")
bstack11ll1l1l_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭ዒ"),
  bstack1ll1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪዓ"),
  bstack1ll1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬዔ"),
  bstack1ll1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫዕ"),
  bstack1ll1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪዖ"),
  bstack1ll1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ዗"),
  bstack1ll1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨዘ"),
  bstack1ll1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫዙ"),
  bstack1ll1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬዚ"),
  bstack1ll1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬዛ"),
  bstack1ll1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ዜ"),
  bstack1ll1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬዝ"),
  bstack1ll1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪዞ"),
  bstack1ll1ll1_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩዟ"),
  bstack1ll1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ዠ"),
  bstack1ll1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪዡ"),
  bstack1ll1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧዢ"),
  bstack1ll1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬዣ"),
  bstack1ll1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧዤ"),
  bstack1ll1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ዥ"),
  bstack1ll1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧዦ"),
]
bstack1l1l1lll1_opy_ = bstack1ll1ll1_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧዧ")
bstack1lll1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll1_opy_ (u"ࠪࢂࠬየ")), bstack1ll1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫዩ"), bstack1ll1ll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫዪ"))
bstack1111lll1ll_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧያ")
bstack11111l1lll_opy_ = [ bstack1ll1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧዬ"), bstack1ll1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧይ"), bstack1ll1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨዮ"), bstack1ll1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪዯ")]
bstack11ll1111_opy_ = [ bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫደ"), bstack1ll1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫዱ"), bstack1ll1ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬዲ"), bstack1ll1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧዳ") ]
bstack11l11l11l1_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ዴ"): bstack1ll1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩድ"),
  bstack1ll1ll1_opy_ (u"ࠪࡊࡆࡏࡌࠨዶ"): bstack1ll1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዷ"),
  bstack1ll1ll1_opy_ (u"࡙ࠬࡋࡊࡒࠪዸ"): bstack1ll1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧዹ")
}
bstack1lll11l11_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠢࡨࡧࡷࠦዺ"),
  bstack1ll1ll1_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣዻ"),
  bstack1ll1ll1_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧዼ"),
  bstack1ll1ll1_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦዽ"),
  bstack1ll1ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥዾ"),
  bstack1ll1ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤዿ"),
  bstack1ll1ll1_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨጀ"),
  bstack1ll1ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦጁ"),
  bstack1ll1ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦጂ"),
  bstack1ll1ll1_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣጃ"),
  bstack1ll1ll1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦጄ"),
  bstack1ll1ll1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦጅ"),
  bstack1ll1ll1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥጆ"),
  bstack1ll1ll1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧጇ"),
  bstack1ll1ll1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧገ"),
  bstack1ll1ll1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨጉ"),
  bstack1ll1ll1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨጊ"),
  bstack1ll1ll1_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤጋ"),
  bstack1ll1ll1_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨጌ")
]
bstack11111lllll_opy_ = [
  bstack1ll1ll1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦግ"),
  bstack1ll1ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጎ"),
  bstack1ll1ll1_opy_ (u"ࠢࡢࡷࡷࡳࠧጏ"),
  bstack1ll1ll1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣጐ"),
  bstack1ll1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ጑")
]
bstack1l11l111l1_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤጒ"): [bstack1ll1ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥጓ")],
  bstack1ll1ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤጔ"): [bstack1ll1ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጕ")],
  bstack1ll1ll1_opy_ (u"ࠢࡢࡷࡷࡳࠧ጖"): [bstack1ll1ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ጗"), bstack1ll1ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧጘ"), bstack1ll1ll1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢጙ"), bstack1ll1ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥጚ")],
  bstack1ll1ll1_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧጛ"): [bstack1ll1ll1_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨጜ")],
  bstack1ll1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤጝ"): [bstack1ll1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥጞ")],
}
bstack111111ll11_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣጟ"): bstack1ll1ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤጠ"),
  bstack1ll1ll1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣጡ"): bstack1ll1ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤጢ"),
  bstack1ll1ll1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥጣ"): bstack1ll1ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤጤ"),
  bstack1ll1ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦጥ"): bstack1ll1ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦጦ"),
  bstack1ll1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧጧ"): bstack1ll1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨጨ")
}
bstack11l1111lll_opy_ = {
  bstack1ll1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩጩ"): bstack1ll1ll1_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫጪ"),
  bstack1ll1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪጫ"): bstack1ll1ll1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩጬ"),
  bstack1ll1ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧጭ"): bstack1ll1ll1_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧጮ"),
  bstack1ll1ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨጯ"): bstack1ll1ll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬጰ")
}
bstack111111l1ll_opy_ = 65536
bstack1111l111l1_opy_ = bstack1ll1ll1_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧጱ")
bstack111111lll1_opy_ = [
      bstack1ll1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩጲ"), bstack1ll1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጳ"), bstack1ll1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬጴ"), bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧጵ"), bstack1ll1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ጶ"),
      bstack1ll1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨጷ"), bstack1ll1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩጸ"), bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨጹ"), bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩጺ"),
      bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጻ"), bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጼ"), bstack1ll1ll1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧጽ")
    ]
bstack11111l1l1l_opy_= {
  bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩጾ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪጿ"),
  bstack1ll1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫፀ"): bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬፁ"),
  bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨፂ"): bstack1ll1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧፃ"),
  bstack1ll1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫፄ"): bstack1ll1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬፅ"),
  bstack1ll1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩፆ"): bstack1ll1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪፇ"),
  bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪፈ"): bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫፉ"),
  bstack1ll1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ፊ"): bstack1ll1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧፋ"),
  bstack1ll1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩፌ"): bstack1ll1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪፍ"),
  bstack1ll1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪፎ"): bstack1ll1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫፏ"),
  bstack1ll1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧፐ"): bstack1ll1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨፑ"),
  bstack1ll1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨፒ"): bstack1ll1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩፓ"),
  bstack1ll1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪፔ"): bstack1ll1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫፕ"),
  bstack1ll1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪፖ"): bstack1ll1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫፗ"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧፘ"): bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ፙ"),
  bstack1ll1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧፚ"): bstack1ll1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ፛"),
  bstack1ll1ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ፜"): bstack1ll1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ፝"),
  bstack1ll1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ፞"): bstack1ll1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ፟"),
  bstack1ll1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ፠"): bstack1ll1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ፡"),
  bstack1ll1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ።"): bstack1ll1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ፣"),
  bstack1ll1ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ፤"): bstack1ll1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ፥"),
  bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ፦"): bstack1ll1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ፧"),
  bstack1ll1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ፨"): bstack1ll1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭፩"),
  bstack1ll1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ፪"): bstack1ll1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ፫"),
  bstack1ll1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭፬"): bstack1ll1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ፭"),
  bstack1ll1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ፮"): bstack1ll1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ፯")
}
bstack1111l111ll_opy_ = [bstack1ll1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭፰"), bstack1ll1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭፱")]
bstack1l1llll11_opy_ = bstack1ll1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳࡬ࡸࡩࡥࡵ࠲ࠦ፲")
bstack111l11111_opy_ = bstack1ll1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫ࡷ࡯ࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࠣ፳")
bstack11ll1l111_opy_ = bstack1ll1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠦ፴")
class EVENTS(Enum):
  bstack1111l11l11_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ፵")
  bstack1lll11l1l_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࠪ፶") # final bstack1111l11111_opy_
  bstack1111l11l1l_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࡭ࡱࡪࡷࠬ፷")
  bstack1lll11111_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ፸")
  bstack1ll11ll1l1_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ፹")
  bstack11111l1111_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨࠧ፺")
  bstack11111ll1l1_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨ፻")
  bstack1ll1l1ll1l_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭፼")
  bstack111l11llll_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡴࡣࡹࡩ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭፽")
  bstack111ll1111_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡲࡨࡶ࡫ࡵࡲ࡮ࡵࡦࡥࡳ࠭፾")
  bstack1llll11111_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀ࡬ࡰࡥࡤࡰࠬ፿")
  bstack111l1l111_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡦࡶࡰ࠮ࡷࡳࡰࡴࡧࡤࠨᎀ")
  bstack1ll1l1l11_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡥ࡬࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹࠧᎁ")
  bstack1l11llll1_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫᎂ")
  bstack11ll11ll_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫᎃ")
  bstack111111llll_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹࠨᎄ")
  SDK_PERCY_SCREENSHOT = bstack1ll1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᎅ")
  bstack1l11ll1l1_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡴࡶࡤࡸࡺࡹࠧᎆ")
  bstack11l11ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᎇ")
  bstack11111l1ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡱࡻࡽ࠲ࡹࡥࡵࡷࡳࠫᎈ")
  bstack1ll1l1ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡷࡹࡵ࠭ᎉ")
  bstack11111lll1l_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡰࡤࡴࡸ࡮࡯ࡵࠩᎊ") # not bstack111111l1l1_opy_ in python
  bstack1l1ll1llll_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡴࡹ࡮ࡺࠧᎋ") # used in bstack11111lll11_opy_
  bstack11ll1llll_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧᎌ") # used in bstack11111lll11_opy_
  bstack1l11l1ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩᎍ")
  bstack11llll111l_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭ᎎ")
  bstack11lll1l111_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭ᎏ") #
  bstack1l11l1ll11_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭᎐")
  bstack1l1lll1ll1_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭᎑")
  bstack11ll11ll11_opy_ = bstack1ll1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫ᎒")
  bstack1l1ll111_opy_ = bstack1ll1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭᎓")
  bstack11ll11llll_opy_ = bstack1ll1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᎔")
  bstack1l1ll1ll1l_opy_ = bstack1ll1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ᎕")
  bstack111111ll1l_opy_ = bstack1ll1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ᎖")
  bstack11111ll11l_opy_ = bstack1ll1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨ᎗")
class STAGE(Enum):
  bstack1ll11l11_opy_ = bstack1ll1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ᎘")
  END = bstack1ll1ll1_opy_ (u"ࠬ࡫࡮ࡥࠩ᎙")
  SINGLE = bstack1ll1ll1_opy_ (u"࠭ࡳࡪࡰࡪࡰࡪ࠭᎚")