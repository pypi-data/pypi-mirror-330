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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11111llll1_opy_, bstack111111lll1_opy_
import tempfile
import json
bstack1lll111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭ᖬ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1ll1_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᖭ"),
      datefmt=bstack1ll1ll1_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᖮ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11lllll_opy_():
  global bstack1lll111llll_opy_
  if os.path.exists(bstack1lll111llll_opy_):
    os.remove(bstack1lll111llll_opy_)
def bstack11l11l1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11111l111_opy_(config, log_level):
  bstack1lll11lll1l_opy_ = log_level
  if bstack1ll1ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᖯ") in config and config[bstack1ll1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᖰ")] in bstack11111llll1_opy_:
    bstack1lll11lll1l_opy_ = bstack11111llll1_opy_[config[bstack1ll1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᖱ")]]
  if config.get(bstack1ll1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᖲ"), False):
    logging.getLogger().setLevel(bstack1lll11lll1l_opy_)
    return bstack1lll11lll1l_opy_
  global bstack1lll111llll_opy_
  bstack11l11l1ll_opy_()
  bstack1lll111ll11_opy_ = logging.Formatter(
    fmt=bstack1ll1ll1_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᖳ"),
    datefmt=bstack1ll1ll1_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧᖴ")
  )
  bstack1lll111l1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll111llll_opy_)
  file_handler.setFormatter(bstack1lll111ll11_opy_)
  bstack1lll111l1l1_opy_.setFormatter(bstack1lll111ll11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll111l1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨᖵ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll111l1l1_opy_.setLevel(bstack1lll11lll1l_opy_)
  logging.getLogger().addHandler(bstack1lll111l1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll11lll1l_opy_
def bstack1lll11l1ll1_opy_(config):
  try:
    bstack1lll11llll1_opy_ = set(bstack111111lll1_opy_)
    bstack1lll111lll1_opy_ = bstack1ll1ll1_opy_ (u"ࠧࠨᖶ")
    with open(bstack1ll1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᖷ")) as bstack1lll11l1l11_opy_:
      bstack1lll11ll11l_opy_ = bstack1lll11l1l11_opy_.read()
      bstack1lll111lll1_opy_ = re.sub(bstack1ll1ll1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪᖸ"), bstack1ll1ll1_opy_ (u"ࠪࠫᖹ"), bstack1lll11ll11l_opy_, flags=re.M)
      bstack1lll111lll1_opy_ = re.sub(
        bstack1ll1ll1_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧᖺ") + bstack1ll1ll1_opy_ (u"ࠬࢂࠧᖻ").join(bstack1lll11llll1_opy_) + bstack1ll1ll1_opy_ (u"࠭ࠩ࠯ࠬࠧࠫᖼ"),
        bstack1ll1ll1_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᖽ"),
        bstack1lll111lll1_opy_, flags=re.M | re.I
      )
    def bstack1lll11l11l1_opy_(dic):
      bstack1lll11ll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll11llll1_opy_:
          bstack1lll11ll1l1_opy_[key] = bstack1ll1ll1_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᖾ")
        else:
          if isinstance(value, dict):
            bstack1lll11ll1l1_opy_[key] = bstack1lll11l11l1_opy_(value)
          else:
            bstack1lll11ll1l1_opy_[key] = value
      return bstack1lll11ll1l1_opy_
    bstack1lll11ll1l1_opy_ = bstack1lll11l11l1_opy_(config)
    return {
      bstack1ll1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬᖿ"): bstack1lll111lll1_opy_,
      bstack1ll1ll1_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᗀ"): json.dumps(bstack1lll11ll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll11l111l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll1ll1_opy_ (u"ࠫࡱࡵࡧࠨᗁ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll11ll1ll_opy_ = os.path.join(log_dir, bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭ᗂ"))
  if not os.path.exists(bstack1lll11ll1ll_opy_):
    bstack1lll11l1lll_opy_ = {
      bstack1ll1ll1_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢᗃ"): str(inipath),
      bstack1ll1ll1_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤᗄ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᗅ")), bstack1ll1ll1_opy_ (u"ࠩࡺࠫᗆ")) as bstack1lll11l11ll_opy_:
      bstack1lll11l11ll_opy_.write(json.dumps(bstack1lll11l1lll_opy_))
def bstack1lll11l1l1l_opy_():
  try:
    bstack1lll11ll1ll_opy_ = os.path.join(os.getcwd(), bstack1ll1ll1_opy_ (u"ࠪࡰࡴ࡭ࠧᗇ"), bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᗈ"))
    if os.path.exists(bstack1lll11ll1ll_opy_):
      with open(bstack1lll11ll1ll_opy_, bstack1ll1ll1_opy_ (u"ࠬࡸࠧᗉ")) as bstack1lll11l11ll_opy_:
        bstack1lll11ll111_opy_ = json.load(bstack1lll11l11ll_opy_)
      return bstack1lll11ll111_opy_.get(bstack1ll1ll1_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧᗊ"), bstack1ll1ll1_opy_ (u"ࠧࠨᗋ")), bstack1lll11ll111_opy_.get(bstack1ll1ll1_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪᗌ"), bstack1ll1ll1_opy_ (u"ࠩࠪᗍ"))
  except:
    pass
  return None, None
def bstack1lll11l1111_opy_():
  try:
    bstack1lll11ll1ll_opy_ = os.path.join(os.getcwd(), bstack1ll1ll1_opy_ (u"ࠪࡰࡴ࡭ࠧᗎ"), bstack1ll1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᗏ"))
    if os.path.exists(bstack1lll11ll1ll_opy_):
      os.remove(bstack1lll11ll1ll_opy_)
  except:
    pass
def bstack1l1l11ll1l_opy_(config):
  from bstack_utils.helper import bstack11lll1lll_opy_
  global bstack1lll111llll_opy_
  try:
    if config.get(bstack1ll1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᗐ"), False):
      return
    uuid = os.getenv(bstack1ll1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᗑ")) if os.getenv(bstack1ll1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᗒ")) else bstack11lll1lll_opy_.get_property(bstack1ll1ll1_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥᗓ"))
    if not uuid or uuid == bstack1ll1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᗔ"):
      return
    bstack1lll111ll1l_opy_ = [bstack1ll1ll1_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ᗕ"), bstack1ll1ll1_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬᗖ"), bstack1ll1ll1_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ᗗ"), bstack1lll111llll_opy_]
    bstack1lll111l1ll_opy_, root_path = bstack1lll11l1l1l_opy_()
    if bstack1lll111l1ll_opy_ != None:
      bstack1lll111ll1l_opy_.append(bstack1lll111l1ll_opy_)
    if root_path != None:
      bstack1lll111ll1l_opy_.append(os.path.join(root_path, bstack1ll1ll1_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫᗘ")))
    bstack11l11l1ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭ᗙ") + uuid + bstack1ll1ll1_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩᗚ"))
    with tarfile.open(output_file, bstack1ll1ll1_opy_ (u"ࠤࡺ࠾࡬ࢀࠢᗛ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll111ll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll11l1ll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll11lll11_opy_ = data.encode()
        tarinfo.size = len(bstack1lll11lll11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll11lll11_opy_))
    bstack11l11l111_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨᗜ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1ll1_opy_ (u"ࠫࡷࡨࠧᗝ")), bstack1ll1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪᗞ")),
        bstack1ll1ll1_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᗟ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᗠ"),
      data=bstack11l11l111_opy_,
      headers={bstack1ll1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᗡ"): bstack11l11l111_opy_.content_type},
      auth=(config[bstack1ll1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᗢ")], config[bstack1ll1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᗣ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᗤ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᗥ") + str(e))
  finally:
    try:
      bstack1lll11lllll_opy_()
      bstack1lll11l1111_opy_()
    except:
      pass